from app.services.openai_service import create_embedding

embedding = create_embedding(
    "Merhaba ben Company RAG Assistant"
)

print(len(embedding))
print(embedding[:10])
