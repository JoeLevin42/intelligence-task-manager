from fastapi import FastAPI 
import uvicorn
from database.db_connection import DBconnection
from routes.agent_routes import router as agent_router
from routes.mission_routes import router as mission_router
from routes.report_routes import router as report_router
import logging 

connector = DBconnection()
logger = logging.getLogger(__name__)
logging.basicConfig(filename="./logs/app.log",level=logging.INFO, format="%(asctime)s|%(levelname)s|%(message)s") 
app = FastAPI()

connector.create_database()

connector.create_tables()


app.include_router(agent_router)
app.include_router(mission_router)
app.include_router(report_router)

if __name__ == "__main__":
    uvicorn.run(app)