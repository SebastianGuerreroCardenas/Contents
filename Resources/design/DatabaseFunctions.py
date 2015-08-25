#sguerrer

#functions for managing Database
import dropbox
import io
import sys
import string
import copy
import random
import os.path
import time

#not included in the final version, it is here for testing
##########################################################
app_key = 'hb836zy9vopr0n6'
app_secret = 'vlf9cl35tcdzbr7'

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
client = dropbox.client.DropboxClient('116qlQWoAWAAAAAAAAAABW24IpLBPzt2mblm7QiTIxmiEFp3SVM8RVoubrP22Rsa')

##########################################################

def printshit():
	print 'hello'


#creates a file
def createTextFile(filename,content=''):
	assert(type(filename) == str)
	try:
		file = open(filename,'w')
		file.write(content)
		file.close()
	except:
		print "file could not be created, check if file already exists"
		sys.exit(0)




def readFile(filename, mode="rb"):
    # rt = "read text"
    with open(filename, mode) as fin:
        return fin.read()

#downloads a file to local directory
def downloadFile(filename):
	out = open(filename, 'wb')
	with client.get_file('/'+ filename) as f:
		out.write(f.read())
		out.close()

#creates a folder given a path and a foldername
def createFolder(path,foldername):
	client.file_create_folder('/'+ path +'/'+ foldername)



def save(filename):
	f = open(filename, 'rb')
	response = client.put_file('/'+filename, f,overwrite=True)

#makes a lsit of letters and numbers and returns one at random
def randomLetterOrNumber():
	letters = string.ascii_letters
	numbers = string.digits
	lettersAndNumbers = letters + numbers
	sizeOfLettersAndNumbers = len(lettersAndNumbers)
	index = random.randint(0,sizeOfLettersAndNumbers - 1)
	return lettersAndNumbers[index]

#make a random object id containg ten characters
def makeObjectId():
	objectId = ''
	sizeOfId = 10
	for char in xrange(sizeOfId):
		objectId += randomLetterOrNumber()
	return objectId


#Makes the file in the  local file and also online
#ColumnNames are written in a list of tuples that conatin the name and 
# in the second value it contains what type of item it is in string Ex. String, Interger, Boolean,
#List (str, bool, list , int)  EX. [('Name',str),('Newsletter',bool),('Friends',list),('Age',int)]
#names must not have underscores
def makeStringOfColumns(ColumnNames):
	topRowString = ''
	firstCol = "objectId_<type 'str'>;"
	topRowString += firstCol
	title = 0
	typeofcol = 1
	for i, col in enumerate(ColumnNames):
		if i != len(ColumnNames) - 1:
			topRowString += col[0] + '_' + str(col[1]) + ';'
		else:
			topRowString += col[0] + '_' + str(col[1])
	return topRowString


#ColumnNames = [('Name',str),('Newsletter',bool),('Friends',list),('Age',int)]

def createClass(className,ColumnNames):
	check = "accessed"
	if  os.path.isfile(className) == False:
		content = makeStringOfColumns(ColumnNames)
		createTextFile(className,content)
		createTextFile(check + className)
		save(check + className)
		save(className)
	else:
		downloadFile(className)
		downloadFile(check + className)


#createClass('user.txt', ColumnNames)

#simple struct class that we got from class
class Struct(object):
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)

	def __repr__(self):
		d = self.__dict__
		results = [type(self).__name__ + "("] 
		for key in sorted(d.keys()):
			if (len(results) > 1): results.append(", ")
			results.append(key + "=" + repr(d[key]))
		results.append(")")
		return "".join(results)

	def __eq__(self, other):
		return self.__dict__ == other.__dict__

	def __hash__(self):
		return hash(repr(self))


#converts a csv string into alist 
def csvToList(csv):
	csvList = []
	for line in csv.splitlines():
		obj = []
		for section in line.split(";"):
			obj.append(section)
		csvList.append(obj)
	return csvList

#evaluates all the string values in the string into what theit true value
def listEval(listOfObjects):
	newListOfObjects = copy.deepcopy(listOfObjects)
	for lists in xrange(len(listOfObjects)):
		for element in xrange(len(listOfObjects[lists])):
			try:
				value = listOfObjects[lists][element]
				value = eval(value)
				newListOfObjects[lists][element] = value
			except:
				pass
	return newListOfObjects

def listTocsv(csvlist):
	content = ''
	for row in csvlist:
		for i, section in enumerate(row):
			if i < len(row) - 1:
				content += str(section) + ';'
			else:
				content += str(section)
		content += '\n'
	return content.rstrip()


