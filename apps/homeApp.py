from pytabs.apps.apps import AbstractApp
from pytabs.tabs import AbstractTabContent

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow


class HomeApp(AbstractApp):

    def __init__(self, mainWindow: QMainWindow):
        super().__init__("Home", QIcon('pytabs/resources/home.png'), mainWindow)

    def getTabContentForUrl(self, url: str) -> AbstractTabContent:
        return HomeTabContent(url)


class HomeTabContent(AbstractTabContent):

    def __init__(self, url: str):
        super().__init__(url)
        self.url = url
        self.title = 'Home'

    def runInBackground(self):
        # from time import sleep; sleep(1.5); print('HomeTabContent.rIB: sleeping for testing reasons!')
        pass

    def getContentWidget(self):
        from PyQt5.QtWidgets import QLabel
        return QLabel('Home')
