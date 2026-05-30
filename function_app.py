import azure.functions as func
import logging
import json
import os
from azure.storage.blob import BlobServiceClient
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import PyPDF2
import docx

app = func.FunctionApp()

# This function runs when a blob is uploaded
@app.blob_trigger(arg_name="myblob", 
                   path="resumes/{name}",
                   connection="AzureWebJobsStorage")
def analyze_resume(myblob: func.InputStream):
    logging.info(f"Processing resume: {myblob.name}")
    
    # Step 1: Extract text from PDF/DOCX
    text = extract_text_from_blob(myblob)
    
    # Step 2: Call Azure Text Analytics to extract skills
    skills = extract_skills_with_azure(text)
    
    # Step 3: Store results in Cosmos DB
    store_in_cosmosdb(myblob.name, skills)
    
    logging.info(f"Extracted skills: {skills}")
    return skills

def extract_text_from_blob(blob):
    """Extract text from PDF or DOCX file"""
    # Check file extension
    if blob.name.endswith('.pdf'):
        # PDF extraction logic
        pdf_reader = PyPDF2.PdfReader(blob)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    elif blob.name.endswith('.docx'):
        # DOCX extraction logic
        doc = docx.Document(blob)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    else:
        return blob.read().decode('utf-8')

def extract_skills_with_azure(text):
    """Call Azure Text Analytics API to extract key phrases (skills)"""
    # Get API credentials from environment variables
    endpoint = os.environ["TEXT_ANALYTICS_ENDPOINT"]
    key = os.environ["TEXT_ANALYTICS_KEY"]
    
    # Create client
    client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )
    
    # Extract key phrases
    response = client.extract_key_phrases(documents=[text])
    key_phrases = response[0].key_phrases
    
    # Filter for skills (you can add custom logic here)
    # Common skill keywords
    skill_keywords = ["Python", "Java", "SQL", "Azure", "AWS", 
                      "React", "Node.js", "Docker", "Kubernetes"]
    
    extracted_skills = [phrase for phrase in key_phrases 
                        if any(skill.lower() in phrase.lower() 
                        for skill in skill_keywords)]
    
    return extracted_skills

def store_in_cosmosdb(filename, skills):
    """Store results in Cosmos DB"""
    # Cosmos DB connection
    cosmos_url = os.environ["COSMOS_DB_URL"]
    cosmos_key = os.environ["COSMOS_DB_KEY"]
    database_name = "ResumeDB"
    container_name = "Results"
    
    # Document to store
    document = {
        "id": filename.replace("/", "_"),
        "filename": filename,
        "skills": skills,
        "timestamp": str(datetime.now())
    }
    
    # Store in Cosmos DB
    client = CosmosClient(cosmos_url, credential=cosmos_key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    container.upsert_item(document)
