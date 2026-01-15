from fastapi import FastAPI
import logging
import os

# Debug support for Docker
if os.getenv("ENABLE_DEBUG") == "true":
    import debugpy
    debugpy.listen(("0.0.0.0", 5678))
    print("⏳ Waiting for debugger attach on port 5678...")
    debugpy.wait_for_client()
    print("✅ Debugger attached!")

from app.api.http.controllers.file_controller import router as files_router
from app.api.http.controllers.users_controller import router as users_router
from app.api.http.controllers.book_controller import router as books_router
from app.api.http.controllers.chapter_controller import router as chapters_router

from app.api.http.controllers.parser_controller import router as parser_router
# from app.api.http.controllers.parser_dev_controller import router as parser_dev_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

app = FastAPI(
    title="Translator API",
    version="0.1.0",
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(users_router)
app.include_router(files_router)
app.include_router(books_router)
app.include_router(chapters_router)
app.include_router(parser_router)
# app.include_router(parser_dev_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.run:app", host="0.0.0.0", port=8000, reload=True)