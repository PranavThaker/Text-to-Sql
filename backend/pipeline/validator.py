import sqlglot
from sqlglot import exp

def validator_sql(sql:str):
    if not sql or not sql.strip():
        return False,"SQL query is empty"
    
    try:
        statements = sqlglot.parse(sql)
        if len(statements)!=1:
            return False,"Only one SQL statement is allowed."

        parsed_sql = statements[0]
        
        if not isinstance(parsed_sql,exp.Select):
            return False,"Only SELECT statements are allowed."
        
        return True,"SQL validation passed."
    
    except Exception as e:
        return False,f"Invalid SQL : {e}"