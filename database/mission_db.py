from db_connection import DBconnection

connector = DBconnection()

class MissionDB():

    
    def create_mission(self,data:dict):
        pass

    def get_all_missions(self):
        pass

    def get_mission_by_id(self, id: int):
        pass

    def assign_mission(self, m_id: int, a_id: int):
        pass

    def update_mission_status(self,id: int,status: str):
        pass

    def get_open_missions_by_agent(self,id: int):
        pass

    def count_all_missions(self):
        pass

    def count_by_status(self, status: str):
        pass

    def count_open_missions(self):
        pass

    def count_critical_missions():
        pass

    def get_top_agent():
        pass