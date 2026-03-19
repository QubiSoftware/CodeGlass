import json
import subprocess
import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent


class AnalyzeRequest(BaseModel):
    path: str


app = FastAPI(title="CodeGlass Core", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def run_translator(target: Path) -> dict:
    """
    Call core.translator as a subprocess and return the JSON payload.
    This keeps a clean separation between the web API and the analysis logic.
    """
    cmd = [sys.executable, "-m", "core.translator", str(target)]
    proc = subprocess.run(cmd, capture_output=True, text=True)

    if proc.returncode != 0:
        raise HTTPException(
            status_code=500,
            detail=f"translator failed: {proc.stderr.strip()}",
        )

    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"invalid JSON from translator: {exc}",
        )


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/analyze")
def analyze(req: AnalyzeRequest) -> dict:
    """
    Analyze a Python file and return a CodeGlass graph payload.
    """
    target = (BASE_DIR / req.path).resolve()

    if not target.is_file():
        raise HTTPException(status_code=404, detail=f"file not found: {target}")

    return run_translator(target)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("core.server:app", host="127.0.0.1", port=8000, reload=True)

