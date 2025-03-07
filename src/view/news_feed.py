import feedparser
import requests
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QStackedWidget, QPushButton, QVBoxLayout, QTextEdit
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt, QTimer

class NewsFeed(QWidget):
    """
    **NewsFeed Class**
    
    **Class Purpose:**
    - Displays a scrolling news feed from an RSS source.
    - Fetches and updates news dynamically.
    - Allows users to manually scroll through news articles or let them rotate automatically.
    
    **Why This Class Exists:**
    - Provides users with the latest news relevant to the gaming cafe or community.
    - Reduces the need for manual updates by fetching content directly from an RSS feed.
    - Implements a visually appealing and interactive scrolling display.
    """
    
    def __init__(self, feed_url: str):
        """ Initializes the NewsFeed widget and fetches the latest news articles. """
        super().__init__()

        # Store Feed URL & Initialize Data
        self.feed_url = feed_url  # RSS feed URL
        self.news_data = self.fetch_news()  # Retrieve news articles
        self.current_index = 0  # Track currently displayed article

        # Create Layout & Set Fixed Width
        self.setFixedWidth(500)  # Define width to maintain UI consistency
        self.layout = QHBoxLayout(self)  # Main layout for the widget

        # Add Navigation Buttons
        self.left_button = QPushButton("←")  # Create left arrow button
        self.left_button.setStyleSheet("border: 2px; background-color: #a00000; border-color: #ff5555; height: 30px; width: 30px; border-radius: 15px; padding: 2px, 2px, 2px, 2px;")  # Style the button
        self.left_button.clicked.connect(self.previous_news)  # Connect button to previous_news method
        self.layout.addWidget(self.left_button)  # Add left button to layout

        # Create News Container
        self.news_container = QStackedWidget()  # Stacked widget to cycle through news
        self.news_container.setStyleSheet("border: 5px; border-color: #fc0202; border-style: groove; background-color: #6a0000")  # Style news container
        self.layout.addWidget(self.news_container)  # Add news container to layout

        # Add Right Navigation Button
        self.right_button = QPushButton("→")  # Create right arrow button
        self.right_button.setStyleSheet("border: 2px; background-color: #a00000; border-color: #ff5555; height: 30px; width: 30px; border-radius: 15px; padding: 2px, 2px, 2px, 2px;")  # Style the button
        self.right_button.clicked.connect(self.next_news)  # Connect button to next_news method
        self.layout.addWidget(self.right_button)  # Add right button to layout

        # Load News Data into UI
        self.load_news()  # Calls function to populate stacked widget

        # Implement Auto-Scroll Feature
        self.timer = QTimer(self)  # Create timer instance
        self.timer.timeout.connect(self.next_news)  # Connect timer to next_news function
        self.timer.start(10000)  # Set timer to switch news every 10 seconds


    def fetch_news(self):
        """
        **Fetches the latest news from the RSS feed and extracts relevant data.**
        
        **Why This Function Exists:**
        - Dynamically pulls news articles from the given RSS feed.
        - Extracts and formats article information into a structured dictionary.
        - Limits the number of articles displayed to ensure readability and performance.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Parse RSS Feed**
           - Uses `feedparser.parse()` to retrieve data from the RSS feed URL.
        
        2️⃣ **Step 2 - Initialize Empty News List**
           - Creates an empty list `news_list` to store extracted news articles.
        
        3️⃣ **Step 3 - Extract Article Data**
           - Iterates over the first 5 entries of the feed (to limit the number of articles displayed).
        
        4️⃣ **Step 4 - Extract Image URL (If Available)**
           - Checks for images in `media_content` or `links` within the article.
           - If an image exists, its URL is stored; otherwise, `image_url` remains `None`.
        
        5️⃣ **Step 5 - Store News Data in Dictionary**
           - Extracts the title, link, description, and image URL for each news entry.
           - Stores this data as a dictionary and appends it to `news_list`.
        
        6️⃣ **Step 6 - Return Extracted News Data**
           - Returns `news_list`, which contains formatted news articles.
        """
        
        # Step 1 - Parse RSS Feed
        feed = feedparser.parse(self.feed_url)  # Retrieve feed data
        news_list = []  # Step 2 - Initialize Empty News List

        # Step 3 - Extract Article Data
        for entry in feed.entries[:5]:  # Limit to first 5 articles
            image_url = None  # Default to None
        
            # Step 4 - Extract Image URL (If Available)
            if "media_content" in entry and len(entry.media_content) > 0:
                image_url = entry.media_content[0]["url"]  # Extract image from media_content
            elif "links" in entry:
                for link in entry.links:
                    if link.get("rel") == "enclosure" and "image" in link.get("type", ""):
                        image_url = link["href"]  # Extract image from links
        
            # Step 5 - Store News Data in Dictionary
            news_list.append({
                "title": entry.title,  # News title
                "link": entry.link,  # URL to full article
                "description": entry.get("description", ""),  # News description snippet
                "image": image_url  # Image URL (if available)
            })
    
        return news_list  # Step 6 - Return Extracted News Data

    def load_news(self):
        """
        **Loads and displays fetched news articles into the stacked widget.**
        
        **Why This Function Exists:**
        - Processes the fetched news data and formats it into a structured UI.
        - Ensures each article is visually separated and easy to read.
        - Allows easy navigation through the news stack using the left and right buttons.
        
        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Iterate Over Fetched News Articles**
           - Loops through `self.news_data`, which contains parsed news articles.
        
        2️⃣ **Step 2 - Create a Layout for Each News Item**
           - Initializes `QVBoxLayout()` for structuring article elements.
           - Creates a `QWidget()` container to hold each news article's details.
           
        3️⃣ **Step 3 - Create and Configure Title Label**
           - Sets the article's title as a clickable `QLabel` hyperlink.
           - Configures font, alignment, and removes borders.
        
        4️⃣ **Step 4 - Check and Load Image if Available**
           - If an image URL exists, fetches and processes the image.
           - Ensures error handling for failed image requests.
           - Resizes and aligns the image properly within the layout.
        
        5️⃣ **Step 5 - Add Article Description**
           - If available, adds a `QTextEdit` widget containing the article snippet.
           - Restricts height to prevent excessive expansion.
           
        6️⃣ **Step 6 - Add Formatted News Widget to Stacked Container**
           - Adds the structured news widget to `self.news_container`.
        """
        for news in self.news_data:
            # Step 1 - Create layout and widget for each news article
            news_layout = QVBoxLayout()
            news_widget = QWidget()
            news_widget.setStyleSheet("border: none;")
            news_widget.setLayout(news_layout)

            # Step 2 - Create a title label that is clickable
            title_label = QLabel(f'<a href="{news["link"]}">{news["title"]}</a>')
            title_label.setOpenExternalLinks(True)  # Enables hyperlink clicking
            title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))  # Set font style
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the title
            title_label.setStyleSheet("border: none;")  # Remove default label border
            news_layout.addWidget(title_label)  # Add title label to layout

            # Step 3 - Check if an image exists and process it
            if news["image"]:
                image_label = QLabel()
                pixmap = QPixmap()
                try:
                    response = requests.get(news["image"], timeout=5)  # Fetch image with timeout
                    response.raise_for_status()  # Check if request was successful
                    pixmap.loadFromData(response.content)  # Load image from fetched data
                    pixmap = pixmap.scaled(180, 100, Qt.AspectRatioMode.KeepAspectRatio)  # Resize image proportionally
                    image_label.setPixmap(pixmap)  # Set image to label
                    image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the image
                    image_label.setStyleSheet("border: none;")  # Remove any border
                    news_layout.addWidget(image_label)  # Add image to layout
                except requests.exceptions.RequestException:
                    print(f"Failed to load image: {news['image']}")  # Print error message if image fails to load

            # Step 4 - If a description exists, add it to the layout
            if news["description"]:
                description_label = QTextEdit()
                description_label.setText(news["description"])  # Set description text
                description_label.setReadOnly(True)  # Make text non-editable
                description_label.setFixedHeight(60)  # Limit height to avoid excessive expansion
                description_label.setStyleSheet("border: none; color: #ffffff;")  # Style text color and remove borders
                news_layout.addWidget(description_label)  # Add description to layout

            # Step 5 - Add formatted article to the stacked container
            self.news_container.addWidget(news_widget)

    def next_news(self):
        """
        **Advances to the next news article in the feed.**

        **Why This Function Exists:**
        - Provides navigation to cycle through news articles.
        - Ensures the news feed loops back to the first article when reaching the end.

        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Increment Current Index**
           - Increases `self.current_index` by 1 to move to the next news article.
           - Uses modulo (`% len(self.news_data)`) to wrap around to the first article if the end is reached.
        
        2️⃣ **Step 2 - Update Displayed News Article**
           - Updates the `QStackedWidget` to show the news article at `self.current_index`.
        """
        self.current_index = (self.current_index + 1) % len(self.news_data)  # Step 1: Increment and loop back if at the end
        self.news_container.setCurrentIndex(self.current_index)  # Step 2: Update displayed news article

    def previous_news(self):
        """
        **Moves to the previous news article in the feed.**

        **Why This Function Exists:**
        - Allows navigation backward through the news articles.
        - Ensures the news feed loops back to the last article when at the beginning.

        **Step-by-Step Explanation:**
        1️⃣ **Step 1 - Decrement Current Index**
           - Decreases `self.current_index` by 1 to move to the previous news article.
           - Uses modulo (`% len(self.news_data)`) to wrap around to the last article if at the beginning.
        
        2️⃣ **Step 2 - Update Displayed News Article**
           - Updates the `QStackedWidget` to show the news article at `self.current_index`.
        """
        self.current_index = (self.current_index - 1) % len(self.news_data)  # Step 1: Decrement and loop back if at the beginning
        self.news_container.setCurrentIndex(self.current_index)  # Step 2: Update displayed news article
