from __future__ import annotations

from fastapi import UploadFile


async def extract_text(file: UploadFile) -> str:
    raw = await file.read()
    filename = (file.filename or "").lower()

    if filename.endswith(".pdf"):
        try:
            import fitz  # type: ignore

            text = []
            with fitz.open(stream=raw, filetype="pdf") as doc:
                for page in doc:
                    text.append(page.get_text())
            return "\n".join(text).strip()
        except Exception:
            # Fallback if PDF parser is unavailable.
            return raw.decode("utf-8", errors="ignore").strip()

    return raw.decode("utf-8", errors="ignore").strip()
