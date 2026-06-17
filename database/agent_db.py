from db_connection import DBconnection

connector = DBconnection()

class AgentsDB():

    def create_agent(self,data:dict):
        
        conn =  connector.get_connection()
        cursor = conn.cursor(dictionary=True)

        keys_parts = [f"`{key}`" for key in data.keys()]
        keys_str = ", ".join(keys_parts)
        place_holders = ", ".join(["%s"]*len(keys_parts))
        values = tuple(data.values())

        sql = f"INSERT INTO agents ({keys_str}) VALUES ({place_holders})"

        try:
            cursor.execute(sql,values)
            conn.commit()
           
            new_id = cursor.lastrowid

            agent_dict = self.get_agent_by_id(new_id) 
            return agent_dict
        
        except Exception as e:
            conn.rollback()

            raise

        finally:
            cursor.close()
            conn.close()

    def get_all_agents(self):
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT * FROM agents"

        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
        
        finally:
            cursor.close()
            conn.close()
            

    def get_agent_by_id(self,id:int):
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT * FROM agents WHERE id = %s"

        try:
            cursor.execute(sql,(id,))
            row = cursor.fetchone()
            return row
        
        finally:
            cursor.close()
            conn.close()

    def update_agent(self,id:int, data:dict):
        
        
        conn =  connector.get_connection()
        cursor = conn.cursor()

        columns_parts = [f"`{key}`=%s" for key in data.keys()]
        columns_str = ", ".join(columns_parts)
        values = tuple(data.values()) + (id,) # The id have to be last

        sql = f"UPDATE agents SET {columns_str} WHERE id = %s"

        try:
            cursor.execute(sql,values)
            is_changed = cursor.rowcount >0
            conn.commit()

        except Exception as e:
            conn.rollback()

            raise

        finally:
            cursor.close()
            conn.close()

    def deactivate_agent(self,id:int):
        
        conn =  connector.get_connection()
        cursor = conn.cursor()

        sql = "UPDATE agents SET is_active = FALSE WHERE id = %s"

        try:
            cursor.execute(sql,(id,))
            is_changed = cursor.rowcount > 0
            conn.commit()

        except Exception as e:
            conn.rollback()

            raise

        finally:
            cursor.close()
            conn.close()

    def increment_completed(self,id:int):
        
        conn =  connector.get_connection()
        cursor = conn.cursor()

        sql = "UPDATE agents SET completed_missions = completed_missions + 1 WHERE id = %s"

        try:
            cursor.execute(sql,(id,))
            is_changed = cursor.rowcount > 0

            conn.commit()

        except Exception as e:
            conn.rollback()

            raise

        finally:
            cursor.close()
            conn.close()


    def increment_failed(self,id:int):
        conn =  connector.get_connection()
        cursor = conn.cursor()

        sql = "UPDATE agents SET failed_missions = failed_missions + 1 WHERE id = %s"

        try:
            cursor.execute(sql,(id,))
            is_changed = cursor.rowcount > 0
    
            conn.commit()

        except Exception as e:
            conn.rollback()

            raise

        finally:
            cursor.close()
            conn.close()

    def get_agent_performance(self,id:int):
        
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql =  "SELECT * FROM agents WHERE id = %s" # returns the dict 
        try:
            cursor.execute(sql,(id,))
            row = cursor.fetchone()

            if row is None:
                return None # its for not start to calc with none type
            total_missions = (row.get("completed_missions")) + (row.get("failed_missions"))
            if total_missions > 0:
                success_rate = (row.get("completed_missions") * 100) / total_missions
            else:
                success_rate = 0

            """
            completed, failed, total, success_rate
            """
            performance_dict = {
                "completed" : row.get("completed_missions"),
                "failed" : row.get("failed_missions"),
                "total" : total_missions,
                "success_rate" : success_rate
            }

            return performance_dict
        finally:
            cursor.close()
            conn.close()


    def count_active_agents(self):
        
        conn = connector.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT COUNT(*) AS total_active FROM agents WHERE `is_active` = TRUE"

        try:
            cursor.execute(sql)
            row = cursor.fetchone() #Returns {total_active:number} #optional ["total_active"] 
            return row
        
        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    ag_db = AgentsDB()

    # """
    #  CREATE TABLE IF NOT EXISTS agents (
    #         id INT PRIMARY KEY AUTO_INCREMENT,
    #         name VARCHAR(100) NOT NULL,
    #         specialty VARCHAR(100) NOT NULL,
    #         is_active BOOLEAN DEFAULT TRUE NOT NULL,
    #         completed_missions INT DEFAULT 0 NOT NULL,
    #         failed_missions INT DEFAULT 0 NOT NULL,
    #         agent_rank ENUM('Junior','Senior','Commander') NOT NULL
    #         )"""
    create_dict = {"name":"David","specialty":"writer","agent_rank":"Junior"}
    # print(ag_db.create_agent(data=create_dict))
    # ag_db.increment_failed(3)
    # ag_db.increment_completed(3)
    # print(ag_db.get_agent_performance(3)) # need to check what to do with 0 completed
    print(ag_db.get_agent_by_id(2))
    