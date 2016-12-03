The pytabs project is a tab-based application framework.  The framework makes developing extensible and
responsive GUI apps easy.

Components:
- gui -- launching the app, and the defining the main window
- tabs -- implementation of browser-like tab functionality, i.e. URL-based navigation and off-GUI thread processing
- urls -- customizable content based on URL dispatching
- apps -- abstractions for content implementation, default implementations of example apps, error handling
- config -- customization, e.g. application name, icon, etc
- standards -- look and feel

Import order:
- gui
- tabs
- config
- apps
- standards
- urls
