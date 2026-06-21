# Company RAG Assistant

AI-powered document assistant built with FastAPI, React, PostgreSQL, pgvector and OpenAI.

## Overview

Company RAG Assistant is a secure Retrieval-Augmented Generation (RAG) platform that allows company employees to upload internal documents and ask natural language questions about them.

The system extracts document content, generates vector embeddings, stores them in PostgreSQL using pgvector, and retrieves the most relevant information to answer user queries.

---

## Features

### Authentication & Authorization

* JWT Authentication
* Secure Password Hashing
* Role-Based Access Control (RBAC)

Supported roles:

| Role     | Permissions                                                 |
| -------- | ----------------------------------------------------------- |
| ADMIN    | Full access, user management, role management, delete users |
| MANAGER  | Document management, employee management                    |
| EMPLOYEE | Ask questions and access company knowledge                  |

---

### Document Management

* PDF Upload
* PDF Text Extraction
* Automatic Chunking
* Vector Embedding Generation
* Document Listing
* Document Deletion

---

### AI-Powered Question Answering

Users can ask questions in natural language:

Examples:

* What are Concurrency Patterns?
* Explain the Observer Pattern.
* What are the responsibilities of a Project Manager?
* Summarize chapter 3.

The system:

1. Converts the question into an embedding.
2. Searches similar document chunks using vector similarity.
3. Retrieves the most relevant content.
4. Generates an AI answer using OpenAI.

---

### Chat History

* User-specific chat history
* Automatic history cleanup on logout
* Persistent storage in PostgreSQL

---

### User Management

Admin users can:

* View all users
* Change user roles
* Delete users

Managers can:

* View employees
* Manage company documents

---

## System Architecture

```text
React Frontend
      │
      ▼
FastAPI Backend
      │
      ├── JWT Authentication
      ├── Role Management
      ├── RAG Engine
      │
      ▼
PostgreSQL + pgvector
      │
      ▼
OpenAI Embeddings + GPT
```

---

## Technology Stack

### Frontend

* React
* Axios
* Vite
* CSS3

### Backend

* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn

### Database

* PostgreSQL
* pgvector

### AI

* OpenAI Embeddings
* OpenAI Chat Models

### Security

* JWT
* Passlib
* Bcrypt

### DevOps

* Docker
* Docker Compose
* Git
* GitHub

---

## Database Schema

### Users

```text
id
email
password
role
created_at
```

### Documents

```text
id
filename
created_at
```

### Chunks

```text
id
document_id
page_number
content
embedding
```

### Chat Messages

```text
id
user_id
question
answer
created_at
```

---

## Running Locally

### Clone Repository

```bash
git clone https://github.com/yigitsancar/company-rag-assistant.git
cd company-rag-assistant
```

### Configure Environment

Create:

```bash
backend/.env
```

Example:

```env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/companyrag
OPENAI_API_KEY=your_openai_api_key
ADMIN_API_KEY=your_admin_api_key
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Start Application

```bash
docker compose up --build
```

Frontend:

```text
http://localhost:3000
```

Backend:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

## Current Status

### Completed

* Authentication
* Authorization
* User Management
* PDF Upload
* Vector Database
* Embeddings
* Semantic Search
* AI Question Answering
* Chat History
* Dockerization

### Planned

* AWS Deployment
* Domain & HTTPS
* Hybrid Search (BM25 + Vector Search)
* Local LLM Support (Ollama)
* Conversation Memory
* Re-ranking
* Audit Logs

---

## Author

Yiğit Sancar

Software Engineering Student

Interested in:

* Backend Development
* DevOps
* Cloud Computing
* AI Systems
* Retrieval-Augmented Generation (RAG)

GitHub:

https://github.com/yigitsancar
