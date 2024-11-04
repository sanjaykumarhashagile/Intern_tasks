

import os
import google.generativeai as genai
import json


genai.configure(api_key=os.environ["GEMINI_API_KEY"])


generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = model.start_chat(
  history=[
  ]
)

filepath = '/home/sanjay_kumar/Downloads/web-developer-resume-example.pdf'
filepath2='/home/sanjay_kumar/Desktop/resume parser/resume/web-developer-resume-example (copy).jpeg'
file_name, file_extension = os.path.splitext(filepath)

try:
  if file_extension == '.pdf':
    sample_pdf = genai.upload_file(filepath, mime_type='application/pdf')
    response = model.generate_content(["Give me all the keypoints like name,email,contact_number,education(degree,major,university,year_of_passout),college_name,skills,internship_experiences(remove the new lines and replace it with full stops in each paragraph),soft_skills,languages-known,courser of this pdf file",sample_pdf])
    string_output = response.text
    try:
      json_output = json.loads(string_output)
      print(json_output)
    except json.JSONDecodeError as e:
      print(f"Response is not a valid JSON --- {e}")



  elif file_extension == '.docx':
    sample_docx = genai.upload_file(filepath, mime_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response = model.generate_content(["Give me all the keypoints like name,email,contact_number,education(degree,major,university,year_of_passout),college_name,skills,internship_experiences(remove the new lines and replace it with full stops in each paragraph ) of this  file in json format",sample_docx])
    string_output = response.text
    try:
      json_output = json.loads(string_output)
      print(json_output)
    except json.JSONDecodeError as e:
      print(f"Response is not a valid JSON --- {e}")

except Exception as e:
    print(f"An error occurred: {e}")

print(file_name)
print(file_extension)
