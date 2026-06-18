# INTELLIGENCE_TASK_MANAGER

## system description

This system supposed to manage agents and their missions with ordered tables
there is important rules that this system keeps and giving for the good order
the rules is down below

## Running instructions

**Python environment command**

```
python -m venv .venv
.\.venv\Scripts\activate
```

**Python packages to install also in the requirements.txt**

```
pip install fastapi uvicorn  mysql-connector-python 
or
python -m pip install -r requirements.txt
or
pip install -r requirements.txt
```

**Open Docker app and run this in the cli**

```
docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 \
  -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0
```

## Python DB to run:

create object from DBconnection class in db_connection.py
and run this for example **ONLY FOR TESTS!**

```
my_db = DBconnection()
my_db.create_database()
my_db.create_tables()
```

## PYTHON RUN THE SERVER ALL COMMANDS

```Pwershell
uvicorn main:app 
or
py main.py 
```


**DATABASE NAME** = Intelligence_db


## folders and files structure

```
intelligence-task-manager/
├── main.py 
├── database/ 
├── routes/ 
│ ├── agent_routes.py
│ ├── mission_routes.py
│ └── report_routes.py
├── logs/ 
│ └── app.log
├── README.md 
└── requirements.txt

```

# THE data tables

**RULE** everywhere that not written what need to return , so return success/error message
 
## agents table

- **id** | INT PRIMARY KEY AUTO_INCREMENT | | the agent id
- **name** | VARCHAR | the name of the agent
- **specialty** | VARCHAR | the specialty of the agent
- **is_active** | BOOLEAN | the activity status of the agent
- **completed_missions** | INT | DEFAULT 0
- **failed_mission** | INT | DEFAULT 0
- **agent_rank** | ENUM/VARCHAR | (Junior / Senior / Commander ) ONLY

**RULE** everywhere that need to return list if not found data , so return empty list [] 
## missions table

- **id** | INT PRIMARY KEY AUTO_INCREMENT | id of the mission
- **title** | VARCHAR | the title of the mission
- **description** | TEXT | free text description of the mission
- **location** | VARCHAR | location of the mission
- **difficulty** | INT | from 1 - 10 only!
- **importance** | INT | from 1- 10 only!
- **status** | VARCHAR | DEFAULT NEW
- **risk_level** | VARCHAR | AUTOMATICALLY (FORMULA DOWN BELOW)
- **assigned_agent_id** | INT | the agent id that handles the mission | DEFAULT NULL until assignment

**Formula risk level** = (difficulty * 2) + importance = risk_level

### Table of risk level

- **RISK LEVEL** | **SCORE** |
- **LOW** | 0 -9 |
- **MEDIUM** | 10 - 17 |
- **HIGHT** | 18 - 24 |
- **CRITICAL** | 25 +|

## Table of mission status

**STATUS** | **MEANING** |
**NEW** | new mission default in creation|
**ASSIGNED** | assigned to agent |
**IN_PROGRESS** | in progress right now|
**COMPLETED** | the mission successfully completed |
**CANCELLED** | the mission canceled|


# THE DATABASE CLASSES

## DB_connection

**get_connection()** | returns active connection to mysql
**create_database()** | creating the database if not exists (Intelligence_db) 
**create_tables()** | creating the two tables (agents , missions) if not exists

The functions create_database() and create_tables() will run in the start of the system


## AgentsDB

- **create_agent(data:dict)** | creating new agent to the db
- **get_all_agents()** | returns list of dicts of all the agents
- **get_agent_by_id(id:int)** | returns specific agent by id
- **update_agent(id:int,data:dict)** | updating all the the row , cant change id
- **deactivate_agent(id:int)** | deactivate the agent status to not active (FALSE)
- **increment_completed(id:int)** | incrementing the total completed_missions column
- **increment_failed(id:int)** | incrementing the total failed_missions column
- **get_agent_performance(id:int)** | returns dict with this keys (completed,failed,total,success_rate) , with the number of this key (the **success_rate** need to calculated from this data)
- **count_active_agents()** | returns int of the total **active** agents only


## MissionDB 

- **create_mission(data:dict)** | creating new mission , and returns the mission object (row)
- **get_all_missions** | returns list of dicts of all the missions
- **get_mission_by_id(id:int)** | returns specific mission by id or None if not exists
- **assign_mission(m_id:int,a_id:int)** | assigning mission to agent by mission id and agent id
- **update_mission_status(id:int,status:str)** | updates the status of the mission (by the allowed status)
- **get_open_missions_by_agent(id:int)** | returns mission (ASSIGNED/IN_PROGRESS) of the agent (the id is of the agent)
- **count_all_missions()** | returns int of all the missions
- **count_by_status(status:str)** | count the missions by status given as param
- **count_open_missions()** | count opens missions (ASSIGNED/IN_PROGRESS)
- **count_critical_missions()** | count the mission with CRITICAL
- **get_top_agent()** | returns the agent with teh highest completed missions (only one)


## Business logic rules

- **rank** | have to be Junior/Senior/Commander -  Something else raise error
- **difficulty , importance** | have to be between 1- 10 everything else raise an error
- **risk_level** | automatically calculated the user doesn't sends it 
- **agent with , active = False** | cant receive missions
- **agent cant hold more than three opened missions** | opened missions (ASSIGNED/IN_PROGRESS)
- **if risk_level = critical** | only agent in rank Commander can receive the mission
- **Can assign new mission** | only if the mission in status **NEW** after assignment **status=ASSIGNED**
- **Can to start mission** | only in status **ASSIGNED** after status **status=IN_PROGRESS** 
- **Can to end mission** | only in status **IN_PROGRESS** after finish **status=failed, completed** 
- **Can to cancel mission** | only in status **NEW , ASSIGNED** else raise an error


## Main.py:

initialize the fastapi with all the routes and when the server up calling to created database
and tables if not exist and runs the uvicorn server on the fastapi


## Agents endpoints

- **POST** |  /agents |  create new agent
- **GET** | /agents| get all the agents
- **GET** |/agents/{id} | get agents by id
- **PUT** |/agents{id}| update agent
- **PUT** |/agents/{id}/ deactivate| deactivate the agent
- **GET** |/agents/{id}/performance| giving the agents performances 

## Missions endpoints

- **POST** | /missions |create new mission
- **GET** | /missions | get all missions
- **GET** | /missions/{id}| get mission by id
- **PUT** |/missions/{id}/assign/{agent_id}| assign mission to agent
- **PUT** |/missions/{id}/start| start mission
- **PUT** |/missions/{id}/complete| complete and end the mission
- **PUT** |
/missions/{id}/fail| fail and end the mission
- **PUT** |
/missions/{id}/cancel  | cancel the mission

## Reports endpoints

- **GET** |
/reports/summary | general report of all the system
- **GET** |/reports/missions-by-status
| missions by status report 
- **GET** |/reports/top-agent | the agent with the most complete missions

- **/reports/summary** returns 

for example
```
}
"active_agents_count": 0,
"total_missions": 0,
"open_missions": 0,
"completed_missions": 0,
"failed_missions": 0,
"critical_missions": 0
}
```

- **/reports/summary** returns 

for example 

```
{
"open": 5,
"in_progress": 3,
"completed": 12,
"failed": 1,
"canceled": 2
}

```


## Assign mission check

- check if the mission exists | if not 404
- check if the agent exist | if not 404
- the mission in status NEW | if not not available 400
- the agent active | if not 400
- less than three mission - | 400 status
- critical mission to not commander - 400 status