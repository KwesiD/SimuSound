# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

class MapperMenu(QDialog):
	def __init__(self, parent=None):
		super(MapperMenu, self).__init__(parent)
		self.setWindowTitle("Mapper")

		self.mapper = {}

		self.mapLabel = QLabel(str(self.mapper))
		self.mapLabel.setAlignment(Qt.AlignCenter)
		self.mapLabel.setFont(QFont("Arial",16))

		self.mainLayout = QVBoxLayout()

		self.mainLayout.addWidget(self.mapLabel)

		regions = ["Heart","L Chest","R Chest","Abdominal"]
		for region in regions:
			button = QPushButton(region)
			button.clicked.connect(self.generator(region))
			self.mainLayout.addWidget(button)
			self.mapper[region] = None
		
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
		self.mapLabel.setText(str(self.mapper))

	def complete(self):
		self.close()


class RegistrationMenu(QDialog):
	def __init__(self, parent=None,text=None):
		super(RegistrationMenu, self).__init__(parent)
		self.setWindowTitle("Register A Tag")
		self.parent = parent
		self.text = text

		self.waitingLabel = QLabel("Registering value for " + self.text + "\nWaiting on probe...")
		self.waitingLabel.setAlignment(Qt.AlignCenter)
		self.waitingLabel.setFont(QFont("Arial",16))

		self.mainLayout = QVBoxLayout()

		self.mainLayout.addWidget(self.waitingLabel)

		self.setLayout(self.mainLayout)



	def getValue(self,content):
		print(content)
		return "Test"

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
				self.parent.mapper[self.text] = value
				self.timer.stop()
				self.parent.updateMap()
				self.close()
			else:
				return None
		except:
			return None

	def setText(self,text):
		self.text = text

	def start(self):
		self.show()
		self.getProbeInput()
