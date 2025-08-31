from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class QueryRequest(BaseModel):
    """Request model for asking questions about Kenyan leaders"""
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "question": "Who is the governor of Meru County?"
                },
                {
                    "question": "List all senators from Central Kenya"
                },
                {
                    "question": "What are the 47 counties in Kenya?"
                },
                {
                    "question": "Who is the current Deputy President of Kenya?"
                }
            ]
        }
    )
    
    question: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Your question about Kenyan political leaders, government positions, or administrative structure",
        examples=[
            "Who is the governor of Meru County?",
            "List all MCAs of Nairobi County",
            "What are the 47 counties in Kenya?"
        ]
    )

class QueryResponse(BaseModel):
    """Response model containing the AI-generated answer"""
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "question": "Who is the governor of Meru County?",
                    "answer": "The current Governor of Meru County is **Kawira Mwangaza**.",
                    "timestamp": "2025-08-31T13:16:36.227707",
                    "ai_model_used": "gemini-2.0-flash",
                    "response_time_ms": 1205
                }
            ]
        }
    )
    
    question: str = Field(
        description="The original question that was asked"
    )
    answer: str = Field(
        description="AI-generated response with information about Kenyan leaders"
    )
    timestamp: datetime = Field(
        description="When the response was generated (UTC)"
    )
    ai_model_used: str = Field(
        default="gemini-2.0-flash",
        description="The AI model used to generate the response"
    )
    response_time_ms: Optional[int] = Field(
        default=None,
        description="Response time in milliseconds"
    )

class ExampleQuery(BaseModel):
    """Example query for the examples endpoint"""
    query: str = Field(description="Example question")
    category: str = Field(description="Category of the question")

class ExamplesResponse(BaseModel):
    """Response containing example queries users can ask"""
    
    examples: List[str] = Field(
        description="List of example questions about Kenyan leaders"
    )
    total: int = Field(
        description="Total number of example queries"
    )
    usage_tip: str = Field(
        description="Tip on how to use the API effectively"
    )

class HealthResponse(BaseModel):
    """Health check response model"""
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "status": "healthy",
                    "model": "gemini-2.0-flash",
                    "timestamp": "2025-08-31T13:16:16.217390",
                    "uptime_seconds": 3600,
                    "version": "1.0.0"
                }
            ]
        }
    )
    
    status: str = Field(
        description="API health status",
        examples=["healthy", "unhealthy"]
    )
    model: str = Field(
        description="AI model being used"
    )
    timestamp: datetime = Field(
        description="Current server timestamp (UTC)"
    )
    uptime_seconds: Optional[int] = Field(
        default=None,
        description="Server uptime in seconds"
    )
    version: str = Field(
        default="1.0.0",
        description="API version"
    )

class ErrorResponse(BaseModel):
    """Error response model"""
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "error": "Invalid input",
                    "detail": "Question must be between 1 and 500 characters",
                    "timestamp": "2025-08-31T13:16:16.217390",
                    "error_code": "VALIDATION_ERROR"
                }
            ]
        }
    )
    
    error: str = Field(
        description="Error message summary"
    )
    detail: Optional[str] = Field(
        default=None,
        description="Detailed error description"
    )
    timestamp: datetime = Field(
        description="When the error occurred (UTC)"
    )
    error_code: Optional[str] = Field(
        default=None,
        description="Machine-readable error code"
    )

class HistoryItem(BaseModel):
    """Individual query history item"""
    
    id: str = Field(description="Unique identifier for the query")
    question: str = Field(description="The question that was asked")
    answer: str = Field(description="The AI-generated response")
    timestamp: datetime = Field(description="When the query was made (UTC)")
    ai_model_used: str = Field(description="AI model used for the response")
    response_time_ms: Optional[int] = Field(description="Response time in milliseconds")

class HistoryResponse(BaseModel):
    """Response containing query history"""
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "history": [
                        {
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "question": "Who is the governor of Meru County?",
                            "answer": "The current Governor of Meru County is **Kawira Mwangaza**.",
                            "timestamp": "2025-08-31T13:16:36.227707",
                            "ai_model_used": "gemini-2.0-flash",
                            "response_time_ms": 1205
                        }
                    ],
                    "total": 1,
                    "page": 1,
                    "per_page": 10
                }
            ]
        }
    )
    
    history: List[HistoryItem] = Field(description="List of previous queries")
    total: int = Field(description="Total number of queries in history")
    page: int = Field(default=1, description="Current page number")
    per_page: int = Field(default=10, description="Number of items per page")

class HistoryClearResponse(BaseModel):
    """Response after clearing history"""
    
    message: str = Field(description="Success message")
    cleared_count: int = Field(description="Number of queries cleared")
    timestamp: datetime = Field(description="When the history was cleared")