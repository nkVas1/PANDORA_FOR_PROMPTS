"""
File management service for saving prompts and project files
"""
from pathlib import Path
from typing import Optional
import json
from datetime import datetime
import sys
import os


class FileService:
    """Service for managing file storage of prompts and projects"""
    
    @staticmethod
    def get_data_dir() -> Path:
        """
        Get the data directory path (next to executable)
        
        Returns:
            Path to data directory
        """
        # If running as PyInstaller exe
        if getattr(sys, 'frozen', False):
            base_dir = Path(sys.executable).parent
        else:
            # Running as script
            base_dir = Path(__file__).parent.parent.parent.parent
        
        data_dir = base_dir / "data"
        data_dir.mkdir(exist_ok=True)
        
        return data_dir
    
    @staticmethod
    def get_prompts_dir() -> Path:
        """Get or create prompts directory"""
        prompts_dir = FileService.get_data_dir() / "prompts"
        prompts_dir.mkdir(exist_ok=True)
        return prompts_dir
    
    @staticmethod
    def get_projects_dir() -> Path:
        """Get or create projects directory"""
        projects_dir = FileService.get_data_dir() / "projects"
        projects_dir.mkdir(exist_ok=True)
        return projects_dir
    
    @staticmethod
    def save_prompt_as_txt(prompt_id: int, title: str, content: str, 
                           category: str = "general", tags: list = None) -> str:
        """
        Save prompt as TXT file
        
        Args:
            prompt_id: Prompt ID
            title: Prompt title
            content: Prompt content
            category: Prompt category
            tags: List of tags
        
        Returns:
            Path to saved file
        """
        prompts_dir = FileService.get_prompts_dir()
        
        # Create category subdirectory
        category_dir = prompts_dir / category
        category_dir.mkdir(exist_ok=True)
        
        # Create safe filename from title
        safe_filename = "".join(c for c in title if c.isalnum() or c in ' -_').rstrip()
        safe_filename = safe_filename.replace(' ', '_')[:50]  # Limit length
        
        file_path = category_dir / f"{prompt_id}_{safe_filename}.txt"
        
        # Create file content with metadata
        file_content = f"""╔════════════════════════════════════════════════════════╗
║           PANDORA PROMPT EXPORT - v1.0               ║
╚════════════════════════════════════════════════════════╝

📋 TITLE:
{title}

🏷️  CATEGORY:
{category}

🔖 TAGS:
{', '.join(tags) if tags else 'No tags assigned'}

📅 SAVED:
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*56}
📝 CONTENT:
{'='*56}

{content}

{'='*56}
"""
        
        file_path.write_text(file_content, encoding='utf-8')
        return str(file_path)
    
    @staticmethod
    def save_prompt_json(prompt_id: int, title: str, content: str, 
                        category: str = "general", tags: list = None,
                        version: str = "1.0", description: str = "") -> str:
        """
        Save prompt as JSON file
        
        Args:
            prompt_id: Prompt ID
            title: Prompt title
            content: Prompt content
            category: Prompt category
            tags: List of tags
            version: Prompt version
            description: Prompt description
        
        Returns:
            Path to saved file
        """
        prompts_dir = FileService.get_prompts_dir()
        
        safe_filename = "".join(c for c in title if c.isalnum() or c in ' -_').rstrip()
        safe_filename = safe_filename.replace(' ', '_')[:50]
        
        file_path = prompts_dir / f"{prompt_id}_{safe_filename}.json"
        
        data = {
            "id": prompt_id,
            "title": title,
            "content": content,
            "category": category,
            "tags": tags or [],
            "version": version,
            "description": description,
            "saved_at": datetime.now().isoformat(),
            "export_version": "1.0"
        }
        
        file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        return str(file_path)
    
    @staticmethod
    def create_project_structure(project_id: int, project_name: str) -> dict:
        """
        Create directory structure for a project
        
        Args:
            project_id: Project ID
            project_name: Project name
        
        Returns:
            Dictionary with paths to project subdirectories
        """
        projects_dir = FileService.get_projects_dir()
        
        # Create safe project folder name
        safe_name = "".join(c for c in project_name if c.isalnum() or c in ' -_').rstrip()
        safe_name = safe_name.replace(' ', '_')[:40]
        
        project_dir = projects_dir / f"{project_id}_{safe_name}"
        project_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        tasks_dir = project_dir / "tasks"
        process_dir = project_dir / "process"
        files_dir = project_dir / "files"
        
        tasks_dir.mkdir(exist_ok=True)
        process_dir.mkdir(exist_ok=True)
        files_dir.mkdir(exist_ok=True)
        
        # Create initial files
        (tasks_dir / "tasks.txt").write_text("# Project Tasks\n\n", encoding='utf-8')
        (process_dir / "process.txt").write_text("# Project Process\n\n", encoding='utf-8')
        (project_dir / "README.txt").write_text(
            f"Project: {project_name}\nID: {project_id}\nCreated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            encoding='utf-8'
        )
        
        return {
            "project_dir": str(project_dir),
            "tasks_dir": str(tasks_dir),
            "process_dir": str(process_dir),
            "files_dir": str(files_dir)
        }
    
    @staticmethod
    def update_project_file(project_id: int, project_name: str, 
                          file_type: str, content: str) -> str:
        """
        Update project file (tasks.txt or process.txt)
        
        Args:
            project_id: Project ID
            project_name: Project name
            file_type: Type of file ('tasks' or 'process')
            content: File content
        
        Returns:
            Path to updated file
        """
        projects_dir = FileService.get_projects_dir()
        
        safe_name = "".join(c for c in project_name if c.isalnum() or c in ' -_').rstrip()
        safe_name = safe_name.replace(' ', '_')[:40]
        
        project_dir = projects_dir / f"{project_id}_{safe_name}"
        project_dir.mkdir(exist_ok=True)
        
        if file_type == 'tasks':
            file_path = project_dir / "tasks" / "tasks.txt"
        elif file_type == 'process':
            file_path = project_dir / "process" / "process.txt"
        else:
            raise ValueError(f"Unknown file type: {file_type}")
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding='utf-8')
        
        return str(file_path)
    
    @staticmethod
    def read_project_file(project_id: int, project_name: str, file_type: str) -> Optional[str]:
        """
        Read project file content
        
        Args:
            project_id: Project ID
            project_name: Project name
            file_type: Type of file ('tasks' or 'process')
        
        Returns:
            File content or None if not found
        """
        projects_dir = FileService.get_projects_dir()
        
        safe_name = "".join(c for c in project_name if c.isalnum() or c in ' -_').rstrip()
        safe_name = safe_name.replace(' ', '_')[:40]
        
        if file_type == 'tasks':
            file_path = projects_dir / f"{project_id}_{safe_name}" / "tasks" / "tasks.txt"
        elif file_type == 'process':
            file_path = projects_dir / f"{project_id}_{safe_name}" / "process" / "process.txt"
        else:
            return None
        
        if file_path.exists():
            return file_path.read_text(encoding='utf-8')
        
        return None
    
    @staticmethod
    def list_prompts() -> list:
        """List all saved prompts"""
        prompts_dir = FileService.get_prompts_dir()
        prompts = []
        
        for file in prompts_dir.rglob("*.txt"):
            prompts.append({
                "path": str(file),
                "name": file.name,
                "category": file.parent.name
            })
        
        return prompts
    
    @staticmethod
    def list_projects() -> list:
        """List all project directories"""
        projects_dir = FileService.get_projects_dir()
        projects = []
        
        if projects_dir.exists():
            for folder in projects_dir.iterdir():
                if folder.is_dir():
                    projects.append({
                        "path": str(folder),
                        "name": folder.name
                    })
        
        return projects
