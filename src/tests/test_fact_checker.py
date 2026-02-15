"""Test script for the Fact-Checker Agent (full pipeline test)."""

import sys
from pathlib import Path
# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.lib.agents.researcher import run_researcher
from src.lib.agents.writer import run_writer
from src.lib.agents.fact_checker import run_fact_checker
from src.lib.logger import generate_run_id
from src.tests.sample_prd import sample_prd


def test_fact_checker():
    """Test the Fact-Checker Agent with full pipeline."""
    
    print("\n")
    print("")
    print("")
    print("      🔍 Fact-Checker Agent Test (Python)          ")
    print("")
    print("")
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

        print("-" * 60)
        print("\n✍️  Step 2: Running writer...\n")
        
        draft = run_writer(sample_prd, research, run_id)
        
        if not draft.success:
            print("❌ Writing failed!")
            sys.exit(1)
        
        print(f"\n✅ Draft complete: {draft.word_count} words, {len(draft.citations)} citations\n")
        
       
        print("-" * 60)
        print("\n🔍 Step 3: Running fact-checker...\n")
        
        import time
        start_time = time.time()
        
        fact_check = run_fact_checker(draft, research, run_id)
        
        duration = time.time() - start_time
        
        # Display results
        print("\n")
     
        print("📋 Fact-Checker Output")
     
        print("\n")
        
        print(f" Success: {fact_check.success}")
        print(f"Duration: {duration:.1f}s")
        print(f" Passed: {fact_check.passed}")
        print(f"Issues found: {len(fact_check.issues)}")
        print(f"Summary: {fact_check.content}")
        print("\n")
        
        if fact_check.issues:
            print("🚨 Issues detected:")
            print("-" * 60)
            for i, issue in enumerate(fact_check.issues, 1):
                severity_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(issue.severity, '⚪')
                print(f"\n{i}. {severity_icon} [{issue.severity.upper()}]")
                print(f"   Claim: \"{issue.claim[:80]}...\"" if len(issue.claim) > 80 else f"   Claim: \"{issue.claim}\"")
                print(f"   Reason: {issue.reason}")
            print("\n")
            
            if fact_check.feedback:
                print("📋 Feedback for revision:")
                print("-" * 60)
                print(fact_check.feedback[:500] + "..." if len(fact_check.feedback) > 500 else fact_check.feedback)
                print("\n")
        else:
            print("✅ No issues found - draft is factually accurate!")
            print("\n")
        
        # ═══════════════════════════════════════════════════════════
        # Step 4: Test revision loop (if fact-check failed)
        # ═══════════════════════════════════════════════════════════
        if not fact_check.passed and fact_check.feedback:
            print("-" * 60)
            print("\n🔄 Step 4: Testing revision loop...\n")
            
            # Run writer with feedback
            revised_draft = run_writer(
                sample_prd, 
                research, 
                run_id, 
                feedback=fact_check.feedback,
                retry_count=1
            )
            
            print(f"\n✅ Revised draft: {revised_draft.word_count} words\n")
            
            # Re-run fact-checker
            print("🔍 Re-checking revised draft...\n")
            revised_check = run_fact_checker(revised_draft, research, run_id, retry_count=1)
            
            print(f"\n📊 Revised check - Passed: {revised_check.passed}, Issues: {len(revised_check.issues)}")
            print("\n")
        
        # Final status
        print("╔═══════════════════════════════════════════════════════════╗")
        if fact_check.passed:
            print("║  ✅ Test Passed - Fact-check completed successfully!      ║")
        else:
            print("║  ⚠️  Test Completed - Issues detected (expected behavior) ║")
        print("╚═══════════════════════════════════════════════════════════╝")
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
    test_fact_checker()
