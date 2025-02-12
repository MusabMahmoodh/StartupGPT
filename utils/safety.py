from langchain.tools import BaseTool
from typing import Optional, Literal
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain_experimental.utilities import PythonREPL
from pydantic import Field

class SandboxedPythonREPLTool(BaseTool):
    name: Literal["code_executor"] = "code_executor" 
    description: str = "Execute Python code safely"
    repl: PythonREPL = Field(default_factory=PythonREPL) 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repl = PythonREPL()
    
    def _run(
        self, 
        code: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Execute the Python code with safety checks."""
        forbidden = ["os.system", "subprocess", "rm -rf", "shutil"]
        if any(cmd in code for cmd in forbidden):
            return "Error: Dangerous command blocked!"
        print("code detected", code)
        return self.repl.run(code)
    
    async def _arun(
        self,
        code: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Async implementation of the Python code executor."""
        return self._run(code, run_manager)
