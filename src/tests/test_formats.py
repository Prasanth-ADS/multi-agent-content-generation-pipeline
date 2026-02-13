import sys
from pathlib import Path

# Add src to python path
sys.path.append(str(Path(__file__).parent.parent))

from lib.formatters import convert_to_format

from lib.formatters import convert_to_format

def test_all_formats():
    """Test all output formats"""
    
    sample_markdown = """
# Introduction to AI Agents

AI agents are autonomous programs that can perceive their environment and take actions [1].

## Key Features

- Autonomous decision making
- Environmental perception
- Goal-oriented behavior

### Code Example
```python
def simple_agent():
    return "Hello, World!"
```

## Benefits

1. Increased efficiency
2. 24/7 availability
3. Scalability

**Bold text** and *italic text* for emphasis.
"""
    
    output_dir = Path('test_outputs')
    output_dir.mkdir(exist_ok=True)
    
    formats = ['md', 'html', 'pdf', 'docx']
    
    print("Testing Output Formats\n")
    
    for fmt in formats:
        print(f"Testing {fmt.upper()}...")
        
        output_path = output_dir / f"test_output.{fmt}"
        
        try:
            result_path = convert_to_format(
                sample_markdown,
                fmt,
                str(output_path),
                "AI Agents Guide"
            )
            
            # Check file was created
            if Path(result_path).exists():
                size = Path(result_path).stat().st_size
                print(f"  Success: {result_path} ({size} bytes)")
            else:
                print(f"  Failed: File not created")
                
        except Exception as e:
            print(f"  Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print(f"\nAll test files saved to: {output_dir.absolute()}")

if __name__ == "__main__":
    test_all_formats()
