from fastapi import APIRouter , HTTPException
from pydantic import BaseModel
from database import agent_db
from typing import Literal
import logging

ag_db = agent_db.AgentsDB()
router = APIRouter()
logger = logging.getLogger(__name__)

     # The another things is default in the database is_active optional?
class CreateAgent(BaseModel):
     name : str
     specialty : str
     agent_rank : str

class UpdateAgent(BaseModel):

     name : str | None = None
     specialty : str | None = None
     is_active : bool | None = None
     completed_missions : int | None = None
     failed_missions : int | None = None
     agent_rank : Literal['Junior','Senior','Commander']  | None = None
     #check the patch
"""
 id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(100) NOT NULL,
specialty VARCHAR(100) NOT NULL,
is_active BOOLEAN DEFAULT TRUE NOT NULL,
completed_missions INT DEFAULT 0 NOT NULL,
failed_missions INT DEFAULT 0 NOT NULL,
agent_rank ENUM('Junior','Senior','Commander') NOT NULL
""" 

@router.post("/agents",status_code=201)
def create_agent(data: CreateAgent):
     
     check_data = data.model_dump()
     if check_data is None:
          logger.error("Something not valid with the body data")
          raise HTTPException(status_code=400, detail="Something not valid with the body data")
     
     if data.agent_rank not in ['Junior','Senior','Commander']: #need to check if it getting here
          logger.error("The agent type is not illegal")
          raise HTTPException(status_code=400 , detail="The agent type is not illegal")
        
     try:
            logger.info("Trying to create new agent")
            agent_dict = ag_db.create_agent(data=check_data)
            if agent_dict is None:
                logger.error("The agent didn't created something went wrong")
                raise HTTPException(status_code=400 , detail="The agent didn't created something went wrong")

            logger.info("agent successfully created and send the object to the user")        
            return agent_dict
     
     except Exception as e:
          
          raise HTTPException(status_code=503, detail=f"Something went wrong in database {str(e)}")

@router.get("/agents")
def get_all_agents():
    all_agents = ag_db.get_all_agents()

    return all_agents

@router.put("/agents/{id}")
def update_agent(id: int , data : UpdateAgent):

     if type(id) != int:
          logger.error("id have to be int!")
          raise HTTPException(status_code=422 , detail="id have to be int!") 
     
     the_agent = ag_db.get_agent_by_id(id=id)
     if the_agent is None:
          logger.error("The agent not found")
          raise HTTPException(status_code=404, detail="The agent not found")
     
     valid_dict = data.model_dump(exclude_unset=True)
     print(valid_dict)
     if not valid_dict:
          logger.error("The data is empty cant update! or something not legal")
          raise HTTPException(status_code=400, detail="The data is empty can update!")   

     
     is_changed = ag_db.update_agent(id=id, data=valid_dict)
     # if not is_changed:
     #      raise HTTPException(status_code=400 , detail="The agent not updated try again")
     logger.info("The agent successfully updated!")
     return {"message":"The agent successfully updated!"}

    
     
@router.put("/agents/{id}/deactivate")
def deactivate_agent(id: int):
     
     the_agent = ag_db.get_agent_by_id(id=id)
     if the_agent is None:
          logger.info("The agent not found")
          raise HTTPException(status_code=404 , detail="The agent not found")


     is_changed = ag_db.deactivate_agent(id=id)
     if not is_changed:
          raise HTTPException(status_code=400 , detail="The agent didn't updated")

     logger.info("The agent successfully deactivated!")
     return {"message":"The agent successfully deactivated!"}

      


@router.get("/agents/{id}") # path param!!!
def get_agent_by_id(id: int):
    
     if type(id) != int:
         logger.error("The id have to be int!")
         raise HTTPException(status_code=422 , detail="The id have to be int!")

     logger.info("trying to search the agent")
     the_agent = ag_db.get_agent_by_id(id=id)
     
     if the_agent is None:
          logger.error("The agent not found!")
          raise HTTPException(status_code=404, detail="The agent not found")
     logger.info("The agent found and sending to the user")
     return the_agent


@router.get("/agents/{id}/performance") ###path param!!!!!
def get_agent_performance(id: int ):
     
     if type(id) != int:
         logger.error("The id have to be int!")
         raise HTTPException(status_code=422 , detail="The id have to be int!")
    
#     
     logger.info("Trying to get the performance to the agent")
     performance_dict = ag_db.get_agent_performance(id=id)
     if performance_dict is None:
          logger.error("The agent not found")
          raise HTTPException(status_code=404, detail="The agent not found")
     
     logger.info("The performance dict send to user!")
     return performance_dict

