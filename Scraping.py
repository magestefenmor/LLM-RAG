import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv

# Fonction pour extraire les articles d'une page donnée
def extract_articles(url):
    articles = []  # Liste pour stocker les articles
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifie les erreurs de requête
        html = response.content
        soup = BeautifulSoup(html, "html.parser")

        # Récupérer toutes les tables contenant des articles
        tables = soup.find_all("table", class_="ts")
        
        # Boucle à travers chaque table
        for table in tables:
            # Récupérer les lignes des articles
            rows = table.find_all("td", class_="top news-tbn")
            for row in rows:
                # Extraire le lien, le titre et la date
                link_tag = row.find("a")
                #title = link_tag.text.strip() if link_tag else "Titre indisponible"
                relative_link = link_tag["href"] if link_tag else None
                link = f"https://www.agenceecofin.com{relative_link}" if relative_link else None

                # Trouver la date dans le conteneur suivant
                date_span = row.find_next("span", class_="f nsa")
                date_text = date_span.text.strip() if date_span else None

                # Convertir la date en objet datetime
                article_date = None
                if date_text:
                    try:
                        article_date = datetime.strptime(date_text, "%d/%m/%Y")
                    except ValueError:
                        print(f"Erreur de format de date pour l'article: {title}")
                        article_date = None

                # Récupérer le texte de l'article
                article_text = ""
                if link:
                    try:
                        article_response = requests.get(link)
                        article_response.raise_for_status()
                        article_html = article_response.content
                        article_soup = BeautifulSoup(article_html, "html.parser")
                        
                        # Extraire le texte à partir de la structure fournie
                        text_div = article_soup.find("div", class_="itemIntroText")
                        if text_div:
                            paragraphs = text_div.find_all("p")
                            article_text = "\n".join(p.get_text(strip=True) for p in paragraphs)

                    except requests.RequestException as e:
                        print(f"Erreur lors de la récupération de l'article {link}: {e}")
                        article_text = "Texte indisponible"
                else:
                    article_text = "Lien indisponible"

                # Ajouter les détails de l'article à la liste
                articles.append({
                    "link": link,
                    "date": article_date,
                    "text": article_text
                })

        # Trouver le lien vers la page suivante
        next_page_link = soup.find("a", title="Suivant")
        next_page_url = next_page_link["href"] if next_page_link else None
        if next_page_url and next_page_url.startswith('/'):
            next_page_url = f"https://www.agenceecofin.com{next_page_url}"

        return articles, next_page_url
    
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération de {url}: {e}")
        return articles, None

# URL de la première page
url = "https://www.agenceecofin.com/a-la-une/recherche-article?filterTitle=&submit.x=0&submit.y=0&filterTousLesFils=Tous&filterCategories=Sous-rubrique&filterDateFrom=&filterDateTo=&option=com_dmk2articlesfilter&view=articles&filterFrench=French&Itemid=269&userSearch=1&layout=#dmk2articlesfilter_results"
all_articles = []
stop_date = datetime.now() - timedelta(days=7)  # Date d'arrêt dynamique pour 7 jours en arrière

while True:
    print(f"Extraction des articles à partir de : {url}")
    articles, next_page = extract_articles(url)

    # Ajouter les articles extraits à la liste totale
    if articles:
        all_articles.extend(articles)

        # Vérifier si la date de l'article le plus récent est inférieure à stop_date
        # On vérifie que article_date n'est pas None
        if articles[-1]["date"] and articles[-1]["date"] < stop_date:
            print("Un article a été trouvé avant la date limite de 7 jours, arrêt de l'extraction.")
            break

    # Aller à la page suivante si disponible
    if next_page:
        url = next_page
    else:
        break

# Afficher tous les articles récupérés
print("\nTous les articles extraits :")
if all_articles:
    for article in all_articles:
        print(f"Lien: {article['link']}, Date: {article['date']}, Texte: {article['text'][:100]}...")  # Affiche les 100 premiers caractères du texte
else:
    print("Aucun article trouvé.")

# Enregistrer les articles dans un fichier CSV
with open("articles.csv", mode="w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Lien", "Date", "Texte"])  # Écrire l'en-tête
    for article in all_articles:
        writer.writerow([article['link'], article['date'].strftime('%d/%m/%Y') if article['date'] else '', article['text']])

print("\nTous les articles extraits et enregistrés dans 'articles.csv'.")