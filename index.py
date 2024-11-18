import feedparser
from bs4 import BeautifulSoup
import requests
import json
import os
import time
from queue import Queue
from threading import Thread
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# Configuration Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNELS_INTERESTS = {
    "-1002319220599": ["technologie", "science", "Bitcoin", "innovation"],
    "-1001234567890": ["politique", "économie", "climat", "santé"],
}

# Liste des flux RSS
RSS_FEEDS = [
    "https://news.google.com/rss",
    "https://rss.cnn.com/rss/cnn_topstories.rss",
    "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"
]

# Fichier pour stocker les liens des news déjà affichées
STORAGE_FILE = "seen_news.json"

# Queue pour gérer les messages à envoyer
message_queue = Queue()

# Fonction pour charger les liens déjà affichés
def load_seen_links():
    try:
        if os.path.exists(STORAGE_FILE):
            with open(STORAGE_FILE, "r") as f:
                return json.load(f)
    except (json.JSONDecodeError, ValueError):
        print("⚠️ [WARNING] Fichier JSON corrompu. Réinitialisation...")
        return {}
    return {}

# Fonction pour sauvegarder les liens déjà affichés
def save_seen_links(seen_links):
    with open(STORAGE_FILE, "w") as f:
        json.dump(seen_links, f)

# Fonction pour récupérer les news depuis un flux RSS
def fetch_news(feed_url, seen_links):
    feed = feedparser.parse(feed_url)
    new_news = []

    # Si le flux n'a pas d'historique, créer une liste vide
    if feed_url not in seen_links:
        seen_links[feed_url] = []

    for entry in feed.entries:
        link = entry.link if 'link' in entry else None

        # Ignorer les actualités déjà affichées pour ce flux
        if link and link in seen_links[feed_url]:
            continue

        # Récupération des informations clés
        title = entry.title if 'title' in entry else 'Titre non disponible'
        published_date = entry.published if 'published' in entry else 'Date non disponible'
        raw_summary = entry.summary if 'summary' in entry else 'Résumé non disponible'

        # Nettoyage du résumé en supprimant les balises HTML
        summary = BeautifulSoup(raw_summary, "html.parser").get_text()

        # Ajouter les nouvelles actualités à la liste
        new_news.append({
            "title": title,
            "published_date": published_date,
            "summary": summary,
            "link": link,
        })

        # Ajouter le lien au set de liens déjà vus pour ce flux
        if link:
            seen_links[feed_url].append(link)

    return new_news

# Fonction pour envoyer un message à Telegram
def send_telegram_message(chat_id, message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        print(f"✅ [INFO] Message envoyé avec succès au channel {chat_id}.")
    except requests.exceptions.RequestException as e:
        print(f"❌ [ERREUR] Échec de l'envoi au channel {chat_id} : {e}")

# Fonction pour traiter les messages dans la queue
def process_message_queue():
    while True:
        chat_id, message = message_queue.get()
        send_telegram_message(chat_id, message)
        message_queue.task_done()
        time.sleep(1)  # Pause entre les requêtes pour éviter les erreurs 429

# Fonction pour envoyer les actualités pertinentes au channel Telegram
def send_news_to_channels(news_list):
    for chat_id, interests in CHANNELS_INTERESTS.items():
        # Filtrer les actualités selon les mots-clés d'intérêt
        relevant_news = [
            news for news in news_list
            if any(keyword.lower() in (news["title"] + news["summary"]).lower() for keyword in interests)
        ]

        # Envoyer uniquement les actualités pertinentes
        for news in relevant_news:
            message = (
                f"📰 *Nouvelle Actualité*\n\n"
                f"*{news['title']}*\n\n"
                f"{news['summary']}\n\n"
                f"🔗 [Lire l'article]({news['link']})"
            )

            print(f"📤 [INFO] Ajout à la queue : {news['title']}")
            message_queue.put((chat_id, message))

# Tâche principale
def main():
    # Démarrage du thread pour traiter la queue
    worker_thread = Thread(target=process_message_queue, daemon=True)
    worker_thread.start()

    seen_links = load_seen_links()

    while True:
        print("🔍 [INFO] Vérification des nouvelles actualités...")
        all_new_news = []

        # Parcourir tous les flux RSS
        for feed_url in RSS_FEEDS:
            new_news = fetch_news(feed_url, seen_links)
            all_new_news.extend(new_news)

        if all_new_news:
            print(f"📑 [INFO] {len(all_new_news)} nouvelles actualités trouvées.")
            send_news_to_channels(all_new_news)
        else:
            print("ℹ️ [INFO] Aucune nouvelle actualité.")

        save_seen_links(seen_links)
        time.sleep(15 * 60)  # Vérifie les actualités toutes les 15 minutes

# Exécution
if __name__ == "__main__":
    main()
