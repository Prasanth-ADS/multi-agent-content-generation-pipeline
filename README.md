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
- Hugging Face account (free)
- 16GB RAM recommended
- Internet connection

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
HUGGINGFACE_API_TOKEN=your_token_here
HF_MODEL=meta-llama/Llama-3.1-8B-Instruct
LOG_TO_FILE=true
```

Get your token from: <https://huggingface.co/settings/tokens>

### 4. Test Connection

```bash
python src/main.py
```

## Usage

### Quick Start

```bash
# From command line
python src/cli.py --text "Write a blog about AI agents for developers" --title "AI Agents Guide"

# From file
python src/cli.py --file examples/ai_agents_prd.txt --output blog.md

# Interactive mode
python src/cli.py --interactive
```

### Batch Processing

Process multiple PRD files:

```bash
python src/batch_process.py ./examples ./outputs
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

```
content-pipeline/
├── src/
│   ├── lib/
│   │   ├── agents/
│   │   │   ├── researcher.py
│   │   │   ├── writer.py
│   │   │   ├── fact_checker.py
│   │   │   └── style_polisher.py
│   │   ├── huggingface_client.py
│   │   ├── types.py
│   │   ├── logger.py
│   │   └── utils.py
│   ├── tests/
│   ├── cli.py
│   ├── batch_process.py
│   └── main.py
├── examples/
├── logs/
├── requirements.txt
├── .env
└── README.md
```

## Examples

See `examples/` directory for sample PRDs.

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

**Model loading error:**

- Wait 30 seconds and retry
- First run always slower (model warm-up)

**Rate limit error:**

- Free tier: ~1000 requests/day
- Wait or upgrade to Hugging Face Pro

**Connection failed:**

- Check HUGGINGFACE_API_TOKEN in .env
- Verify internet connection

## Cost

- Hugging Face API: Free tier (sufficient for development)
- No GPU required (uses cloud inference)

## License

MIT License

## Credits

Built with:

- Hugging Face Inference API
- Llama 3.1 8B model
- Python 3.x
