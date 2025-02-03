import chainlit as cl
from query_index import query_index

@cl.on_chat_start
async def start():
    """Message d'accueil avec une image"""
    await cl.Message(
        content="![Chatbot](https://cdn-icons-png.flaticon.com/512/4712/4712035.png)\n\n"
                "# 🤖 Chatbot RAG avec LlamaIndex\n"
                "Bienvenue sur mon chatbot basé sur la recherche sémantique"
    ).send()



@cl.on_message
async def main(message: cl.Message):
    query = message.content  #Extraire le texte de l'utilisateur
    retrieved_docs = query_index(query)  # 🔹 Récupérer les documents pertinents

    if not retrieved_docs:
        await cl.Message(content="**Aucun document pertinent trouvé.** 😕").send()
        return

    await cl.Message(content="**🔎 Voici les résultats les plus pertinents :**").send()
    
    for doc in retrieved_docs:
        title = doc.metadata.get("titre", "Article sans titre")
        url = doc.metadata.get("url", "#")  # Si l'URL est absente, éviter un lien cassé
        date = doc.metadata.get("date", "Date inconnue")
        content_snippet = doc.text[:200] + "..."

        # 🔹 Construire un message avec Markdown (sans HTML)
        message_content = f"""
        **📄 {title}**
        📅 **Date :** {date}  
        📖 **Aperçu. :** {content_snippet}  
        🔗 **[Lire l'article]({url})**
        """

        await cl.Message(content=message_content).send()
