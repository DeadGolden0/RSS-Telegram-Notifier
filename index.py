import feedparser
import pywhatkit as kit
import schedule
import time
from datetime import datetime

# Liste d'utilisateurs et leurs sujets d'intérêt
users = {
    "+12345678901": ["technologie", "science"],
    "+19876543210": ["sports", "politique"]
}

# Fonction pour vérifier les nouvelles annonces dans le flux RSS
def fetch_news(feed_url, keywords):
    feed = feedparser.parse(feed_url)
    news_to_send = []

    for entry in feed.entries:
        title = entry.title.lower()
        summary = entry.summary.lower()
        link = entry.link

        for keyword in keywords:
            if keyword.lower() in title or keyword.lower() in summary:
                news_to_send.append((title, summary, link))
                break  # Éviter les doublons si plusieurs mots-clés correspondent

    return news_to_send

# Fonction pour envoyer des messages via WhatsApp
def send_whatsapp_message(phone, news):
    for title, summary, link in news:
        message = f"📰 *Nouvelle Actualité*\n\n*{title}*\n\n{summary}\n\n🔗 {link}"
        # Envoie le message à l'utilisateur
        kit.sendwhatmsg_instantly(phone, message, wait_time=10, tab_close=True)

# Tâche principale
def check_and_notify():
    print(f"Vérification des news - {datetime.now()}")
    feed_url = "https://news.google.com/rss"

    for user, interests in users.items():
        news = fetch_news(feed_url, interests)
        if news:
            send_whatsapp_message(user, news)

# Planifier une vérification toutes les 15 minutes
schedule.every(15).minutes.do(check_and_notify)

print("Service de notifications WhatsApp RSS lancé...")

# Boucle d'écoute continue
while True:
    schedule.run_pending()
    time.sleep(1)
