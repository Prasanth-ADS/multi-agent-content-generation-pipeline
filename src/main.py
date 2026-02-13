from lib.ollama_client import test_connection
from cli import main as cli_main
import sys

def main():
    """Main entry point - test connection and show usage"""
    
    print("\n" + "="*70)
    print("MULTI-AGENT CONTENT GENERATION PIPELINE")
    print("="*70 + "\n")
    
    # Test connection
    print("Testing Ollama connection...")
    if not test_connection():
        print("\nConnection failed. Make sure Ollama is running ('ollama serve')")
        sys.exit(1)
    
    print("\nConnection successful!\n")
    print("="*70)
    print("USAGE")
    print("="*70)
    print("\nRun the pipeline:")
    print("  python src/cli.py --text 'Your PRD here' --title 'Blog Title'")
    print("\nFor more options:")
    print("  python src/cli.py --help")
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If arguments provided, run CLI
        cli_main()
    else:
        # Otherwise show help
        main()
