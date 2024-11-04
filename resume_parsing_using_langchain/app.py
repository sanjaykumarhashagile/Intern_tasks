
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import FileResponse
import uvicorn
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import jsons


load_dotenv()
GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")
USERNAME = os.getenv("API_USERNAME")
PASSWORD = os.getenv("API_PASSWORD")


app = FastAPI()
security = HTTPBasic()

def load_resume(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents[0]  

def generate_fields_from_resume(resume_text):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GOOGLE_KEY)

    prompt_template = PromptTemplate.from_template(
        "Extract the following details from this resume:\n"
        "1. Name"
        "2. Email"
        "3. Contact Number"
        "4. Education (Degree, Major, University, Year of Passout)"
        "5. College Name"
        "6. Skills"
        "7. Internship Experiences"
        "8. Soft Skills"
        "9. Languages Known"
        "10. Courses"
        "Resume Text:\n{resume_text}\n\n"
        "Provide the details in a json format."
    )

    
    chain = LLMChain(llm=llm, prompt=prompt_template)

    
    response = chain.run(resume_text=resume_text)
    return jsons.load(response)

@app.get("/")
def read_resume(credentials: HTTPBasicCredentials = Depends(security)):
    
    if credentials.username != USERNAME or credentials.password != PASSWORD:
       
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    # resume_file_path = "/home/sanjay_kumar/Downloads/web-developer-resume-example.pdf"  

    
    return extracted_details

if __name__ == "__main__":
    resume_file_path = "/home/sanjay_kumar/Downloads/web-developer-resume-example.pdf"  
    try:
        resume_text = load_resume(resume_file_path)
        extracted_details = generate_fields_from_resume(resume_text)
        print("Extracted Details:")
        print(extracted_details)
    except Exception as e:
        print(f"Error processing resume: {e}")

   
    uvicorn.run(app, host="127.0.0.1", port=5001)
