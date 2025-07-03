import datetime
from typing import Any
from azure.ai.agents.models import AsyncFunctionTool

def get_current_time() -> str:
    """
    Returns the current date and time.
    
    :return: Current date and time as a formatted string.
    """
    current_time = datetime.datetime.now()
    return current_time.strftime("%Y-%m-%d %H:%M:%S")

async def get_current_time_async() -> str:
    """
    Returns the current date and time (async version).
    
    :return: Current date and time as a formatted string.
    """
    return get_current_time()

# Define user functions for the agent (sync functions)
user_functions = {get_current_time}

# Create AsyncFunctionTool for use with AsyncToolSet
# According to Azure SDK, AsyncFunctionTool takes sync functions and can handle them asynchronously
async_function_tool = AsyncFunctionTool(functions=user_functions)
