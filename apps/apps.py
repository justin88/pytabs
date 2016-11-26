from PyQt5.QtWidgets import QWidget

appsDict = { }

class AbstractApp():

    def __init__(self, name:str):
        self.name = name


    # abstract method that should be overridden in implementing subclasses
    def getTabContentForUrl(self, url:str): # -> AbstractTabContent implementation
        return None


def registerApp(app:AbstractApp):
    print('pytabs.apps.apps.registerApp: adding: {}'.format(app.name))
    appsDict[app.name] = app


def getErrorTabContentForUrl(url:str):
    from pytabs.tabs import AbstractTabContent

    class ErrorTabContent(AbstractTabContent):

        def __init__(self, url:str):
            super().__init__(url)


        def getContentWidget(self) -> QWidget:
            from PyQt5.QtWidgets import QLabel
            from PyQt5.QtCore import Qt
            from PyQt5.QtGui import QColor
            label = QLabel('Unknown app while parsing url: {}'.format(self.url))
            label.setAlignment(Qt.AlignCenter)
            palette = label.palette()
            palette.setColor(label.backgroundRole(), QColor(255, 192, 192))
            label.setAutoFillBackground(True)
            label.setPalette(palette)
            return label

    return ErrorTabContent(url)





