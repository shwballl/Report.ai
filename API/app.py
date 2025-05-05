from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from AI.run import run_pipeline_cli

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или ["http://localhost:3000"] для большей безопасности
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    url: str
    analysis_type: str = None

@app.post('/')
async def analyze(request: AnalysisRequest) -> dict:
    github_url = request.url
    analysis_type = request.analysis_type
    
    await run_pipeline_cli(github_url=github_url, analysis_type=analysis_type)
    
    return {"status": "OK", "report_path": "report.html"}

from fastapi.responses import FileResponse
import os

@app.get("/report")
async def get_report():
    path = os.path.abspath("report.html")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"Report file at path {path} does not exist.")
    return FileResponse(path, media_type="text/html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)