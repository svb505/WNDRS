import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView

app = QApplication(sys.argv)

window = QMainWindow()
browser = QWebEngineView()

browser.load(QUrl("https://google.com"))

window.setCentralWidget(browser)
window.show()

app.exec_()