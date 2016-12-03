from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtGui import QColor, QPalette


def centerWidgetOnScreen(widget: QWidget):
    geometry = widget.frameGeometry()
    desktopCenter = QApplication.desktop().availableGeometry().center()
    geometry.moveCenter(desktopCenter)
    widget.move(geometry.topLeft())


def fixButtonColor(button: QPushButton):
    palette = button.palette()
    palette.setColor(QPalette.Button, QColor(208, 208, 208))
    # button.setAutoFilledBackground(True)
    button.setPalette(palette)
    return button
