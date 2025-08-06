import os
from app.tools.go1_tools import get_learning_objects_tool
import autogen
from dotenv import load_dotenv
from app.prompts.main_agent_prompt import MAIN_AGENT_PROMPT

# Load environment variables
load_dotenv()

# --- Autogen Configuration ---
config_list = [
    {
        "base_url": os.getenv("OPENAI_API_BASE"),
        "api_key": os.getenv("OPENAI_API_KEY"),
        "model": "o3-mini",
    }
]

llm_config = {
    "config_list": config_list,
    "cache_seed": 42,
}

# --- Main Service Function ---
def solve_task_with_agent(task: str) -> str:
    """
    Sets up and runs an AutoGen agent conversation to solve a given task.
    """
    # Define the Assistant Agent
    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config=llm_config,
        # Add a system message to encourage termination
        system_message=MAIN_AGENT_PROMPT,
    )

    # Define the User Proxy Agent
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=2, # A lower limit is better for simple Q&A
        # The UserProxyAgent will look for "TERMINATE" to end the conversation
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config=False,
    )

    autogen.register_function(
        get_learning_objects_tool,
        caller=assistant,      # The assistant suggests the function call
        executor=user_proxy,   # The user_proxy executes the function call
        name="get_learning_objects_tool",
        description="Get learning objects from Go1 API with optional keyword search.",
    )

    # The UserProxyAgent initiates the chat with the AssistantAgent
    chat_result = user_proxy.initiate_chat(
        assistant,
        message=task,
        clear_history=True
    )

    

    # Return the final summary from the chat
    return chat_result.summary
