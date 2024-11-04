
FROM python:3.10.12

WORKDIR /app

COPY main.py .

RUN pip install fastapi uvicorn python-dotenv langchain langchain-google-genai langchain-community pypdf

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
