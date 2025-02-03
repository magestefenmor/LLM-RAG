import pandas as pd
import re
import unicodedata


article = pd.read_csv("articles.csv")

article.isnull().sum()

def extraire_source_et_contenu(texte):
    """Extrait la source et le contenu à partir du texte."""
    # Utiliser re.split pour diviser le texte en deux parties
    parties = re.split(r' - ', texte, 1)  # Limite à 1 pour ne diviser qu'une fois
    if len(parties) == 2:
        source = parties[0].strip()  # Partie avant le tiret
        contenu = parties[1].strip()  # Texte après le tiret
        
        # Supprimer les parenthèses et leur contenu de la source
        #source = re.sub(r'\(.*?\)', '', source).strip()
        source = re.sub(r'^\((.*?)\)$', r'\1', source).strip()
    else:
        source = None
        contenu = texte.strip()  # Si aucun tiret n'est trouvé, tout le texte est mis dans contenu

    return source, contenu


def nettoyer_contenu(contenu):
    """Nettoie le contenu en supprimant les espaces inutiles, en corrigeant le format, et en supprimant le texte après la dernière occurrence de '.\n'."""
    
    # Trouver l'index de la dernière occurrence de '.\n'
    index_sequence = contenu.rfind('.\n')
    if index_sequence != -1:
        # Conserver le texte jusqu'à la dernière occurrence de '.\n'
        contenu = contenu[:index_sequence + 1].strip()  

    # Correction des formats spécifiques
    contenu = re.sub(r'(\d+)e([a-zA-ZéèêëÉÈÊË])', r'\1e \2', contenu)
    
    # Remplacer les sauts de ligne par des espaces
    contenu = re.sub(r'\n+', ' ', contenu)
    
    # Supprimer les espaces multiples
    contenu = re.sub(r'\s{2,}', ' ', contenu)
    
    # Supprimer les espaces en début et en fin
    contenu = contenu.strip()
    
    return contenu



article[['Source', 'Contenu']] = article['Texte'].apply(lambda x: pd.Series(extraire_source_et_contenu(x)))
article['Contenu'] = article['Contenu'].apply(nettoyer_contenu)


# Fonction pour extraire le titre
def extraire_titre(url):
    # Vérifier le format avec des nombres suivis de tirets
    match_nombres = re.search(r'actualites/\d+-\d+-(.*)', url)
    # Vérifier le format avec un titre simple
    #match_simple = re.search(r'actualites-(.*)', url)
    match_simple = re.search(r'actualites-[a-z]+/\d+-\d+-(.*)', url)
    
    if match_nombres:
        return match_nombres.group(1).replace('-', ' ').capitalize()  # Remplacer les tirets par des espaces
    elif match_simple:
        return match_simple.group(1).replace('-', ' ').capitalize()  # Titre simple
    return "Titre non trouvé."


article['titre'] = article['Lien'].apply(lambda x: extraire_titre(x))


def preprocess(text):
    # Convertir en minuscules
    text = text.lower()
    # Supprimer les espaces inutiles
    text = text.strip()
    return text


article['Texte_index'] = article['Contenu'].apply(lambda x: preprocess(x))


data = article[["Source", "titre", "Contenu", "Texte_index", "Date", "Lien"]]


data.to_csv("data.csv", index=False, encoding="utf-8")