#!/usr/bin/env python3
"""
ZoomToApp - AI-Driven SDLC Automation Tool
Converts Zoom meeting recordings into deployed web applications
"""

import os
import sys
import json
import time
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Optional
import click
from dotenv import load_dotenv

from src.transcriber import AudioTranscriber
from src.story_generator import StoryGenerator
from src.code_generator import CodeGenerator
from src.test_runner import TestRunner
from src.deployer import AppDeployer
from src.report_generator import ReportGenerator
from src.utils import setup_logging, log_step

# Load environment variables
load_dotenv()

class ZoomToAppPipeline:
    """Main pipeline orchestrator for ZoomToApp"""
    
    def __init__(self, output_dir: str = "./output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.start_time = time.time()
        
        # Initialize components
        self.transcriber = AudioTranscriber()
        self.story_generator = StoryGenerator()
        self.code_generator = CodeGenerator()
        self.test_runner = TestRunner()
        self.deployer = AppDeployer()
        self.report_generator = ReportGenerator()
        
        # Pipeline state
        self.state = {
            'transcript': '',
            'user_stories': [],
            'architecture': '',
            'generated_code': {},
            'test_results': {},
            'deployment_urls': {},
            'metrics': {}
        }
    
    def run(self, audio_file: str, project_name: str = "todo-app") -> Dict:
        """Run the complete ZoomToApp pipeline"""
        log_step("🚀 Starting ZoomToApp Pipeline")
        
        try:
            # Step 1: Transcription
            log_step("🎵 Step 1: Transcribing audio")
            self.state['transcript'] = self.transcriber.transcribe(audio_file)
            
            # Step 2: Story Generation
            log_step("📝 Step 2: Generating user stories")
            stories_result = self.story_generator.generate_stories(self.state['transcript'])
            self.state['user_stories'] = stories_result['stories']
            self.state['architecture'] = stories_result['architecture']
            
            # Step 3: Code Generation
            log_step("💻 Step 3: Generating application code")
            self.state['generated_code'] = self.code_generator.generate_app(
                self.state['user_stories'], 
                project_name,
                str(self.output_dir)
            )
            
            # Step 4: Testing
            log_step("🧪 Step 4: Running automated tests")
            self.state['test_results'] = self.test_runner.run_tests(
                str(self.output_dir / project_name)
            )
            
            # Step 5: Deployment
            log_step("🚀 Step 5: Deploying application")
            self.state['deployment_urls'] = self.deployer.deploy_app(
                str(self.output_dir / project_name),
                project_name
            )
            
            # Step 6: Generate Report
            log_step("📊 Step 6: Generating final report")
            execution_time = time.time() - self.start_time
            self.state['metrics']['execution_time'] = execution_time
            
            report_path = self.report_generator.generate_report(
                self.state,
                str(self.output_dir / "report.md")
            )
            
            log_step(f"✅ Pipeline completed successfully in {execution_time:.2f} seconds!")
            log_step(f"📋 Report generated: {report_path}")
            
            if self.state['deployment_urls'].get('frontend'):
                log_step(f"🌐 Frontend URL: {self.state['deployment_urls']['frontend']}")
            if self.state['deployment_urls'].get('backend'):
                log_step(f"⚙️  Backend URL: {self.state['deployment_urls']['backend']}")
            
            return self.state
            
        except Exception as e:
            log_step(f"❌ Pipeline failed: {str(e)}")
            raise

@click.command()
@click.option('--file', '-f', required=True, help='Path to Zoom recording file (MP3/MP4)')
@click.option('--project-name', '-p', default='todo-app', help='Name for the generated project')
@click.option('--output-dir', '-o', default='./output', help='Output directory for generated files')
def main(file: str, project_name: str, output_dir: str):
    """ZoomToApp - Convert Zoom recordings to deployed web applications"""
    
    # Validate inputs
    if not os.path.exists(file):
        click.echo(f"❌ Error: File '{file}' not found")
        sys.exit(1)
    
    if not os.getenv('OPENAI_API_KEY'):
        click.echo("❌ Error: OPENAI_API_KEY environment variable not set")
        click.echo("Please copy .env.example to .env and add your OpenAI API key")
        sys.exit(1)
    
    # Setup logging
    setup_logging()
    
    # Run pipeline
    pipeline = ZoomToAppPipeline(output_dir)
    
    try:
        result = pipeline.run(file, project_name)
        click.echo("\n🎉 ZoomToApp completed successfully!")
        click.echo(f"📁 Check the '{output_dir}' directory for all generated files")
        
    except Exception as e:
        click.echo(f"\n❌ ZoomToApp failed: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()