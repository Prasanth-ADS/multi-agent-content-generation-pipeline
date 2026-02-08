"""Test script for the Researcher Agent."""

import sys
from pathlib import Path
# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.lib.agents.researcher import run_researcher
from src.lib.logger import generate_run_id
from src.tests.sample_prd import sample_prd


def test_researcher():
    """Test the Researcher Agent with sample PRD."""
    
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                                                           ║")
    print("║      🔬 Researcher Agent Test (Python)                    ║")
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print("\n")
    
    # Log PRD details
    print("📄 PRD Details:")
    print(f"   Title: {sample_prd.title}")
    print(f"   Length: {len(sample_prd.text)} characters")
    print(f"   Category: {sample_prd.metadata.get('category', 'N/A') if sample_prd.metadata else 'N/A'}")
    print("\n")
    
    # Generate run ID
    run_id = generate_run_id()
    print(f"🆔 Run ID: {run_id}\n")
    
    try:
        # Run the researcher
        print("🚀 Starting Researcher Agent...\n")
        
        import time
        start_time = time.time()
        
        result = run_researcher(sample_prd, run_id)
        
        duration = time.time() - start_time
        
        # Log results
        print("\n")
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║  📊 Research Results                                      ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print("\n")
        
        print(f"✅ Success: {result.success}")
        print(f"⏱️  Duration: {duration:.1f}s")
        print(f"📚 Sources: {len(result.sources)}")
        print(f"📝 Facts: {len(result.facts)}")
        print("\n")
        
        # List topics (source titles)
        print("🔍 Topics Researched:")
        for i, source in enumerate(result.sources, 1):
            topic = source.title.replace('Research Article: ', '')
            print(f"   {i}. {topic} (relevance: {source.relevance})")
        print("\n")
        
        # Show sample facts
        print("💡 Sample Facts:")
        for i, fact in enumerate(result.facts[:3], 1):
            truncated = fact[:80] + '...' if len(fact) > 80 else fact
            print(f"   {i}. {truncated}")
        print("\n")
        
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║  ✅ Test Passed!                                          ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print("\n")
        
        print(f"💾 Log file created: logs/{run_id}.json")
        print("\n")
        
    except Exception as e:
        print("\n")
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║  ❌ Test Failed!                                          ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print("\n")
        
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        sys.exit(1)


if __name__ == "__main__":
    test_researcher()
