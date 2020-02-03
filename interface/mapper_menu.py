# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import requests
import json

class MapperMenu(QDialog):
	def __init__(self, parent=None):
		super(MapperMenu, self).__init__(parent)
		self.setWindowTitle("Mapper")
		self.parent = parent
		self.mapper = {}

		self.mapLabel = QLabel(str(self.mapper))
		self.mapLabel.setAlignment(Qt.AlignCenter)
		self.mapLabel.setFont(QFont("Arial",10))

		self.mainLayout = QVBoxLayout()

		self.mainLayout.addWidget(self.mapLabel)

		regions = ["Heart","L Lung","R Lung","Abdominal"]
		for region in regions:
			button = QPushButton(region)
			button.clicked.connect(self.generator(region))
			self.mainLayout.addWidget(button)
			self.mapper[region] = {"uid":None,"image":None}
		
		self.completeButton = QPushButton("Complete")
		self.completeButton.clicked.connect(self.complete)
		self.mainLayout.addWidget(self.completeButton)
		# self.mainLayout.addWidget(self.newSettingsButton)

		self.setLayout(self.mainLayout)


	def generator(self,text):
		def register():
			register = RegistrationMenu(self,text)
			register.start()
			#register.setText(text)
		return register

	def updateMap(self):
		self.mapLabel.setText(json.dumps(self.mapper,indent=4))

	def complete(self):
		self.parent.parent.mapper = self.mapper
		self.close()


class RegistrationMenu(QDialog):
	def __init__(self, parent=None,text=None):
		super(RegistrationMenu, self).__init__(parent)
		self.setWindowTitle("Register A Tag")
		self.parent = parent
		self.text = text
		self.currentValue = ""

		self.waitingLabel = QLabel("Registering value for " + self.text + "\nWaiting on probe...\nCurrent value = " + self.currentValue)
		self.waitingLabel.setAlignment(Qt.AlignCenter)
		self.waitingLabel.setFont(QFont("Arial",10))

		self.setImageButton = QPushButton("Set Image")
		self.setImageButton.clicked.connect(self.setImage)

		self.completeButton = QPushButton("Save Mapping")
		self.completeButton.clicked.connect(self.complete)

		self.mainLayout = QVBoxLayout()

		self.mainLayout.addWidget(self.waitingLabel)
		self.mainLayout.addWidget(self.setImageButton)
		self.mainLayout.addWidget(self.completeButton)

		self.setLayout(self.mainLayout)



	def getValue(self,content):
		value = content.decode("utf-8").strip()
		if value == "":
			value = None
		return value

	def getProbeInput(self):
		self.timer = QTimer()
		self.timer.timeout.connect(self.getID)
		self.timer.start(200)  # 1000 milliseconds = 1 sec

	def getID(self):
		url = "http://192.168.4.1/"
		try:
			res = requests.get(url,timeout=.1) #####TODO: Update this to change header to a "connection check" header
			value = self.getValue(res.content)
			if value != None:
				self.parent.mapper[self.text]["uid"] = value
				self.currentValue = value
				self.updateLabel()
			else:
				return None
		except:
			return None

	def setText(self,text):
		self.text = text

	def setImage(self):
		imageName = QFileDialog.getOpenFileName(self, 'Open file','c:\\',"Image files (*.jpg *.gif)")[0]
		if imageName != "":
			self.parent.mapper[self.text]["image"] = imageName

	def complete(self):
		self.timer.stop()
		self.parent.updateMap()
		self.close()

	def updateLabel(self):
		self.waitingLabel.setText("Registering value for " + self.text + "\nWaiting on probe...\nCurrent value = " + self.currentValue)

	def start(self):
		self.show()
		self.getProbeInput()
