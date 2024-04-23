import streamlit as st
from pathlib import Path
import tempfile  
import hashlib
import mimetypes
import google.generativeai as genai
genai.configure(api_key="AIzaSyB8ovRcedOCeXnAsdXX4MDXDkvcSQHNnfs")

st.title("Arabic to English Traslation")
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

uploaded_files = []

def upload_if_needed(pathname: str) -> list[str]:
  path = Path(pathname)
  hash_id = hashlib.sha256(path.read_bytes()).hexdigest()
  try:
    existing_file = genai.get_file(name=hash_id)
    return [existing_file]
  except:
    pass
  uploaded_files.append(genai.upload_file(path=path, display_name=hash_id))
  return [uploaded_files[-1]]

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
  if uploaded_file.type in ["image/jpeg", "image/jpg", "image/png"]:
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as temp_file:
      temp_file.write(uploaded_file.read())
      path = temp_file.name
      prompt_parts = [
        *upload_if_needed(str(path)),
        "Return the arabic text in the image and translate this arabic caligraphy into english\n\n",
      ]
      response = model.generate_content(prompt_parts)
      st.write(response.text)
  else:
    st.error("Unsupported file type. Please upload an image in JPEG or PNG format.")









