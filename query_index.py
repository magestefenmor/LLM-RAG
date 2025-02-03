#from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import StorageContext, load_index_from_storage
#from transformers import pipeline


#Charger le modèle de summarization
#summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

#def generate_summary(text):
    #"""Génère un résumé court d'un texte donné."""
    #if len(text) < 100:  # Si le texte est court, inutile de le résumer
        #return text

    #summary = summarizer(text[:1024], max_length=100, min_length=30, do_sample=False)
    #return summary[0]["summary_text"]


# Fonction pour charger l'index et l'interroger
def query_index(question):
    # Charger l'embedding
    embedding = HuggingFaceEmbedding(model_name="all-MiniLM-L6-v2")

    # Charger l'index depuis le stockage
    storage_context = StorageContext.from_defaults(persist_dir="Save/index_data")
    index = load_index_from_storage(storage_context, embed_model=embedding)

    # Créer un retriever
    retriever = index.as_retriever()

    # Récupérer les documents pertinents
    retrieved_docs = retriever.retrieve(question)
    
    #un résumé à chaque document
    #for doc in retrieved_docs:
        #doc.metadata["summary"] = generate_summary(doc.text)

    # Retourner les documents pertinents
    return retrieved_docs

# Test (exécuter avec "python query_index.py")
if __name__ == "__main__":
    query = input("🔍 Pose ta question : ")
    results = query_index(query)

    for doc in results:
        print(f"\n📄 {doc.text[:200]}...")
        print(f"🔗 {doc.metadata}")

