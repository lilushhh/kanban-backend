from fastapi import FastAPI
from routers.project_router import router as project_router
from routers.task_router import router as task_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(project_router)
app.include_router(task_router)
