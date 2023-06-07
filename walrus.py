# importing required libraries
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
import os
import sys

# main window
class MainWindow(QMainWindow):

    # constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # creating a tab widget
        self.tabs = QTabWidget()

        # making document mode true
        self.tabs.setDocumentMode(True)

        # adding action when double clicked
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

        # adding action when tab is changed
        self.tabs.currentChanged.connect(self.current_tab_changed)

        # making tabs closeable
        self.tabs.setTabsClosable(True)

        # adding action when tab close is requested
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        # making tabs as central widget
        self.setCentralWidget(self.tabs)

        # creating a status bar
        self.status = QStatusBar()

        # setting status bar to the main window
        self.setStatusBar(self.status)

        # creating a tool bar for navigation
        navtb = QToolBar("Navigation")

        # adding tool bar to the main window
        self.addToolBar(navtb)

        # creating back action
        back_btn = QAction("⬅️", self)

        # setting status tip
        back_btn.setStatusTip("Back to the previous page")

        # adding action to back button
        # making the current tab go back
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())

        # adding this to the navigation tool bar
        navtb.addAction(back_btn)

        # similarly adding next button
        next_btn = QAction("➡️", self)
        next_btn.setStatusTip("Forward to the next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        # similarly adding reload button
        reload_btn = QAction("🔄", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        # creating home action
        home_btn = QAction("🏠", self)
        home_btn.setStatusTip("Go home")

        # adding action to home button
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        # creating about action
        about_btn = QAction("📢", self)
        about_btn.setStatusTip("Read about Walrus")

        # adding action to about button
        about_btn.triggered.connect(self.navigate_about)
        navtb.addAction(about_btn)

        # adding a separator
        navtb.addSeparator()

        # creating a line edit widget for URL
        self.urlbar = QLineEdit()

        # adding action to line edit when return key is pressed
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        # adding line edit to tool bar
        navtb.addWidget(self.urlbar)

        # similarly adding stop action
        stop_btn = QAction("🛑", self)
        stop_btn.setStatusTip("Stop loading the current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)

        # creating download action
        download_btn = QAction("⬇️", self)
        download_btn.setStatusTip("Download")
        download_btn.triggered.connect(self.download)
        navtb.addAction(download_btn)

        # creating the first tab
        self.add_new_tab(QUrl('https:/google.com'), 'Homepage')

        # showing all the components
        self.show()

        # setting window title
        self.setWindowTitle("Walrus Browser")

        # create a network access manager
        self.network_manager = QNetworkAccessManager()
        self.network_manager.finished.connect(self.download_finished)

        # dictionary to store download paths
        self.downloads = {}

    # method for adding a new tab
    def add_new_tab(self, qurl=None, label="Blank"):

        # if the URL is blank
        if qurl is None:
            # creating a default URL
            qurl = QUrl('https://google.com')

        # creating a QWebEngineView object
        browser = QWebEngineView()

        # setting the URL to the browser
        browser.setUrl(qurl)

        # setting tab index
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        # adding action to the browser when the URL is changed
        # update the URL
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        # adding action to the browser when loading is finished
        # set the tab title
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    def navigate_about(self):
        self.tabs.currentWidget().setUrl(QUrl("https://walrus.mrsn0ww0lf.repl.co"))

    # when double-clicked is pressed on tabs
    def tab_open_doubleclick(self, i):

        # checking index i.e
        # No tab under the click
        if i == -1:
            # creating a new tab
            self.add_new_tab()

    # when the tab is changed
    def current_tab_changed(self, i):

        # get the URL
        qurl = self.tabs.currentWidget().url()

        # update the URL
        self.update_urlbar(qurl, self.tabs.currentWidget())

        # update the title
        self.update_title(self.tabs.currentWidget())

    # when the tab is closed
    def close_current_tab(self, i):

        # if there is only one tab
        if self.tabs.count() < 2:
            # do nothing
            return

        # else remove the tab
        self.tabs.removeTab(i)

    # method for updating the title
    def update_title(self, browser):

        # if the signal is not from the current tab
        if browser != self.tabs.currentWidget():
            # do nothing
            return

        # get the page title
        title = self.tabs.currentWidget().page().title()

        # set the window title
        self.setWindowTitle("%s - New Tab" % title)

    # action to go to the home
    def navigate_home(self):

        # go to Google
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    # method for navigating to a URL
    def navigate_to_url(self):

        # get the line edit text
        # convert it to a QUrl object
        q = QUrl(self.urlbar.text())

        # if the scheme is blank
        if q.scheme() == "":
            # set the scheme
            q.setScheme("http")

        # set the URL
        self.tabs.currentWidget().setUrl(q)

    # method to update the URL
    def update_urlbar(self, q, browser=None):

        # If this signal is not from the current tab, ignore
        if browser != self.tabs.currentWidget():
            return

        # set text to the URL bar
        self.urlbar.setText(q.toString())

        # set cursor position
        self.urlbar.setCursorPosition(0)

    def download(self):
        # get the current tab
        current_tab = self.tabs.currentWidget()

        # get the URL of the current page
        url = current_tab.url()

        # create a QNetworkRequest with the URL
        request = QNetworkRequest(url)

        # send the request using the network access manager
        self.network_manager.get(request)

    def download_finished(self, reply):
        # get the URL of the finished download
        url = reply.url().toString()

        # get the file name from the URL
        file_name = os.path.basename(url)

        # get the path where the file will be saved
        path, _ = QFileDialog.getSaveFileName(self, "Save File", file_name)

        # save the downloaded file to the chosen path
        if path:
            file = QFile(path)
            if file.open(QIODevice.WriteOnly):
                file.write(reply.readAll())
                file.close()
                QMessageBox.information(self, "Download Complete", "File saved successfully.")

    def closeEvent(self, event):
        # clean up downloads
        for path in self.downloads.values():
            QFile.remove(path)
        super().closeEvent(event)

# creating a PyQt5 application
app = QApplication(sys.argv)

# setting name to the application
app.setApplicationName("Walrus Browser")

# creating a MainWindow object
window = MainWindow()

# loop
app.exec_()
