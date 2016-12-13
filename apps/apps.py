from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMainWindow, QMenu, QWidget

appsDict = {}


class AbstractApp:

    def __init__(self, name: str, icon: QIcon, mainWindow: QMainWindow):
        self.name = name
        self.canonicalName = name.lower()
        self.mainWindow = mainWindow
        if icon is None:
            self.icon = QIcon('pytabs/resources/add.png')
        else:
            self.icon = icon

        # app menu
        self.menu = QMenu(self.name)
        self.menu.setIcon(self.icon)
        self.menuAction = QAction(self.icon, '{}'.format(self.name), self.menu)
        self.menuAction.setShortcut('Ctrl+H')
        self.menuAction.triggered.connect(self.showApp)
        self.menu.addAction(self.menuAction)

    # abstract method that should be overridden in implementing subclasses
    def getTabContentForUrl(self, url: str):  # -> AbstractTabContent implementation
        return None

    def getMenu(self) -> QMenu:
        return self.menu

    def showApp(self):
        from pytabs import urls
        self.mainWindow.tabWidget.addTabWithUrl(urls.baseUrlForApp(self.canonicalName))


def registerApp(app: AbstractApp):
    appsDict[app.canonicalName] = app


def deregisterApp(app: AbstractApp):
    if app is None:
        return
    elif isinstance(app, str):
        del appsDict[app]
    if isinstance(app, AbstractApp):
        del appsDict[app.canonicalName]


def getErrorTabContentForUrl(url: str, app: str):
    from pytabs.tabs import AbstractTabContent

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
