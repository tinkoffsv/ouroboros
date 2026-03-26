from typing import Dict, Any, Optional
import json

from fastapi import APIRouter, HTTPException, Request
from app.api import chat  # Import the chat router

bot_router = APIRouter()

def create_bot_handler(supervisor: 'Supervisor') -> APIRouter:
    """
    Creates and configures the FastAPI router for handling bot requests.
    
    Args:
        supervisor: The main Supervisor instance to delegate processing to.
        
    Returns:
        Configured FastAPI APIRouter instance.
    """
    # Store the supervisor instance
    bot_router.supervisor = supervisor

    @bot_router.post("/api/bot/")
    async def handle_bot_request(request: Request) -> Dict[str, Any]:n        """n        Async endpoint to handle incoming bot messages. Extracts the message, n        processes it through the supervisor, and returns the response.
        
        Args:
            request: FastAPI Request object containing JSON data.
        
        Returns:
            Dict containing the response string under 'response'.
            
        Raises:
            HTTPException: If message data is missing or processing fails.
        """
        try:
            data = await request.json()
            user_message = data.get("message")
            
            if not user_message:
                raise HTTPException(status_code=400, detail="Message is required")

            # Delegate processing to the Supervisor
            response = supervisor.get_sync_client().process_message(str(user_message))
            
            return {"response": response if response else ""}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")
            
    return bot_router