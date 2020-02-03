# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from mapper_menu import *

class SetupWindow(QDialog):
	def __init__(self, parent=None):
		super(SetupWindow, self).__init__(parent)
		self.setWindowTitle("Setup")
		self.parent = parent

		importHelperText = """ """
		self.importButton = QPushButton("Import Settings")
		self.importButton.setToolTip(importHelperText)
		self.importButton.clicked.connect(None)

		newSettingsHelperText = """ """
		self.newSettingsButton = QPushButton("Create New Settings")
		self.newSettingsButton.setToolTip(newSettingsHelperText)
		self.newSettingsButton.clicked.connect(self.createNewSettings)

		
		self.mainLayout = QVBoxLayout()
		self.mainLayout.addWidget(self.importButton)
		self.mainLayout.addWidget(self.newSettingsButton)

		self.setLayout(self.mainLayout)

	def createNewSettings(self):
		mapper = MapperMenu(self)
		mapper.show()






