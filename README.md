 #  Système RAG avec Langchain, Llama et Chainlit

 ## Introduction

# 🤖 Chatbot RAG basé sur le Web Scraping et LlamaIndex  

Ce projet implémente un **système RAG (Retrieval-Augmented Generation)** permettant de répondre aux questions en s'appuyant sur des articles collectés via **Web Scraping**.  

### **🛠️ Comment fonctionne notre pipeline ?**  
Le projet est structuré en trois grandes étapes :  

1️⃣ **Collecte des données (Web Scraping) 🕸️**  
   - Extraction automatique d'articles via **BeautifulSoup4** et **requests**.  
   - Stockage des articles en format JSON pour traitement.  

2️⃣ **Traitement et Indexation des documents 📂**  
   - Nettoyage et prétraitement des textes.  
   - Génération d'embeddings avec **Hugging Face** (`all-MiniLM-L6-v2`).  
   - Indexation des documents avec **LlamaIndex** pour une recherche optimisée.  

3️⃣ **Recherche et génération de réponses 🤖**  
   - Recherche des documents les plus pertinents dans l’index (**retriever**).  
   - Génération de résumés avec **Hugging Face** (`facebook/bart-large-cnn`).  
   - Affichage des réponses via une interface **Chainlit**.  

---

### **💡 Technologies utilisées**
- **BeautifulSoup4** 🕸️ : Scraping et extraction d’articles.  
- **LlamaIndex** 🔗 : Indexation et recherche documentaire.  
- **Hugging Face** 🤗 : Génération d’embeddings et de résumés.  
- **Chainlit** 💬 : Interface interactive pour discuter avec le chatbot.  
- **Python** 🐍 : Langage principal du projet.  

Le projet permet d'interagir avec un **chatbot intelligent** qui répond aux questions en s’appuyant sur des documents collectés et indexés.  



Instructions d'Installation et d'Exécution
1. Création d'un environnement virtuel
Avec Conda

Assurez-vous d'abord que Conda est installé sur votre système. Ensuite, créez et activez un environnement virtuel avec la commande suivante :

 - conda create -n .venv python=3.11 -y && conda activate .venv

Avec Python (pour Linux/OS)

 - python3 -m venv /path/to/new_env && source /path/to/new_env/bin/activate

2. Installation des dépendances

Installez les packages Python nécessaires en exécutant :

 - pip install -r requirements.txt

3. Exécution du web scraping

Pour effectuer le web scraping, lancez le script suivant :

 - python Scraping.py

(Vous pouvez également utiliser le fichier article.csv si nécessaire.)

Ensuite, exécutez :

 - python Traitement.py

Finalement, exécutez :

 - python Stockage.py

4. Création des embeddings

Pour créer les embeddings et les stocker localement, utilisez la commande suivante :

 - python query_index.py

5. Exécution de l'interface utilisateur de l'application

Pour démarrer l'interface utilisateur, exécutez :

 - chainlit run apps.py -w








