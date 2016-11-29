from apps.apps import AbstractApp
from tabs import AbstractTabContent


class HomeApp(AbstractApp):

    def __init__(self):
        super().__init__("home")



    def getTabContentForUrl(self, url:str) -> AbstractTabContent:
        print('HomeApp.getTabContentForUrl: {}'.format(url))
        return HomeTabContent(url)


class HomeTabContent(AbstractTabContent):

    def __init__(self, url:str):
        super().__init__(self)
        self.url = url


    def runInBackground(self):
        # from time import sleep; sleep(1.5); print('HomeTabContent.rIB: sleeping for testing reasons!')
        pass

    def getContentWidget(self):
        from PyQt5.QtWidgets import QLabel
        return QLabel('Home')