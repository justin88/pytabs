from apps.apps import AbstractApp
from tabs import AbstractTabContent

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow


class SettingsApp(AbstractApp):

    def __init__(self, mainWindow: QMainWindow):
        super().__init__("Settings", QIcon('resources/preferences.png'), mainWindow)

    def getTabContentForUrl(self, url: str) -> AbstractTabContent:
        return SettingsTabContent(url)


class SettingsTabContent(AbstractTabContent):

    def __init__(self, url: str):
        super().__init__(url)
        self.url = url
        self.title = 'Settings'

    def runInBackground(self):
        # from time import sleep; sleep(1.5); print('HomeTabContent.rIB: sleeping for testing reasons!')
        pass

    def getContentWidget(self):
        from PyQt5.QtWidgets import QLabel
        return QLabel('Settings')
