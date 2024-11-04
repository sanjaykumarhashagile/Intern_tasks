from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn
import os
import json
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from databases import Database
import logging
import tempfile
from kafka import KafkaConsumer
import asyncio

load_dotenv()
GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")
USERNAME = os.getenv("API_USERNAME")
PASSWORD = os.getenv("API_PASSWORD")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

app = FastAPI()
security = HTTPBasic()
database = Database(DATABASE_URL)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup():
    try:
        await database.connect()
        logger.info("Database connection established successfully.")
        
        query = "SELECT version();"
        version = await database.fetch_one(query)
        logger.info(f"Connected to database version: {version[0]}")
        
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")

@app.on_event("shutdown")
async def shutdown():
    try:
        await database.disconnect()
        logger.info("Database connection closed successfully.")
    except Exception as e:
        logger.error(f"Failed to disconnect from the database: {e}")

async def load_resume_from_db(file_id: int):
    query = "SELECT data FROM pdf_files WHERE id = :file_id"
    file_record = await database.fetch_one(query, {"file_id": file_id})

    if file_record is None:
        raise HTTPException(status_code=404, detail="File not found")

    pdf_data = file_record['data']
    
    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        temp_file.write(pdf_data)
        temp_file.flush()  
        
        # Load PDF from the temporary file
        loader = PyPDFLoader(temp_file.name)
        documents = loader.load()
        resume_text = "\n".join(doc.page_content for doc in documents)
    
    return resume_text

def generate_fields_from_resume(resume_text):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GOOGLE_KEY)
    prompt_template = PromptTemplate.from_template(
        """Extract the following fields from the resume text 
1. first_name
2. last_name
3. emails
4. phones
5. skills (extract only the skills from technical details like programming languages, frameworks,database skills and not any soft or communication skills )
6. highest_degree_details
7. pg_degree (extract the post graduate degree from the career summary e.g., MCA, M.E.)
8. ug_degree (extract the under graduate degree from the career summary e.g. BCA, B.E., B.Sc.)
9. ug_graduation_year (year of undergraduate graduation)
10. first_working_date
11. state
12. city
13. company_history (an array of work experiences)
14. marital_status
15. gender
16. skill_bucket
17. domain_experience (an array)

Please extract each field based on the context of the resume. Ensure the ug_degree, pg_degree, and their corresponding graduation years are identified, even if they are presented in varied formats. 

Resume Text:
{resume_text}

Provide the details only in JSON format, with no extra lines or text.
"""
    )

    chain = LLMChain(llm=llm, prompt=prompt_template)
    response = chain.run(resume_text=resume_text)
    
    return json.loads(response)

async def insert_candidate(candidate_data):
    # Insert candidate details
    query = """
    INSERT INTO candidates (first_name, last_name, email, phone_number, skills, 
                            state, city, marital_status, gender, skill_bucket, 
                            domain_experience)
    VALUES (:first_name, :last_name, :email, :phone_number, :skills, 
            :state, :city, :marital_status, :gender, :skill_bucket, 
            :domain_experience)
    RETURNING id
    """
    
    candidate_id = await database.execute(query, {
        "first_name": candidate_data.get("first_name"),
        "last_name": candidate_data.get("last_name"),
        "email": candidate_data.get("emails", []),
        "phone_number": candidate_data.get("phones", []),
        "skills": candidate_data.get("skills", []),
        "state": candidate_data.get("state"),
        "city": candidate_data.get("city"),
        "marital_status": candidate_data.get("marital_status"),
        "gender": candidate_data.get("gender"),
        "skill_bucket": candidate_data.get("skill_bucket", []),
        "domain_experience": candidate_data.get("domain_experience", [])
    })

    # Insert education details
    await insert_education(candidate_id, candidate_data)
    # Insert experience details
    await insert_experience(candidate_id, candidate_data.get("company_history", []))

async def insert_education(candidate_id, candidate_data):
    query = """
    INSERT INTO education (candidate_id, highest_degree_details, pg_degree, 
                           ug_degree, ug_graduation_year)
    VALUES (:candidate_id, :highest_degree_details, :pg_degree, 
            :ug_degree, :ug_graduation_year)
    """
    
    await database.execute(query, {
        "candidate_id": candidate_id,
        "highest_degree_details": candidate_data.get("highest_degree_details"),
        "pg_degree": candidate_data.get("pg_degree"),
        "ug_degree": candidate_data.get("ug_degree"),
        "ug_graduation_year": candidate_data.get("ug_graduation_year"),
    })

async def insert_experience(candidate_id, company_history):
    for experience in company_history:
        query = """
        INSERT INTO experience (candidate_id, company_name, location, designation, 
                                start_date, end_date, project_details)
        VALUES (:candidate_id, :company_name, :location, :designation, 
                :start_date, :end_date, :project_details)
        """
        await database.execute(query, {
            "candidate_id": candidate_id,
            "company_name": experience.get("company"),
            "location": experience.get("location"),
            "designation": experience.get("title"),
            "start_date": experience.get("start_date"),
            "end_date": experience.get("end_date"),
            "project_details": experience.get("project_details")
        })

def consume_resumes():
    consumer = KafkaConsumer(
        'pdf_resume',
        bootstrap_servers='localhost:9092',  # Change this if needed
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='resume_consumer_group',
        value_deserializer=lambda x: x  # Assuming the value is raw PDF data
    )

    for message in consumer:
        file_id = int(message.value.decode('utf-8'))  # Adjust based on your message format
        asyncio.run(process_resume(file_id))

async def process_resume(file_id):
    try:
        resume_text = await load_resume_from_db(file_id)
        extracted_details = generate_fields_from_resume(resume_text)
        print(json.dumps(extracted_details, indent=2))  # Display the results
        await insert_candidate(extracted_details)
    except Exception as e:
        logger.error(f"Error processing resume: {e}")

if __name__ == "__main__":
    # Start the Kafka consumer in a separate thread or asyncio task
    import threading

    consumer_thread = threading.Thread(target=consume_resumes)
    consumer_thread.start()
    
    uvicorn.run(app, host="0.0.0.0", port=8003)
