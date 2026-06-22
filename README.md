# Company RAG Platform

Company RAG Platform is a full-stack AI-powered document question-answering platform.
It allows users to upload company documents, ask natural language questions, and receive AI-generated answers based on the uploaded documents.

The project was developed as a production-ready MVP using FastAPI, React, PostgreSQL with pgvector, Docker, AWS EC2, Nginx, JWT authentication, and role-based access control.

---

## Features

* User registration and login
* JWT-based authentication
* Role-based authorization

  * ADMIN
  * MANAGER
  * EMPLOYEE
* PDF document upload
* PDF text extraction
* Text chunking
* OpenAI embedding generation
* PostgreSQL + pgvector semantic search
* RAG-based question answering
* Source preview for retrieved document chunks
* Admin dashboard
* User management
* Document management
* Dockerized deployment
* AWS EC2 deployment
* Elastic IP configuration
* Nginx reverse proxy
* Docker auto restart

---

## User Roles

### ADMIN

ADMIN users can:

* Ask questions
* Upload documents
* List documents
* Delete documents
* View dashboard statistics
* List users
* Change user roles
* Delete users

### MANAGER

MANAGER users can:

* Ask questions
* Upload documents
* List documents
* Delete documents

### EMPLOYEE

EMPLOYEE users can:

* Ask questions based on uploaded documents

---

## Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* pgvector
* OpenAI API
* JWT
* Passlib / bcrypt
* Uvicorn

### Frontend

* React
* Vite
* Axios
* CSS

### Infrastructure

* Docker
* Docker Compose v2
* AWS EC2
* Elastic IP
* Nginx Reverse Proxy
* Ubuntu Server

---

## System Architecture

```text
User
↓
React Frontend
↓
Nginx Reverse Proxy
↓
FastAPI Backend
↓
PostgreSQL + pgvector
↓
OpenAI Embeddings / Chat Completion
```

---

## RAG Pipeline

### Document Upload Flow

```text
PDF Upload
↓
Text Extraction
↓
Chunking
↓
Embedding Generation
↓
Vector Storage in PostgreSQL
```

### Question Answering Flow

```text
User Question
↓
Question Embedding
↓
Similarity Search with pgvector
↓
Relevant Chunks Retrieved
↓
Context Sent to OpenAI
↓
Answer + Sources Returned
```

---

## Database Tables

The project uses the following main tables:

* `users`
* `documents`
* `chunks`
* `chat_messages`

### users

Stores registered users and their roles.

### documents

Stores uploaded document metadata.

### chunks

Stores extracted document chunks and their vector embeddings.

### chat_messages

Prepared for storing question-answer history.

---

## Deployment

The project is deployed on AWS EC2 using Docker Compose.

### Running Containers

```text
company-rag-frontend
company-rag-backend
company-rag-postgres
```

### Public Access

```text
http://13.62.87.94
```

The application is served through Nginx reverse proxy.

```text
/      → Frontend
/api/  → Backend
```

---

## Docker Commands

Start the project:

```bash
docker compose up -d --build
```

Stop the project:

```bash
docker compose down
```

Check running containers:

```bash
docker ps
```

View backend logs:

```bash
docker logs company-rag-backend --tail=100
```

---

## Environment Variables

The backend requires a `.env` file.

Example:

```env
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/companyrag
OPENAI_API_KEY=your_openai_api_key
ADMIN_API_KEY=your_admin_api_key
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

The real `.env` file is not committed to GitHub.

---

## Current Status

The MVP is completed and deployed.

Completed features:

* Authentication
* Authorization
* Role management
* Document upload
* Document delete
* Vector search
* AI question answering
* Source preview
* Admin dashboard
* Docker deployment
* EC2 deployment
* Nginx reverse proxy
* Auto restart policy

---

## Future Improvements

Possible future improvements:

* HTTPS with SSL certificate
* Custom domain
* CI/CD with GitHub Actions
* Audit logs
* Better dashboard analytics
* PDF preview
* Local embedding model support
* Local LLM support with Ollama
* Advanced hybrid search
* Reranking for better retrieval quality

---

## Author

Developed by Yiğit Sancar
Final-year Software Engineering student