class Class(Struct):
	def __init__(self, className):
		self.filename = className
		self.isClass()
		self.csv_txt = readFile(self.filename, mode="rb")
		self.csv = listEval(csvToList(self.csv_txt))
		self.check = "accessed"
		self.cols = len(self.csv[0])
		self.typeDict = self.typePerCol()

	def update(self):
		self.csv_txt = readFile(self.filename, mode="rb")
		self.csv = listEval(csvToList(self.csv_txt))
		self.cols = len(self.csv[0])
		self.typeDict = self.typePerCol()

	def getCSVLIST(self):
		self.update()
		return self.csv

	def saveUpdates(self,CSV):
		self.lockAccess()
		self.update()
		OriginalCSV = self.csv
		if CSV[0] != OriginalCSV[0]:
			print "There is an error: You switched the names of Columns, That is not allowed"
			sys.unlockAccess()
			sys.exit(0)
		if len(CSV) != len(OriginalCSV):
			print "There is an error: You cannont delete Rows, you may only change values"
			sys.unlockAccess()
			sys.exit(0)
		for i, row in enumerate(OriginalCSV):
			if len(row) != len(CSV[i]):
				print "There is an error: You added extra values to row" + str(i)
				sys.unlockAccess()
				sys.exit(0)
			if row[0] != CSV[i][0]:
				print "There is an error: cannont change the unique object ID of your objects" 
				sys.unlockAccess()
				sys.exit(0)
			for j, value in enumerate(OriginalCSV):
				if self.typeDict[j] != str(type(CSV[i][j])):
					print "There is an error: one of your values doesnot match its column name type" 
					sys.unlockAccess()
					sys.exit(0)
		content = listTocsv(CSV)
		createTextFile(self.filename,content)
		save(self.filename)
		downloadFile(self.filename)
		self.unlockAccess()
		self.update()

		




		downloadFile(className)
		downloadFile(check + className)
		f = open(filename, 'rb')
		response = client.put_file('/'+filename, f,overwrite=True)



	def typePerCol(self):
		typeDict = {}
		firstCol = 0
		typeString = 1
		for i, col in enumerate(self.csv[firstCol]):
			colName = col.split('_')
			typeDict[i] = colName[typeString]
		return typeDict


	#determines if the class you are looking for exists in your app
	def isClass(self):
		try:
			downloadFile(self.filename)
		except:
			print "Error, either the Project Name or the Classname does not exist"
			sys.exit(0)

	#Checks if someone else is accessing the class of your choice, If it is 
	#being updated it waits until it can be accessed
	def canChange(self):
		filename = self.check + self.filename
		downloadFile(filename)
		BeingChecked = readFile(filename, mode="rb")
		count = 0
		while BeingChecked != '':
			time.sleep(1)
			downloadFile(filename)
			BeingChecked = readFile(filename, mode="rb")
			count += 1
			if count  == 5:
				print 'Server is busy!'
				return False 
		return True

	#when a change is going to be made into the class, it locks the file so no onw else can access it
	def lockAccess(self):
		lock = 'locked'
		filename = self.check + self.filename
		with open(filename,'a+') as myfile:
			myfile.write(lock)
			myfile.close
		save(filename)

	#unlocks the file at the end of a command so it can be accesd again
	def unlockAccess(self):
		unlock = ''
		filename = self.check + self.filename
		createTextFile(filename,unlock)
		save(filename)	

	#adds a row with all the given fields

	def checkIfValuesArePossible(self,inputs):
		start = 1
		for inputVal in inputs:
			valueType = str(type(inputVal))
			if valueType != self.typeDict[start]:
				return False
			start += 1
		return True

	def addRow(self,*inputs):
		inputs = list(inputs)
		objectID = 1
		if len(inputs) != self.cols - objectID:
			print ("Error: Wrong a amount of inputs places, should have " + str(self.cols - objectID)
					+ ". Make sure they are in the correct order. Reference back to your create class")
			sys.exit(0)
		if self.checkIfValuesArePossible(inputs) == False:
			print "One of the values you input is the wrong type that does not mach the Column type"
			sys.exit(0)
		if self.canChange():
			self.lockAccess()
			objID = makeObjectId()
			newRow = '\n' + str(objID) + ';'
			for i, val in enumerate(inputs):
				if i < len(inputs) - objectID:
					newRow += str(val) + ';'
				else:
					newRow += str(val)
			with open(self.filename,'a+') as myfile:
				myfile.write(newRow)
				myfile.close
			save(self.filename)
			downloadFile(self.filename)
			self.unlockAccess()
			self.update()

	#row number should n > 0, else it cannot delete
	def deleteRow(self, rowNum):
		self.lockAccess()
		self.update()
		CSVLIST = copy.deepcopy(self.csv)
		NewCSV = []
		if rowNum == 0 or rowNum > len(CSVLIST):
			print "required row does not exists"
			self.unlockAccess()
			sys.exit(0)
		for i , value in enumerate(CSVLIST):
			if i == rowNum:
				pass
			else:
				NewCSV += [value]
		print NewCSV
		content = listTocsv(NewCSV)
		createTextFile(self.filename,content)
		save(self.filename)
		downloadFile(self.filename)
		self.unlockAccess()
		self.update()

	#Just like the create a class function add the name and type in a tuple
	#the values it will set will be empty , and for boolean it will be set as False
	#if it is an int or float return to 0 or 0.0
	def addCol(self,ColumnNames):
		semiColon = ''
		under = '_'
		name = ColumnNames[0]
		typeOfValue = ColumnNames[1]
		ColName = semiColon + name + under + str(typeOfValue)
		value = None
		print "Step 1: ColName is equal to " + ColName
		if typeOfValue == bool: value = False
		elif typeOfValue == str: value = ''
		elif typeOfValue == list: value = []
		elif typeOfValue == int: value = 0
		elif typeOfValue == float: value = 0.0
		elif value == None: 
			print "value type does not exists"
			sys.exit(0)
		print "Step2: Value is equal to" + str(value)
		self.lockAccess()
		self.update()
		CSVLIST = copy.deepcopy(self.csv)
		for i in xrange(len(CSVLIST)):
			if i != 0:
				CSVLIST[i] += [value]
			else:
				CSVLIST[i] += [ColName]
		content = listTocsv(CSVLIST)
		createTextFile(self.filename,content)
		save(self.filename)
		downloadFile(self.filename)
		self.unlockAccess()
		self.update()


	def query(self,constraints, function):
		pass

	def show():
		pass

#newcheck = Class('user.txt')


#newcheck.addRow('Tifany', True, [2], 1,True)

#newcheck.addCol(('last',bool))
#print newcheck.typeDict

# when using this api or module, you must put into exsitance all the classes at the 
#beginning of your code, you must include the createClass() to intiate a new class, or if the
#app is starting the class already exsist it provides the most uptodatefile





