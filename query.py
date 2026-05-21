from sentence_transformers import SentenceTransformer
import psycopg2

# Load embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    local_files_only=True
)

# Connect PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="vectordb",
    user="dev",
    password="welcome"
)

cursor = conn.cursor()

query = "dark futuristic action game"

# Convert query into vector
query_embedding = model.encode(
    query
).tolist()

# Semantic similarity search
cursor.execute(
    """
    SELECT content,
           embedding <=> %s::vector AS distance
    FROM documents
    ORDER BY distance
    LIMIT 2;
    """,
    (query_embedding,)
)

results = cursor.fetchall()

print("\nResults:\n")

for row in results:
    print(row)

cursor.close()
conn.close()