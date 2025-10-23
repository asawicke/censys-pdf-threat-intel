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