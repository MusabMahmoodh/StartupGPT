from langchain.tools import BaseTool
from typing import Optional, Literal
from langchain.callbacks.manager import CallbackManagerForToolRun
from github import Github
import os
from dotenv import load_dotenv
from pydantic import Field

load_dotenv()

class GitHubCreateRepoTool(BaseTool):
    name: Literal["create_repo"] = "create_repo" 
    description: str = "Create GitHub repositories"
    token: str = Field(default=os.getenv("GITHUB_TOKEN")) 
    client: Github = Field(default=None)  

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.token = os.getenv("GITHUB_TOKEN")  
        if not self.token:
            raise ValueError("GitHub token is missing. Set GITHUB_TOKEN in your .env file.")
        self.client = Github(self.token)
    
    def _run(
        self,
        name: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Create a GitHub repository."""
        try:
            repo = self.client.get_user().create_repo(name, auto_init=True)
            return f"Repo created: {repo.html_url}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def _arun(
        self,
        name: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Async implementation of GitHub repo creation."""
        return self._run(name, run_manager)
