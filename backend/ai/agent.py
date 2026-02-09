import os
import json
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from sqlmodel import Session, select
from openai import OpenAI
from db import engine
from models import Conversation, Message, Task
from mcp.server.fastmcp import FastMCP

# Import tools directly to execute them
# In a real distributed MCP setup, we would use an MCP Client to call them over network.
# But here we are in the same process, so we can wrap them or call them.
# However, to strictly follow "MCP Server" architecture, we should probably treat them as tools.
# For simplicity in this "Monolith" Phase III, we will just use the function definitions.
from mcp.server import add_task, list_tasks, complete_task, delete_task, update_task # Wait, imports might be tricky if not exported
# Actually, let's just import the mcp object and access tools if possible, or import functions.
from backend.mcp.server import add_task, list_tasks, complete_task, delete_task, update_task

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Define Tool Schemas for OpenAI
# Normally MCP SDK can generate these, but let's hardcode for the "Basic Level" to be sure.
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["user_id", "title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List tasks for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "status": {"type": "string", "enum": ["all", "pending", "completed"]}
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "task_id": {"type": "integer"}
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "task_id": {"type": "integer"}
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update a task",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "task_id": {"type": "integer"},
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["user_id", "task_id"]
            }
        }
    }
]

def get_session():
    return Session(engine)

def run_agent(user_id: str, message: str, conversation_id: Optional[int] = None):
    with get_session() as session:
        # 1. Get or Create Conversation
        if conversation_id:
            conversation = session.get(Conversation, conversation_id)
            if not conversation or conversation.user_id != user_id:
                 # Create new if not found (stateless resilience)
                 conversation = Conversation(user_id=user_id)
                 session.add(conversation)
                 session.commit()
                 session.refresh(conversation)
        else:
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)
            
        # 2. Store User Message
        user_msg = Message(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content=message
        )
        session.add(user_msg)
        session.commit()
        
        # 3. Build Context (History)
        # Fetch last N messages to keep context window manageable
        # For this hackathon, let's fetch all (or last 20)
        history_stmt = select(Message).where(Message.conversation_id == conversation.id).order_by(Message.created_at)
        history_msgs = session.exec(history_stmt).all()
        
        messages = [{"role": "system", "content": "You are a helpful Todo Assistant. You manage tasks for the user using the available tools. Always check the current date/time if needed. Today is " + datetime.now().isoformat()}]
        for m in history_msgs:
            messages.append({"role": m.role, "content": m.content})
            
        # 4. Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4o", # Or gpt-3.5-turbo
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )
        
        assistant_message = response.choices[0].message
        
        # 5. Handle Tool Calls
        if assistant_message.tool_calls:
            # Append assistant message with tool calls to history (virtual, for the next turn)
            messages.append(assistant_message)
            
            for tool_call in assistant_message.tool_calls:
                function_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                
                # Execute Tool
                result_content = ""
                if function_name == "add_task":
                    result_content = add_task(**arguments)
                elif function_name == "list_tasks":
                    result_content = list_tasks(**arguments)
                elif function_name == "complete_task":
                    result_content = complete_task(**arguments)
                elif function_name == "delete_task":
                    result_content = delete_task(**arguments)
                elif function_name == "update_task":
                    result_content = update_task(**arguments)
                else:
                    result_content = f"Error: Tool {function_name} not found."
                
                # Append Tool Output
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": str(result_content)
                })
            
            # 6. Get Final Response after Tool Execution
            second_response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            final_content = second_response.choices[0].message.content
        else:
            final_content = assistant_message.content
            
        # 7. Store Assistant Response
        asst_msg = Message(
            conversation_id=conversation.id,
            user_id=user_id,
            role="assistant",
            content=final_content
        )
        session.add(asst_msg)
        session.commit()
        
        return {
            "conversation_id": conversation.id,
            "response": final_content,
            "tool_calls": [t.function.name for t in assistant_message.tool_calls] if assistant_message.tool_calls else []
        }
