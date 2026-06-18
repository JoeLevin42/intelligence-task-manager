from fastapi import APIRouter , HTTPException
from database import agent_db
from database import mission_db
import logging

logger = logging.getLogger(__name__)
ag_db = agent_db.AgentsDB()
ms_db = mission_db.MissionDB()

router = APIRouter()

@router.get("/reports/summary")
def get_report_summary():
    try:
        the_agents = ag_db.get_all_agents()
        the_missions = ms_db.get_all_missions()

        active_agents_count = ag_db.count_active_agents()
        total_missions = ms_db.count_all_missions()
        open_missions = ms_db.count_open_missions()
        completed_missions = ms_db.count_by_status(status="COMPLETED")
        failed_missions = ms_db.count_by_status(status="FAILED")
        critical_missions = ms_db.count_critical_missions()

        if not (the_agents or the_missions):
            logger.info("Not found any mission or agents so everything is 0")
            summary_dict = {
            "active_agents_count": 0,
            "total_missions": 0,
            "open_missions": 0,
            "completed_missions": 0,
            "failed_missions": 0 ,
            "critical_missions": 0,
            }
        else:
            logger.info("The summary is full")
            summary_dict = {
                "active_agents_count": active_agents_count,
                "total_missions": total_missions,
                "open_missions": open_missions,
                "completed_missions": completed_missions,
                "failed_missions": failed_missions ,
                "critical_missions": critical_missions
                }
        
        return summary_dict
    
    except Exception as e:
        logger.error(f"The DB is down or there is problem {str(e)}")
        raise HTTPException(status_code=500 , detail=f"The DB is down or there is problem {str(e)}")
    
@router.get("/reports/missions-by-status")
def get_mission_by_status():
    # try:
        the_missions = ms_db.get_all_missions()
        if not the_missions:
            logger.info("Not found any mission so everything is 0")
            reports_by_status = {
                        "open": 0,
                        "in_progress": 0,
                        "completed": 0,
                        "failed": 0,
                        "canceled": 0
                        }
            
        

        open_missions = ms_db.count_open_missions()
        in_progress_mission = ms_db.count_by_status(status= "IN_PROGRESS")
        completed_missions = ms_db.count_by_status(status= "COMPLETED")
        failed_missions = ms_db.count_by_status(status= "FAILED")
        canceled_missions = ms_db.count_by_status(status= "CANCELLED")
        logger.info("The reports is full")
        reports_by_status = {
                "open": open_missions,
                "in_progress": in_progress_mission,
                "completed": completed_missions,
                "failed": failed_missions,
                "canceled": canceled_missions
                }
    
        return reports_by_status
    
    # except Exception as e:
    #         logger.error(f"The DB is down or there is problem {str(e)}")
    #         raise HTTPException(status_code=500 , detail=f"The DB is down or there is problem {str(e)}")
    
@router.get("/reports/top-agent")
def get_top_agent():
    # try:


        top_agent_id = ms_db.get_top_agent()
        if top_agent_id is None:
            logger.error("No top agent probably the list empty")
            raise HTTPException(status_code=404, detail="No top agent probably the list empty")

        top_agent = ag_db.get_agent_by_id(id=top_agent_id)
        if top_agent is None:
            raise HTTPException(status_code=404 , detail="No agent in with id")
            
        else:
             return top_agent
    
    # except Exception as e:
            
    #         logger.error(f"The DB is down or there is problem {str(e)}")
    #         raise HTTPException(status_code=500 , detail=f"The DB is down or there is problem {str(e)}")