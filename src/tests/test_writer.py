"""Test script for the Writer Agent."""

import sys
from pathlib import Path
# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.lib.agents.researcher import run_researcher
from src.lib.agents.writer import run_writer
from src.lib.logger import generate_run_id
from src.tests.sample_prd import sample_prd


def test_writer():
    """Test the Writer Agent with sample PRD."""
    
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                                                           ║")
    print("║      ✍️  Writer Agent Test (Python)                        ║")
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print("\n")
    
    # Generate run ID
    run_id = generate_run_id()
    print(f"🆔 Run ID: {run_id}\n")
    
    try:
        # Step 1: Run researcher
        print("📚 Step 1: Running researcher...\n")
        research = run_researcher(sample_prd, run_id)
        
        if not research.success:
            print("❌ Research failed!")
            sys.exit(1)
        
        print(f"\n✅ Research complete: {len(research.sources)} sources, {len(research.facts)} facts\n")
        
        # Step 2: Run writer
        print("-" * 60)
        print("\n✍️  Step 2: Running writer...\n")
        
        import time
        start_time = time.time()
        
        result = run_writer(sample_prd, research, run_id)
        
        duration = time.time() - start_time
        
        # Display results
        print("\n")
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║  📝 Writer Output                                         ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print("\n")
        
        print(f"✅ Success: {result.success}")
        print(f"⏱️  Duration: {duration:.1f}s")
        print(f"📊 Word count: {result.word_count}")
        print(f"🔗 Citations: {len(result.citations)}")
        print("\n")
        
        # Draft preview
        print("📖 Draft preview (first 500 chars):")
        print("-" * 60)
        preview = result.draft[:500] if len(result.draft) > 500 else result.draft
        print(preview)
        print("-" * 60)
        print("\n")
        
        # Citations used
        print(f"📚 Citations used: {result.citations}")
        print("\n")
        
        # Validation
        if result.word_count >= 500:
            print("╔═══════════════════════════════════════════════════════════╗")
            print("║  ✅ Test Passed - Draft generated successfully!           ║")
            print("╚═══════════════════════════════════════════════════════════╝")
        else:
            print(f"⚠️  Warning: Draft is short ({result.word_count} words)")
            print("   Expected at least 500 words for a complete blog post")
        
        print("\n")
        print(f"💾 Log file: logs/{run_id}.json")
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
    test_writer()
