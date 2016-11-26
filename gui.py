import sys

from PyQt5.QtGui import QIcon

from pytabs.tabs import *

class GuiMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.tabWidget = QTabWidget()
        self.initUI()


    def addTab(self):
        # add new tab and select it
        self.tabWidget.setCurrentIndex(self.tabWidget.addTab(TabPage(QTextEdit()), 'New Tab'))


    def closeTab(self):
        index = self.tabWidget.currentIndex()
        widget = self.tabWidget.widget(index)
        # TODO: alert tab internal widget that it's about to close
        if widget is not None:
            widget.deleteLater()
        self.tabWidget.removeTab(index)


    def initUI(self):
        # create menu
        bar = self.menuBar()
        fileMenu = bar.addMenu('&File')

        addTabAction = QAction(QIcon('exit.png'), 'Add New &Tab', self) # TODO: fix icon
        addTabAction.setShortcut('Ctrl+T')
        addTabAction.triggered.connect(self.addTab)
        fileMenu.addAction(addTabAction)

        closeTabAction = QAction(QIcon('exit.png'), '&Close Tab', self) # TODO: fix icon
        closeTabAction.setShortcut('Ctrl+W')
        closeTabAction.triggered.connect(self.closeTab)
        fileMenu.addAction(closeTabAction)

        fileMenu.addSeparator()

        exitAction = QAction(QIcon('exit.png'), 'E&xit', self) # TODO: fix icon
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application') # TODO: where is this rendered
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
        from pytabs.apps import apps
        from pytabs.apps.homeApp import HomeApp
        apps.registerApp(HomeApp.HomeApp())
        # import and register custom apps here
        # apps.registerApp(MyApp())

        # add starter tab
        self.tabWidget.setMovable(True) # enable drag and drop
        self.tabWidget.addTab(TabPage(QTextEdit()), 'New Tab')

        self.setWindowTitle(config.WINDOW_TITLE)
        self.setCentralWidget(self.tabWidget)
        self.resize(config.INITIAL_WINDOW_WIDTH, config.INITIAL_WINDOW_HEIGHT)


def launch():
    app = QApplication(sys.argv)

    guiMainWindow = GuiMainWindow()
    from pytabs import standards
    standards.centerWidgetOnScreen(guiMainWindow)
    guiMainWindow.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    launch()
