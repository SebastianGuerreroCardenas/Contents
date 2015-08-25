#sguerrer
#Sebastian Guerrero + section H
import dropbox
import io
import sys
import string
import copy
import random
import os.path
import time
import json

#intiatees flow with the server
def flowS(app_key = 'hb836zy9vopr0n6', app_secret = 'vlf9cl35tcdzbr7'):
	flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
	return flow

#Sets the client
def clientS(ClientID):
	client =  dropbox.client.DropboxClient(ClientID)
 	return client


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

#reads a file and gets the data
def readFile(filename, mode="rb"):
    # rt = "read text"
    with open(filename, mode) as fin:
        return fin.read()

#downloads a file to local directory
def downloadFile(client,filename):
	out = open(filename, 'wb')
	with client.get_file('/'+ filename) as f:
		out.write(f.read())
		out.close()

#creates a folder given a path and a foldername
def createFolder(client, path,foldername):
	client.file_create_folder('/'+ path +'/'+ foldername)

#save data to the cloud
def save(client,filename):
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

#returns the names
def classNames(client):
	listofclasses = []
	lock = '/accessed'
	folder_metadata = client.metadata('/')
	resp_dict = json.loads(json.dumps(folder_metadata,sort_keys=True,indent=4, separators=(',', ': ')))
	for files in resp_dict['contents']:
		className = files['path']
		className = className.encode()
		if className.startswith(lock) == False:
			listofclasses += [className[1:]]
		else:
			pass
	return listofclasses

#creates a class when the class has sevreal things
def createClass(client,className,ColumnNames):
	check = "accessed"
	listOFclasses = classNames(client)
	if  os.path.isfile(className) == False and className not in listOFclasses:
		content = makeStringOfColumns(ColumnNames)
		createTextFile(className,content)
		createTextFile(check + className)
		save(client,check + className)
		save(client,className)
	else:
		downloadFile(client,className)
		downloadFile(client,check + className)


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
	if csv == "objectId_<type 'str'>;":
		return [["objectId_<type 'str'>"]]
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

#makes a string out a list csv
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

