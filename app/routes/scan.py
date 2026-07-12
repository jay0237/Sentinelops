import time

from fastapi import APIRouter, Depends, File, Request, UploadFile
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config.api_key import verify_api_key
from app.config.deps import get_db
from app.core.observability import (
    BLOCKED_PROMPT_COUNT,
    HIGH_THREAT_COUNT,
    REQUEST_COUNT,
    REQUEST_DURATION,
    SAFE_PROMPT_COUNT,
    limiter,
)
from app.models.prompt_log import PromptLog
from app.schemas.scan import PromptScanRequest, ScanResponse
from app.security.engine import scan
from app.utils.injection_detector import detect_prompt_injection
from app.utils.pii_scanner import detect_pii

router = APIRouter()


@router.post("/scan", response_model=ScanResponse)
@limiter.limit("5/minute")
def scan_ai_prompt(
    request: Request,
    prompt: PromptScanRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):

    start_time = time.time()

    REQUEST_COUNT.inc()

    text = prompt.text
    result = scan(text, db)

    if result["safe"]:
        SAFE_PROMPT_COUNT.inc()
    else:
        BLOCKED_PROMPT_COUNT.inc()

    if result["severity"] in ["high", "critical"]:
        HIGH_THREAT_COUNT.inc()

    log = PromptLog(
        prompt=result["original_text"],
        status="safe" if result["safe"] else "blocked",
        reason=result["reason"],
        severity=result.get("severity"),
        category=result.get("category", "General")
    )

    try:
        db.add(log)
        db.commit()
    except SQLAlchemyError:
        db.rollback()

    REQUEST_DURATION.observe(
        time.time() - start_time
    )

    return result


@router.post("/scan-file")
async def scan_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    content = await file.read()

    text = content.decode("utf-8", errors="ignore")

    result = scan(text, db)

    return {
        "filename": file.filename,
        "result": result,
        "scan_result": result
    }


@router.post("/detect-pii")
def detect_pii_endpoint(data: dict):

    result = detect_pii(data["text"])

    return {
        "pii_detected": result
    }


@router.post("/detect-injection")
def detect_injection(data: dict):

    result = detect_prompt_injection(
        data["text"]
    )

    return result
