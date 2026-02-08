"""
Multi-Agent Content Generation Pipeline
Main entry point for testing connections and running the pipeline.
"""

import sys
from pathlib import Path
# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.lib.ollama_client import test_connection


def main():
    """Main entry point."""
    
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                                                           ║")
    print("║      🚀 Content Pipeline - Python Version (Ollama)        ║")
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print("\n")
    
    print("📡 Step 1: Testing Ollama connection...\n")
    
    if test_connection():
        print("\n")
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║  ✅ Ollama connection successful!                         ║")
        print("║                                                           ║")
        print("║  Pipeline is ready for content generation!               ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print("\n")
        
        print("📋 Available agents:")
        print("   1. Researcher - Extract topics and gather sources")
        print("   2. Writer - Create draft blog post")
        print("   3. Fact Checker - Validate claims")
        print("   4. Style Polisher - Improve readability")
        print("\n")
        
        print("💡 Run test: python src/tests/test_researcher.py")
        print("\n")
        
    else:
        print("\n")
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║  ❌ Connection failed!                                    ║")
        print("║                                                           ║")
        print("║  Make sure Ollama is running: ollama serve                ║")
        print("║  And phi3 model is pulled: ollama pull phi3               ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print("\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
