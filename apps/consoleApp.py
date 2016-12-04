from apps.apps import AbstractApp
from tabs import AbstractTabContent

from PyQt5.QtWidgets import QMainWindow


class ConsoleApp(AbstractApp):

    def __init__(self, mainWindow: QMainWindow):
        super().__init__('console', mainWindow)

    def getTabContentForUrl(self, url: str) -> AbstractTabContent:
        print('ConsoleApp.getTabContentForUrl: {}'.format(url))
        return ConsoleTabContent(url)


class ConsoleTabContent(AbstractTabContent):

    def __init__(self, url: str):
        super().__init__(self)
        self.title = 'Console'
        self.url = url
        self.kernelManager = None
        self.kernel = None
        self.kernelClient = None
        self.jupyterWidget = None

    def runInBackground(self):
        # from time import sleep; sleep(1.5); print('ConsoleTabContent.rIB: sleeping for testing reasons!')
        pass

    def getContentWidget(self):
        # create an in-process kernel
        from qtconsole.inprocess import QtInProcessKernelManager
        self.kernelManager = QtInProcessKernelManager()
        self.kernelManager.start_kernel(show_banner=False)
        self.kernel = self.kernelManager.kernel
        self.kernel.gui = 'qt4'  # TODO: ???
        self.kernelClient = self.kernelManager.client()
        self.kernelClient.start_channels()

        # create jupyter qtconsole widget
        from qtconsole.rich_jupyter_widget import RichJupyterWidget
        self.jupyterWidget = RichJupyterWidget()
        self.jupyterWidget.kernel_manager = self.kernelManager
        self.jupyterWidget.kernel_client = self.kernelClient
        # self.jupyterWidget.syntax_style = 'monokai' # doesn't work -- foreground becomes invisible on Ubuntu
        self.jupyterWidget.execute('%matplotib inline')
        # more executes here to set up config
        self.jupyterWidget.execute('')  # TODO: why?

        # layout
        from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QWidget
        hBox = QHBoxLayout()
        vBox = QVBoxLayout()
        vBox.addWidget(QLabel('Variables'))
        vBox.addWidget(QLabel('::variables go here::'), stretch=1)
        hBox.addLayout(vBox)
        hBox.addWidget(self.jupyterWidget)

        widget = QWidget()
        widget.setLayout(hBox)
        return widget
