import os
import sys

import zipfile
from zipfile import ZipFile

import shutil

class Zip():
	
	def __init__(self):
		
		self.nameFolder = 'ZIP/'
		self.nameZipFile = None
		self.thisfile = None

	def Saludar(self):
		print(self.phrase)

	def CreateFile(self, task):
		self.nameZipFile = self.nameFolder + 'Task' + str(task) + '.zip'
		
		self.thisfile = ZipFile(self.nameZipFile, 'a', zipfile.ZIP_DEFLATED)
		
		src_files = os.listdir('/tmp/')
		
		src_files_jpg = list()
	
		for i in range(len(src_files)):
			if src_files[i].startswith('image_' + str(task) + '_') and src_files[i].endswith('.jpg'):
				src_files_jpg.append(src_files[i])
				
		src_files_order_jpg = sorted(src_files_jpg)
		
		for i in range(len(src_files_order_jpg)):
			checkFile = os.path.isfile('/tmp/' + src_files_order_jpg[i])
			if checkFile == True:
				shutil.copy('/tmp/' + src_files_order_jpg[i], self.nameFolder)
				self.thisfile.write(self.nameFolder + src_files_order_jpg[i])
				os.remove(self.nameFolder + src_files_order_jpg[i])		

		self.thisfile.close()
