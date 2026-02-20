# ContentForge AI

**Multi-Agent Content Generation Pipeline**

A production-ready AI system that transforms Product Requirements Documents (PRDs) into publication-ready blog posts using a coordinated team of 4 specialized AI agents with automatic fact-checking, style refinement, and multi-format export.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)]()

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Deployment](#deployment)
- [Performance](#performance)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

ContentForge AI automates the entire content creation workflow by employing a multi-agent architecture where each agent specializes in a specific task:

1. **Researcher Agent** - Searches the web and extracts relevant information
2. **Writer Agent** - Creates initial drafts with proper citations
3. **Fact-Checker Agent** - Verifies claims and triggers revisions if needed
4. **Style-Polisher Agent** - Refines tone, grammar, and readability

**Input:** A Product Requirements Document (PRD) - a simple text brief describing what you want written.

**Output:** A complete, fact-checked, professionally written blog post in your choice of format (Markdown, HTML, PDF, or DOCX).

**Time:** 30-60 seconds from PRD to finished content.

---

## ✨ Features

### Core Capabilities

- ✅ **Multi-Agent Architecture** - 4 specialized agents working in sequence
- ✅ **Web Search Integration** - Real-time information gathering via DuckDuckGo
- ✅ **Automatic Fact-Checking** - Verifies claims with up to 3 revision attempts
- ✅ **Multiple Output Formats** - Markdown, HTML, PDF, DOCX
- ✅ **REST API** - Full-featured FastAPI service with authentication
- ✅ **Async Processing** - Celery + Redis for background job management
- ✅ **Progress Tracking** - Real-time status updates during generation
- ✅ **Complete Audit Trail** - Full logging of all pipeline executions
- ✅ **CLI Interface** - Command-line tool for quick content generation
- ✅ **Batch Processing** - Process multiple PRDs simultaneously

### Production Features

- 🔒 **Authentication** - API key and JWT token support
- 📊 **Progress Monitoring** - Track generation progress in real-time
- ♻️ **Retry Logic** - Automatic retry with exponential backoff
- 📝 **Comprehensive Logging** - Structured logs for debugging
- 🎨 **Customizable Output** - Configurable formatting and styling
- 🚀 **Scalable Architecture** - Horizontal scaling via Celery workers

---

## 🏗️ System Architecture
```
┌─────────────────────────────────────────────────────┐
│                  FastAPI REST API                   │
│                                                     │
│  POST /api/generate  →  GET /api/status/{id}      │
│  GET /api/download/{id}                            │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│              Celery + Redis Queue                   │
│          (Asynchronous Task Processing)             │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│           Multi-Agent Pipeline (Sequential)         │
│                                                     │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐       │
│  │Researcher│ → │  Writer  │ → │Fact-Check│       │
│  │          │   │          │   │          │       │
│  │Web Search│   │  Draft   │   │ Verify   │       │
│  └──────────┘   └──────────┘   └────┬─────┘       │
│                                      │             │
│                              Failed? │             │
│                              ┌───────┘             │
│                              ▼                     │
│                      ┌──────────────┐              │
│                      │ Retry Writer │              │
│                      │ (max 3 times)│              │
│                      └──────┬───────┘              │
│                             │                      │
│                             ▼                      │
│                      ┌──────────┐                  │
│                      │ Polisher │                  │
│                      │          │                  │
│                      │  Refine  │                  │
│                      └─────┬────┘                  │
└────────────────────────────┼─────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │Format Converter│
                    │(MD/HTML/PDF/   │
                    │     DOCX)      │
                    └────────┬───────┘
                             │
                             ▼
                      Final Output
```

### Agent Workflow
```
PRD Input
    │
    ▼
┌───────────────────────────────────────────────────┐
│ 1. RESEARCHER (5-10s)                             │
│ ─────────────────────                             │
│ • Extract topics from PRD                         │
│ • Search web for each topic                       │
│ • Gather sources and snippets                     │
│ • Extract key facts                               │
│                                                   │
│ Output: ResearchOutput (sources + facts)          │
└────────────────────┬──────────────────────────────┘
                     │
                     ▼
┌───────────────────────────────────────────────────┐
│ 2. WRITER (15-25s)                                │
│ ──────────────────                                │
│ • Analyze PRD requirements                        │
│ • Incorporate research findings                   │
│ • Generate structured blog post                   │
│ • Add citations from sources                      │
│                                                   │
│ Output: WriterOutput (draft + citations)          │
└────────────────────┬──────────────────────────────┘
                     │
                     ▼
┌───────────────────────────────────────────────────┐
│ 3. FACT-CHECKER (5-10s)                           │
│ ───────────────────────                           │
│ • Verify claims against sources                   │
│ • Identify unsupported statements                 │
│ • Generate revision feedback                      │
│ • Pass/Fail decision                              │
│                                                   │
│ Output: FactCheckOutput (passed + issues)         │
└────────────────────┬──────────────────────────────┘
                     │
              Failed? │ Yes → Return to Writer (max 3x)
                     │ No
                     ▼
┌───────────────────────────────────────────────────┐
│ 4. STYLE-POLISHER (5-8s)                          │
│ ─────────────────────────                         │
│ • Improve clarity and readability                 │
│ • Enhance tone and flow                           │
│ • Fix grammar and punctuation                     │
│ • Strengthen transitions                          │
│                                                   │
│ Output: StylePolisherOutput (polished content)    │
└────────────────────┬──────────────────────────────┘
                     │
                     ▼
              Format & Export
           (MD, HTML, PDF, DOCX)
```

---

## 🛠️ Technology Stack

### Core Framework
- **Language:** Python 3.8+
- **API Framework:** FastAPI (0.104+)
- **Task Queue:** Celery (5.3+) + Redis (5.0+)
- **Server:** Uvicorn (ASGI)

### AI & LLM Infrastructure
- **Inference Engine:** Ollama (local LLM serving)
- **Default Model:** Microsoft Phi-3-mini-4k-instruct
- **Web Search:** DuckDuckGo Search API (duckduckgo-search)
- **Architecture:** Custom multi-agent system (no LangChain/CrewAI)

### Output Processing
- **Document Generation:**
  - `python-docx` - Word documents (DOCX)
  - `xhtml2pdf` - PDF generation
  - `markdown2` - HTML conversion
- **Data Validation:** Pydantic (2.5+)
- **Configuration:** python-dotenv

### Development Tools
- **Testing:** pytest
- **API Documentation:** Swagger UI (built-in FastAPI)
- **Logging:** Python logging module + file-based persistence

---

## 📦 Installation

### Prerequisites

Ensure you have the following installed:

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Redis** - [Installation Guide](https://redis.io/download)
- **Ollama** - [Download](https://ollama.ai/download)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/contentforge-ai.git
cd contentforge-ai
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
# Core Framework
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
celery>=5.3.4
redis>=5.0.0

# AI & LLM
ollama>=0.1.7
duckduckgo-search>=4.1.0

# Output Processing
python-docx>=1.1.0
xhtml2pdf>=0.2.13
markdown2>=2.4.0

# Utilities
pydantic>=2.5.0
python-dotenv>=1.0.0
python-multipart>=0.0.6
aiofiles>=23.2.1

# Authentication
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4

# WebSockets
websockets>=12.0
```

### Step 4: Set Up Ollama
```bash
# Pull the Phi-3 model
ollama pull phi3

# Verify installation
ollama run phi3 "Hello, are you working?"
```

### Step 5: Configure Environment Variables

Create a `.env` file in the project root:
```bash
# Copy template
cp .env.example .env

# Edit with your settings
nano .env
```

**.env:**
```bash
# Ollama Configuration
OLLAMA_MODEL=phi3
OLLAMA_HOST=http://localhost:11434

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# API Configuration
API_KEY=your-secure-api-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Logging
LOG_TO_FILE=true
LOG_LEVEL=INFO

# Web Search
USE_WEB_SEARCH=true
MAX_SOURCES_PER_TOPIC=2
```

### Step 6: Initialize Database and Logs
```bash
# Create necessary directories
mkdir -p logs outputs uploads

# Set permissions (Linux/macOS)
chmod 755 logs outputs uploads
```

---

## 🚀 Quick Start

### Option 1: Using Startup Script (Recommended)

**Windows:**
```bash
.\start_all.bat
```

**Linux/macOS:**
```bash
chmod +x start_all.sh
./start_all.sh
```

This will start all services:
1. Redis server
2. Celery worker
3. FastAPI server
4. Ollama (if not running)

### Option 2: Manual Startup

**Terminal 1 - Start Ollama:**
```bash
ollama serve
```

**Terminal 2 - Start Redis:**
```bash
# Windows (WSL)
sudo service redis-server start

# macOS
brew services start redis

# Linux
sudo systemctl start redis
```

**Terminal 3 - Start Celery Worker:**
```bash
celery -A api.celery_app worker --loglevel=info --pool=solo
```

**Terminal 4 - Start FastAPI Server:**
```bash
python run_api.py
```

### Verify Installation

Open your browser and navigate to:

- **API Root:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs (Swagger UI)
- **Health Check:** http://localhost:8000/health

You should see:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

---

## 💻 Usage

### CLI Interface

#### Basic Usage
```bash
# Generate from text
python src/cli.py --text "Write a blog about Python programming" --title "Python Guide"

# Generate from file
python src/cli.py --file examples/sample_prd.txt --output blog.md

# Specify output format
python src/cli.py --file prd.txt --format html --output blog.html
python src/cli.py --file prd.txt --format pdf --output blog.pdf
python src/cli.py --file prd.txt --format docx --output blog.docx

# Interactive mode
python src/cli.py --interactive
```

#### CLI Options
```bash
python src/cli.py --help

Options:
  --text TEXT        PRD text directly
  --file FILE        Path to PRD file
  --interactive      Interactive mode
  --title TITLE      Blog post title
  --output OUTPUT    Output file path
  --format FORMAT    Output format: md, html, pdf, docx (default: md)
  --help            Show this message and exit
```

### API Interface

#### 1. Generate Content

**Request:**
```bash
curl -X POST "http://localhost:8000/api/generate" \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "prd_text": "Write an 800-word blog post about AI agents for developers",
    "title": "Understanding AI Agents",
    "format": "html"
  }'
```

**Response:**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "message": "Job queued for processing",
  "estimated_time": 60
}
```

#### 2. Check Status

**Request:**
```bash
curl -X GET "http://localhost:8000/api/status/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer your-api-key"
```

**Response (In Progress):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress": 45,
  "current_step": "Writer",
  "created_at": "2024-01-15T10:30:00.000Z"
}
```

**Response (Completed):**
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": 100,
  "current_step": "Complete",
  "result": {
    "run_id": "run_1705315800_abc123",
    "download_url": "/api/download/550e8400-e29b-41d4-a716-446655440000",
    "format": "html",
    "word_count": 856,
    "fact_check_passed": true
  },
  "created_at": "2024-01-15T10:30:00.000Z",
  "completed_at": "2024-01-15T10:30:42.000Z"
}
```

#### 3. Download Result

**Request:**
```bash
curl -X GET "http://localhost:8000/api/download/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer your-api-key" \
  -o output.html
```

### Python SDK
```python
from src.lib.agents.researcher import run_researcher
from src.lib.agents.writer import run_writer
from src.lib.agents.fact_checker import run_fact_checker
from src.lib.agents.style_polisher import run_style_polisher
from src.lib.types import PRDInput
from src.lib.logger import generate_run_id

# Create PRD
prd = PRDInput(
    title="My Blog Post",
    text="""
    Write an 800-word blog post about Python programming.
    Target audience: beginners
    Tone: friendly and encouraging
    """
)

# Generate run ID
run_id = generate_run_id()

# Execute pipeline
research = run_researcher(prd, run_id)
draft = run_writer(prd, research, run_id)
fact_check = run_fact_checker(draft, research, run_id)

# Retry if needed
if not fact_check.passed:
    draft = run_writer(prd, research, run_id, 
                      feedback=fact_check.feedback, 
                      retry_count=1)
    fact_check = run_fact_checker(draft, research, run_id, retry_count=1)

# Polish
final = run_style_polisher(draft, prd, run_id)

print(final.polished)
```

### Batch Processing

Process multiple PRDs at once:
```bash
python src/batch_process.py ./input_prds ./output_blogs
```

This will:
1. Find all `.txt` and `.md` files in `./input_prds`
2. Process each one through the pipeline
3. Save outputs to `./output_blogs`
4. Generate a summary JSON file

---

## 📚 API Documentation

### Interactive Documentation

Access the full interactive API documentation at:

**Swagger UI:** http://localhost:8000/docs

**ReDoc:** http://localhost:8000/redoc

### Endpoints Overview

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | API root information | No |
| GET | `/health` | Health check | No |
| POST | `/api/generate` | Submit generation job | Yes |
| GET | `/api/status/{job_id}` | Check job status | Yes |
| GET | `/api/download/{job_id}` | Download result | Yes |
| DELETE | `/api/jobs/{job_id}` | Delete job and files | Yes |

### Request/Response Models

#### GenerateRequest
```json
{
  "prd_text": "string (50-10000 chars, required)",
  "title": "string (optional)",
  "format": "md|html|pdf|docx (default: md)"
}
```

#### JobStatusResponse
```json
{
  "job_id": "string (UUID)",
  "status": "pending|processing|completed|failed",
  "progress": "integer (0-100)",
  "current_step": "string (optional)",
  "result": {
    "run_id": "string",
    "download_url": "string",
    "format": "string",
    "word_count": "integer",
    "fact_check_passed": "boolean"
  },
  "error": "string (if failed)",
  "created_at": "datetime",
  "completed_at": "datetime (optional)"
}
```

### Authentication

The API supports two authentication methods:

**1. API Key (Header):**
```bash
Authorization: Bearer your-api-key-here
```

**2. JWT Token:**
```bash
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## ⚙️ Configuration

### Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OLLAMA_MODEL` | LLM model to use | `phi3` | No |
| `OLLAMA_HOST` | Ollama server URL | `http://localhost:11434` | No |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` | Yes |
| `API_KEY` | API authentication key | None | Yes |
| `JWT_SECRET_KEY` | JWT signing key | None | Yes |
| `CORS_ORIGINS` | Allowed CORS origins | `*` | No |
| `LOG_TO_FILE` | Enable file logging | `true` | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |
| `USE_WEB_SEARCH` | Enable web search | `true` | No |
| `MAX_SOURCES_PER_TOPIC` | Sources per topic | `2` | No |

### Model Configuration

Supported Ollama models:
```bash
# Default (recommended)
OLLAMA_MODEL=phi3

# Alternatives
OLLAMA_MODEL=llama2
OLLAMA_MODEL=mistral
OLLAMA_MODEL=mixtral
```

To use a different model:
```bash
# Pull the model
ollama pull mistral

# Update .env
OLLAMA_MODEL=mistral

# Restart services
```

### Output Format Configuration

Default settings in `src/lib/formatters.py`:
```python
# HTML styling
HTML_FONT_FAMILY = "Arial, sans-serif"
HTML_MAX_WIDTH = "800px"
HTML_LINE_HEIGHT = "1.6"

# PDF page size
PDF_PAGE_SIZE = "A4"
PDF_MARGIN = "2cm"

# DOCX styles
DOCX_FONT_NAME = "Calibri"
DOCX_FONT_SIZE = 11
```

---

## 📁 Project Structure
```
contentforge-ai/
│
├── api/                          # FastAPI application
│   ├── __init__.py
│   ├── main.py                  # FastAPI app entry point
│   ├── celery_app.py            # Celery configuration
│   ├── celery_tasks.py          # Background tasks
│   ├── auth.py                  # Authentication logic
│   ├── models.py                # Pydantic models
│   ├── config.py                # Configuration settings
│   └── routes/                  # API routes
│       ├── __init__.py
│       └── knowledge.py         # Knowledge base routes (optional)
│
├── src/                          # Core pipeline code
│   ├── lib/                     # Library modules
│   │   ├── agents/              # Agent implementations
│   │   │   ├── __init__.py
│   │   │   ├── researcher.py   # Researcher agent
│   │   │   ├── writer.py       # Writer agent
│   │   │   ├── fact_checker.py # Fact-checker agent
│   │   │   └── style_polisher.py # Style-polisher agent
│   │   │
│   │   ├── ollama_client.py    # Ollama API client
│   │   ├── web_search.py       # Web search integration
│   │   ├── formatters.py       # Output format converters
│   │   ├── types.py            # Type definitions
│   │   ├── logger.py           # Logging utilities
│   │   └── utils.py            # Helper functions
│   │
│   ├── tests/                   # Test modules
│   │   ├── __init__.py
│   │   ├── sample_prd.py       # Sample PRDs
│   │   ├── test_researcher.py  # Researcher tests
│   │   ├── test_writer.py      # Writer tests
│   │   ├── test_fact_checker.py # Fact-checker tests
│   │   ├── test_style_polisher.py # Polisher tests
│   │   └── test_full_pipeline.py # Integration tests
│   │
│   ├── cli.py                   # CLI interface
│   ├── batch_process.py         # Batch processing
│   └── main.py                  # Main entry point
│
├── examples/                     # Example PRD files
│   ├── ai_agents_prd.txt
│   ├── product_launch_prd.txt
│   └── python_tutorial_prd.txt
│
├── logs/                         # Log files (auto-generated)
│   ├── master.jsonl             # Master log
│   ├── results/                 # Pipeline results
│   └── run_*.json               # Individual run logs
│
├── outputs/                      # Generated content (auto-generated)
│   └── *.md, *.html, *.pdf, *.docx
│
├── uploads/                      # Temporary file uploads
│
├── .env                          # Environment configuration
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
├── run_api.py                   # API server startup
├── start_all.bat                # Windows startup script
├── start_all.sh                 # Linux/macOS startup script
├── LICENSE                      # MIT License
└── README.md                    # This file
```

---

## 🧪 Testing

### Run All Tests
```bash
# Run full test suite
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest src/tests/test_researcher.py

# Run with coverage report
pytest --cov=src --cov-report=html
```

### Individual Agent Tests
```bash
# Test Researcher
python src/tests/test_researcher.py

# Test Writer
python src/tests/test_writer.py

# Test Fact-Checker
python src/tests/test_fact_checker.py

# Test Style-Polisher
python src/tests/test_style_polisher.py

# Test Full Pipeline
python src/tests/test_full_pipeline.py
```

### API Tests
```bash
# Test API endpoints
python api/test_api.py

# Test with cURL
curl http://localhost:8000/health
```

### Load Testing
```bash
# Install locust
pip install locust

# Run load test
locust -f tests/load_test.py --host http://localhost:8000
```

---

## 🚀 Deployment

### Docker Deployment

#### Build Docker Image
```bash
docker build -t contentforge-ai:latest .
```

#### Run with Docker Compose
```bash
docker-compose up -d
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_models:/root/.ollama
    ports:
      - "11434:11434"

  celery:
    build: .
    command: celery -A api.celery_app worker --loglevel=info
    depends_on:
      - redis
      - ollama
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
      - ./outputs:/app/outputs

  api:
    build: .
    command: uvicorn api.main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    depends_on:
      - redis
      - ollama
      - celery
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
      - ./outputs:/app/outputs

volumes:
  redis_data:
  ollama_models:
```

### Cloud Deployment (Railway)

1. **Create Railway Project:**
```bash
   railway init
```

2. **Add Redis:**
```bash
   railway add redis
```

3. **Configure Environment:**
   - Add all variables from `.env`
   - Update `OLLAMA_HOST` to cloud endpoint

4. **Deploy:**
```bash
   railway up
```

### Cloud Deployment (Render)

1. Create `render.yaml`:
```yaml
services:
  - type: web
    name: contentforge-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn api.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
      - key: REDIS_URL
        fromService:
          name: redis
          type: redis
          property: connectionString

  - type: redis
    name: redis
    ipAllowList: []

  - type: worker
    name: celery-worker
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: celery -A api.celery_app worker --loglevel=info
```

2. Push to GitHub and connect to Render

---

## 📊 Performance

### Benchmarks

| Metric | Value | Notes |
|--------|-------|-------|
| **Avg Generation Time** | 30-60s | Depends on PRD length |
| **Researcher Speed** | 5-10s | With 3-5 web searches |
| **Writer Speed** | 15-25s | 800-1000 words |
| **Fact-Checker Speed** | 5-10s | Per check |
| **Polisher Speed** | 5-8s | Final refinement |
| **Success Rate** | 95%+ | With retry logic |
| **Throughput** | 60-120/hr | Single worker |

### Scalability

**Vertical Scaling:**
- Increase Celery workers: `celery worker --concurrency=4`
- Add more Redis memory
- Use faster LLM (e.g., larger Ollama models)

**Horizontal Scaling:**
- Deploy multiple Celery workers across machines
- Use Redis Cluster for job queue
- Load balance API servers

**Optimization Tips:**
- Cache web search results (15min TTL)
- Batch similar PRDs
- Use smaller models for fact-checking
- Pre-warm Ollama models

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Ollama Connection Failed

**Error:**
```
[Ollama] Connection failed: connection refused
```

**Solution:**
```bash
# Check if Ollama is running
ollama ps

# Start Ollama
ollama serve

# Verify model is pulled
ollama list
ollama pull phi3
```

#### 2. Redis Connection Error

**Error:**
```
redis.exceptions.ConnectionError: Connection refused
```

**Solution:**
```bash
# Windows (WSL)
sudo service redis-server start
redis-cli ping

# macOS
brew services start redis

# Linux
sudo systemctl start redis
sudo systemctl enable redis
```

#### 3. Celery Worker Not Processing

**Error:**
Jobs stuck in "pending" state

**Solution:**
```bash
# Check worker status
celery -A api.celery_app inspect active

# Restart worker
celery -A api.celery_app worker --loglevel=info --pool=solo

# Clear queue
celery -A api.celery_app purge
```

#### 4. Model Loading Timeout

**Error:**
```
[Ollama] Model loading timeout
```

**Solution:**
```bash
# Pre-load model
ollama run phi3 "test"

# Check model size and available RAM
ollama list

# Use smaller model if needed
ollama pull phi3:mini
```

#### 5. Out of Memory

**Error:**
```
MemoryError: Unable to allocate memory
```

**Solution:**
- Use smaller model (phi3:mini instead of phi3)
- Reduce `max_tokens` in agent calls
- Increase system swap space
- Use cloud-hosted LLM instead of local

#### 6. Web Search Rate Limit

**Error:**
```
[WebSearcher] Rate limit exceeded
```

**Solution:**
```python
# Increase delay in web_search.py
time.sleep(2)  # Instead of 1

# Reduce MAX_SOURCES_PER_TOPIC in .env
MAX_SOURCES_PER_TOPIC=1
```

### Debug Mode

Enable detailed logging:
```bash
# Set in .env
LOG_LEVEL=DEBUG

# Run with verbose output
python -v src/cli.py --text "test"
```

### Check Logs
```bash
# View recent logs
tail -f logs/master.jsonl

# View specific run
cat logs/run_XXXXX.json | jq

# Check API logs
tail -f logs/api.log

# Check Celery logs
tail -f logs/celery.log
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Install dev dependencies: `pip install -r requirements-dev.txt`
4. Make your changes
5. Run tests: `pytest`
6. Commit: `git commit -m 'Add amazing feature'`
7. Push: `git push origin feature/amazing-feature`
8. Open a Pull Request

### Code Style

- Follow PEP 8 style guide
- Use type hints
- Add docstrings for all functions
- Keep functions under 50 lines
- Write tests for new features

### Testing Requirements

All PRs must:
- Pass existing tests
- Include new tests for added features
- Maintain >80% code coverage
- Include documentation updates

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
MIT License

## Credits

Built with:

- Ollama
- Microsoft Phi-3 Model
- DuckDuckGo Search
- Python 3.x
