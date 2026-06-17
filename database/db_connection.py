import mysql.connector as seqel 

class DBconnection:
    def __init__(self):
        self.host = "localhost"
        self.database = "Intelligence_db"
        self.user = "root"
        self.password = "1234" # need to check if it recognize as int (maybe its need to be str)

    def get_connection(self):

        cnx = seqel.connect(
            host = self.host,
            database = self.database,
            user = self.user,
            password = self.password
        )

        return cnx
    
    def create_database(self):
        #creating here independent connection because the get_connection
        #is already connected to the database and this method will run
        #only if the database is not exists

        conn = seqel.connect(
            host = self.host,
            user = self.user,
            password = self.password
        )

        cursor = conn.cursor()

        sql = """
        CREATE DATABASE IF NOT EXISTS Intelligence_db
        """
        try:
            cursor.execute(sql)

            is_changed = cursor.rowcount >0
            if is_changed:
                return {"message":"The database created successfully!"}
            
            return {"message":"the database is already exists"}

        except Exception as e:

            raise
        
        finally:
            cursor.close()
            conn.close()

    def create_tables(self):
        conn = self.get_connection() ## Need to check this if this is working!!!!!
        cursor = conn.cursor()

        try:

            sql_table_agent = """
            CREATE TABLE IF NOT EXISTS agents (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            specialty VARCHAR(100) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE NOT NULL,
            completed_missions INT DEFAULT 0 NOT NULL,
            failed_missions INTz DEFAULT 0 NOT NULL,
            agent_rank ENUM('Junior','Senior','Commander') NOT NULL
            )
            """
            cursor.execute(sql_table_agent)

            sql_table_missions = """
            CREATE TABLE IF NOT EXISTS missions(
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            location VARCHAR(100) NOT NULL,
            difficulty INT NOT NULL,
            importance INT NOT NULL,
            status VARCHAR(100) DEFAULT 'NEW' NOT NULL,
            risk_level VARCHAR(100) NOT NULL,
            assigned_agent_id INT DEFAULT NULL
            )
            """

            #Maybe check here if created?

            cursor.execute(sql_table_missions)

        finally:
            cursor.close()
            conn.close()

