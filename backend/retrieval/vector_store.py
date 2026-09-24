import chromadb
from retrieval.schema_descriptions import schema_descriptions
from retrieval.example_queries import example_queries

# Creates chromaDb Object
def init_vector_store():
    chroma_client = chromadb.Client()

    collection = chroma_client.get_or_create_collection(name="my_collection")

    return collection

# Converts models into embeddings and example questions and sql output into embeddings.
def embed_schema():
    
    collection = init_vector_store()
    
    documents = []
    metadatas = []
    ids = []
    
    for table_name,table_info in schema_descriptions.items():
        description = table_info['description']
        
        columns = "\n".join(
            f"{column} : {column_description}"
            for column, column_description in table_info['columns'].items()
        )
        
        document = f"""
        Table : {table_name}
        
        Description : {description}
        
        Columns : {columns}
        """
        
        documents.append(document)
        
        ids.append(f"schema_{table_name}")
        
        metadatas.append({
            "type":"schema",
            "table":table_name
        })
        
    for index, example in enumerate(example_queries):
        document = f"""
    Question:
    {example["question"]}

    SQL:
    {example["sql"]}
    """

        documents.append(document)
        ids.append(f"example_{index}")
        metadatas.append({
            "type": "example_query"
        })

    collection.add(
        documents=documents,
        ids=ids,
        metadatas=metadatas
    )

    print(f"Added {len(documents)} documents to ChromaDB.")

# Extracts top 5 matching results from database by comparing 
def retrieve_context(question:str):
    collection = init_vector_store()
    
    results = collection.query(
        query_texts=[question],
        n_results=5
    )
    
    return results

# embed_schema()