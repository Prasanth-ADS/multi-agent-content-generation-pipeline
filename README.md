# Multi-Agent Content Generation Pipeline (Python)

An AI-powered system that converts Product Requirements Documents into polished blog posts using 4 specialized agents.

## Agents

1. **Researcher** - Extracts topics and gathers relevant information
2. **Writer** - Creates a draft blog post based on research
3. **Fact-Checker** - Validates claims and citations
4. **Style-Polisher** - Improves readability and consistency

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Get Hugging Face API token from <https://huggingface.co/settings/tokens>

3. Add token to `.env` file:

   ```
   HUGGINGFACE_API_TOKEN=hf_your_token_here
   ```

4. Run connection test:

   ```bash
   python src/main.py
   ```

## Testing

Test the Researcher agent:

```bash
python src/tests/test_researcher.py
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
│   │   ├── sample_prd.py
│   │   └── test_researcher.py
│   └── main.py
├── logs/
├── requirements.txt
├── .env
└── README.md
```
