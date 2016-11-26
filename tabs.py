from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from pytabs.urls import *
import pytabs.config as config

HOME_URL = config.URL_SCHEME_WITH_SEPARATOR + 'home'
DEFAULT_URL_FOR_NEW_TAB = HOME_URL

class TabWorkerQThread(QtCore.QThread):

    connector = QtCore.pyqtSignal(object)

    def __init__(self, tabContent):
        QtCore.QThread.__init__(self)
        self.tabContent = tabContent


    def run(self):
        self.tabContent.runInBackground()
        self.connector.emit('{} run'.format(self.tabContent.url))


class AbstractTabContent:

    def __init__(self, url:str):
        self.url = url


    # Override this when subclassing
    def runInBackground(self):
        pass


    # Override this when subclassing
    def getContentWidget(self) -> QWidget:
        return QTextEdit()


class TabPage(QWidget):

    def __init__(self, parentTabWidget:QTabWidget):
        super().__init__()

        self.guiThread = QtCore.QThread.currentThread()
        self.tabWidget = parentTabWidget
        self.tabContent = AbstractTabContent(DEFAULT_URL_FOR_NEW_TAB)
        self.contentWidget = QTextEdit()

        # back/forward navigation state
        self.currentUrl = None
        self.historyBackStack = []
        self.historyForwardStack = []

        # widgets for navigation bar
        from pytabs import standards
        self.backButton = standards.fixButtonColor(QPushButton('Back'))
        self.forwardButton = standards.fixButtonColor(QPushButton('Forward'))
        self.homeButton = standards.fixButtonColor(QPushButton('Home'))
        self.refreshButton = standards.fixButtonColor(QPushButton('Refresh'))
        self.urlLineEdit = QLineEdit()
        self.goButton = standards.fixButtonColor(QPushButton('Go'))
        # TODO: put menu button here; remove menu bar
        # TODO: icons instead of text; (make preference?)

        # main layout
        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.hbox.setSpacing(4)
        self.vbox.setSpacing(4)
        self.progressBar = None
        self.workerThread = None # needed to ensure WorkerThread is allocated on the heap and not garbage collected

        self.initUI()
        self.go()


    def back(self):
        self.historyForwardStack.append(self.currentUrl)
        self.navigate(self.historyBackStack.pop())


    def forward(self):
        self.historyBackStack.append(self.currentUrl)
        self.navigate(self.historyForwardStack.pop())


    def home(self):
        self.urlLineEdit.setText(HOME_URL)
        self.go()


    def refresh(self):
        self.urlLineEdit.setText(self.currentUrl) # user may have edited the URL but not pushed Go; use original URL
        self.go()


    def go(self):
        url = self.urlLineEdit.text()
        if self.currentUrl is not None:
            self.historyBackStack.append(self.currentUrl)
        self.historyForwardStack.clear()
        self.navigate(url)


    def navigate(self, url:str):
        progressBar = QProgressBar()
        progressBar.setRange(0.0, 0.0) # indeterminate progress bar
        progressBar.setMaximumHeight(10.0)
        self.vbox.insertWidget(1, progressBar)

        self.currentUrl = url
        self.urlLineEdit.setText(url)
        self.backButton.setEnabled(len(self.historyBackStack) > 0)
        self.forwardButton.setEnabled(len(self.historyForwardStack) > 0)

        from pytabs import urls
        self.tabContent = urls.getTabContentForUrl(url)
        self.workerThread = TabWorkerQThread(self.tabContent)
        self.workerThread.connector.connect(self.onBackgroundProcessingCompleted)
        self.workerThread.start()


    def onBackgroundProcessingCompleted(self):
        # remove progressBar
        for item in self.children():
            if item is None or not isinstance(item, QProgressBar):
                continue
            item.setParent(None) # removeWidget in layout does NOT work

        # replace content widget
        newWidget = self.tabContent.getContentWidget()
        self.contentWidget.setParent(None) # this removes the old widget
        self.contentWidget = newWidget
        self.vbox.addWidget(self.contentWidget, stretch=1)


    def initUI(self):
        # set background color
        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.lightGray)
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # attach callbacks
        self.backButton.clicked.connect(self.back)
        self.forwardButton.clicked.connect(self.forward)
        self.homeButton.clicked.connect(self.home)
        self.refreshButton.clicked.connect(self.refresh)
        self.urlLineEdit.setText(DEFAULT_URL_FOR_NEW_TAB)
        # self.urlLineEdit.setFont() # TODO: set fixed width font
        self.urlLineEdit.returnPressed.connect(self.go)
        self.goButton.clicked.connect(self.go)

        # layout widgets
        self.hbox.addWidget(self.backButton)
        self.hbox.addWidget(self.forwardButton)
        self.hbox.addWidget(self.homeButton)
        self.hbox.addWidget(self.refreshButton)
        self.hbox.addWidget(self.urlLineEdit, stretch=1)
        self.hbox.addWidget(self.goButton)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.contentWidget, stretch=1)
        self.setLayout(self.vbox)