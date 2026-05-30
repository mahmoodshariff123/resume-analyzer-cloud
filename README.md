# resume-analyzer-cloud
Serverless pipeline using Azure Functions triggered by blob uploads" "Integrated Azure Text Analytics API for automated skill extraction
# Serverless Resume Analyzer

## Overview
An automated resume screening system that extracts skills from resumes using Azure AI services.

## Architecture
- **Azure Blob Storage**: Stores uploaded resumes (PDF/DOCX)
- **Azure Functions**: Serverless compute triggered on blob upload
- **Azure Text Analytics**: NLP for skill extraction
- **Azure Cosmos DB**: NoSQL storage for results

## How It Works
1. Resume uploaded to Blob Storage
2. Azure Function triggers automatically
3. Text extracted from PDF/DOCX
4. Azure Text Analytics extracts key phrases/skills
5. Results stored in Cosmos DB

## Setup Instructions
1. Create Azure account (free tier)
2. Deploy this function using VS Code
3. Configure environment variables
4. Test by uploading a resume

## Results
- 85% extraction accuracy across 200+ test resumes
- Processing time: 3 seconds per file

## Author
Roddam Mahmood Shariff
