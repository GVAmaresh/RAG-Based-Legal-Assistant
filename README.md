# RAG-Based-Legal-Assistant

> Team: **Access Denied**
>
> Hackathon Project: **Aventus**

Aventus is a RAG-based legal assistant created during a hackathon to help lawyers and users get quick, accurate answers to legal questions—without flipping through thousands of pages in legal books.

It uses Retrieval-Augmented Generation (RAG) with LLaMA 2, BERT (bert-base-uncased), and the LangChain framework to extract grounded answers from domain-specific resources like books on Intellectual Property and Patent Law.

## Features
#### Book-Based Legal Q&A
- Ask questions directly from legal books and get accurate, contextual answers.

#### RAG Pipeline (LLaMA 2 + BERT)
- Retrieval and generation system combines the strengths of transformer-based models.

#### Next.js Frontend + API Backend
- Fast, interactive UI built in Next.js with API connection to the RAG system.

#### MongoDB Integration
- Used for storing book chunks, embeddings, and user interactions.

#### Designed for Legal Experts & General Users
- Makes legal knowledge accessible and understandable.

## Tech Stack

| Component       | Technology                                       |
| --------------- | ------------------------------------------------ |
| **LLMs**        | LLaMA 2, BERT (bert-base-uncased)                |
| **Framework**   | LangChain                                        |
| **Frontend**    | Next.js                                            |
| **Backend**     | Node.js / Python FastAPI *(based on your stack)* |
| **Database**    | MongoDB                                          |
| **Data Source** | Legal books (IP, Patents, etc.)                  |


## Folder Structure

```
RAG-Based-Legal-Assistant/
├── frontend/        # Next.js UI
├── backend/         # API server and RAG logic and Database Connection
```

## Setup Instructions
#### Backend (RAG System)
```bash

cd backend
pip install -r requirements.txt  # or npm install (if Node)
python app.py                    # or npm run dev
```
Make sure you have access to LLaMA 2 weights and BERT. Use HuggingFace or local models.

#### Frontend
```bash

cd frontend
npm install
npm run dev
```
Ensure .env or config file points to the correct backend API URL.

### Sample Queries
- *"What is considered a patent violation?"*

- *"Can software be patented under Indian law?"*

- *"What falls under fair use in copyright?"*

The model responds using **book-based knowledge**, not generic web data.

## Use Case
Helps:

- Lawyers to avoid time-consuming manual reference checks

- General users to understand rights without legal jargon

- Academicians for quick citation from domain texts

## Future Scope
- Citation references and source tracking

- Authentication and role management

- Add books from more legal domains (e.g., contract law, cyber law)

- Voice query and multilingual support


## Hackathon Impact
Built in limited time under intense constraints

Applied real-world NLP (RAG) to solve an important legal accessibility problem

