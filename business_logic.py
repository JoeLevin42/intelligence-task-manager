from database import agent_db , mission_db

class MoreThanThree(Exception):
    pass

class AgentNotActive(Exception):
    pass

ag_db = agent_db.AgentsDB()
ms_db = mission_db.MissionDB()

def assign_mission_logic(a_id:int , m_id: int):

    open_missions = len(ms_db.get_open_missions_by_agent(id=a_id)) #int
    if open_missions >=3:
        raise  MoreThanThree()
    
    the_agent = ag_db.get_agent_by_id(id=a_id)
    if the_agent.get("is_active") != True:
        raise AgentNotActive()
    
    the_mission = ms_db.get_mission_by_id(id=m_id)
    if the_mission.get("risk_level") ==  "CRITICAL":
        return "only commander can receive the mission"
    
    if the_mission.get("status") != "NEW":
        return "The mission not new cant to assign"
    else:
        ms_db.update_mission_status(id=m_id,status="ASSIGNED")
    
