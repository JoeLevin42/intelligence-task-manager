from db_connection import DBconnection

connector = DBconnection()

class MissionDB():

    
    def create_mission(self,data:dict):
       
        conn =  connector.get_connection()
        cursor = conn.cursor(dictionary=True)

        risk_level_calc = (data.get("difficulty")*2) + data.get("importance")
        risk_level = ""
        if risk_level_calc >= 0 and risk_level_calc <= 9:
            risk_level = "LOW"
        elif risk_level_calc >=10 and risk_level_calc <= 17:
            risk_level = "MEDIUM"
        elif risk_level_calc >=18 and risk_level_calc <= 24:
            risk_level = "HIGH"
        elif risk_level_calc >= 25:
            risk_level = "CRITICAL"

        data.update({"risk_level":risk_level})

        keys_parts = [f"`{key}`" for key in data.keys()]
        keys_str = ", ".join(keys_parts)
        place_holders = ", ".join(["%s"]*len(keys_parts))
        values = tuple(data.values())


        sql = f"INSERT INTO missions ({keys_str}) VALUES ({place_holders})"

        try:
            cursor.execute(sql,values)
            conn.commit()
           
            new_id = cursor.lastrowid

            agent_dict = self.get_mission_by_id(new_id) 
            return agent_dict
        
        except Exception as e:
            conn.rollback()

            raise

        finally:
            cursor.close()
            conn.close()

    def get_all_missions(self):
        
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT * FROM missions"

        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
        
        finally:
            cursor.close()
            conn.close()

    def get_mission_by_id(self, id: int):
        
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT * FROM missions WHERE id = %s"

        try:
            cursor.execute(sql,(id,))
            row = cursor.fetchone()
            return row
        
        finally:
            cursor.close()
            conn.close()

    def assign_mission(self, m_id: int, a_id: int):

        conn = connector.get_connection()
        cursor = conn.cursor()
        values = (a_id,m_id) # the order matters
        sql = "UPDATE missions SET assigned_agent_id = %s WHERE id = %s"

        try:
            cursor.execute(sql,values)
            conn.commit()
            is_changed = cursor.rowcount > 0

            if is_changed:
                return {"message":f"The mission assign successfully to agent! : {a_id}"}
            else:
                return  {"message":f"The mission assign Failed!"}
            
        except Exception as e:
            conn.rollback()

            raise
        finally:
            cursor.close()
            conn.close()

    def update_mission_status(self,id: int,status: str):
        
        conn = connector.get_connection()
        cursor = conn.cursor()
        values = (status,id) # The order matter
        sql = "UPDATE missions SET status  = %s WHERE id = %s"

        try:
            cursor.execute(sql,values)
            conn.commit()
            is_changed = cursor.rowcount > 0
            if is_changed:
                return {"message":"The mission status updated"}
            else:
                return {"message":"The mission status failed"}
            
        except Exception as e:
            conn.rollback()

            raise

        finally:
            cursor.close()
            conn.close()


    def get_open_missions_by_agent(self,id: int):
        
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        #open_missions = ("ASSIGNED", "IN_PROGRESS")

        sql = """
        SELECT * FROM missions 
        WHERE assigned_agent_id = %s 
        AND (status = 'IN_PROGRESS' OR status = 'ASSIGNED')
        """


        try:
            cursor.execute(sql,(id,))
            rows = cursor.fetchall() # Returns 
            return rows
        
        finally:
            cursor.close()
            conn.close()

    def count_all_missions(self):
        
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        sql = "SELECT COUNT(*) AS total_missions FROM missions"

        try:
            cursor.execute(sql)
            row = cursor.fetchone() # Returns dict {total_missions:number}
            return row
        
        finally:
            cursor.close()
            conn.close()

    def count_by_status(self, status: str):
        
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        sql = "SELECT COUNT(*) AS total_missions FROM missions WHERE status = %s"

        try:
            cursor.execute(sql,(status,))
            row = cursor.fetchone() # Returns dict {missions_by_status:number}
            return row
        
        finally:
            cursor.close()
            conn.close()

    def count_open_missions(self):
        
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        open_missions = ("ASSIGNED", "IN_PROGRESS")
        sql = """
        SELECT COUNT(*) AS total_open_missions 
            FROM missions 
            WHERE status = 'ASSIGNED' OR status = 'IN_PROGRESS'
        """

        try:
            cursor.execute(sql)
            row = cursor.fetchone() # Returns dict {total_open_missions :number}
            return row
        
        finally:
            cursor.close()
            conn.close()

    def count_critical_missions():
        
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)
        #open_missions = ("ASSIGNED", "IN_PROGRESS")

        sql = """
        SELECT COUNT(*) AS total_critical_missions
            FROM missions 
            WHERE status = 'ASSIGNED' OR status = 'IN_PROGRESS'
        """

        try:
            cursor.execute(sql)
            row = cursor.fetchone() # Returns dict {total_critical_missions :number}
            return row
        
        finally:
            cursor.close()
            conn.close()

    def get_top_agent(self):
         
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
         SELECT assigned_agent_id , COUNT(*) AS total_completed 
         FROM missions 
         WHERE `status` = 'COMPLETED' 
         GROUP BY assigned_agent_id 
         ORDER BY total_completed DESC
         LIMIT 1
        """

        try:
            cursor.execute(sql)
            row = cursor.fetchone() # Returns {assigned_agent_id : number} # IF ISNT ANY NUMBER NONE!

            return row
        
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    ms_db = MissionDB()
    create_dict = {"title":"blDEablaDE","description":"This mission is very important","location":"Iran",
                   "difficulty":10 , "importance":5}
    # print(ms_db.create_mission(create_dict))
    # print(ms_db.assign_mission(6,2)) #not changing nothing in the status
    print((ms_db.get_mission_by_id(2)))
    # print(ms_db.count_by_status("IN_PROGRESS"))
    # print(ms_db.count_open_missions())
    # print(ms_db.get_top_agent())
    