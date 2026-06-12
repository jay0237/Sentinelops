# SentinelOps

Production-style backend security platform built with FastAPI, PostgreSQL, SQLAlchemy, and JWT authentication.

## Overview

SentinelOps is a backend-focused project designed to strengthen backend engineering, authentication systems, database architecture, and DevOps foundations.

The project focuses on building everything step-by-step manually instead of relying on AI-generated automation.

---

# Tech Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* JWT Authentication
* Passlib + Bcrypt
* Pydantic
* Uvicorn
* Prisidio

---

# Features
#fronted:
*React and Typescript
*real time security (working)
*add Threat Allocation

## Authentication System

* User Registration API
* User Login API
* Password Hashing using Bcrypt
* JWT Access Token Generation
* Secure Password Verification
* prompting auditorium
* Add Threat Scoring
* improving fronted
  

## Backend Architecture

* Dependency Injection
* SQLAlchemy ORM
* PostgreSQL Integration
* Structured Project Architecture
* Environment Variable Support
* add a log status
## API System

* Swagger Documentation
* JSON API Responses
* Request Validation
* Database Connectivity Check

---

# Project Structure

```bash
sentinelops/
│
├── app/
│   ├── config/
│   │   ├── base.py
│   │   ├── database.py
│   │   └── deps.py
│   │
│   ├── models/
│   │   └── user.py
│   │
│   ├── schemas/
│   │   └── user.py
│   │
│   ├── utils/
│   │   ├── auth.py
│   │   └── security.py
│   │
│   └── main.py
│
├── venv/
├── .env
├── requirements.txt
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/jay0237/Sentinelops.git
```

```bash
cd Sentinelops
```

---

# Create Virtual Environment

```bash
python -m venv venv
```

Activate:

## macOS/Linux

```bash
source venv/bin/activate
```

## Windows

```bash
venv\Scripts\activate
```

---

# Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv
```

```bash
pip install "passlib[bcrypt]"
```

```bash
pip install python-jose
```

```bash
pip install email-validator
```

---

# PostgreSQL Setup

Create database:

```sql
CREATE DATABASE sentinelops;
```

---

# Environment Variables

Create `.env` file:

```env
DATABASE_URL=postgresql://username:password@localhost/sentinelops
```

---

# Run Server

```bash
python -m uvicorn app.main:app --reload
```

Server:

```bash
http://127.0.0.1:8000
```

Swagger Docs:

```bash
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Health Check

```http
GET /health
```

---

## Database Check

```http
GET /db-check
```

---

## Register User

```http
POST /register
```

Example Request:

```json
{
  "username": "jay",
  "email": "jay@gmail.com",
  "password": "123456"
}
```

---

## Login User

```http
POST /login
```

Example Request:

```json
{
  "email": "jay@gmail.com",
  "password": "123456"
}
```

Example Response:

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer"
}
```

---

# Security Features

* Passwords hashed using Bcrypt
* JWT-based authentication
* Email validation
* Request validation with Pydantic
* Secure login verification

---

# Future Roadmap

* Protected Routes
* Role-Based Access Control
* Docker Integration
* Redis Caching
* API Rate Limiting
* CI/CD Pipeline
* Monitoring & Logging
* Kubernetes Deployment
* AI Security Monitoring

---

# Learning Goals

This project is focused on learning:

* Backend Engineering
* Authentication Systems
* Database Architecture
* API Design
* Security Engineering
* DevOps Foundations
* Production-Level Backend Development

---

# Author

## Jay Joshi

* GitHub: [https://github.com/jay0237](https://github.com/jay0237)
* LinkedIn: [https://www.linkedin.com/in/jay-joshi-12aa04283/](https://www.linkedin.com/in/jay-joshi-12aa04283/)

---

# License

This project is open-source and available
