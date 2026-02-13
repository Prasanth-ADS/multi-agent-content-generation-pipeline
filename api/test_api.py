import requests
import time
import os
from pathlib import Path

BASE_URL = "http://localhost:8000"
# Get API key from env or use default
API_KEY = "demo-api-key-123"

def test_api():
    """Test API endpoints"""
    
    print("Testing ContentForge AI API\n")
    
    try:
        # Test 1: Health check
        print("1. Health Check...")
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
        
        if response.status_code != 200:
            print("HTTP Status Code was not 200, is the server running?")
            return

        # Test 2: Generate content
        print("2. Generate Content...")
        payload = {
            "prd_text": """
# Blog Post: AI Agents for Developers

Write an 800-word blog post about AI agents.
Cover what they are, how they work, and practical use cases.
This text needs to be at least 50 characters long to pass validation.
            """.strip(),
            "title": "Introduction to AI Agents",
            "format": "html"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/generate",
            json=payload,
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        
        if response.status_code != 200:
            print(f"   Failed to generate content: {response.text}")
            return
            
        result = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Job ID: {result['job_id']}")
        print(f"   Status: {result['status']}\n")
        
        job_id = result['job_id']
        
        # Test 3: Check status
        print("3. Check Status...")
        for i in range(30): # Wait up to 90 seconds
            time.sleep(3)
            
            response = requests.get(
                f"{BASE_URL}/api/status/{job_id}",
                headers={"Authorization": f"Bearer {API_KEY}"}
            )
            
            status_data = response.json()
            print(f"   Progress: {status_data['progress']}% - {status_data.get('current_step', 'Unknown')}")
            
            if status_data['status'] == 'completed':
                print(f"\n   ✓ Completed!")
                print(f"   Download URL: {status_data['result']['download_url']}")
                break
            elif status_data['status'] == 'failed':
                print(f"\n   ✗ Failed: {status_data.get('error', 'Unknown error')}")
                break
        
        # Test 4: Download
        if status_data['status'] == 'completed':
            print("\n4. Download Result...")
            download_url = status_data['result']['download_url']
            response = requests.get(
                f"{BASE_URL}{download_url}",
                headers={"Authorization": f"Bearer {API_KEY}"}
            )
            
            output_file = Path("test_output.html")
            output_file.write_bytes(response.content)
            
            print(f"   ✓ Downloaded to {output_file.absolute()}")
            print(f"   Size: {output_file.stat().st_size} bytes")

    except requests.exceptions.ConnectionError:
        print("\nERROR: Could not connect to the API. Make sure the server is running!")
        print("Run: python run_api.py")

if __name__ == "__main__":
    test_api()
