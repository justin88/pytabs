from pytabs.apps import apps
import pytabs.config as config
from urllib.parse import urlparse

config.URL_SCHEME

def getTabContentForUrl(url:str): # -> AbstractTabContent
    tupl = urlparse(url) # -> (scheme, netloc, path, params, query, fragment)
    print('pytabs.urls.getTabContentForUrl: {}'.format(tupl))
    app = tupl[1] # netloc = app name
    if app in apps.appsDict:
        return apps.appsDict[app].getTabContentForUrl(url)
    else:
        return apps.getErrorTabContentForUrl(url)