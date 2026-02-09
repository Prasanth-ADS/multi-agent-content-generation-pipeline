import sys
import argparse
from pathlib import Path
from lib.agents.researcher import run_researcher
from lib.agents.writer import run_writer
from lib.agents.fact_checker import run_fact_checker
from lib.agents.style_polisher import run_style_polisher
from lib.logger import generate_run_id, print_log_summary, save_pipeline_result
from lib.types import PRDInput
from lib.utils import count_words
import time

def run_pipeline(prd_text: str, title: str = None, output_file: str = None):
    """Run the complete multi-agent pipeline"""
    
    print("\n" + "="*70)
    print("MULTI-AGENT CONTENT GENERATION PIPELINE")
    print("="*70 + "\n")
    
    # Create PRD input
    prd = PRDInput(text=prd_text, title=title)
    run_id = generate_run_id()
    
    print(f"Run ID: {run_id}")
    print(f"PRD Title: {title or 'Untitled'}")
    print(f"PRD Length: {len(prd_text)} characters\n")
    
    start_time = time.time()
    
    try:
        # Step 1: Research
        print("[1/4] Researcher Agent - Gathering sources and facts...")
        research = run_researcher(prd, run_id)
        print(f"      Found {len(research.sources)} sources, {len(research.facts)} facts\n")
        
        # Step 2: Write
        print("[2/4] Writer Agent - Creating draft...")
        draft = run_writer(prd, research, run_id)
        print(f"      Generated {draft.word_count} words, {len(draft.citations)} citations\n")
        
        # Step 3: Fact-check with retry
        print("[3/4] Fact-Checker Agent - Verifying claims...")
        max_retries = 3
        fact_check = None
        
        for attempt in range(max_retries):
            fact_check = run_fact_checker(draft, research, run_id, retry_count=attempt)
            
            if fact_check.passed:
                print(f"      Fact-check PASSED - {len(fact_check.issues)} issues\n")
                break
            
            print(f"      Fact-check FAILED - {len(fact_check.issues)} issues found")
            
            if attempt < max_retries - 1:
                print(f"      Retrying ({attempt + 1}/{max_retries - 1})...")
                draft = run_writer(prd, research, run_id, 
                                 feedback=fact_check.feedback, 
                                 retry_count=attempt + 1)
            else:
                print(f"      Warning: Proceeding with unresolved issues\n")
        
        # Step 4: Polish
        print("[4/4] Style-Polisher Agent - Refining content...")
        final = run_style_polisher(draft, prd, run_id)
        final_word_count = count_words(final.polished)
        print(f"      Applied {len(final.changes)} improvements")
        print(f"      Final: {final_word_count} words\n")
        
        # Save result
        duration = time.time() - start_time
        
        result = {
            'run_id': run_id,
            'prd_title': title,
            'duration_seconds': round(duration, 2),
            'final_content': final.polished,
            'research': {'sources': len(research.sources), 'facts': len(research.facts)},
            'draft': {'word_count': draft.word_count, 'citations': len(draft.citations)},
            'fact_check': {'passed': fact_check.passed, 'issues': len(fact_check.issues)},
            'final': {'word_count': final_word_count, 'changes': len(final.changes)},
            'status': 'success'
        }
        
        save_pipeline_result(result)
        
        # Output final content
        if output_file:
            output_path = Path(output_file)
            output_path.write_text(final.polished)
            print(f"Content saved to: {output_file}")
        else:
            print("\n" + "="*70)
            print("FINAL CONTENT")
            print("="*70 + "\n")
            print(final.polished)
            print("\n" + "="*70)
        
        # Summary
        print("\n" + "="*70)
        print("PIPELINE SUMMARY")
        print("="*70)
        print(f"Status: SUCCESS")
        print(f"Duration: {duration:.1f} seconds")
        print(f"Final word count: {final_word_count}")
        print(f"Fact-check: {'PASSED' if fact_check.passed else 'FAILED'}")
        print(f"Run ID: {run_id}")
        print("="*70 + "\n")
        
        return result
        
    except Exception as e:
        print(f"\nPIPELINE FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Multi-Agent Content Generation Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # From text
  python src/cli.py --text "Write a blog about AI agents" --title "AI Agents Guide"
  
  # From file
  python src/cli.py --file prd.txt --title "My Blog Post"
  
  # Save output
  python src/cli.py --file prd.txt --output blog.md
  
  # Interactive mode
  python src/cli.py --interactive
        """
    )
    
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--text', type=str, help='PRD text directly')
    input_group.add_argument('--file', type=str, help='Path to PRD file')
    input_group.add_argument('--interactive', action='store_true', help='Interactive mode')
    
    parser.add_argument('--title', type=str, help='Blog post title')
    parser.add_argument('--output', type=str, help='Output file path (default: print to console)')
    
    args = parser.parse_args()
    
    # Get PRD text
    if args.interactive:
        print("Interactive Mode - Enter your PRD (press Ctrl+D or Ctrl+Z when done):\n")
        prd_text = sys.stdin.read().strip()
        if not prd_text:
            print("No input provided")
            sys.exit(1)
        title = input("\nBlog post title (optional): ").strip() or None
        output_file = input("Output file (optional, press Enter to print): ").strip() or None
    elif args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"File not found: {args.file}")
            sys.exit(1)
        prd_text = file_path.read_text(encoding='utf-8')
        title = args.title
        output_file = args.output
    else:
        prd_text = args.text
        title = args.title
        output_file = args.output
    
    # Validate PRD
    if len(prd_text) < 50:
        print("Error: PRD text too short (minimum 50 characters)")
        sys.exit(1)
    
    # Run pipeline
    run_pipeline(prd_text, title, output_file)

if __name__ == "__main__":
    main()
