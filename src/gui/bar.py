from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import math


class Bar(QtWidgets.QWidget):

    def __init__(self, vmin, vmax, vyellow, vred, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )

        self.setMaximumWidth(5)
        self.setMaximumWidth(20)

        self.value = vmin

        self.vmin = vmin
        self.vmax = vmax

        self._pc_yellow = (vyellow - vmin) / (vmax - vmin)
        self._pc_red = (vred - vmin) / (vmax - vmin)

        self._background_color = QtGui.QColor('black')
        self._padding = 1

    def paintEvent(self, e):
        painter = QtGui.QPainter(self)

        brush = QtGui.QBrush()
        brush.setColor(self._background_color)
        brush.setStyle(Qt.SolidPattern)
        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)

        # Define our canvas.
        d_height = painter.device().height() - (self._padding * 2)
        d_width = painter.device().width() - (self._padding * 2)

        # Calculate the y-stop position, from the value in range.
        pc = (self.value - self.vmin) / (self.vmax - self.vmin)

        # Draw green box (up to -12 dB)
        if pc > 0:
            brush.setColor(QtGui.QColor('green'))
            painter.fillRect(self._green_rect(pc, d_height, d_width), brush)

        # Draw yellow box (from -12 dB up to 0 dB)
        if pc > self._pc_yellow:
            brush.setColor(QtGui.QColor('yellow'))
            painter.fillRect(self._yellow_rect(pc, d_height, d_width), brush)

        # Draw red box (from 0 dB up to 12 dB)
        if pc > self._pc_red:
            brush.setColor(QtGui.QColor('red'))
            painter.fillRect(self._red_rect(pc, d_height, d_width), brush)

        painter.end()

    def _green_rect(self, pc, d_height, d_width):
        if pc < self._pc_yellow:
            top = round(self._padding + d_height * (1 - pc))
            height = round(d_height * pc)
        else:
            top = round(self._padding + d_height * (1 - self._pc_yellow))
            height = round(d_height * self._pc_yellow)

        return QtCore.QRect(
            self._padding,
            self._padding + top - 1,
            d_width,
            height
        )

    def _yellow_rect(self, pc, d_height, d_width):
        if pc < self._pc_red:
            top = round(self._padding + d_height * (1 - pc))
            height = round(d_height * (pc - self._pc_yellow))
        else:
            top = round(self._padding + d_height * (1 - self._pc_red))
            height = round(d_height * (self._pc_red - self._pc_yellow))

        return QtCore.QRect(
            self._padding,
            self._padding + top - 1,
            d_width,
            height
        )

    def _red_rect(self, pc, d_height, d_width):
        top = round(self._padding + d_height * (1 - pc))
        height = round(d_height * (pc - self._pc_red))

        return QtCore.QRect(
            self._padding,
            self._padding + top - 1,
            d_width,
            height
        )
