import os
import io
import zipfile
import tempfile
import shutil
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from src.workflow import Workflow

load_dotenv()

app = FastAPI(
    title="Chess Endgame AI Agent",
    description="An AI-powered chess endgame lesson generator",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LessonRequest(BaseModel):
    query: str


class HealthResponse(BaseModel):
    status: str
    message: str


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(status="ok", message="Chess Endgame AI Agent is running")


@app.post("/lessons")
async def generate_lessons(request: LessonRequest):
    """
    Generate chess endgame lessons based on the provided query.
    Returns a zip file containing all generated PDF lessons.
    """
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        # Initialize and run the workflow
        workflow = Workflow()
        result = workflow.run(request.query.strip())

        # Check if lessons were generated
        if not result.book_text_content:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate lessons. Please try again."
            )

        # Check if file paths exist
        if not result.file_paths or len(result.file_paths) == 0:
            raise HTTPException(
                status_code=500,
                detail="No lesson files were generated."
            )

        # Create a zip file in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for file_path in result.file_paths:
                if os.path.exists(file_path):
                    # Get just the filename for the archive
                    filename = os.path.basename(file_path)
                    zip_file.write(file_path, filename)

        # Reset buffer position
        zip_buffer.seek(0)

        # Create safe filename from query
        safe_query = "".join(c if c.isalnum() or c in " -_" else "" for c in request.query)
        safe_query = safe_query.replace(" ", "_")[:50]
        zip_filename = f"chess_lessons_{safe_query}.zip"

        # Return the zip file as a streaming response
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={
                "Content-Disposition": f'attachment; filename="{zip_filename}"'
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while generating lessons: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)