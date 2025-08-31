import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from ..models.schemas import HistoryItem

class HistoryService:
    """Simple in-memory history service for storing query history"""
    
    def __init__(self):
        self._history: List[Dict[str, Any]] = []
    
    def add_query(self, question: str, answer: str, ai_model: str, response_time_ms: Optional[int] = None) -> str:
        """Add a new query to history and return the ID"""
        query_id = str(uuid.uuid4())
        
        history_item = {
            "id": query_id,
            "question": question,
            "answer": answer,
            "timestamp": datetime.now(),
            "ai_model_used": ai_model,
            "response_time_ms": response_time_ms
        }
        
        # Add to beginning of list (most recent first)
        self._history.insert(0, history_item)
        
        # Keep only the last 100 queries to prevent memory issues
        if len(self._history) > 100:
            self._history = self._history[:100]
        
        return query_id
    
    def get_history(self, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """Get paginated query history"""
        # Calculate pagination
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        
        # Get paginated items
        paginated_items = self._history[start_index:end_index]
        
        # Convert to HistoryItem objects
        history_items = [
            HistoryItem(**item) for item in paginated_items
        ]
        
        return {
            "history": history_items,
            "total": len(self._history),
            "page": page,
            "per_page": per_page
        }
    
    def clear_history(self) -> int:
        """Clear all history and return the number of items cleared"""
        cleared_count = len(self._history)
        self._history.clear()
        return cleared_count
    
    def get_total_count(self) -> int:
        """Get total number of queries in history"""
        return len(self._history)

# Global instance
history_service = HistoryService()