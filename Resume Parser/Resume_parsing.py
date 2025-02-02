

import pandas as pd
import os
import json
import pdfplumber
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from pandarallel import pandarallel
import time
import docxpy



filetypes=['.pdf','.docx','.png','.jpg','.jpeg' ]
folder = '/home/sanjay_kumar/Downloads/Resumes'



def get_file_names_from_folder():
    resumes = []
    for file in os.listdir(folder):
        file_name, file_extension = os.path.splitext(file)
        if file_extension in filetypes:
            resumes.append(file)   
    return resumes
resume_files = get_file_names_from_folder()



def get_file_properties(resume_files):
    file_properties = []
    for file in resume_files:
        file_name, file_extension = os.path.splitext(file)
        if file_extension in filetypes:
            filepath = folder+'/'+file
            filesize = os.path.getsize(filepath)/(1024*1024)
            filetype = file_extension
            file_properties.append([filepath,round(filesize,2),filetype])
        
    return file_properties

resume_files_properties = get_file_properties(resume_files)



def create_dataframe_for_files(resume_files,resume_files_properties):
    df = pd.DataFrame()
    df['File_name']=[x for x in resume_files]
    df['File_path']=[x[0] for x in resume_files_properties]
    df['File_size']=[x[1] for x in resume_files_properties]
    df['File_type']=[x[2] for x in resume_files_properties]
    pandarallel.initialize()
    df['File_text']=df['File_path'].parallel_apply(extract_text_from_resumes)
    # df['JSON_data']=df['File_text'].apply(extract_json_from_text)
    return df


def extract_text_from_resumes(File_path):
        if File_path.endswith(".pdf"):
            text = ""
            with pdfplumber.open(File_path) as pdf:
                for page in pdf.pages:  
                    text += page.extract_text() + '\n' 
            cleaned_text = text.replace('\n', ' ').replace('  ', ' ') 
            cleaned_text = ' '.join(cleaned_text.split())
            print(cleaned_text)
            return cleaned_text
        elif File_path.endswith(".docx"):
            text = docxpy.process(File_path)
            cleaned_text = text.replace('\n', ' ').replace('  ', ' ') 
            cleaned_text = ' '.join(cleaned_text.split())
            print(cleaned_text)
            return cleaned_text
    
dataframe = create_dataframe_for_files(resume_files,resume_files_properties)





def extract_json_from_text(File_text):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key="AIzaSyDdboS08dTCPmGGTeq62L5l7BA5cXPRZ8I")
    prompt_template = PromptTemplate.from_template(
        """Extract the following fields from the resume text 
1. first_name
2. last_name
3. emails
4. phones
5. skills
6. highest_degree_details
7. pg_degree
8. ug_degree
9. ug_graduation_year
10. first_working_date
11. state
12. city
13. company_history (Don't include internships and courses)
14. marital_status
15. gender
16. skill_bucket
17. domain_experience

Resume Text:
{resume_text}

Provide the details only in JSON datatype, with no extra lines or text or words so that the output can be converted into a proper json type
"""
    )

    chain = LLMChain(llm=llm, prompt=prompt_template)
    response = chain.run(resume_text=File_text)
    time.sleep(10)
    return json.loads(response)
dataframe['JSON_data']=dataframe['File_text'].apply(extract_json_from_text)





dataframe.to_parquet('/home/sanjay_kumar/Downloads/resume1.parquet', engine='pyarrow')

