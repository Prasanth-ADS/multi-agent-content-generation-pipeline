# Multi-Agent Content Generation Pipeline

An AI-powered system that converts Product Requirements Documents (PRDs) into polished, publication-ready blog posts using a coordinated team of 4 specialized AI agents.

## Overview

This pipeline automates the entire content creation process:

1. **Researcher Agent** - Extracts topics and gathers relevant information
2. **Writer Agent** - Creates an initial draft with citations
3. **Fact-Checker Agent** - Verifies claims and triggers revisions if needed
4. **Style-Polisher Agent** - Refines tone, style, and clarity

## Features

- Fully automated content generation (PRD → blog post)
- Automatic fact-checking with retry logic
- Complete audit trail (all steps logged)
- Multiple output formats (markdown, text)
- Batch processing support
- CLI and programmatic interfaces

## Requirements

- Python 3.8+
- Ollama (installed and running)
- 16GB RAM recommended
- Internet connection
-mobile

## Installation

### 1. Clone/Download the Project

```bash
cd content-pipeline
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create `.env` file:

```bash
OLLAMA_MODEL=phi3
LOG_TO_FILE=true
API_KEY=demo-api-key-123
USE_WEB_SEARCH=true
```

Make sure Ollama is running:

```bash
ollama serve
ollama pull phi3
```

### 4. Test Connection

```bash
python src/main.py
```

## Usage

### Quick Start

```bash
# From command line (easiest)
python src/cli.py --text "Write a blog about AI agents for developers" --title "AI Agents Guide"

# Interactive mode
python src/cli.py --interactive
```

### File Input

Create a text file (e.g., `my_prd.txt`) with your requirements, then run:

```bash
python src/cli.py --file my_prd.txt --output blog.md
```

### Batch Processing

To process multiple files, sort them into a folder (e.g., `prds/`) and run:

```bash
python src/batch_process.py ./prds ./outputs
```

### Programmatic Usage

```python
from src.lib.agents.researcher import run_researcher
from src.lib.agents.writer import run_writer
from src.lib.agents.fact_checker import run_fact_checker
from src.lib.agents.style_polisher import run_style_polisher
from src.lib.types import PRDInput
from src.lib.logger import generate_run_id

# Create PRD
prd = PRDInput(
    text="Your PRD content here...",
    title="Blog Post Title"
)

run_id = generate_run_id()

# Run pipeline
research = run_researcher(prd, run_id)
draft = run_writer(prd, research, run_id)
fact_check = run_fact_checker(draft, research, run_id)
final = run_style_polisher(draft, prd, run_id)

print(final.polished)
```

## Project Structure

```text
content-pipeline/
├── src/
│   ├── lib/
│   │   ├── agents/
│   │   │   ├── researcher.py
│   │   │   ├── writer.py
│   │   │   ├── fact_checker.py
│   │   │   └── style_polisher.py
│   │   ├── ollama_client.py
│   │   ├── types.py
│   │   ├── logger.py
│   │   └── utils.py
│   ├── tests/
│   ├── cli.py
│   ├── batch_process.py
│   └── main.py
├── logs/           # (Local only)
├── requirements.txt
├── .env
└── README.md
```

## Sample PRD Format

When using a file input, format your text like this:

```text
# Blog Post: Introduction to AI Agents

Target Audience: Software developers
Tone: Professional but accessible
Length: 800-1000 words

Requirements:
- Explain what AI agents are
- Discuss practical applications
- Provide examples of frameworks

Key Points:
1. Definition of AI agents
2. Difference from chatbots
3. Real-world use cases
4. Popular frameworks (LangChain, CrewAI)
```

## Logging

All pipeline runs are logged to `logs/`:

- `logs/run_XXXXX.json` - Individual run logs
- `logs/master.jsonl` - Master log file
- `logs/results/` - Final pipeline results

## Performance

Typical pipeline execution:

- Duration: 20-50 seconds
- Output: 800-1500 words
- Success rate: ~95%

## Troubleshooting

**Model not found:**

- Run `ollama pull phi3`

**Connection failed:**

- Ensure Ollama is running (`ollama serve`)
- Verify `OLLAMA_MODEL` in `.env` matches your pulled model

## Cost

- Local Inference: Free (via Ollama)
- Web Search: Free (via DuckDuckGo)

## License

MIT License

## Credits

Built with:

- Ollama
- Microsoft Phi-3 Model
- DuckDuckGo Search
- Python 3.x
