import sys

from tabs import *

class GuiMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.tabWidget = QTabWidget()
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

        # set background color
        palette = self.tabWidget.palette()
        from PyQt5.QtGui import QColor, QPalette
        palette.setColor(QPalette.Window, Qt.darkGray)
        palette.setColor(QPalette.Button, QColor(184, 184, 184)) # this sets the foreground of the tab in the TabBar
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setPalette(palette)

        # initialize apps
        import apps
        from apps.homeApp import HomeApp
        apps.apps.registerApp(HomeApp())
        from apps.consoleApp import ConsoleApp
        apps.apps.registerApp(ConsoleApp())
        # import and register custom apps here
        # apps.registerApp(MyApp())

        # add starter tab
        self.tabWidget.setMovable(True) # enable drag and drop
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.tabWidget.addTab(TabPage(self.tabWidget), 'New Tab')

        self.setWindowTitle(config.WINDOW_TITLE)
        self.setCentralWidget(self.tabWidget)
        self.resize(config.INITIAL_WINDOW_WIDTH, config.INITIAL_WINDOW_HEIGHT)


    def closeTab(self, index):
        self.tabWidget.widget(index).closeTab()


def launch():
    app = QApplication(sys.argv)

    guiMainWindow = GuiMainWindow()
    import standards
    standards.centerWidgetOnScreen(guiMainWindow)
    guiMainWindow.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    launch()
