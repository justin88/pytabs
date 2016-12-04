# parameters that go in Settings, probably...
REMEMBER_TABS_ON_CLOSE = True


class PyTabsConfiguration:

    def __init__(self, apps=[]):
        self.apps = apps
        self.APPLICATION_ICON_PATH = "pytabs/resources/tabs.png"
        self.APPLICATION_NAME = "pytabs"
        self.APPLICATION_CONFIG_FILE_LOCATION = "." + self.APPLICATION_NAME.lower()
        self.WINDOW_TITLE = 'pytabs'

        self.URL_SCHEME = 'pytabs'
        self.URL_SCHEME_WITH_SEPARATOR = self.URL_SCHEME + '://'

        self.INITIAL_WINDOW_WIDTH = 1024
        self.INITIAL_WINDOW_HEIGHT = 768

    def getApps(self):
        return self.apps
