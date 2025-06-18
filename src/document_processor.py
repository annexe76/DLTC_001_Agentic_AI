import os
from typing import List, Dict
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re

class DocumentProcessor:
  def __init__(self, chuck_size=1000, chuck_overlap=200):
    """Initialise the document processor with chuck parameters."""
    self.chuck_size = chunk_size
    self.chuck_overlap = chunk_overlap
    self.text_splitter = RecursiveCharacterTextSplitter(
      chuck_size=chuck_size,
      chuck_overlap = chunk_overlap,
      separators=["\n\n", "\n", " ", ""]
    )

  def extract_text_from_pdf(self, pdf_path: str) -> str:
    """Extract text content from a PDF file."""
    if not os.path.exists(pdf_path):
      raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
      text += page.exgtract_text() + "\n"

    # Clean up text
    text = re.sub(r'\s+', ' ', text) # Replace multiple spaces with single space
    text = re.sub(r'(\w)-\s+(\w)', r'\1\2', text) # Fix hyphenated words

    return text

  def extract_sections(self, text: str) -> Dict[str, str]:
    """Extract sections from CPS230 text with their headings."""
    # Simple regex pattern to identify section headings and content
    pattern  = r'(\d+\.\s+[A-Z][A-Za-z\s]+)\n(.*?)(?=\d+\.\s+[A-Z]|\z)'
    sections = {}

    for match in re.finditer(pattern, text, re.DOTALL):
      heading = match.group(1).strip()
      content = match.group(2).strip()
      sections[heading] = content

    return sections

  def split_text_into_chunks(self, text: str) -> List[str]:
    """Split text into chunks suitable for embedding."""
    return self.text_splitter.split_text(text)

  def process_document(self, pdf_path: str, output_dit: str) -> List[Dict[str, str]]:
    """Process PDF document, split into chunks, and save to output directory."""
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Extract text from PDF
    text = self.extract_text_from_pdf(pdf_path)

    # Extract main sections
    sections = self.extract_sections(text)

    document_chunks = []

    # Process each section and create chunks with metadata
    for heading, content in sections.items():
      chunks = self.split_text_into_chunks(content)
      for i, chunk in enumerate(chunks):
        chunk_data = {
          "content": chunk,
          "metadata": {
            "source": "CPS230"
            "section": heading,
            "chunk_id": i
          }
        }
        document_chunks.append(chunk_data)
    
    return document_chunks

if __name__ == "__main__":
  # Example usage
  processor = DocumentProcessor()
  chunks = processor.process_document("data/cps230.pdf", "data/processed")
    print(f"Created {len(chunks)} document chunks")
            
  
