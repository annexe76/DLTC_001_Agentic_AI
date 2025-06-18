# Dong Learns To Code Series!

Thanks for visiting my humble github repository where I practice how to code.
The first series is to build an Agentic.AI to conduct following procedure: 

  1. Extract data from a pdf file - APRA CPS230
  2. Build RAG using extracted data
  3. Create vector
  4. Using LangChain to orchestrate agent
  5. Streamlit to facilitate UX

## APRA CPS230 Compliance Assistant

This repository contains a proof-of_concept chatbot application that helps financial institutions understand
and implement the requirements of the Australian Prudential Regulation Authority's (APRA) Predential Standard CPS230
on Operational Risk Management.

## Features

- **Plain English Explanations**: Converts regulatory language into clear, accessible explanations
- **Implementation Guidance**: Provides step-by-step guidance for implementing CPS230 requirements
- **Interactive Chat Interface**: User-friendly Streamlit application for asking questions
- **RAG Architecture**: Uses Retrieval Augmented Generation to provide accurate, context-specific response

## Setup Instruction

## Prerequisites

- Python 3.9+
- OpenAI API Key

## Installation

1. Clone this repository

git clone https://github.com/annexe76/DLTC_001_Agentic_AI.git
cd DLTC_001_Agentic_AI

2. Create a virtual environment:

python -m venv venv
source venv/bin/active #On Windows: venv\Scripts\activate

3. Install dependencies:

pip install -r requirements.txt

4. Create a '.env' file in the root directory:

OPENAI_API_KEY=your_api_key_here

5. Add the CPS230 PDF document:
- Download the official APRA CPS230 document
- Place it in the 'data' folder with the name 'cps230.pdf'

### Running the application

1. Start the Streamlit application:

streamlit run src/app.py

2. Open your web browser and navigate to the URL displayed in the terminal (typically 'http://localhost:8501')

