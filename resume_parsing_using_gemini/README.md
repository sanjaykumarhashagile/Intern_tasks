
# Resume Parser with Google Generative AI

This project is a Python script that leverages Google Generative AI to extract key information from PDF and DOCX resumes. The application analyzes the content of the resume files and returns important details in JSON format.

## Features

- Supports both PDF and DOCX file formats for resume parsing.
- Extracts key information such as name, email, contact number, education details, skills, internship experiences, and more.
- Handles JSON response parsing with error handling for invalid JSON formats.

## Requirements

- Python 3.8+
- `google-generativeai` package
- `json` module (part of Python's standard library)

## Environment Variables

To use this application, you need to set the following environment variable:

GEMINI_API_KEY=<your_gemini_api_key>

bash


You can set this variable in your environment or create a `.env` file in the project directory.

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd your-repo-name

    Install required packages:

    Make sure you have google-generativeai installed. If you haven't installed it yet, you can do so using pip:

    bash

    pip install google-generativeai

Usage

    Prepare Your Resume: Place the PDF or DOCX resume you want to process in a known directory. Update the filepath variable in the script with the correct path to your resume file.

    Run the Script:

    Execute the Python script:

    bash

    python your_script_name.py

    View Output: The script will print the extracted details in JSON format to the console.

Example Output

When processing a resume, the output may look like this:

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

Error Handling

The script includes error handling to manage cases where the response from the Google Generative AI is not a valid JSON. If an error occurs during the extraction process, an error message will be printed to the console.
Contributing

Contributions are welcome! Feel free to submit issues or pull requests for improvements or bug fixes.
License

This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

    Google Generative AI
