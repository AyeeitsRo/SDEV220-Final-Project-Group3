import feedparser
import requests
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QStackedWidget, QPushButton, QVBoxLayout, QTextEdit
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QTimer

class NewsFeed(QWidget):
    def __init__(self, feed_url):
        super().__init__()

        self.feed_url = feed_url
        self.news_data = self.fetch_news()
        self.current_index = 0

        # Layout for news feed
        self.setFixedWidth(500)
        self.layout = QHBoxLayout(self)

        # Left arrow button
        self.left_button = QPushButton("←")
        self.left_button.setStyleSheet("border: 2px; background-color: #a00000; border-color: #ff5555; height: 30px; width: 30px; border-radius: 15px; padding: 2px, 2px, 2px, 2px;")
        self.left_button.clicked.connect(self.previous_news)
        self.layout.addWidget(self.left_button)

        # News container (Stacked Widget)
        self.news_container = QStackedWidget()
        self.news_container.setStyleSheet("border: 5px; border-color: #fc0202; border-style: groove; background-color: #6a0000")
        self.layout.addWidget(self.news_container)

        # Right arrow button
        self.right_button = QPushButton("→")
        self.right_button.setStyleSheet("border: 2px; background-color: #a00000; border-color: #ff5555; height: 30px; width: 30px; border-radius: 15px; padding: 2px, 2px, 2px, 2px;")
        self.right_button.clicked.connect(self.next_news)
        self.layout.addWidget(self.right_button)

        # Load news into stacked widget
        self.load_news()

        # Timer for auto-scroll
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_news)
        self.timer.start(10000)  # Auto-scroll every 10 seconds

    def fetch_news(self):
        feed = feedparser.parse(self.feed_url)
        news_list = []

        for entry in feed.entries[:5]:  # Limit to 5 articles
            image_url = None
        
            # Extract image URL from media content if available
            if "media_content" in entry and len(entry.media_content) > 0:
                image_url = entry.media_content[0]["url"]
            elif "links" in entry:
                for link in entry.links:
                    if link.get("rel") == "enclosure" and "image" in link.get("type", ""):
                        image_url = link["href"]
        
            news_list.append({
                "title": entry.title,
                "link": entry.link,
                "description": entry.get("description", ""),  # Get description text
                "image": image_url
            })
    
        return news_list

    def load_news(self):
        for news in self.news_data:
            news_layout = QVBoxLayout()
            news_widget = QWidget()
            news_widget.setStyleSheet("border: none;")
            news_widget.setLayout(news_layout)

            # Title (Clickable)
            title_label = QLabel(f'<a href="{news["link"]}">{news["title"]}</a>')
            title_label.setOpenExternalLinks(True)
            title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title_label.setStyleSheet("border: none;")
            news_layout.addWidget(title_label)

            # Image (if available)
            if news["image"]:
                image_label = QLabel()
                pixmap = QPixmap()
                try:
                    response = requests.get(news["image"], timeout=5)
                    response.raise_for_status()  # Check for errors
                    pixmap.loadFromData(response.content)
                    pixmap = pixmap.scaled(180, 100, Qt.AspectRatioMode.KeepAspectRatio)  # Resize
                    image_label.setPixmap(pixmap)
                    image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    image_label.setStyleSheet("border: none;")
                    news_layout.addWidget(image_label)
                except requests.exceptions.RequestException:
                    print(f"Failed to load image: {news['image']}")  # Debugging

            # Description (Snippet)
            if news["description"]:
                description_label = QTextEdit()
                description_label.setText(news["description"])
                description_label.setReadOnly(True)
                description_label.setFixedHeight(60)  # Prevent it from expanding too much
                description_label.setStyleSheet("border: none; color: #ffffff;")
                news_layout.addWidget(description_label)

            # Add the complete widget to the stacked container
            self.news_container.addWidget(news_widget)

    def next_news(self):
        self.current_index = (self.current_index + 1) % len(self.news_data)
        self.news_container.setCurrentIndex(self.current_index)

    def previous_news(self):
        self.current_index = (self.current_index - 1) % len(self.news_data)
        self.news_container.setCurrentIndex(self.current_index)
