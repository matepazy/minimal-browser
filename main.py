import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *

class Browser(QMainWindow):
    def __init__(self):
        super(Browser, self).__init__()
        self.setWindowTitle("Minimal Browser")

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.new_tab)
        self.tabs.currentChanged.connect(self.update_url_bar)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        self.tabs.setStyleSheet("""
            QTabWidget::pane { 
                border-top: 1px solid #C2C7CB; 
                background: #f0f0f0;
            }
            QTabBar::tab {
                background: #e0e0e0; 
                padding: 10px;
                margin-right: 2px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QTabBar::tab:selected {
                background: #ffffff; 
                font-weight: bold;
            }
        """)

        nav_bar = QToolBar("Navigation")
        nav_bar.setIconSize(QSize(20, 20))
        nav_bar.setStyleSheet("""
            QToolBar { 
                background: #f5f5f5; 
                padding: 5px; 
                border-bottom: 1px solid #ccc;
            }
            QToolButton { 
                margin: 5px;
                background-color: #ffffff;
                border-radius: 3px;
            }
            QToolButton:hover {
                background-color: #dcdcdc;
            }
        """)
        self.addToolBar(nav_bar)

        back_btn = QAction("⬅️ Back", self)
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        nav_bar.addAction(back_btn)

        forward_btn = QAction("Forward ➡️", self)
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        nav_bar.addAction(forward_btn)

        reload_btn = QAction("🔄️", self)
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        nav_bar.addAction(reload_btn)

        home_btn = QAction("🏠", self)
        home_btn.triggered.connect(self.navigate_home)
        nav_bar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background: #f9f9f9;
                margin-left: 10px;
                width: 500px;
            }
            QLineEdit:hover {
                border: 1px solid #aaa;
            }
        """)
        nav_bar.addWidget(self.url_bar)

        settings_btn = QAction("⚙️", self)
        settings_btn.triggered.connect(self.open_settings)
        nav_bar.addAction(settings_btn)

        self.add_new_tab(QUrl("https://duckduckgo.com/"), "New Tab")

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None:
            qurl = QUrl("https://duckduckgo.com/")

        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.titleChanged.connect(lambda title, browser=browser: self.update_tab_title(browser))
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url_bar(self.tabs.currentIndex()))

    def update_tab_title(self, browser):
        index = self.tabs.indexOf(browser)
        if index != -1:
            self.tabs.setTabText(index, browser.title())

    def update_url_bar(self, i):
        current_browser = self.tabs.widget(i)
        
        if isinstance(current_browser, QWebEngineView):
            url = current_browser.url().toString()
            self.url_bar.setText(url)
        else:
            self.url_bar.clear()

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.tabs.currentWidget().setUrl(QUrl(url))

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://duckduckgo.com/"))

    def new_tab(self, i):
        if i == -1:
            self.add_new_tab()

    def close_current_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def open_settings(self):
        settings_window = QDialog(self)
        settings_window.setWindowTitle("Settings")

        layout = QVBoxLayout()
        settings_window.setLayout(layout)

        homepage_label = QLabel("Set Homepage URL:")
        self.homepage_input = QLineEdit()
        layout.addWidget(homepage_label)
        layout.addWidget(self.homepage_input)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(lambda: self.save_settings(settings_window))
        layout.addWidget(save_btn)

        settings_window.exec_()

    def save_settings(self, window):
        homepage = self.homepage_input.text()
        if homepage:
            QMessageBox.information(self, "Saved", f"Homepage set to: {homepage}")
        window.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Minimal Browser")
    window = Browser()
    window.show()
    sys.exit(app.exec_())
