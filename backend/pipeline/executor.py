from sqlalchemy import text
from database.connection import get_session

def execute_query(sql:str):
    session = get_session()
    sql = sql.strip()
    try:
        
        if sql.upper().startswith('SELECT') and 'LIMIT' not in sql.upper():
            sql = sql.rstrip().rstrip(';')+ " LIMIT 100"
        
        session.execute(text('SET statement_timeout = 5000'))
        
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