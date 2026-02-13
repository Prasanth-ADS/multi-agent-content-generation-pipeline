from src.lib.agents.researcher import run_researcher
from src.lib.agents.writer import run_writer
from src.lib.agents.fact_checker import run_fact_checker
from src.lib.agents.style_polisher import run_style_polisher
from src.lib.logger import generate_run_id
from src.lib.types import PRDInput
from src.lib.utils import count_words

def test_full_pipeline_with_web():
    """Test complete pipeline with web search and Phi-3"""
    
    print("="*70)
    print("Testing Full Pipeline: Web Search + Phi-3")
    print("="*70)
    print()
    
    # Create PRD about a current topic
    prd = PRDInput(
        title="AI Developments in 2024",
        text="""
# Blog Post: Recent AI Developments

Write an 800-word blog post about recent developments in AI.
Cover the latest breakthroughs, new models, and industry trends.

Target Audience: Tech professionals and AI enthusiasts
Tone: Informative and engaging
Length: 800-1000 words

Key Points:
- Latest AI models and their capabilities
- Industry trends and applications
- Future implications

Include specific examples and recent news.
        """.strip()
    )
    
    run_id = generate_run_id()
    print(f"Run ID: {run_id}\n")
    
    try:
        # Step 1: Research (with web search)
        print("[1/4] Running Researcher with web search...")
        research = run_researcher(prd, run_id)
        
        if not research.success:
            print("   Failed!")
            return
        
        print(f"   Success: {len(research.sources)} sources found")
        print(f"   Sources:")
        for i, source in enumerate(research.sources[:3], 1):
            print(f"     {i}. {source.title[:60]}...")
        print()
        
        # Step 2: Write (with Phi-3)
        print("[2/4] Running Writer with Phi-3...")
        draft = run_writer(prd, research, run_id)
        
        if not draft.success:
            print("   Failed!")
            return
        
        print(f"   Success: {draft.word_count} words, {len(draft.citations)} citations")
        print()
        
        # Step 3: Fact-check
        print("[3/4] Running Fact-Checker...")
        fact_check = run_fact_checker(draft, research, run_id)
        
        print(f"   Result: {'PASSED' if fact_check.passed else 'FAILED'}")
        print(f"   Issues: {len(fact_check.issues)}")
        
        # Retry if failed
        if not fact_check.passed and len(fact_check.issues) > 0:
            print("   Retrying with feedback...")
            draft = run_writer(prd, research, run_id, 
                             feedback=fact_check.feedback, 
                             retry_count=1)
            fact_check = run_fact_checker(draft, research, run_id, retry_count=1)
            print(f"   Retry result: {'PASSED' if fact_check.passed else 'FAILED'}")
        
        print()
        
        # Step 4: Polish
        print("[4/4] Running Style-Polisher...")
        final = run_style_polisher(draft, prd, run_id)
        
        final_word_count = count_words(final.polished)
        print(f"   Success: {final_word_count} words")
        print(f"   Changes: {len(final.changes)}")
        print()
        
        # Display results
        print("="*70)
        print("PIPELINE COMPLETE")
        print("="*70)
        print()
        print("Final Content Preview (first 500 chars):")
        print("-"*70)
        print(final.polished[:500])
        print("...")
        print("-"*70)
        print()
        
        print("Statistics:")
        print(f"  - Sources from web: {len(research.sources)}")
        print(f"  - Facts extracted: {len(research.facts)}")
        print(f"  - Final word count: {final_word_count}")
        print(f"  - Fact-check: {'PASSED' if fact_check.passed else 'FAILED'}")
        print()
        
        print("Test PASSED!")
        
    except Exception as e:
        print(f"\nTest FAILED: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_full_pipeline_with_web()
