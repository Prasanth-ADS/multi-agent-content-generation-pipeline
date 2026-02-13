import sys
from pathlib import Path
from datetime import datetime
import traceback
import asyncio

# Add src to path to allow imports
# This is needed because api/tasks.py is running as part of the api package
# but needs access to src.lib which is a sibling of api/
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.lib.agents.researcher import run_researcher
from src.lib.agents.writer import run_writer
from src.lib.agents.fact_checker import run_fact_checker
from src.lib.agents.style_polisher import run_style_polisher
from src.lib.formatters import convert_to_format
from src.lib.types import PRDInput
from src.lib.logger import generate_run_id, save_pipeline_result

def process_pipeline_job(
    job_id: str,
    prd_text: str,
    title: str,
    output_format: str,
    jobs_dict: dict
):
    """
    Process content generation pipeline as background task
    """
    
    try:
        # Update status to processing
        jobs_dict[job_id]["status"] = "processing"
        jobs_dict[job_id]["progress"] = 0
        
        # Create PRD
        prd = PRDInput(text=prd_text, title=title)
        run_id = generate_run_id()
        
        # Step 1: Researcher (25%)
        jobs_dict[job_id]["current_step"] = "Researcher"
        jobs_dict[job_id]["progress"] = 5
        
        # Note: These are synchronous functions, so they block the thread
        # In a real production app with Celery, these would be separate tasks
        # For FastAPI background tasks, we can run them directly but better to offload
        # Since they are CPU bound, running in executor would be better, but keeping simple for now
        
        research = run_researcher(prd, run_id)
        
        jobs_dict[job_id]["progress"] = 25
        
        # Step 2: Writer (50%)
        jobs_dict[job_id]["current_step"] = "Writer"
        jobs_dict[job_id]["progress"] = 30
        
        draft = run_writer(prd, research, run_id)
        
        jobs_dict[job_id]["progress"] = 50
        
        # Step 3: Fact-Checker (75%)
        jobs_dict[job_id]["current_step"] = "Fact-Checker"
        jobs_dict[job_id]["progress"] = 55
        
        fact_check = run_fact_checker(draft, research, run_id)
        
        # Retry if needed
        if not fact_check.passed:
            for attempt in range(2):
                jobs_dict[job_id]["message"] = f"Fact check failed, retrying ({attempt+1}/2)..."
                
                draft = run_writer(prd, research, run_id, 
                                 feedback=fact_check.feedback, 
                                 retry_count=attempt + 1)
                fact_check = run_fact_checker(draft, research, run_id, 
                                            retry_count=attempt + 1)
                if fact_check.passed:
                    break
        
        jobs_dict[job_id]["progress"] = 75
        jobs_dict[job_id]["message"] = "Polishing content..."
        
        # Step 4: Style-Polisher (90%)
        jobs_dict[job_id]["current_step"] = "Style-Polisher"
        jobs_dict[job_id]["progress"] = 80
        
        final = run_style_polisher(draft, prd, run_id)
        
        jobs_dict[job_id]["progress"] = 90
        
        # Step 5: Format conversion (100%)
        jobs_dict[job_id]["current_step"] = "Formatting"
        jobs_dict[job_id]["progress"] = 95
        jobs_dict[job_id]["message"] = "Generating output file..."
        
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        
        # For file download, we use the job_id as filename
        output_file = output_dir / f"{job_id}.{output_format}"
        
        convert_to_format(
            final.polished,
            output_format,
            str(output_file),
            title or "Generated Content"
        )
        
        # Complete
        jobs_dict[job_id]["status"] = "completed"
        jobs_dict[job_id]["progress"] = 100
        jobs_dict[job_id]["current_step"] = "Complete"
        jobs_dict[job_id]["message"] = "Generation complete"
        jobs_dict[job_id]["completed_at"] = datetime.utcnow()
        jobs_dict[job_id]["result"] = {
            "run_id": run_id,
            "file_path": str(output_file),
            "download_url": f"/api/download/{job_id}",
            "format": output_format,
            "word_count": len(final.polished.split()),
            "fact_check_passed": fact_check.passed
        }
        
        # Save to logs
        result = {
            "run_id": run_id,
            "job_id": job_id,
            "prd_title": title,
            "final_content": final.polished,
            "format": output_format,
            "status": "success"
        }
        save_pipeline_result(result)
        
    except Exception as e:
        # Handle errors
        jobs_dict[job_id]["status"] = "failed"
        jobs_dict[job_id]["error"] = str(e)
        jobs_dict[job_id]["message"] = "Generation failed"
        jobs_dict[job_id]["completed_at"] = datetime.utcnow()
        
        print(f"Job {job_id} failed: {str(e)}")
        traceback.print_exc()
