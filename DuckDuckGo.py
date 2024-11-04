import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLineEdit, QToolBar, QAction, QFileDialog, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window settings
        self.setWindowTitle("DuckDuckGo Browser - Chrome Inspired")
        self.setGeometry(100, 100, 1200, 800)

        # Mode control: dark or light mode
        self.is_dark_mode = False

        # Initialize layout and tabs
        self.layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)

        # Add tabs to layout
        self.layout.addWidget(self.tabs)

        # Set the main layout
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Toolbar with navigation and bookmarks
        self.toolbar = QToolBar("Navigation")
        self.addToolBar(self.toolbar)

        # Navigation Buttons with Chrome-style icons
        self.add_navigation_actions()

        # URL bar with Chrome-style design
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_url)
        self.url_bar.setFixedHeight(30)
        self.url_bar.setStyleSheet("border-radius: 15px; background-color: #f0f0f0; padding: 0 8px;")
        self.toolbar.addWidget(self.url_bar)

        # Mode switcher action (Dark/Light Mode)
        self.mode_action = QAction("🌞", self)
        self.mode_action.triggered.connect(self.toggle_mode)
        self.toolbar.addAction(self.mode_action)

        # Add "About" section to toolbar
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        self.toolbar.addAction(about_action)

        # Add a new tab with the default search engine
        self.add_new_tab(QUrl("https://start.duckduckgo.com"))

        # Apply default light mode
        self.set_light_mode()

    def add_navigation_actions(self):
        # Back button
        back_btn = QAction("⟲", self)
        back_btn.triggered.connect(self.go_back)
        self.toolbar.addAction(back_btn)

        # Forward button
        forward_btn = QAction("⟳", self)
        forward_btn.triggered.connect(self.go_forward)
        self.toolbar.addAction(forward_btn)

        # Reload button
        reload_btn = QAction("⭮", self)
        reload_btn.triggered.connect(self.reload_page)
        self.toolbar.addAction(reload_btn)

        # Home button (loads default search engine)
        home_btn = QAction("🏠", self)
        home_btn.triggered.connect(lambda: self.tabs.currentWidget().setUrl(QUrl("https://start.duckduckgo.com")))
        self.toolbar.addAction(home_btn)

        # Add a "New Tab" button with Ctrl+T shortcut
        new_tab_action = QAction("➕ New Tab", self)
        new_tab_action.triggered.connect(self.new_tab)
        new_tab_action.setShortcut("Ctrl+T")
        self.toolbar.addAction(new_tab_action)

    def set_light_mode(self):
        light_mode_style = """
            QMainWindow { background-color: #f5f5f5; }
            QTabWidget::pane { background: #ffffff; }
            QTabBar::tab { background: #e0e0e0; color: black; padding: 8px; margin: 1px; }
            QTabBar::tab:selected { background: #ffffff; color: black; }
            QLineEdit { background-color: #f0f0f0; color: black; }
            QToolBar { background-color: #f5f5f5; padding: 5px; }
        """
        self.setStyleSheet(light_mode_style)
        self.mode_action.setText("🌞")  # Light mode icon

    def set_dark_mode(self):
        dark_mode_style = """
            QMainWindow { background-color: #303030; }
            QTabWidget::pane { background: #202020; }
            QTabBar::tab { background: #505050; color: white; padding: 8px; margin: 1px; }
            QTabBar::tab:selected { background: #404040; color: white; }
            QLineEdit { background-color: #606060; color: white; }
            QToolBar { background-color: #303030; padding: 5px; }
        """
        self.setStyleSheet(dark_mode_style)
        self.mode_action.setText("🌜")  # Dark mode icon

    def toggle_mode(self):
        if self.is_dark_mode:
            self.set_light_mode()
            self.is_dark_mode = False
        else:
            self.set_dark_mode()
            self.is_dark_mode = True

    def add_new_tab(self, qurl=None):
        browser = QWebEngineView()
        browser.setUrl(qurl if qurl else QUrl("https://start.duckduckgo.com"))

        # Enable persistent cookies and session storage
        browser.page().profile().setPersistentCookiesPolicy(QWebEngineProfile.AllowPersistentCookies)
        browser.page().profile().downloadRequested.connect(self.download_requested)

        # Update URL when page changes
        browser.urlChanged.connect(lambda qurl: self.url_bar.setText(qurl.toString()))

        # Add a new tab
        i = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(i)

    def load_url(self):
        url = self.url_bar.text()
        if "http" not in url:
            url = "https://start.duckduckgo.com/?q=" + url
        self.tabs.currentWidget().setUrl(QUrl(url))

    def go_back(self):
        self.tabs.currentWidget().back()

    def go_forward(self):
        self.tabs.currentWidget().forward()

    def reload_page(self):
        self.tabs.currentWidget().reload()

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def show_about(self):
        about_dialog = QMessageBox()
        about_dialog.setWindowTitle("About")
        about_dialog.setText("DuckDuckGo Browser - Chrome Inspired\nA custom browser using PyQt5 and QtWebEngine.")
        about_dialog.exec_()

    def download_requested(self, download):
        # Open file dialog to choose where to save the file
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", download.path())
        if file_path:
            download.setPath(file_path)
            download.accept()

    def new_tab(self):
        self.add_new_tab(QUrl("https://start.duckduckgo.com"))

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())
