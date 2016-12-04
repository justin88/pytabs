import sys

from tabs import *


class PyTabsMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.tabWidget = PyTabsTabWidget()
        self.initUI()

    def initUI(self):
        import config
        self.setWindowTitle(config.APPLICATION_NAME)
        self.setWindowIcon(QIcon(config.APPLICATION_ICON_PATH))

        # create menu
        bar = self.menuBar()
        fileMenu = bar.addMenu('&File')
        exitAction = QAction(QIcon('resources/exit.png'), 'E&xit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        # initialize apps
        import apps
        from apps.homeApp import HomeApp
        apps.apps.registerApp(HomeApp(self))
        from apps.consoleApp import ConsoleApp
        apps.apps.registerApp(ConsoleApp(self))
        # import and register custom apps here
        # from myApp import MyApp
        # apps.registerApp(MyApp())

        # add starter tab
        self.tabWidget.addTab(PyTabsPage(self.tabWidget), 'New Tab')

        # set central widget, window title, and size on screen
        self.setCentralWidget(self.tabWidget)
        self.setWindowTitle(config.WINDOW_TITLE)
        self.resize(config.INITIAL_WINDOW_WIDTH, config.INITIAL_WINDOW_HEIGHT)


def launch():
    app = QApplication(sys.argv)
    guiMainWindow = PyTabsMainWindow()
    import standards
    standards.centerWidgetOnScreen(guiMainWindow)
    guiMainWindow.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    launch()
