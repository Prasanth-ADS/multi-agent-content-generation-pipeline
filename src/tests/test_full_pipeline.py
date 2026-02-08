import sys
import time
from pathlib import Path

# Add src to path
sys.path.append(str(Path.cwd()))

from src.lib.agents.researcher import run_researcher
from src.lib.agents.writer import run_writer
from src.lib.agents.fact_checker import run_fact_checker
from src.lib.agents.style_polisher import run_style_polisher
from src.lib.logger import generate_run_id, save_pipeline_result
from src.tests.sample_prd import sample_prd, complex_prd

def run_full_pipeline(prd, test_name="Test"):
    """Run complete pipeline and return results"""
    
    print(f"\n{'='*60}")
    print(f"Running Full Pipeline: {test_name}")
    print(f"{'='*60}\n")
    
    run_id = generate_run_id()
    start_time = time.time()
    
    # Step 1: Research
    research = run_researcher(prd, run_id)
    
    # Step 2: Write
    draft = run_writer(prd, research, run_id)
    
    # Step 3: Fact-check with retry loop
    max_retries = 3
    final_fact_check = None
    final_draft = draft
    
    for attempt in range(max_retries):
        fact_check = run_fact_checker(final_draft, research, run_id)
        final_fact_check = fact_check
        
        if fact_check.passed:
            break
        
        if attempt < max_retries - 1:
            print(f"[Pipeline] Revision attempt {attempt + 1}/{max_retries}")
            final_draft = run_writer(prd, research, run_id, 
                             feedback=fact_check.feedback, 
                             retry_count=attempt + 1)
    
    # Step 4: Polish
    final = run_style_polisher(final_draft, prd, run_id)
    
    # Calculate metrics
    duration = time.time() - start_time
    
    result = {
        'run_id': run_id,
        'test_name': test_name,
        'prd_title': getattr(prd, 'title', 'Untitled'),
        'duration_seconds': duration,
        'research': {
            'sources': len(research.sources),
            'facts': len(research.facts)
        },
        'draft': {
            'word_count': draft.word_count,
            'citations': len(draft.citations)
        },
        'fact_check': {
            'passed': final_fact_check.passed,
            'issues': len(final_fact_check.issues),
            'retries': attempt if 'attempt' in locals() else 0
        },
        'final': {
            'word_count': len(final.polished.split()),
            'changes': final.changes
        },
        'status': 'success' if final.success else 'failed'
    }
    
    # Save result
    save_pipeline_result(result)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Pipeline Summary: {test_name}")
    print(f"{'='*60}")
    print(f"Duration: {duration:.1f}s")
    print(f"Status: {result['status']}")
    print(f"Final word count: {result['final']['word_count']}")
    print(f"Fact-check: {'PASSED' if final_fact_check.passed else 'FAILED'}")
    print(f"{'='*60}\n")
    
    return result

def main():
    print("Full Pipeline Test Suite\n")
    
    try:
        # Test 1: Simple PRD
        result1 = run_full_pipeline(sample_prd, "Simple PRD")
        
        # Test 2: Complex PRD
        result2 = run_full_pipeline(complex_prd, "Complex PRD")
        
        # Overall summary
        print("\n" + "="*60)
        print("TEST SUITE COMPLETE")
        print("="*60)
        print(f"Test 1 (Simple): {result1['status']} - {result1['duration_seconds']:.1f}s")
        print(f"Test 2 (Complex): {result2['status']} - {result2['duration_seconds']:.1f}s")
        print("="*60)
    except Exception as e:
        print(f"Test suite failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
