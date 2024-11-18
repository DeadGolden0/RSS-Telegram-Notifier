## 🤖 RSS Telegram Notifier

Welcome to the **RSS Telegram Notifier** repository! This project is a Python-based application that monitors an RSS feed, filters news articles based on user-defined interests, and sends relevant updates to specified Telegram channels. It efficiently handles rate limits using a message queue to ensure smooth and reliable notifications.

> [!WARNING]
> **Excessive API Requests Can Lead to a Temporary or Permanent Ban of Your Telegram Bot**  
> Be mindful of the number of API requests your bot sends to Telegram. Sending too many requests in a short amount of time can trigger Telegram's anti-spam mechanisms, which may result in your bot being temporarily or permanently banned. This is particularly important if your bot monitors multiple RSS feeds or sends frequent updates to multiple channels. To mitigate this, the script uses a message queue with a delay between requests, but it is still recommended to monitor your bot's activity and avoid overwhelming the Telegram API.

## 🚀 Features

- Monitors RSS feeds for new articles.
- Filters articles based on keywords defined for each Telegram channel.
- Sends relevant articles to multiple Telegram channels.
- Handles Telegram rate limits with a message queue.
- Supports Markdown formatting for Telegram messages.

## 📋 Prerequisites

- VPS or dedicated server
- Python 3.10 or higher
- Telegram bot API token
- Access to the RSS feed you want to monitor

## ⚙️ Installation

```bash
git clone https://github.com/DeadGolden0/RSS-Telegram-Notifier
cd RSS-Telegram-Notifier
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## 📋 Configuration

### 1. Telegram Bot Setup
- Create a Telegram bot using [BotFather](https://core.telegram.org/bots#botfather).
- Note down the bot's API token.
- Add the bot to the desired Telegram channel(s) as an administrator.

> [!NOTE]
> **Why Telegram and not WhatsApp?**  
> Telegram is chosen for this project because it offers a simpler and more accessible integration for developers. With Telegram, you can create a bot in minutes using the [BotFather](https://core.telegram.org/bots#botfather) and get a dedicated API token for free. Additionally, Telegram bots do not require a phone number and have no fees for sending messages, unlike WhatsApp, which requires the use of the WhatsApp Business API, a phone number, and often incurs usage costs. Telegram's developer-friendly API and its focus on openness make it an excellent choice for projects like this.

### 2. Update Configuration

Rename the `.env.example` file to `.env` in the root directory and update it with your API keys and configuration variables:

```env
TELEGRAM_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```

Edit the `CHANNELS_INTERESTS` dictionary in the Python script to specify the channels and their respective interests:

```python
CHANNELS_INTERESTS = {
    "-1002319220599": ["technologie", "science", "Bitcoin", "innovation"],
    "-1001234567890": ["politique", "économie", "climat", "santé"],
}
```

### 3. (Optional) Customize Settings
- RSS Feed URL: Update the `feed_url` in the `main()` function if you want to monitor a different feed. Default is Google News RSS (https://news.google.com/rss).
- Check Frequency: Adjust the `time.sleep(15 * 60)` interval in seconds to control how often the feed is checked. Ex : `time.sleep(15 * 60)` = `15 minutes`

## 🖥️ Usage

### Running the Application
Run the script with:

```bash
python script.py
```

### Logs
- Success and error logs are displayed in the terminal with helpful emojis for clarity.
- Example log output:

```bash
🔍 [INFO] Vérification des nouvelles actualités...
📑 [INFO] 3 nouvelles actualités trouvées.
📤 [INFO] Ajout à la queue : Titre de l\'actualité
✅ [INFO] Message envoyé avec succès au channel -1002319220599.
```

### Clearing `seen_news.json`

If you want to resend news that has already been sent, you can clear the `seen_news.json` file. This will remove the record of previously sent links, allowing the script to treat all news as new.

To clear the file, follow these steps:

1. Stop the script if it is currently running.
2. Delete the `seen_news.json` file manually or use :
   ```bash
   rm seen_news.json
   ```
3. Restart the script:
   ```bash
   python script.py
   ```

> [!CAUTION]
> Clearing seen_news.json will result in all previously sent news being treated as new. Use this action carefully to avoid spamming your Telegram channel or violating Telegram's API rate limits.

## ⚠️ Disclaimer

This script is provided as-is for educational and learning purposes only. The author is not responsible for any issues, damages, bans, or other consequences that may arise from its use. By using this script, you acknowledge that you are solely responsible for its application and compliance with any relevant policies or terms of service, including Telegram's API usage guidelines. Use this script at your own risk.

 
## 🤝 Contributing

Your contributions make the open source community a fantastic place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ✉️ Contact

For any questions or suggestions, please feel free to contact me:

[![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/w92W7XR9Yg)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:deadgolden9122@gmail.com)
[![Steam](https://img.shields.io/badge/steam-%23000000.svg?style=for-the-badge&logo=steam&logoColor=white)](https://steamcommunity.com/id/DeAdGoLdEn/)

## 💖 Support Me

If you find this project helpful and would like to support my work, you can contribute through PayPal. Any support is greatly appreciated and helps me continue developing and maintaining the project.

[![PayPal](https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/DeadGolden0)