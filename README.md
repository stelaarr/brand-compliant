# Brand Compliance Checker with Multimodal LLMs

## Overview

This project implements a workflow that uses multi-modal Large Language Models (LLMs) to assess brand compliance of creative assets (images) against a provided brand kit. 

### Usage

  1. Upload a brand kit (PDF) containing brand compliance information.
  
  2. Upload an image asset (JPG or PNG).

     ![image](https://github.com/user-attachments/assets/263c0516-a221-49da-8c72-e46584e9bb7c)

  
  3. The system extracts brand rules and the LLM evaluates compliance.

     ![image](https://github.com/user-attachments/assets/2ab698df-2bb0-441f-a825-c19a83518dbd)

     
  4. Receive a compliance score between 0 and 4, with optional detailed reasoning.

     ![image](https://github.com/user-attachments/assets/ab5b3e13-d9f0-4097-b5de-c67c3d2813a6)


---
## Project Structure

```
brand-compliance-checker/
├── app/
│ ├── main.py #  backend entry point
│ ├── parser.py # PDF parsing 
│ ├── llm_checker.py # Multi-modal LLM agent
│ └── llm_mock.py # Mock LLM implementation
├── frontend/
│ └── app.py # Streamlit app
├── Dockerfile 
├── docker-compose.yml 
└──  requirements.txt 
```

---

## Setup & Run Instructions

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/stelaarr/brand-compliance-checker.git
   cd brand-compliance-checker
   ```

2. Create and activate a Python virtual environment:
  ```bash 
  python -m venv venv
  source venv/bin/activate
  ```

3. Install dependencies:
  ```bash 
  pip install -r requirements.txt
  ```
4. Start the backend API:
  ```bash
  uvicorn app.main:app --reload
  ```
5. Launch the website:
  ```bash
  streamlit run frontend/app.py
  ```

#### Using Docker
Build and start both backend and frontend:
  ```bash
  docker-compose up --build

