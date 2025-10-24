# PDF Threat Intellengence Extraction Service
A FastAPI microservice that extracts threat actors and CVEs from PDF threat intelligence reports using AI agents.

## Overview
This AI-powered service receives a PDF report, extracts text content, and identifies structured cybersecurity entities.

## How it works
1. Upload a PDF file via `/upload/`
2. Text is extracted using `pdfminer.six`
3. Regex-based logic identifies actors and CVEs
4. Data is stored in SQLite for easy retrieval

## Installation
Clone the repository and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn sqlalchemy pdfminer.six python-multipart
```

## Setup
Run the FastAPI sever: 
```uvicorn main:app --reload```
Then go to http://127.0.0.1:8000/

## Documentation
FastAPI documentation https://fastapi.tiangolo.com/#requirements