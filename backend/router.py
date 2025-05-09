from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from langchaincore.run import run_pipeline_cli

router = APIRouter()


class AnalysisRequest(BaseModel):
    url: str
    analysis_type: str = None

@router.post('/')
async def analyze(request: AnalysisRequest) -> dict:
    github_url = request.url
    analysis_type = request.analysis_type
    
    await run_pipeline_cli(github_url=github_url, analysis_type=analysis_type)
    
    return {"status": "OK", "report_path": "report.html"}

from fastapi.responses import FileResponse
import os

@router.get("/report")
async def get_report():
    path = os.path.abspath("report.html")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"Report file at path {path} does not exist.")
    return FileResponse(path, media_type="text/html")