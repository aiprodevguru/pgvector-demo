from sentence_transformers import SentenceTransformer
import psycopg2

# Load local embedding model
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

documents = [
    "Cyberpunk futuristic racing game",
    "Fantasy RPG with dragons",
    "Zombie survival horror game",
    "Space shooter with lasers"
]

for doc in documents:

    # Create embedding
    embedding = model.encode(
        doc
    ).tolist()

    # Insert into database
    cursor.execute(
        """
        INSERT INTO documents
        (content, embedding)
        VALUES (%s, %s)
        """,
        (doc, embedding)
    )

conn.commit()

cursor.close()
conn.close()

print("Documents inserted")