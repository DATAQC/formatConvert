import pandas as pd
import os

class dataFile:
	def __init__(self,fileObject,file_dir,file_name):
		self.fileObject = fileObject
		self.file_dir = file_dir
		self.file_name = file_name


	def delimitedToExcel(self):
		outputFileName = os.path.join(self.file_dir,self.file_name.split('.')[0]+'.xlsx')	
		self.delimitedDF = pd.read_csv(self.fileObject,keep_default_na=False)
		self.delimitedDF.to_excel(outputFileName,index=False,encoding = 'utf-8')

	def excelToDelimited(self):
		outputFileName = os.path.join(self.file_dir,self.file_name.split('.')[0]+'.csv')	
		self.excelDF = pd.read_excel(self.fileObject,keep_default_na=False,encoding='utf-8')
		#self.excelDF.to_csv(outputFileName,index=False)


def main():
	file_location = 'C:\\projects\\dataConvert\\bigdata.csv'
	file_dir = os.path.dirname(file_location)
	file_name = os.path.basename(file_location)
	with open(file_location,'r',encoding="utf8") as fileObject:
		dataObject = dataFile(fileObject,file_dir,file_name)
		dataObject.delimitedToExcel()

	# file_location = 'C:\\projects\\dataConvert\\excel.xlsx'
	# file_dir = os.path.dirname(file_location)
	# file_name = os.path.basename(file_location)
	
	# with open(file_location,'r',encoding="utf8") as fileObject:
	# 	dataObject = dataFile(fileObject,file_dir,file_name)
	# 	export_delimited = dataObject.excelToDelimited()


if __name__ == '__main__':
	main()

