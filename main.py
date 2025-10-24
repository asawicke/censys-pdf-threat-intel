from fastapi import FastAPI, UploadFile, File, HTTPException
from pdfminer.high_level import extract_text
from sqlalchemy import create_engine, Column, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import ForeignKey
from uuid import uuid4
import os, re, shutil


app = FastAPI(title="PDF Threat Intelligence Extraction Service")

# Database setup (SQLite database engine - threatintel.db)
Base = declarative_base()
engine = create_engine("sqlite:///threatintel.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# Table storing uploaded PDF documents and their timestamps
class PDFDocument(Base):
    __tablename__ = "pdf_documents"
    id = Column(String, primary_key=True)
    filename = Column(String)
    uploaded_at = Column(DateTime)
    processed_at = Column(DateTime)


# Table for extracted threat actors
class ThreatActor(Base):
    __tablename__ = "threat_actors"
    id = Column(String, primary_key=True)
    pdf_id = Column(String, ForeignKey("pdf_documents.id"))
    name = Column(String)
    extracted_at = Column(DateTime)

# Table for extracted CVEs
class CVE(Base):
    __tablename__ = "cves"
    id = Column(String, primary_key=True)
    pdf_id = Column(String, ForeignKey("pdf_documents.id"))
    cve_id = Column(String)
    extracted_at = Column(DateTime)


Base.metadata.create_all(engine)

# Helper functions
def extract_entities(text: str):
    actors = re.findall(r"\b(?:DEV-\d{4,}|FIN\d{2,})\b", text)
    cves = re.findall(r"\bCVE-\d{4}-\d{4,7}\b", text)
    return list(set(actors)), list(set(cves))


# Routes
@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    """
     Upload a PDF, extract its text content, detect threat actors and CVEs,
     and store the structured results in the SQLite database.
    """

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    os.makedirs("uploads", exist_ok=True)

    pdf_id = str(uuid4()) # unique ID for each document

     # Save the uploaded PDF to disk
    path = f"uploads/{pdf_id}.pdf"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text from the PDF using pdfminer.six
    try:
        text = extract_text(path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF extraction failed: {e}")

    # Extract threat actors and CVEs from the text
    actors, cves = extract_entities(text)
    now = datetime.utcnow()
    db = SessionLocal()
    db.add(PDFDocument(id=pdf_id, filename=file.filename, uploaded_at=now, processed_at=now))
    for a in actors:
        db.add(ThreatActor(id=str(uuid4()), pdf_id=pdf_id, name=a, extracted_at=now))
    for c in cves:
        db.add(CVE(id=str(uuid4()), pdf_id=pdf_id, cve_id=c, extracted_at=now))
    db.commit()
    db.close()

    # Return structured JSON response
    return {"pdf_id": pdf_id, "actors_found": actors, "cves_found": cves}


@app.get("/actors/")
def list_actors():
    """Return all extracted threat actors with their source document IDs."""
    db = SessionLocal()
    results = db.query(ThreatActor).all()
    db.close()
    return [{"name": a.name, "pdf_id": a.pdf_id} for a in results]


@app.get("/cves/")
def list_cves():
    """Return all extracted CVEs with their associated PDF IDs."""
    db = SessionLocal()
    results = db.query(CVE).all()
    db.close()
    return [{"cve_id": c.cve_id, "pdf_id": c.pdf_id} for c in results]


@app.get("/documents/")
def list_docs():
    """List all processed PDF documents."""
    db = SessionLocal()
    results = db.query(PDFDocument).all()
    db.close()
    return [{"id": d.id, "filename": d.filename, "processed_at": d.processed_at} for d in results]


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Welcome to the PDF Threat Intelligence Extraction API!"}

