#!/usr/bin/env python3
"""
ZoomToApp Demo Script
Demonstrates the complete pipeline using sample data
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from zoom_to_app import ZoomToAppPipeline
from src.utils import setup_logging, log_step

def run_demo():
    """Run ZoomToApp demo with sample data"""
    
    print("🎬 ZoomToApp Demo - AI-Driven SDLC Automation")
    print("=" * 60)
    
    # Setup
    setup_logging()
    output_dir = "./demo_output"
    
    # Check for sample file
    sample_file = "./sample_data/sample_meeting.txt"
    if not os.path.exists(sample_file):
        print(f"❌ Sample file not found: {sample_file}")
        print("Creating sample transcript...")
        
        os.makedirs("./sample_data", exist_ok=True)
        
        sample_transcript = """
        We need to build a todo list application. Users should be able to add new tasks, 
        view all their tasks, mark tasks as completed, and delete tasks they no longer need. 
        The app should have a clean, simple interface that's easy to use. We want to store 
        the tasks in a database so they persist between sessions.
        """
        
        with open(sample_file, 'w') as f:
            f.write(sample_transcript)
    
    # Run pipeline
    try:
        pipeline = ZoomToAppPipeline(output_dir)
        
        log_step("🚀 Starting ZoomToApp Demo Pipeline")
        
        # Simulate with text file (since we don't have actual audio)
        result = pipeline.run(sample_file, "demo-todo-app")
        
        print("\n" + "=" * 60)
        print("🎉 Demo completed successfully!")
        print(f"📁 Check '{output_dir}' for generated files")
        print(f"📋 Report: {output_dir}/report.md")
        
        if result['deployment_urls']:
            print(f"🌐 Frontend URL: {result['deployment_urls'].get('frontend', 'N/A')}")
            print(f"⚙️  Backend URL: {result['deployment_urls'].get('backend', 'N/A')}")
        
        print("\n💡 To run with real audio file:")
        print("   python zoom_to_app.py --file your_recording.mp3")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        return False
    
    return True

if __name__ == '__main__':
    # Set demo environment variable
    os.environ['DEMO_MODE'] = '1'
    
    success = run_demo()
    sys.exit(0 if success else 1)