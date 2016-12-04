from pytabs.apps import apps

from urllib.parse import urlparse


def getTabContentForUrl(url: str):  # -> AbstractTabContent
    tupl = urlparse(url)  # -> (scheme, netloc, path, params, query, fragment)
    app = tupl[1]  # netloc = app name
    if app in apps.appsDict:
        return apps.appsDict[app].getTabContentForUrl(url=url)
    else:
        return apps.getErrorTabContentForUrl(url=url, app=app)


def baseUrlForApp(appName: str):
    from pytabs import config
    return config.URL_SCHEME_WITH_SEPARATOR + appName
