from fastapi import APIRouter , HTTPException
from pydantic import BaseModel
from database import agent_db
from database import mission_db
import logging

ag_db = agent_db.AgentsDB()
ms_db = mission_db.MissionDB()
router = APIRouter()
logger = logging.getLogger(__name__)

class CreateMission(BaseModel):
        title : str
        description : str 
        location  : str
        difficulty : int 
        importance : int
       

@router.post("/missions",status_code=201)
def create_mission(data : CreateMission):

    if data.difficulty <= 0 or data.difficulty > 10:
         logger.error("difficulty have to be between 1- 10 only")
         raise HTTPException (status_code=400 , detail="difficulty have to be between 1- 10 only")

    if data.importance <= 0 or data.importance > 10:
           logger.error("importance have to be between 1- 10 only")
           raise HTTPException (status_code=400 , detail="importance have to be between 1- 10 only")
    
    valid_dict = data.model_dump()
    logger.info("Trying to create the mission")
    mission_dict = ms_db.create_mission(data=valid_dict)
    if mission_dict is None:
         raise HTTPException(status_code=400, detail="The mission not created! something went wrong")
    
    return mission_dict
    


@router.get("/missions")
def get_all_mission():

    all_missions = ms_db.get_all_missions()

    return all_missions

    

@router.get("/missions/{id}")
def get_mission_by_id(id: int):
    
    if type(id) != int:
         logger.error("The id have to be int!")
         raise HTTPException(status_code=422 , detail="The id have to be int!")
    
    the_mission = ms_db.get_mission_by_id(id=id)
    if the_mission is None:
        logger.error("The mission not found!")
        raise HTTPException(status_code=404, detail="The mission not found!")
    logger.info("The mission found and sending to the user")
    return the_mission
    

@router.put("/missions/{id}/assign/{agent_id}")
def assign_mission_to_agent(id: int , agent_id: int):
    
    if type(id) != int or type(agent_id) != int:
         raise HTTPException(status_code=422, detail="The id have to be int!")
    the_agent = ag_db.get_agent_by_id(id=agent_id)
    if the_agent is None:
         logger.error("The agent not found")
         raise HTTPException(status_code=404 , detail="The agent not found")
    if the_agent.get("is_active") != True:
        raise HTTPException(status_code=400, detail="The agent not active and cant get missions")
    
    the_mission = ms_db.get_mission_by_id(id=id)
    if the_mission is None:
         logger.error("The mission not found")
         raise HTTPException(status_code=404 , detail="The mission not found")
    if the_mission.get("risk_level") ==  "CRITICAL" and the_agent.get("agent_rank") != "Commander":
        logger.error("Only Commander can get CRITICAL missions")
        raise HTTPException(status_code=400 , detail="Only Commander can get CRITICAL missions")
    
    
    open_missions = len(ms_db.get_open_missions_by_agent(id=agent_id)) #int
    if open_missions >=3:
        raise  HTTPException(status_code=400, detail="The agent already have 3 open missions")
    
    if the_mission.get("status") != "NEW":
        logger.error("Can assign only NEW mission!")
        raise HTTPException(status_code=400 , detail="Can assign only NEW mission!")
    else:
        logger.info("Successfully assign the mission to the agent")
        ms_db.update_mission_status(id=id,status="ASSIGNED")
        ms_db.assign_mission(m_id=id,a_id=agent_id)

    return {"message":"The mission successfully assign to the agent!"}

@router.put("/missions/{id}/start")
def start_mission(id: int):
    if type(id) != int:
            logger.error("The id have to be int!")
            raise HTTPException(status_code=422, detail="The id have to be int!")
        
    the_mission = ms_db.get_mission_by_id(id=id)
    if the_mission is None:
         logger.error("The mission not found!")
         raise HTTPException(status_code=404 , detail="The mission not found!")
    
    if the_mission.get("status") != "ASSIGNED":
         logger.error("for start mission, status have to be ASSIGEND")
         raise HTTPException(status_code=400 ,detail="for start mission, status have to be ASSIGEND")
    

    message = ms_db.update_mission_status(id=id , status="IN_PROGRESS")
    logger.info("mission had been successfully started!")
    return message


@router.put("/missions/{id}/complete")
def complete_mission(id: int):
    if type(id) != int:
        logger.error("The id have to be int!")
        raise HTTPException(status_code=422, detail="The id have to be int!")
    
    the_mission = ms_db.get_mission_by_id(id=id)
    if the_mission is None:
         logger.error("The mission not found!")
         raise HTTPException(status_code=404 , detail="The mission not found!")
    
    if the_mission.get("status") != "IN_PROGRESS":
         logger.error("for end mission, status have to be IN_PROGRESS!")
         raise HTTPException(status_code=400 ,detail="for end mission, status have to be IN_PROGRESS!")
   
    agent_id = the_mission.get("assigned_agent_id")
    message = ms_db.update_mission_status(id=id , status="COMPLETED")
    logger.info("mission had been successfully completed!")
    ag_db.increment_completed(id=agent_id)
    logger.info(f"The agent completed counter mission increased id : {agent_id}")

    return message

@router.put("/missions/{id}/fail")
def fail_mission(id: int):
    
    if type(id) != int:
        logger.error("The id have to be int!")
        raise HTTPException(status_code=422, detail="The id have to be int!")
    
    the_mission = ms_db.get_mission_by_id(id=id)
    if the_mission is None:
         logger.error("The mission not found!")
         raise HTTPException(status_code=404 , detail="The mission not found!")
    
    if the_mission.get("status") != "IN_PROGRESS":
         logger.error("for end mission, status have to be IN_PROGRESS!")
         raise HTTPException(status_code=400 ,detail="for end mission, status have to be IN_PROGRESS!")
   
    agent_id = the_mission.get("assigned_agent_id")
    message = ms_db.update_mission_status(id=id , status="FAILED")
    logger.info("mission had been FAILED!")
    ag_db.increment_failed(id=agent_id)
    logger.info(f"The agent FAILED counter mission increased id : {agent_id}")

    return message

@router.put("/missions/{id}/cancel")
def cancel_mission(id: int):
     
    if type(id) != int:
        logger.error("The id have to be int!")
        raise HTTPException(status_code=422, detail="The id have to be int!")
        
    the_mission = ms_db.get_mission_by_id(id=id)
    if the_mission is None:
         logger.error("The mission not found!")
         raise HTTPException(status_code=404 , detail="The mission not found!")

    
    if (the_mission.get("status") != "ASSIGNED" and the_mission.get("status") != "NEW"):
         logger.error("for end mission, status have to be have to be ASSIGNED or NEW ONLY!")
         raise HTTPException(status_code=400 ,detail="for end mission, status have to be ASSIGNED or NEW ONLY!")
    
    message = ms_db.update_mission_status(id=id, status="CANCELLED")
    logger.info("mission had been CANCELLED!")

    return message
    