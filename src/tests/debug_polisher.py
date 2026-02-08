import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path.cwd()))

from src.lib.agents.style_polisher import run_style_polisher
from src.lib.types import WriterOutput, PRDInput

def test_isolated_polisher():
    draft = WriterOutput(
        content="This is a test draft. It has some facts. Citation [1].",
        draft="This is a test draft. It has some facts. Citation [1].",
        word_count=10,
        citations=["1"],
        metadata={"agent": "writer", "success": True},
        success=True
    )
    prd = PRDInput(
        text="Target Audience: Developers. Desired Tone: Professional.",
        title="Test PRD",
        metadata={"target_audience": "Developers", "desired_tone": "Professional"}
    )
    run_id = "debug_run"
    
    print("Running isolated Style-Polisher test...")
    try:
        result = run_style_polisher(draft, prd, run_id)
        
        with open("debug_result.txt", "w") as f:
            f.write(f"Success: {result.success}\n")
            f.write(f"Error: {result.error}\n")
            f.write(f"Polished: {result.polished[:100]}...\n")
        
        print(f"Success: {result.success}")
        print(f"Error: {result.error}")
    except Exception as e:
        with open("debug_result.txt", "w") as f:
            f.write(f"CRASH: {str(e)}\n")
        print(f"CRASH: {e}")

if __name__ == "__main__":
    test_isolated_polisher()
