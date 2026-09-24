from sqlalchemy import text
from database.connection import get_session

def execute_query(sql:str):
    session = get_session()
    
    try:
        
        result = session.execute(text(sql))
        
        columns = result.keys()
        rows = result.fetchall()
        
        return {
            "success":True,
            "columns":list(columns),
            "rows":[list(row) for row in rows]
        }
        
    except Exception as e:
        return {
            "success":False,
            "error":str(e)
        }
    
    finally:
        session.close()