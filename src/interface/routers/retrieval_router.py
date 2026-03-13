from fastapi import APIRouter
from fastapi.responses import JSONResponse

from interface.dtos.external.request.retrieval_request import RetrievalRequest
from interface.dtos.external.response.retrieval_response import RetrievalResponse

from interface.validators.validators import validate_retrival_request

from services.retrieval_service import RetrievalService

from utils.logger import logger, log_context

retrieval_router = APIRouter()


@retrieval_router.post("/retrieve")
async def retrieve(request: RetrievalRequest):
    try:
        validate_retrival_request(request)
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content=str(e)
        )
    
    # I want to call functions in RetrievalService here
