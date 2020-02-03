# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import requests
from setup_menu import *

class MainMenu(QDialog):

	def __init__(self, parent=None):
		super(MainMenu, self).__init__(parent)
		self.setWindowTitle("SimuSound")

		self.welcomeLabel = QLabel("Welcome!")
		self.welcomeLabel.setAlignment(Qt.AlignCenter)
		self.welcomeLabel.setFont(QFont("Arial",20))

		instructionsLabelText = """
		Select your desired option from the buttons below.
		Hover over any button for more details.
		"""
		self.instructionsLabel = QLabel(instructionsLabelText)
		self.instructionsLabel.setAlignment(Qt.AlignCenter)
		self.instructionsLabel.setFont(QFont("Arial",16))


		self.connectionLabel = QLabel("Looking for probe....")
		self.connectionLabel.setAlignment(Qt.AlignCenter)

		self.mainLayout = QVBoxLayout()
		self.mainLayout.addWidget(self.welcomeLabel)
		self.mainLayout.addWidget(self.instructionsLabel)
		self.mainLayout.addWidget(self.connectionLabel)



		setupHelpText = """
		<nobr>Setup the ultrasound probe with the RFID tags.</nobr> Map the tags and their unique codes to various body regions."""
		self.setupButton = QPushButton("Setup")
		self.setupButton.setToolTip(setupHelpText)
		self.setupButton.clicked.connect(self.openSetup)
		self.setupButton.setFixedSize(QSize(80, 75))

		
		self.buttonLayout = QHBoxLayout()
		self.buttonLayout.addWidget(self.setupButton)

		self.mainLayout.addLayout(self.buttonLayout)
		self.setLayout(self.mainLayout)

	def checkConnection(self):
		self.timer = QTimer()
		self.timer.timeout.connect(self.updateConnectionText)
		self.timer.start(2000)  # every 10,000 milliseconds
		
	def updateConnectionText(self):
		if checkConnection():
			self.connectionLabel.setText("Probe Connected!")
		else:
			notFoundText = """
			Ultrasound Probe not found. Please ensure probe is powered on.
			This device should be connected to the SimuSound WiFi network
			created by the probe.
			"""
			self.connectionLabel.setText(notFoundText)
	
	def openSetup(self):
		setup = SetupWindow(self)
		setup.show()


	# def openUrl(self):
	# 	url = QUrl('https://github.com')
	# 	if not QDesktopServices.openUrl(url):
	# 		QMessageBox.warning(self, 'Open Url', 'Could not open url')

#Check if probe is found
def checkConnection():
	url = "http://192.168.4.1/"
	try:
		res = requests.get(url,timeout=1) #####TODO: Update this to change header to a "connection check" header
		return True
	except:
		return False

if __name__ == '__main__':
	# Create the Qt Application
	app = QApplication(sys.argv)
	# Create and show the form
	main_menu = MainMenu()
	main_menu.show()
	main_menu.checkConnection()
	# Run the main Qt loop
	sys.exit(app.exec_())
