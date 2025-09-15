"""User story generation using LLM"""

import json
from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage

from .utils import log_step

class StoryGenerator:
    """Generates user stories and architecture from meeting transcript"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3
        )
    
    def generate_stories(self, transcript: str) -> Dict:
        """
        Generate user stories and system architecture from transcript
        
        Args:
            transcript: Meeting transcript text
            
        Returns:
            Dictionary containing stories and architecture
        """
        try:
            # User stories generation prompt
            stories_prompt = ChatPromptTemplate.from_template("""
            Analyze this meeting transcript and generate user stories for a web application.
            
            Transcript: {transcript}
            
            Generate 5-7 user stories in the format:
            "As a [user type], I want [functionality] so that [benefit]"
            
            Focus on creating a todo list application with CRUD operations.
            
            Return ONLY a JSON object with this structure:
            {{
                "stories": [
                    "As a user, I want to...",
                    "As a user, I want to...",
                    ...
                ]
            }}
            """)
            
            # Architecture generation prompt  
            arch_prompt = ChatPromptTemplate.from_template("""
            Based on this transcript about a todo application, create a simple system architecture description.
            
            Transcript: {transcript}
            
            Describe a full-stack architecture with:
            - React frontend with components
            - Express.js backend with REST API
            - SQLite database
            - Deployment strategy
            
            Keep it concise and focused on a todo list app.
            """)
            
            log_step("Generating user stories...")
            stories_response = self.llm.invoke(stories_prompt.format(transcript=transcript))
            
            log_step("Generating architecture...")
            arch_response = self.llm.invoke(arch_prompt.format(transcript=transcript))
            
            # Parse stories JSON
            try:
                stories_data = json.loads(stories_response.content)
                stories = stories_data.get('stories', [])
            except json.JSONDecodeError:
                log_step("⚠️  Failed to parse stories JSON, using fallback")
                stories = self._get_fallback_stories()
            
            architecture = arch_response.content
            
            log_step(f"✅ Generated {len(stories)} user stories")
            
            return {
                'stories': stories,
                'architecture': architecture
            }
            
        except Exception as e:
            log_step(f"❌ Story generation failed: {str(e)}")
            return {
                'stories': self._get_fallback_stories(),
                'architecture': self._get_fallback_architecture()
            }
    
    def _get_fallback_stories(self) -> List[str]:
        """Fallback user stories for demo purposes"""
        return [
            "As a user, I want to create new todo tasks so that I can track what I need to do",
            "As a user, I want to view all my todo tasks so that I can see my current workload", 
            "As a user, I want to mark tasks as completed so that I can track my progress",
            "As a user, I want to delete tasks so that I can remove items I no longer need",
            "As a user, I want to edit existing tasks so that I can update task details",
            "As a user, I want a clean interface so that the app is easy to use"
        ]
    
    def _get_fallback_architecture(self) -> str:
        """Fallback architecture description"""
        return """
        ## System Architecture

        **Frontend (React)**
        - TodoApp component (main container)
        - TodoList component (displays tasks)
        - TodoItem component (individual task)
        - AddTodo component (form to add tasks)

        **Backend (Express.js)**
        - GET /api/todos - fetch all todos
        - POST /api/todos - create new todo
        - PUT /api/todos/:id - update todo
        - DELETE /api/todos/:id - delete todo

        **Database (SQLite)**
        - todos table: id, title, description, completed, created_at

        **Deployment**
        - Frontend: Vercel
        - Backend: Railway/Heroku
        """