#Class that neds a client and the class name and it has sevral functions inside
class Class(Struct):
	def __init__(self,client ,className):
		self.client = client
		self.filename = className
		self.isClass()
		self.csv_txt = readFile(self.filename, mode="rb")
		self.csv = listEval(csvToList(self.csv_txt))
		self.check = "accessed"
		self.cols = len(self.csv[0])
		self.typeDict = self.typePerCol()

	#updates data
	def update(self):
		self.csv_txt = readFile(self.filename, mode="rb")
		self.csv = listEval(csvToList(self.csv_txt))
		self.cols = len(self.csv[0])
		self.typeDict = self.typePerCol()

	#returns the csv
	def getCSVLIST(self):
		self.update()
		return self.csv

	#saves update and returns errors
	def saveUpdates(self,CSV):
		if self.canChange():
			self.lockAccess()
			self.update()
			OriginalCSV = self.csv
			if CSV[0] != OriginalCSV[0]:
				msg = "There is an error: You switched the names of Columns, That is not allowed"
				print msg
				self.unlockAccess()
				return msg
				sys.exit(0)
			if len(CSV) != len(OriginalCSV):
				msg = "There is an error: You cannont delete Rows, you may only change values"
				print msg
				self.unlockAccess()
				return msg
				sys.exit(0)
			for i, row in enumerate(OriginalCSV):
				if len(row) != len(CSV[i]):
					msg = "There is an error: You added extra values to row" + str(i)
					print msg
					self.unlockAccess()
					return msg
					sys.exit(0)
				if row[0] != CSV[i][0]:
					msg = "There is an error: cannont change the unique object ID of your objects" 
					print msg 
					self.unlockAccess()
					return msg
					sys.exit(0)
				for j, value in enumerate(row):
					print self.typeDict[j] , (CSV[i][j])
					if i > 0 and self.typeDict[j] != str(type(CSV[i][j])):
						msg = "There is an error: one of your values does not match its column name type" 
						print msg
						self.unlockAccess()
						return msg
						sys.exit(0)
			content = listTocsv(CSV)
			createTextFile(self.filename,content)
			save(self.client,self.filename)
			downloadFile(self.client,self.filename)
			self.unlockAccess()
			self.update()
			return None
		else:
			print 'Could not be updated'

	#returns types per columns 
	def typePerCol(self):
		if len(self.csv) == 1 and len(self.csv[0]) == 1:
			return {1:"<type 'str'>"}
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
			downloadFile(self.client,self.filename)
		except:
			print "Error, either the Project Name or the Classname does not exist"
			sys.exit(0)

	#Checks if someone else is accessing the class of your choice, If it is 
	#being updated it waits until it can be accessed
	def canChange(self):
		filename = self.check + self.filename
		downloadFile(self.client,filename)
		BeingChecked = readFile(filename, mode="rb")
		count = 0
		while BeingChecked != '':
			time.sleep(1)
			downloadFile(self.client,filename)
			BeingChecked = readFile(filename, mode="rb")
			count += 1
			if count  == 20:
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
		save(self.client,filename)

	#unlocks the file at the end of a command so it can be accesd again
	def unlockAccess(self):
		unlock = ''
		filename = self.check + self.filename
		createTextFile(filename,unlock)
		save(self.client,filename)	

	#adds a row with all the given fields
	def checkIfValuesArePossible(self,inputs):
		start = 1
		for inputVal in inputs:
			valueType = str(type(inputVal))
			if valueType != self.typeDict[start]:
				return False
			start += 1
		return True

	#adds rows and returns error
	def addRow(self,*inputs):
		if len(inputs) == 1 and type(inputs[0]) == list:
			inputs = inputs[0]
		else:
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
			save(self.client,self.filename)
			downloadFile(self.client,self.filename)
			self.unlockAccess()
			self.update()

	#row number should n > 0, else it cannot delete
	def deleteRow(self, rowNum):
		if self.canChange():
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
			content = listTocsv(NewCSV)
			createTextFile(self.filename,content)
			save(self.client,self.filename)
			downloadFile(self.client,self.filename)
			self.unlockAccess()
			self.update()
		else:
			print 'could not be updated'

	#Just like the create a class function add the name and type in a tuple
	#the values it will set will be empty , and for boolean it will be set as False
	#if it is an int or float return to 0 or 0.0
	def addCol(self,ColumnNames,One = False):
		under = '_'
		name = ColumnNames[0]
		typeOfValue = ColumnNames[1]
		ColName = name + under + str(typeOfValue)
		if One == True:
			if self.canChange():
				self.lockAccess()
				self.update()
				CSVLIST = copy.deepcopy(self.csv)
				CSVLIST = [CSVLIST[0] + [ColName]]
				content = listTocsv(CSVLIST)
				createTextFile(self.filename,content)
				save(self.client,self.filename)
				downloadFile(self.client,self.filename)
				self.unlockAccess()
				self.update()
				return None
			else:
				print 'Could not be updated'
		value = None
		if typeOfValue == bool: value = False
		elif typeOfValue == str: value = ''
		elif typeOfValue == list: value = []
		elif typeOfValue == int: value = 0
		elif typeOfValue == float: value = 0.0
		elif value == None:
			msg = "value type does not exists"
			print msg
			return msg
			sys.exit(0)
		if self.canChange():
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
			save(self.client,self.filename)
			downloadFile(self.client,self.filename)
			self.unlockAccess()
			self.update()
		else:
			print 'Could not be updated'

	#delete itself and its existence
	def deleteME(self):
		if self.canChange():
			self.client.file_delete('/'+self.filename)
			self.client.file_delete('/'+ self.check+ self.filename)
		else:
			print 'could not be updated'

	#returns a quiery nwith rows that have a value greater than
	def queryNumbersGreater(self,columnname,number):
		num = None
		returnValues = []
		for i,row in enumerate(self.csv):
			if colulmname in row:
				num = i
			if row[number] >= number:
				returnValues.append(row)
		return returnValues

	#returns a quiery nwith rows that have a value less than
	def queryNumbersLess(self,columnname,number):
		num = None
		returnValues = []
		for i,row in enumerate(self.csv):
			if colulmname in row:
				num = i
			if row[number] <= number:
				returnValues.append(row)
		return returnValues


################################################################################
#How you set uo or initilize the code

#how far technology can go foward
#ClientID = '116qlQWoAWAAAAAAAAAABW24IpLBPzt2mblm7QiTIxmiEFp3SVM8RVoubrP22Rsa'
#flow = flowS()
#c = clientS(ClientID)

#lol = Class(c, "pycirrus_users.txt")
#print lol.csv

################################################################################


# when using this api or module, you must put into exsitance all the classes at the 
#beginning of your code, you must include the createClass() to intiate a new class, or if the
#app is starting the class already exsist it provides the most uptodatefile





