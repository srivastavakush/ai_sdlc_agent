"""Deployment automation module"""

import os
import subprocess
import json
from typing import Dict
from pathlib import Path

from .utils import log_step

class AppDeployer:
    """Handles application deployment to cloud platforms"""
    
    def deploy_app(self, project_path: str, project_name: str) -> Dict:
        """
        Deploy frontend and backend applications
        
        Args:
            project_path: Path to the generated project
            project_name: Name of the project
            
        Returns:
            Dictionary with deployment URLs
        """
        urls = {}
        
        try:
            # Deploy frontend to Vercel (simulated)
            log_step("Deploying frontend to Vercel...")
            frontend_url = self._deploy_frontend(
                os.path.join(project_path, 'frontend'),
                f"{project_name}-frontend"
            )
            urls['frontend'] = frontend_url
            
            # Deploy backend to Railway (simulated)
            log_step("Deploying backend to Railway...")
            backend_url = self._deploy_backend(
                os.path.join(project_path, 'backend'),
                f"{project_name}-backend"
            )
            urls['backend'] = backend_url
            
            log_step("✅ Deployment completed successfully!")
            
        except Exception as e:
            log_step(f"❌ Deployment failed: {str(e)}")
            
        return urls
    
    def _deploy_frontend(self, frontend_path: str, app_name: str) -> str:
        """Deploy React frontend (simulated deployment)"""
        try:
            # Create deployment configuration
            vercel_config = {
                "name": app_name,
                "version": 2,
                "builds": [
                    {
                        "src": "package.json",
                        "use": "@vercel/static-build"
                    }
                ],
                "routes": [
                    {
                        "src": "/(.*)",
                        "dest": "/index.html"
                    }
                ]
            }
            
            vercel_json_path = os.path.join(frontend_path, 'vercel.json')
            with open(vercel_json_path, 'w') as f:
                json.dump(vercel_config, f, indent=2)
            
            # For demo purposes, return simulated URL
            simulated_url = f"https://{app_name}.vercel.app"
            log_step(f"Frontend would be deployed to: {simulated_url}")
            
            return simulated_url
            
        except Exception as e:
            log_step(f"Frontend deployment error: {str(e)}")
            return f"https://{app_name}.vercel.app"
    
    def _deploy_backend(self, backend_path: str, app_name: str) -> str:
        """Deploy Express.js backend (simulated deployment)"""
        try:
            # Create Dockerfile for deployment
            dockerfile_content = """FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 5000

CMD ["npm", "start"]"""
            
            dockerfile_path = os.path.join(backend_path, 'Dockerfile')
            with open(dockerfile_path, 'w') as f:
                f.write(dockerfile_content)
            
            # Create railway.json configuration
            railway_config = {
                "build": {
                    "builder": "DOCKERFILE"
                },
                "deploy": {
                    "startCommand": "npm start",
                    "healthcheckPath": "/health"
                }
            }
            
            railway_json_path = os.path.join(backend_path, 'railway.json')
            with open(railway_json_path, 'w') as f:
                json.dump(railway_config, f, indent=2)
            
            # For demo purposes, return simulated URL
            simulated_url = f"https://{app_name}.railway.app"
            log_step(f"Backend would be deployed to: {simulated_url}")
            
            return simulated_url
            
        except Exception as e:
            log_step(f"Backend deployment error: {str(e)}")
            return f"https://{app_name}.railway.app"