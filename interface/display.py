import sys
import traceback
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import requests


class USDisplay(QDialog):
	def __init__(self, mapper, parent=None):
		super(USDisplay, self).__init__(parent)
		self.parent = parent
		self.mapper = mapper
		self.currentImage = None
		self.movie_screen = QLabel()
		# Make label fit the gif
		self.movie_screen.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.movie_screen.setAlignment(Qt.AlignCenter)

		# Create the layout
		main_layout = QVBoxLayout()
		main_layout.addWidget(self.movie_screen)

		self.setLayout(main_layout)

		#print("here")
		self.getProbeInput()



	def setImage(self,image,title):
		#self.movie.stop()
		# Load the file into a QMovie
		if self.currentImage == title:
			return

		print(image,title,sep=":")
		self.movie = QMovie(image, QByteArray(), self)

		size = self.movie.scaledSize()
		self.setGeometry(200, 200, size.width(), size.height())
		self.setWindowTitle(title)
		# Add the QMovie object to the label
		self.movie.setCacheMode(QMovie.CacheAll)
		self.movie.setSpeed(100)
		self.movie_screen.setMovie(self.movie)
		self.movie.start()
		self.currentImage = title
		#self.timer.stop()

	def readProbe(self):
		url = "http://192.168.4.1/"
		try:
			res = requests.get(url,timeout=.1) #####TODO: Update this to change header to a "connection check" header
			uid = self.getValue(res.content)
			#print(uid)
			if uid != None:
				result = self.findID(uid)
				#print(result,self.mapper)
				if result != None:
					#print(result)
					self.setImage(result[1],result[0])
				else:
					self.setImage("none.gif","")
			else:
				self.setImage("none.gif","")
		except Exception as e:
			print(e)
			print(traceback.format_exc())
			return None

	def findID(self,uid):
		for item in self.mapper:
			#print(uid,item,sep=":")
			if uid == self.mapper[item]["uid"]:
				#print(item,self.mapper[item]["image"])
				return item,self.mapper[item]["image"]
		return None

	def getValue(self,content):
		value = content.decode("utf-8").strip()
		if value == "":
			value = None
		return value

	def getProbeInput(self):
		self.timer = QTimer()
		self.timer.timeout.connect(self.readProbe)
		self.timer.start(100)  # 1000 milliseconds = 1 sec
