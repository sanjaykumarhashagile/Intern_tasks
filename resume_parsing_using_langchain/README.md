
# FastAPI Resume Processor

This project is a FastAPI application that extracts key information from PDF resumes using the Langchain framework and Google Generative AI. The application takes a PDF file, processes it, and returns the extracted details in JSON format.

## Features

- Load PDF resumes using the `PyPDFLoader`.
- Extract essential information such as name, email, contact number, education details, skills, and more.
- Basic authentication for accessing the API.
- JSON response format for easy integration and usability.

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Langchain Community
- Langchain Google Generative AI
- Python-dotenv

## Environment Variables

Before running the application, you need to set the following environment variables. Create a `.env` file in the project directory or export them in your environment.

GOOGLE_API_KEY=<your_google_api_key> API_USERNAME=<your_api_username> API_PASSWORD=<your_api_password>

bash


## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd your-repo-name

    Install the required packages:

    bash

    pip install fastapi uvicorn python-dotenv langchain langchain-google-genai langchain-community jsons

Usage

    Add Your PDF Resume: Place the PDF resume you want to process in a known directory. Update the resume_file_path variable in main.py with the correct path to your PDF file.

    Run the Application:

    bash

uvicorn main:app --host 127.0.0.1 --port 5001

Access the API: Open your web browser or use a tool like Postman to send a GET request to the root endpoint.

arduino

    GET http://127.0.0.1:5001/

    You will need to provide basic authentication using the credentials specified in your environment variables.

    View Extracted Details: Upon successful authentication, the application will load the resume, extract the relevant fields, and return them in JSON format.

Example of JSON Response

Here’s what the extracted details might look like in JSON format:

json

{
    "name": "John Doe",
    "email": "johndoe@example.com",
    "contact_number": "+123456789",
    "education": {
        "degree": "B.Sc.",
        "major": "Computer Science",
        "university": "University of Example",
        "year_of_passout": "2020"
    },
    "college_name": "Example College",
    "skills": ["Python", "FastAPI", "Docker"],
    "internship_experiences": [
        {
            "company": "Example Corp",
            "role": "Intern",
            "duration": "3 months"
        }
    ],
    "soft_skills": ["Teamwork", "Communication"],
    "languages_known": ["English", "Spanish"],
    "courses": ["Web Development", "Data Science"]
}

Contributing

Contributions are welcome! Please feel free to submit issues or pull requests for enhancements or bug fixes.
License

This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

    FastAPI
    Langchain
    Python-dotenv

sql


Just copy everything from the beginning to the end and paste it into your `README.md` file!
