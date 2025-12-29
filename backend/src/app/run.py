from fastapi import FastAPI
import logging

from app.api.http.controllers.file_controller import router as files_router
from app.api.http.controllers.users_controller import router as users_router

from app.api.http.controllers.parser_controller import router as parser_router

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
app.include_router(parser_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.run:app", host="0.0.0.0", port=8000, reload=True)