import sys

from pytabs.tabs import *


class PyTabsMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.tabWidget = PyTabsTabWidget()
        self.initUI()

    def initUI(self):
        from pytabs import config
        self.setWindowTitle(config.APPLICATION_NAME)
        self.setWindowIcon(QIcon(config.APPLICATION_ICON_PATH))

        # create menu
        bar = self.menuBar()
        fileMenu = bar.addMenu('&File')
        exitAction = QAction(QIcon('pytabs/resources/exit.png'), 'E&xit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        # initialize apps
        from pytabs import apps
        from pytabs.apps.homeApp import HomeApp
        apps.apps.registerApp(HomeApp(self))
        from pytabs.apps.consoleApp import ConsoleApp
        apps.apps.registerApp(ConsoleApp(self))
        from pytabs.apps.settingsApp import SettingsApp
        apps.apps.registerApp(SettingsApp(self))
        # import and register custom apps here
        # from pytabs.myApp import MyApp
        # apps.registerApp(MyApp())

        # set central widget, window title, and size on screen
        self.setCentralWidget(self.tabWidget)
        self.setWindowTitle(config.WINDOW_TITLE)
        self.resize(config.INITIAL_WINDOW_WIDTH, config.INITIAL_WINDOW_HEIGHT)


def launch(listOfAppClasses):  # list of AbstractApp implementations
    app = QApplication(sys.argv)
    guiMainWindow = PyTabsMainWindow()

    # load external apps
    for appClass in listOfAppClasses:
        from pytabs.apps.apps import registerApp
        registerApp(appClass(guiMainWindow))

    # load external config # TODO

    # add starter tab
    guiMainWindow.tabWidget.addNewTab()

    # center the window
    from pytabs import standards
    standards.centerWidgetOnScreen(guiMainWindow)
    guiMainWindow.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    launch([])
