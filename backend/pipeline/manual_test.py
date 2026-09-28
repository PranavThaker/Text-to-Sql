from pipeline.graph import app

from pipeline.executor import execute_query


def test_readonly_write_query():
    print("\n--- Testing write query against read-only database user ---")

    # Deliberately bypass validator.py and send a DELETE directly to executor.py.
    sql = "DELETE FROM products WHERE product_id = 1"

    result = execute_query(sql)

    print("SQL:", sql)
    print("Result:", result)

    if result["success"]:
        print("ERROR: Write query unexpectedly succeeded.")
    else:
        print("Expected failure: read-only database user rejected the write query.")



questions = [
    "How many products are in each category?",
    "Show me all orders placed by customers.",
    "Which products have the highest prices?",
    "How much money has each customer spent?",
    "Show me the products included in each order."
]

for question in questions:
    print("\n" + "=" * 70)
    print("QUESTION:", question)
    print("=" * 70)
    
    initial_state = {
        "question": question,
        "retrieved_context": {},
        "generated_sql": "",
        "execution_result": {},
        "retry_count": 0,
        'last_error':''
    }
    
    try:
        result = app.invoke(initial_state)

        print("\nGENERATED SQL:")
        print(result["generated_sql"])

        print("\nEXECUTION RESULT:")
        print(result["execution_result"])

        if "summary" in result["execution_result"]:
            print("\nSUMMARY:")
            print(result["execution_result"]["summary"])

        print("\nRETRY COUNT:")
        print(result["retry_count"])

    except Exception as e:
        print("\nPIPELINE ERROR:")
        print(e)
test_readonly_write_query()
        
