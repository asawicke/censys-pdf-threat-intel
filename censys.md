# PDF Threat Intelligence Extraction Service - Take-Home Test

A FastAPI microservice that extracts threat actors and CVEs from PDF threat intelligence reports using AI agents.

## Project Overview

**Your Mission**: Build an AI-powered system that processes PDF threat intelligence reports and extracts structured data about threat actors and Common Vulnerabilities and Exposures (CVEs).

**End-to-End Workflow**:
1. **Upload PDF** → Service receives threat intelligence report PDF
2. **Extract Text** → Parse text content from PDF using Python libraries
3. **AI Analysis** → AI agent identifies and structures threat actors and CVEs
4. **Store Data** → Save results in SQLite with proper relationships
5. **Query API** → REST endpoints to search and retrieve extracted data

This tests your ability to:
- Build production-quality Python code following team guidelines
- Create FastAPI microservice with file upload handling
- Process PDF documents and extract text content
- Use AI Agents (autogen or equivalent framework as necessary) for structured data extraction
- Design relational database schema with proper relationships
- Write comprehensive tests and documentation

## Database Schema

Your SQLite database should have **three main tables**:

```sql
-- PDF documents table
pdf_documents (
  id UUID PRIMARY KEY,
  filename TEXT,
  uploaded_at TIMESTAMP,
  processed_at TIMESTAMP
)

-- Threat actors table
threat_actors (
  id UUID PRIMARY KEY,
  pdf_id UUID FOREIGN KEY, -- Links to pdf_documents.id
  name TEXT,
  aliases JSON, -- Array of known aliases
  description TEXT,
  extracted_at TIMESTAMP
)

-- CVEs table
cves (
  id UUID PRIMARY KEY,
  pdf_id UUID FOREIGN KEY, -- Links to pdf_documents.id
  cve_id TEXT, -- CVE-2023-12345 format
  description TEXT,
  severity TEXT,
  extracted_at TIMESTAMP
)
```

The `pdf_id` foreign key connects threat actors and CVEs to their source document, enabling queries like "show me all threats from document X".
To help set expectations, you should take no more than 4 hours to complete this task. We’re hoping you can get a sense of some of the types of problems we have to solve, as well as get exposed to some of the technology we use to solve them. We want to understand your ability to dive into something new and come up with a solution that other people can understand and build off of.

Please upload the code to a publicly accessible github or bitbucket account.  A readme file should be provided briefly documenting what you are delivering.  Like our own code, we expect testing instructions: whether it’s an automated test framework, or simple manual steps.