import streamlit as st
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Import after environment variables are loaded
from document_processor import DocumentProcessor
from vectorstore import VectorStore
from agent import CPS230Agent

# Set page configuration
st.set_page_config(
  page_title="APRA CPS230 Assistance",
  page_icon=" 📗",
  layout="wide"
)

# Function to initialise session state
def initialize_session_state():
  if 'messages' not in st.session_state:
    st.session_state.messages = []

  if 'agent' not in st.session_state:
    # Check if vectorstore exists, if not create it
    vectorstore_path = "data/processed/vectorstore"
    if not os.path.exists(vectorstore_path):
      st.session_state.setup_status = "creating"
      with st.spinner("Setting up the CPS230 knowledge base...  This may take a few minutes."):
        # Check if PDF exists
        pdf_path = "data/cps230.pdf"
        if not os.path.exists(pdf_path):
          st.error(f"PDF file not found: {pdf_path}. Please ensure the CPS230 document is in the data directory.")
          st.stop()

        # Process document
        processor = DocumentProcessor()
        chunks = processor.process_document(pdf_path, "data/processed")

        # Create vector store
        vectorstore = VectorStore()
        vectorstore.create_from_documents(chunks)
        st.session_state.setup_status = "complete"
            
  else:
    st.session_state.setup_status = "complete"

  # Initialise agent
  vectorstore = VectorStore()
  st.session_state.agent = CPS230Agent(vectorstore)

# Initialise the session state
initialize_session_state()

# Display set up status if necessary
if st.session_state.setup_status == "creating":
    st.info("Setting up the knowledge base. This will only happen once.")
    st.experimental_rerun()

# Header
st.title("APRA CPS230 Compliance Assistant")
st.markdown("""
This assistant help you undersdtand and implement the requirements of APRA's CPS230 Prudential Standards
on Operational Risk Management. Ask questions about specific sections or requesdt implementation duidance.
""")

# Display chat messages
for message in st.session_state.message:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# Input for new message
if prompt := st.chat_input("Ask about CPS230..."):
  # Add user message to chat history
  st.session_state.message.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(promp)

  # Display assistant response
  with st.chat_message("assistant"):
    message_placeholder = st.empty()
    message_placeholder.markdown("Thinking...")

    try:
      # Get response from agent
      result = st.session_state.agent.run(
        prompt,
        chat_history=[(m["role"], m["content"]) for m in st.session_state.messages[:-1]]
      )

      response_content = result.get("output", "I'm having trouble processing your request.")

      # Update placeholder with response
      message_placeholder.,markdown(response_content)

      # Add assistant response to chat history
      st.session_state.messages.append({"role": "assistant", "content": error_message})

# Sidebar with examples
with st.sidebar:
  st.title("Example Questions")
  example_questions = [
    "Explain section 1 of CPS230 in  simple terms",
    "What are the key steps to implement section 15 of CPS230?",
    "What does CPS230 say about third-party risk management?",
    "How should a financial institution prepare for CPS230 compliance?",
    "What documentation is required for CPS230 compliance?"
  ]

  for question in example_questions:
    if st.button(question):
      # Clear input and add question
      st.session_state.messages.append({"role": "user", "content": question})
      st.experimental_rerun()
        
