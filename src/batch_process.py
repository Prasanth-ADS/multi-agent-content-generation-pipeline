import json
from pathlib import Path
from cli import run_pipeline
import sys

import os

def process_batch(input_dir: str, output_dir: str):
    """Process multiple PRD files in a directory"""
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    if not input_path.exists():
        print(f"Input directory not found: {input_dir}")
        sys.exit(1)
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find all PRD files
    prd_files = list(input_path.glob('*.txt')) + list(input_path.glob('*.md'))
    
    if not prd_files:
        print(f"No PRD files found in {input_dir}")
        sys.exit(1)
    
    print(f"\nFound {len(prd_files)} PRD files to process\n")
    
    results = []
    
    for i, prd_file in enumerate(prd_files, 1):
        print(f"\n{'='*70}")
        print(f"Processing {i}/{len(prd_files)}: {prd_file.name}")
        print(f"{'='*70}\n")
        
        try:
            prd_text = prd_file.read_text(encoding='utf-8')
            title = prd_file.stem.replace('_', ' ').replace('-', ' ').title()
            output_file = output_path / f"{prd_file.stem}_output.md"
            
            result = run_pipeline(prd_text, title, str(output_file))
            results.append({
                'file': prd_file.name,
                'status': 'success',
                'output': str(output_file),
                'run_id': result['run_id']
            })
            
        except Exception as e:
            print(f"Failed to process {prd_file.name}: {str(e)}")
            results.append({
                'file': prd_file.name,
                'status': 'failed',
                'error': str(e)
            })
    
    # Save batch summary
    summary_file = output_path / 'batch_summary.json'
    summary_file.write_text(json.dumps(results, indent=2))
    summary_file.write_text(json.dumps(results, ident = 2))
    
    # Print summary
    print("\n" + "="*70)
    print("BATCH PROCESSING COMPLETE")
    print("="*70)
    
    success_count = sum(1 for r in results if r['status'] == 'success')
    print(f"Total files: {len(results)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {len(results) - success_count}")
    print(f"Summary saved to: {summary_file}")
    print("="*70 + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python src/batch_process.py <input_dir> <output_dir>")
        print("Example: python src/batch_process.py ./prds ./outputs")
        sys.exit(1)
    
    process_batch(sys.argv[1], sys.argv[2])
