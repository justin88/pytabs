import apps
from urllib.parse import urlparse


def getTabContentForUrl(url:str): # -> AbstractTabContent
    tupl = urlparse(url) # -> (scheme, netloc, path, params, query, fragment)
    print('pytabs.urls.getTabContentForUrl: {}'.format(tupl))
    app = tupl[1] # netloc = app name
    if app in apps.apps.appsDict:
        return apps.apps.appsDict[app].getTabContentForUrl(url=url)
    else:
        return apps.apps.getErrorTabContentForUrl(url=url, app=app)