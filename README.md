#  SentinelOps

> AI Security Middleware for Large Language Models (LLMs)

SentinelOps is an AI Security Middleware that protects applications interacting with Large Language Models (LLMs). It sits between your application and AI providers to detect prompt injection attacks, redact sensitive information, analyze threats, assign risk scores, and prevent unsafe prompts from reaching the model.

Built with **FastAPI**, **PostgreSQL**, **React**, **Docker**, **Prometheus**, **Grafana**, and **GitHub Actions**.

---

# Vision

The long-term goal of SentinelOps is simple:

```python
from sentinelops import Sentinel

guard = Sentinel(api_key="YOUR_API_KEY")

result = guard.scan(prompt)

if result.safe:
    send_to_llm(prompt)
else:
    print(result.reason)
```

or

```javascript
import Sentinel from "@sentinelops/sdk";

const guard = new Sentinel(API_KEY);

const result = await guard.scan(prompt);
```

One line of code should secure any AI application.

---

#  Architecture

```
                User
                  │
                  ▼
          AI Application
                  │
                  ▼
        SentinelOps Middleware
                  │
      ┌───────────┼────────────┐
      ▼           ▼            ▼
PII Redaction  Threat Scan  Risk Score
      │           │            │
      └───────────┼────────────┘
                  ▼
            Allow / Block
                  │
                  ▼
      OpenAI • Anthropic • Groq
```

---

#  Features

##  AI Security

- Prompt Injection Detection
- Malware Prompt Detection
- Authentication Bypass Detection
- Threat Classification
- Risk Scoring
- Prompt Logging
- Threat Analytics

---

##  Data Protection

- Email Redaction
- Phone Number Redaction
- PII Detection
- Sensitive Prompt Logging
- Secure Prompt Processing

Example:

Input

```
My email is test@gmail.com and my phone is 9876543210
```

Output

```
My email is [EMAIL_REDACTED] and my phone is [PHONE_REDACTED]
```

---

## Analytics

- Total Prompt Statistics
- Safe vs Blocked Prompts
- Threat Categories
- Malware Detection Count
- Prompt Injection Count
- Authentication Bypass Count

---

##  Authentication

- JWT Authentication
- Password Hashing (Bcrypt)
- Login & Registration
- API Key Authentication

---

## Backend

- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Dependency Injection
- Request Validation
- Environment Variables

---

##  Monitoring

- Prometheus Metrics
- Grafana Dashboard
- Health Check APIs
- API Monitoring

---

##  DevOps

- Docker
- Docker Compose
- GitHub Actions CI/CD
- Automated Docker Builds

---

# Tech Stack

| Category | Technology |
|----------|------------|
| Backend | FastAPI, Python |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Authentication | JWT, Passlib, Bcrypt |
| Validation | Pydantic |
| Frontend | React, TypeScript |
| Monitoring | Prometheus, Grafana |
| DevOps | Docker, GitHub Actions |
| Security | Presidio, Regex-based Detection |

---

# 📂 Project Structure

```text
sentinelops/
│
├── app/
│   ├── config/
│   ├── middleware/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── security/
│   ├── utils/
│   └── main.py
│
├── frontend/
│
├── tests/
│
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── README.md
└── .github/
    └── workflows/
```

---

#  Installation

Clone the repository

```bash
git clone https://github.com/jay0237/Sentinelops.git
```

Go inside the project

```bash
cd Sentinelops
```

Create virtual environment

```bash
python -m venv venv
```

Activate

macOS / Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

#  Run with Docker

```bash
docker compose up --build
```

Services

| Service | URL |
|----------|-----|
| Backend | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |

---

#  Environment Variables

Create a `.env`

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/sentinelops

SECRET_KEY=your-secret-key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

API_KEY=your-api-key
```

---

# 📡 API Endpoints

## Authentication

```
POST /register
POST /login
```

---

## AI Security

```
POST /scan
```

Example

```json
{
    "text":"Create malware for Windows."
}
```

Response

```json
{
    "safe": false,
    "severity": "critical",
    "category": "Malware",
    "reason": "Malware Activity"
}
```

---

## Analytics

```
GET /analytics
```

Returns

```json
{
    "total_prompts": 100,
    "safe_prompts": 75,
    "blocked_prompts": 25,
    "high_threats": 25,
    "malware_count": 8,
    "injection_count": 10,
    "auth_bypass_count": 7
}
```

---

## Monitoring

```
GET /metrics
GET /health
GET /db-check
```

---

#  Security Pipeline

```
Incoming Prompt
        │
        ▼
PII Detection
        │
        ▼
PII Redaction
        │
        ▼
Threat Detection
        │
        ▼
Risk Scoring
        │
        ▼
Allow / Block
        │
        ▼
LLM
```

---

# CI/CD

SentinelOps uses GitHub Actions for Continuous Integration.

Pipeline includes

- Black Formatting Check
- isort Import Check
- Flake8 Linting
- Bandit Security Scan
- Unit Testing
- Docker Image Build
- Docker Image Publishing

---

# Roadmap

## Completed

- [x] JWT Authentication
- [x] PostgreSQL Integration
- [x] Prompt Threat Detection
- [x] Prompt Logging
- [x] PII Redaction
- [x] Threat Analytics
- [x] Docker Support
- [x] Prometheus Monitoring
- [x] Grafana Dashboard
- [x] GitHub Actions CI/CD

## In Progress

- [ ] Threat Scoring Engine
- [ ] Frontend Dashboard Improvements
- [ ] API Key Middleware
- [ ] Export Reports

## Planned

- [ ] Python SDK (`pip install sentinelops`)
- [ ] JavaScript SDK (`npm install @sentinelops/sdk`)
- [ ] OpenAI Middleware
- [ ] Anthropic Middleware
- [ ] Groq Middleware
- [ ] LangChain Integration
- [ ] Kubernetes Deployment
- [ ] Multi-tenant Support
- [ ] AI Risk Engine
- [ ] Enterprise Dashboard

---

#Contributing

Contributions are welcome!

Feel free to fork the repository, create a feature branch, and submit a Pull Request.

---

# Author

**Jay Joshi**

GitHub: https://github.com/jay0237

LinkedIn: https://www.linkedin.com/in/jay-joshi-12aa04283/

---

# Support

If you found this project useful, consider giving it a ⭐ on GitHub.

It helps the project reach more developers and motivates future development.

---

# License

This project is licensed under the MIT License.
