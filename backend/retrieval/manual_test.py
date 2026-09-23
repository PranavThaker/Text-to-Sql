from vector_store import retrieve_context

questions = [
    "How many products are in each category?",
    "Show me all orders placed by customers.",
    "Which products have the highest prices?",
    "How much money has each customer spent?",
    "Show me the products included in each order."
]

for question in questions:
    print("\n"+"="*60)
    print("QUESTION:",question)
    print("="*60)
    
    results = retrieve_context(question)
    
    for i,document in enumerate(results['documents'][0]):
        print(f"\n--- Result {i+1} ---")
        print(document)