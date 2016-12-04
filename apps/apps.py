from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMainWindow, QMenu, QWidget

appsDict = {}


class AbstractApp:

    def __init__(self, name: str, mainWindow: QMainWindow):
        self.name = name.lower()  # enforce lowercase
        self.mainWindow = mainWindow
        self.icon = QIcon('resources/add.png')

        # app menu
        self.menu = QMenu(self.name)
        self.showMenuAction = QAction(self.icon, 'Show {}'.format(self.name), self.menu)
        self.showMenuAction.setShortcut('Ctrl+H')
        self.showMenuAction.triggered.connect(self.showApp)
        self.menu.addAction(self.showMenuAction)

    # abstract method that should be overridden in implementing subclasses
    def getTabContentForUrl(self, url: str):  # -> AbstractTabContent implementation
        return None

    def getMenu(self) -> QMenu:
        return self.menu

    def showApp(self):
        import urls
        self.mainWindow.tabWidget.addTabWithUrl(urls.baseUrlForApp(self.name))


def registerApp(app: AbstractApp):
    appsDict[app.name] = app


def getErrorTabContentForUrl(url: str, app: str):
    from tabs import AbstractTabContent

    class ErrorTabContent(AbstractTabContent):

        def __init__(self, urlWithError: str):
            super().__init__(urlWithError)

        def getContentWidget(self) -> QWidget:
            from PyQt5.QtWidgets import QLabel
            from PyQt5.QtCore import Qt
            from PyQt5.QtGui import QColor
            label = QLabel('Unknown app {} while parsing url: {}'.format(app, self.url))
            label.setAlignment(Qt.AlignCenter)
            palette = label.palette()
            palette.setColor(label.backgroundRole(), QColor(255, 192, 192))
            label.setAutoFillBackground(True)
            label.setPalette(palette)
            return label

    return ErrorTabContent(url)
