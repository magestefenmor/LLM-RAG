import pandas as pd
import json


data = pd.read_csv("data.csv")


def chunk_text(texte, taille_max=500):
    # Découpe le texte en blocs tout en gardant les phrases intactes
    phrases = texte.split('. ')
    chunks = []
    chunk = ""
    for phrase in phrases:
        if len(chunk) + len(phrase) <= taille_max:
            chunk += phrase + '. '
        else:
            chunks.append(chunk.strip())
            chunk = phrase + '. '
    if chunk:
        chunks.append(chunk.strip())
    return chunks



data['chunks'] = data['Texte_index'].apply(lambda x: chunk_text(x))


data['metadata'] = data.apply(lambda row: {'titre': row['titre'], 'date': row['Date'], 'url': row['Lien']}, axis=1)


# Préparer les données pour stockage
documents = []
for _, row in data.iterrows():
    for chunk in row['chunks']:
        documents.append({
            'content': chunk,
            'metadata': row['metadata']
        })

# Sauvegarder en JSON
with open('documents.json', 'w', encoding='utf-8') as f:
    json.dump(documents, f, ensure_ascii=False, indent=4)

print("Les documents ont été sauvegardés dans 'documents.json'.")