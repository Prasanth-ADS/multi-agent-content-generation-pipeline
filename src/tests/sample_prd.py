"""Sample PRDs for testing the content pipeline."""

import sys
from pathlib import Path
# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.lib.types import PRDInput


sample_prd = PRDInput(
    title="Introduction to AI Agents for Developers",
    text="""
# Blog Post: Introduction to AI Agents

Target Audience: Software developers interested in AI
Tone: Professional but accessible
Length: 800-1000 words

Requirements:
- Explain what AI agents are
- Discuss practical applications
- Provide examples of agent frameworks
- Include best practices for building agents

Key Points to Cover:
1. Definition of AI agents
2. Difference between agents and traditional chatbots
3. Real-world use cases (customer service, content generation, data analysis)
4. Popular frameworks (LangChain, CrewAI, AutoGPT)
5. Tips for getting started with agent development

Technical Details:
- Mention multi-agent systems
- Discuss tool use and function calling
- Cover agent memory and context management
- Include code examples if relevant
    """.strip(),
    metadata={
        'category': 'technology',
        'priority': 'high',
    }
)


complex_prd = PRDInput(
    title="Product Launch: AI-Powered Code Review Assistant",
    text="""
# Product Launch Blog Post

Product: CodeGuard AI - An intelligent code review assistant
Target Audience: Engineering teams, CTOs, Tech leads
Launch Date: March 2024
Tone: Professional, innovative, trustworthy

Requirements:
- Announce the product launch
- Highlight key features and benefits
- Address security and privacy concerns
- Include customer testimonials
- Call-to-action for early access

Key Features:
1. Automated code review with AI analysis
2. Security vulnerability detection
3. Performance optimization suggestions
4. Integration with GitHub, GitLab, Bitbucket
5. Team collaboration features
6. Custom rule configuration

Benefits:
- Reduce code review time by 60%
- Catch bugs before production
- Enforce coding standards automatically
- Improve team productivity

Pricing: Starting at $49/month per developer
    """.strip(),
    metadata={
        'category': 'product-launch',
        'priority': 'urgent',
    }
)
