import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QTabWidget,
    QProgressBar, QMessageBox, QFrame, QScrollArea
)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QColor
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from modules import username_hunter, email_breach, image_search, darkweb_scanner, geo_locator, social_scraper, phone_search
import asyncio

class SearchWorker(QThread):
    progress = pyqtSignal(int)
    result = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, search_data):
        super().__init__()
        self.search_data = search_data

    def run(self):
        try:
            results = {}
            steps = [
                ('Username Hunter', username_hunter.run, 'username'),
                ('Email Breach', email_breach.run, 'email'),
                ('Phone Search', phone_search.run, 'phone'),
                ('Image Search', image_search.run, 'name'),
                ('Dark Web', darkweb_scanner.run, 'email'),
                ('Geo Locator', geo_locator.run, 'name'),
                ('Social Scraper', social_scraper.run, 'username'),
            ]
            total = sum(1 for _, _, key in steps if self.search_data.get(key))
            if total == 0:
                self.error.emit("No search parameters provided")
                return
            done = 0
            for label, func, key in steps:
                if self.search_data.get(key):
                    try:
                        if label == 'Social Scraper':
                            # Create event loop for async functions
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            results[label] = loop.run_until_complete(func(self.search_data))
                            loop.close()
                        else:
                            results[label] = func(self.search_data)
                        done += 1
                        self.progress.emit(int(done / total * 100))
                    except Exception as e:
                        results[label] = f"Error: {str(e)}"
                        done += 1
                        self.progress.emit(int(done / total * 100))
            self.result.emit(results)
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.progress.emit(100)  # Ensure progress bar reaches 100%

class PersonaXApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PersonaX - Advanced OSINT Tool')
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                background-color: #2d2d2d;
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton {
                padding: 10px 20px;
                background-color: #007acc;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0098ff;
            }
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                font-size: 14px;
            }
            QTabWidget::pane {
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                background-color: #2d2d2d;
            }
            QTabBar::tab {
                background-color: #2d2d2d;
                color: #ffffff;
                padding: 8px 16px;
                border: 2px solid #3d3d3d;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #007acc;
            }
            QProgressBar {
                border: 2px solid #3d3d3d;
                border-radius: 4px;
                text-align: center;
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QProgressBar::chunk {
                background-color: #007acc;
            }
        """)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Title
        title = QLabel('PersonaX')
        title.setStyleSheet('font-size: 32px; font-weight: bold; color: #007acc;')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Input fields
        input_frame = QFrame()
        input_frame.setStyleSheet('background-color: #2d2d2d; border-radius: 8px; padding: 20px;')
        input_layout = QVBoxLayout(input_frame)

        # Name input
        name_layout = QHBoxLayout()
        name_label = QLabel('Full Name:')
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Enter full name')
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        input_layout.addLayout(name_layout)

        # Email input
        email_layout = QHBoxLayout()
        email_label = QLabel('Email:')
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Enter email address')
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)
        input_layout.addLayout(email_layout)

        # Phone input
        phone_layout = QHBoxLayout()
        phone_label = QLabel('Phone:')
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText('Enter phone number')
        phone_layout.addWidget(phone_label)
        phone_layout.addWidget(self.phone_input)
        input_layout.addLayout(phone_layout)

        # Username input
        username_layout = QHBoxLayout()
        username_label = QLabel('Username:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Enter expected username')
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        input_layout.addLayout(username_layout)

        # Search button
        self.search_button = QPushButton('Start Investigation')
        self.search_button.clicked.connect(self.start_search)
        input_layout.addWidget(self.search_button)

        layout.addWidget(input_frame)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Results tabs
        self.tabs = QTabWidget()
        
        # Create tabs for different types of results
        self.result_tabs = {
            'Summary': QTextEdit(),
            'Usernames': QTextEdit(),
            'Social Media': QTextEdit(),
            'Email Leaks': QTextEdit(),
            'Images': QTextEdit(),
            'Dark Web': QTextEdit(),
            'Phone': QTextEdit()
        }

        for tab_name, widget in self.result_tabs.items():
            widget.setReadOnly(True)
            self.tabs.addTab(widget, tab_name)

        layout.addWidget(self.tabs)

    def start_search(self):
        # Get input values
        search_data = {
            'name': self.name_input.text(),
            'email': self.email_input.text(),
            'phone': self.phone_input.text(),
            'username': self.username_input.text()
        }

        # Validate input
        if not any(search_data.values()):
            QMessageBox.warning(self, 'Input Error', 'Please enter at least one search parameter.')
            return

        # Clear previous results
        for widget in self.result_tabs.values():
            widget.clear()

        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        # Disable search button
        self.search_button.setEnabled(False)

        # Create and start worker thread
        self.worker = SearchWorker(search_data)
        self.worker.progress.connect(self.update_progress)
        self.worker.result.connect(self.display_results)
        self.worker.error.connect(self.show_error)
        self.worker.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def display_results(self, results):
        try:
            # Clear all tabs
            for tab in self.result_tabs.values():
                tab.clear()
            
            # Display results in appropriate tabs
            if 'Username Hunter' in results:
                username_text = "Username Search Results:\n\n"
                if isinstance(results['Username Hunter'], dict):
                    for site, status in results['Username Hunter'].items():
                        username_text += f"{site}: {status}\n"
                else:
                    username_text += str(results['Username Hunter'])
                self.result_tabs['Usernames'].setText(username_text)
            
            if 'Email Breach' in results:
                email_text = "Email Breach Results:\n\n"
                if isinstance(results['Email Breach'], dict):
                    for source, data in results['Email Breach'].items():
                        email_text += f"{source}:\n"
                        if isinstance(data, dict):
                            for key, value in data.items():
                                email_text += f"  {key}: {value}\n"
                        else:
                            email_text += f"  {data}\n"
                else:
                    email_text += str(results['Email Breach'])
                self.result_tabs['Email Leaks'].setText(email_text)
            
            if 'Phone Search' in results:
                phone_text = "Phone Search Results:\n\n"
                if isinstance(results['Phone Search'], dict):
                    for source, data in results['Phone Search'].items():
                        phone_text += f"{source}:\n"
                        if isinstance(data, dict):
                            for key, value in data.items():
                                phone_text += f"  {key}: {value}\n"
                        else:
                            phone_text += f"  {data}\n"
                else:
                    phone_text += str(results['Phone Search'])
                self.result_tabs['Phone'].setText(phone_text)
            
            if 'Image Search' in results:
                image_text = "Image Search Results:\n\n"
                if isinstance(results['Image Search'], dict):
                    for source, data in results['Image Search'].items():
                        image_text += f"{source}:\n"
                        if isinstance(data, dict):
                            for key, value in data.items():
                                image_text += f"  {key}: {value}\n"
                        else:
                            image_text += f"  {data}\n"
                else:
                    image_text += str(results['Image Search'])
                self.result_tabs['Images'].setText(image_text)
            
            if 'Dark Web' in results:
                darkweb_text = "Dark Web Results:\n\n"
                if isinstance(results['Dark Web'], dict):
                    for source, data in results['Dark Web'].items():
                        darkweb_text += f"{source}:\n"
                        if isinstance(data, dict):
                            for key, value in data.items():
                                darkweb_text += f"  {key}: {value}\n"
                        else:
                            darkweb_text += f"  {data}\n"
                else:
                    darkweb_text += str(results['Dark Web'])
                self.result_tabs['Dark Web'].setText(darkweb_text)
            
            if 'Social Scraper' in results:
                social_text = "Social Media Results:\n\n"
                if isinstance(results['Social Scraper'], dict):
                    for platform in results['Social Scraper'].get('platforms', []):
                        social_text += f"=== {platform['platform']} ===\n"
                        if platform['status'] == 'Error':
                            social_text += f"Error: {platform['message']}\n"
                        else:
                            profile = platform.get('profile', {})
                            social_text += f"Profile:\n"
                            social_text += f"  Name: {profile.get('name', 'Unknown')}\n"
                            social_text += f"  Description: {profile.get('description', 'No description')}\n"
                            social_text += f"  Location: {profile.get('location', 'Unknown')}\n"
                            social_text += f"  Followers: {profile.get('followers', '0')}\n"
                            social_text += f"  Following: {profile.get('following', '0')}\n\n"
                            
                            posts = platform.get('posts', [])
                            if posts:
                                social_text += f"Recent Posts:\n"
                                for post in posts:
                                    social_text += f"  - {post.get('text', 'No content')}\n"
                                    social_text += f"    Date: {post.get('date', 'Unknown')}\n"
                                    social_text += f"    Likes: {post.get('likes', '0')}\n"
                        social_text += "\n"
                else:
                    social_text += str(results['Social Scraper'])
                self.result_tabs['Social Media'].setText(social_text)

            # Create summary
            summary = f"Investigation completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            summary += f"Parameters searched:\n"
            summary += f"- Name: {self.name_input.text() or 'Not provided'}\n"
            summary += f"- Email: {self.email_input.text() or 'Not provided'}\n"
            summary += f"- Phone: {self.phone_input.text() or 'Not provided'}\n"
            summary += f"- Username: {self.username_input.text() or 'Not provided'}\n\n"
            summary += f"Results found:\n"
            
            if 'Username Hunter' in results:
                summary += f"- Username matches: {results['Username Hunter'].get('found_count', 0)}\n"
            if 'Email Breach' in results:
                summary += f"- Email leaks: {results['Email Breach'].get('total_links', 0)}\n"
            if 'Phone Search' in results:
                if isinstance(results['Phone Search'], dict):
                    summary += f"- Phone number matches: {len(results['Phone Search'].get('results', []))}\n"
                else:
                    summary += f"- Phone search error: {results['Phone Search']}\n"
            if 'Social Scraper' in results:
                if isinstance(results['Social Scraper'], dict):
                    summary += f"- Social media profiles found: {len(results['Social Scraper'].get('platforms', []))}\n"
                else:
                    summary += f"- Social media search error: {results['Social Scraper']}\n"
            
            self.result_tabs['Summary'].setText(summary)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error displaying results: {str(e)}")

    def show_error(self, error_msg):
        QMessageBox.critical(self, 'Error', f'An error occurred: {error_msg}')

def main():
    app = QApplication(sys.argv)
    ex = PersonaXApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()