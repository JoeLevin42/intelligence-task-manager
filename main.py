from fastapi import FastAPI 
import uvicorn
from routes.agent_routes import router as agent_router
from routes.mission_routes import router as mission_router
from routes.report_routes import router as report_router

app = FastAPI()
app.include_router(agent_router)
app.include_router(mission_router)
app.include_router(report_router)
