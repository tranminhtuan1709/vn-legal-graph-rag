from fastapi import APIRouter, Depends
from pydantic import ValidationError
from fastapi.responses import JSONResponse

from interface.dtos.external.request.retrieval_request import RetrievalRequest
from interface.dtos.external.response.retrieval_response import RetrievalResponse
from interface.validators.validators import validate_retrival_request

from dependencies import get_retrieval_service
from services.retrieval_service import RetrievalService
from utils.logger import logger, log_context

retrieval_router = APIRouter()


@retrieval_router.post("/retrieve")
async def retrieve(
    request: RetrievalRequest,
    retrieval_service: RetrievalService = Depends(get_retrieval_service)
):    
    try:
        validate_retrival_request(request)

        request_id = request.request_id
        log_context.set(request_id)
        retrieval_response = retrieval_service.retrieve(request.query)
        
        return JSONResponse(
            status_code=200,
            content=retrieval_response
        )
    except ValidationError as e:
        return JSONResponse(
            status_code=400,
            content=str(e)
        )
    except Exception:
        logger.error(f"Retrieval failed", exc_info=True)

        return JSONResponse(
            status_code=500,
            content="Retrieval Failed"
        )
