from fastapi import APIRouter, HTTPException, status, Response
from datetime import datetime
import logging
import time

from ..models.schemas import QueryRequest, QueryResponse, ErrorResponse, ExamplesResponse, HistoryResponse, HistoryClearResponse
from ..services.gemini_service import gemini_service
from ..services.history_service import history_service

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/api", 
    tags=["Kenyan Leaders Q&A"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error", "model": ErrorResponse},
        422: {"description": "Validation error", "model": ErrorResponse},
    }
)

@router.post(
    "/query", 
    response_model=QueryResponse,
    summary="Ask Question About Kenyan Leaders",
    description="Submit a question about Kenyan political leaders and receive an AI-powered response",
    responses={
        200: {"description": "Successful response with answer", "model": QueryResponse},
        422: {"description": "Validation error - invalid input format", "model": ErrorResponse},
        500: {"description": "Internal server error - AI service unavailable", "model": ErrorResponse}
    }
)
async def ask_question(request: QueryRequest):
    start_time = time.time()
    
    try:
        logger.info(f"Processing query: {request.question[:50]}...")
        
        # Validate input
        if not request.question.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Question cannot be empty"
            )
        
        # Generate response using Gemini
        answer = await gemini_service.generate_response(request.question)
        
        # Calculate response time
        response_time = int((time.time() - start_time) * 1000)
        
        # Create response
        response = QueryResponse(
            question=request.question,
            answer=answer,
            timestamp=datetime.now(),
            ai_model_used="gemini-2.0-flash",
            response_time_ms=response_time
        )
        
        # Save to history
        history_service.add_query(
            question=request.question,
            answer=answer,
            ai_model="gemini-2.0-flash",
            response_time_ms=response_time
        )
        
        logger.info(f"Query processed successfully in {response_time}ms")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI service temporarily unavailable. Please try again later."
        )

@router.get(
    "/examples",
    response_model=ExamplesResponse,
    summary="Get Example Queries", 
    description="Retrieve a list of example questions you can ask about Kenyan leaders",
    responses={
        200: {"description": "List of example queries", "model": ExamplesResponse}
    }
)
async def get_example_queries():
    examples = [
        "Who is the governor of Meru County?",
        "List all senators from Central Kenya",
        "Who is the current Deputy President of Kenya?",
        "What are the 47 counties in Kenya?",
        "Who is the speaker of the National Assembly?",
        "List MCAs of Kiambu County",
        "Who is the Cabinet Secretary for Interior?",
        "What is the role of a county commissioner?"
    ]
    
    return ExamplesResponse(
        examples=examples,
        total=len(examples),
        usage_tip="Ask specific questions about Kenyan political leaders and government positions. Be specific about counties, positions, or regions for better results."
    )

@router.get(
    "/history",
    response_model=HistoryResponse,
    summary="Get Query History",
    description="Retrieve paginated history of previous questions and answers",
    responses={
        200: {"description": "Query history retrieved successfully", "model": HistoryResponse}
    }
)
async def get_query_history(page: int = 1, per_page: int = 10):
    # Validate pagination parameters
    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 10
    if per_page > 50:  # Limit to prevent large responses
        per_page = 50
    
    try:
        history_data = history_service.get_history(page=page, per_page=per_page)
        return HistoryResponse(**history_data)
    except Exception as e:
        logger.error(f"Error retrieving history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve query history"
        )

@router.delete(
    "/history",
    response_model=HistoryClearResponse,
    summary="Clear Query History", 
    description="Clear all stored query history",
    responses={
        200: {"description": "History cleared successfully", "model": HistoryClearResponse}
    }
)
async def clear_query_history():
    try:
        cleared_count = history_service.clear_history()
        
        logger.info(f"Cleared {cleared_count} items from query history")
        
        return HistoryClearResponse(
            message=f"Successfully cleared query history",
            cleared_count=cleared_count,
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Error clearing history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear query history"
        )