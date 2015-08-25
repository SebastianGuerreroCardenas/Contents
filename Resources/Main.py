#sguerrer
#Sebastian Guerrero + section H
from Tkinter import *
import tkMessageBox
import tkSimpleDialog
import os
import subprocess
import pycirrus
import pycirrus2
import string
import dropbox
import io
import sys
import string
import copy
import random
import os.path
import time
import json
import urllib2

#checks wether there is safe connection to the internet
def Internet():
    loop_value = 1
    web = "http://www.google.com"
    while (loop_value == 1):
        try:
            urllib2.urlopen(web)
            return True
        except urllib2.URLError, e:
            time.sleep( 1 )
            return False
        else:
            loop_value = 0

#class that has th information of the user including their classs
class userClass(object):
    def __init__(self, ClientID):
        flow = pycirrus2.flowS()
        self.ClientID = ClientID
        self.client = pycirrus2.clientS(self.ClientID)
        self.classes = pycirrus2.classNames(self.client)
        self.csv = self.getAllCSV()
        self.dictypes = self.getdictypes()

    #gets all of the csv of all the classes the user has
    def getAllCSV(self):
        csv = {}
        for classes in self.classes:
            getcsvs = pycirrus2.Class(self.client, classes)
            csv[classes] = getcsvs.csv
        return csv

    #gets all the dict tyoes of the classes
    def getdictypes(self):
        types = {}
        for classes in self.classes:
            gettypes = pycirrus2.Class(self.client, classes)
            types[classes] = gettypes.typeDict
        return types

    #updates information
    def update(self):
        self.csv = self.getAllCSV()
        self.dictypes = self.getdictypes()
        self.classes = pycirrus2.classNames(self.client)

    #adds a specific row
    def addSpcificRow(self,name,results):
        c = pycirrus2.Class(self.client, name)
        c.addRow(results)

    #delets row
    def delSpecificRow(self,name,rownum):
        c = pycirrus2.Class(self.client, name)
        c.deleteRow(rownum)

    #creates anew class
    def newclass(self,name):
        pycirrus2.createClass(self.client,name,[])

    #deletes class
    def deleteClass(self,name):
        c = pycirrus2.Class(self.client, name)
        c.deleteME()

    #saves updated data
    def saveNewInfo(self,name,CSV):
        c = pycirrus2.Class(self.client, name)
        return c.saveUpdates(CSV)

    def addColumn(self,name,ColumnNames):
        c = pycirrus2.Class(self.client, name)
        c.addCol(ColumnNames)

    def addColumnOne(self,name,ColumnNames):
        c = pycirrus2.Class(self.client, name)
        c.unlockAccess()
        c.addCol(ColumnNames,One = True)

#dialog box for creating a column box
class ColumnDialog(tkSimpleDialog.Dialog):

    def body(self, master):

        message = "Name the columnname and \n select the type of value you want \n"
        Label(master, text=message).grid(row=0,columnspan=2)

        Label(master, text="Column Name:").grid(row=1)
        Label(master, text="Column Type:").grid(row=2)

        self.e1 = Entry(master)
        self.e1.grid(row=1, column=1)

        self.variable = StringVar(master)
        self.variable.set("<type 'str'>") # default value
        self.w = OptionMenu(master, self.variable, "<type 'str'>", "<type 'int'>","<type 'bool'>",str(type(0.0)),str(type([])))
        self.w.grid(row=2, column=1)

        return self.e1 # initial focus

    def apply(self):
        global canvas
        name = canvas.canvas.data["ClassSelected"]
        empty = "No Class Selected"
        csv = canvas.canvas.user.csv
        check = csv[name]
        first = str(self.e1.get())
        if first.count('_') > 0:
            message = "You cannont have an underscore. '_'"
            title = "Message"
            tkMessageBox.showinfo(title, message)
            return None
        second = str(self.variable.get())
        if name == empty:
            message = "You need to select a class"
            title = "Message"
            tkMessageBox.showinfo(title, message)
            return None
        elif len(check) == 1:
            pass
        else:
            title = "Adding a Column"
            coltitle = first
            coltype = second
            addingcolumn(coltitle, coltype,name)

#Adds one column when ther isnt any value
class ColumnONEDialog(tkSimpleDialog.Dialog):

    def body(self, master):

        message = "Name the columnname and \n select the type of value you want \n"
        Label(master, text=message).grid(row=0,columnspan=2)

        Label(master, text="Column Name:").grid(row=1)
        Label(master, text="Column Type:").grid(row=2)

        self.e1 = Entry(master)
        self.e1.grid(row=1, column=1)

        self.variable = StringVar(master)
        self.variable.set("<type 'str'>") # default value
        self.w = OptionMenu(master, self.variable, "<type 'str'>", "<type 'int'>","<type 'bool'>",str(type(0.0)),str(type([])))
        self.w.grid(row=2, column=1)

        return self.e1 # initial focus

    def apply(self):
        global canvas
        name = canvas.canvas.data["ClassSelected"]
        empty = "No Class Selected"
        csv = canvas.canvas.user.csv
        check = csv[name]
        first = str(self.e1.get())
        if first.count('_') > 0:
            message = "You cannont have an underscore. '_'"
            title = "Message"
            tkMessageBox.showinfo(title, message)
            return None
        second = str(self.variable.get())
        if name == empty:
            message = "You need to select a class"
            title = "Message"
            tkMessageBox.showinfo(title, message)
            return None
        elif len(check) == 1:
            title = "Adding a Column"
            coltitle = first
            coltype = second
            addingcolumn(coltitle, coltype,name,One =True)
        else:
            pass

#draws the user screen
def drawUserScreen(canvas,x = 1000,y= 600):
    global master
    canvas.data['csvInputs']= []
    canvas.data['toggleDelete'] = []
    classesList = Listbox(master)
    canvas.canvas.data["classesList"] = classesList
    canvas.delete(ALL)
    canvas.config(scrollregion=(0,0,x,y))
    classesList = canvas.canvas.data['classesList']
    canvas.create_window(75,200,window = classesList)
    classProjects = canvas.user.classes
    classesList.insert(END, "No Class Selected")
    for item in classProjects:
        classesList.insert(END, item)
    #drawing shapes
    canvas.create_rectangle(0,0,x + 1000 ,75,fill='grey',outline="grey")
    canvas.create_rectangle(0,0,150,y + 600,fill='grey',outline="grey")
    canvas.create_text(125, 40, text="PyCirrus!", fill="white", font="verdana 32 bold")
    canvas.create_rectangle(350,20,950,50,fill='white')
    #buttons
    selectClass = canvas.data['selectClass']
    canvas.create_window(75,100,window = selectClass)
    CreateClass = canvas.data['CreateClass']
    canvas.create_window(75,300,window = CreateClass)
    delClassButton = canvas.data['delClassButton']
    canvas.create_window(75,325,window = delClassButton)
    saveButton = canvas.data['saveButton']
    canvas.create_window(700,35,window = saveButton)
    addRowButton = canvas.data['addRowButton']
    canvas.create_window(500,35,window = addRowButton)
    delRowButton = canvas.data['delRowButton']
    canvas.create_window(400,35,window = delRowButton)
    addColButton = canvas.data['addColButton']
    canvas.create_window(600,35,window = addColButton)
    logOutButton = canvas.data['logOutButton']
    canvas.create_window(900,35,window = logOutButton)
    refreshButton = canvas.data['refreshButton']
    canvas.create_window(800,35,window = refreshButton)
    userSettingsButton = canvas.data['userSettingsButton']
    canvas.create_window(75,400,window=userSettingsButton)
    SendErrorButton = canvas.data['SendErrorButton']
    canvas.create_window(75,425,window=SendErrorButton)

#creates a school for a new row
class MyDialog(tkSimpleDialog.Dialog):

    def body(self, master):
        global canvas
        self.dictypes = self.Getdictypes(canvas)
        self.csv = self.Getcsv(canvas)

        message = "Add the right type\n of values for each column\n"
        Label(master, text=message).grid(row=0,columnspan=2)

        self.inputs = []
        self.inputBool = []
        self.placeInputs(master)
        try:
            return self.inputs[0]
        except:
            message = "Add a column first."
            title = "Error"
            tkMessageBox.showinfo(title, message)
            return None

    def placeBool(self,rows,master):
        variable = StringVar(master)
        variable.set(str(True)) # default value
        w = OptionMenu(master, variable, "True", "False")
        w.grid(row = rows, column=1)
        self.inputBool.append
        self.inputs.append(variable)

    def placeEntry(self,rows,master):
        e = Entry(master)
        e.grid(row = rows, column=1)
        self.inputs.append(e)

    def placeInputs(self,master):
        size = len(self.dictypes)
        m = 1
        for i in xrange(m,size):
            name = self.csv[0][i]
            Label(master, text=name).grid(row=i)
            if self.dictypes[i] == str(type(True)):
                self.placeBool(i,master)
            else:
                self.placeEntry(i,master)

    def Getcsv(self,canvas):
        name = canvas.canvas.data["ClassSelected"]
        canvas.user.update()
        csv = canvas.user.csv
        csv = csv[name]
        return csv

    def Getdictypes(self,canvas):
        name = canvas.canvas.data["ClassSelected"]
        canvas.user.update()
        #csv = canvas.user.csv
        dictypes = canvas.user.dictypes
        dictypes = dictypes[name]
        return dictypes

    def addrowToClass(self,canvas,results):
        name = canvas.canvas.data["ClassSelected"]
        canvas.user.addSpcificRow(name,results)


    def listEval(self,listOfObjects):
        newListOfObjects = copy.deepcopy(listOfObjects)
        for element in xrange(len(listOfObjects)):
            try:
                value = listOfObjects[element].strip()
                value = eval(value)
                newListOfObjects[element] = value
            except:
                pass
        return newListOfObjects

    def checkIfTrue(self,results):
        size = len(self.dictypes)
        m = 1
        for i in xrange(m,size):
            if self.dictypes[i] != str(type(results[i -m])):
                return False
        return True


    def apply(self):
        results= []
        global canvas
        for value in self.inputs:
            try:
                result = str(value.get())
            except:
                result = str(self.inputBool.pop().get())
            results.append(result)
        results = self.listEval(results) 
        if self.checkIfTrue(results):
            self.addrowToClass(canvas,results)
        else:
            message = "One of your values had the wrong type."
            title = "Error"
            tkMessageBox.showinfo(title, message)
            return True

#saves data
def saveButtonPressed():
    global canvas
    name = canvas.canvas.data["ClassSelected"]
    names = canvas.canvas.user.csv[name]
    names = names[0]
    rawData = canvas.data['csvInputs']
    DataOutput = []
    check = False
    DataOutput.append(names)
    for i, row in enumerate(rawData):
        newRow= []
        for j, value in enumerate(row):
            if i == 0:
                check = False
            else:
                check = True
                newRow += [value.get()]
        if check:
            DataOutput.append(newRow)
    CSV = pycirrus2.listEval(DataOutput)
    msg = canvas.canvas.user.saveNewInfo(name,CSV)
    if msg == None:
        refreshButtonPressed()
    else:
        message = msg
        title = "Error"
        tkMessageBox.showinfo(title, message)
        refreshButtonPressed()

#adds row button
def addRowButtonPressed():
    global canvas
    name = canvas.canvas.data["ClassSelected"]
    empty = "No Class Selected"
    canvas.user.update()
    csv = canvas.user.csv
    dictypes = canvas.user.dictypes
    dictypes = dictypes[name]
    check = csv[name]
    if len(check[0]) == 1:
        message = "Add a Column First"
        title = "Message"
        tkMessageBox.showinfo(title, message)
        return None
    if name == empty:
        message = "You need to select a class"
        title = "Message"
        tkMessageBox.showinfo(title, message)
    else:
        title='Add Row'
        if MyDialog(canvas,title):
            refreshButtonPressed()

#deletes a row that it selected
def delRowButtonPressed():
	global canvas
	name = canvas.canvas.data["ClassSelected"]
	for part in canvas.canvas.data['toggleDelete']:
		if part.get() != 0:
			canvas.canvas.user.delSpecificRow(name,part.get())
	refreshButtonPressed()

#adding a column
def addingcolumn(coltitle, coltype,name , One = False):
    global canvas
    if coltype == "<type 'str'>":
        coltype = str
    elif coltype == "<type 'int'>":
        coltype = int
    elif coltype == "<type 'bool'>":
        coltype = bool
    elif coltype == str(type(0.0)):
        coltype = float
    elif coltype == str(type([])):
        coltype = list
    if One == True:
        ColumnNames = (coltitle,coltype)
        canvas.canvas.user.addColumnOne(name,ColumnNames)
    else:
        ColumnNames = (coltitle,coltype)
        canvas.canvas.user.addColumn(name,ColumnNames)
    refreshButtonPressed()

#adds acolumn when it pressed
def addColButtonPressed():
    global canvas
    name = canvas.canvas.data["ClassSelected"]
    csv = canvas.canvas.user.csv
    check = csv[name]
    if len(check) == 1:
        title = "Add Column name"
        results = ColumnONEDialog(canvas, title)
    else:
        title = "Adding a Column"
        results = ColumnDialog(canvas, title)

#logs out
def logOutButtonPressed():
    global canvas
    global master
    init(master,canvas)

#refreshed button
def refreshButtonPressed():
    global canvas
    drawChart(canvas,canvas.canvas.data["ClassSelected"])

#draws home screen
def drawHomeTextAndShapes(canvas):
    canvas.delete(ALL)
    canvas.config(scrollregion=(0,0,1000,600))
    #Title
    canvas.create_text(500, 100, text="PyCirrus!", fill="white", font="verdana 45 bold")
    #Left side names for boxes
    canvas.create_text(255, 200, text="Username:", fill="white", font="verdana 20", anchor=E)
    canvas.create_text(255, 250, text="Password:", fill="white", font="verdana 20", anchor=E)
    #Right side names for boxes
    canvas.create_text(722, 200, text="First Name:", fill="white", font="verdana 20", anchor=E)
    canvas.create_text(722, 250, text="Last Name:", fill="white", font="verdana 20", anchor=E)
    canvas.create_text(722, 300, text="Username:", fill="white", font="verdana 20", anchor=E)
    canvas.create_text(722, 350, text="Password:", fill="white", font="verdana 20", anchor=E)
    canvas.create_text(722, 400, text="Client:", fill="white", font="verdana 20", anchor=E)
    #line in middle
    canvas.create_line(500,150,500,500,fill="white",width=5)

def drawHomeScreen(canvas):
    if Internet():
        canvas.data['user'] = None
        drawHomeTextAndShapes(canvas)
        #Buttons
        SignIN = canvas.data['SignIN']
        canvas.create_window(333,300,window = SignIN)
        SignUP = canvas.data['SignUP']
        canvas.create_window(800,450,window = SignUP)
        Instructions = canvas.data['Instructions']
        canvas.create_window(500,550,window = Instructions)
        getpy2 = canvas.data['getpy2']
        canvas.create_window(500,575,window = getpy2)
        #TextBoxesLeft Side
        UsernameSI = canvas.canvas.data['UsernameSI']
        canvas.create_window(333,200,window = UsernameSI)
        PasswordSI = canvas.canvas.data['PasswordSI']
        canvas.create_window(333,250,window = PasswordSI)
        #textBoxesRight Side
        FName = canvas.canvas.data['FName']
        canvas.create_window(800,200,window = FName)
        LName = canvas.canvas.data['LName']
        canvas.create_window(800,250,window = LName)
        UsernameSU = canvas.canvas.data['UsernameSU']
        canvas.create_window(800,300,window = UsernameSU)
        PasswordSU = canvas.canvas.data['PasswordSU']
        canvas.create_window(800,350,window = PasswordSU)
        Client = canvas.canvas.data['Client']
        canvas.create_window(800,400,window = Client)
    else:
        message = "You are not connected to the Internet."
        title = "Message"
        tkMessageBox.showinfo(title, message)

#brings out the intructution    
def InstructionsPressed():
    filename = 'design/instructions.pdf'
    subprocess.call(['open', filename])

#delivers the pycirrus2 module
def getpy2Pressed():
    filename = 'design/pycirrus2.py'
    subprocess.call(['open', filename])

#checks if values are filled
def valuesFilled(values):
    for value in values:
        if value == str():
            return False
    return True

#returns what row the user is on
def locationOFUser(CSV, username):
    locOfUser = 3
    Password = 4
    for i, row in enumerate(CSV):
        if username == row[locOfUser]:
            return row[Password]
    return None

#returns the client
def locationOFclient(CSV, username):
    locOfUser = 3
    client = 5
    for i, row in enumerate(CSV):
        if username == row[locOfUser]:
            return row[client]
    return None

#logs in a user
def SignINPressed():
    global canvas
    try:
        users = pycirrus.Class('pycirrus_users.txt')
        csv = users.csv
        UsernameSI = canvas.canvas.data['UsernameSI']
        PasswordSI = canvas.canvas.data['PasswordSI']
        SignINvalues = [UsernameSI.get().strip(),hash(PasswordSI.get().strip())]
        Password = locationOFUser(csv,SignINvalues[0])
        ClientID = locationOFclient(csv,SignINvalues[0])
        if Password == None:
            message = "User does not exist."
            title = "Error"
            tkMessageBox.showinfo(title, message)
            drawHomeScreen(canvas)
        elif Password != SignINvalues[1]:
            message = "Wrong Password."
            title = "Error"
            tkMessageBox.showinfo(title, message)
            drawHomeScreen(canvas)
        else:
            canvas.data['user'] = SignINvalues[0]
            canvas.user = userClass(ClientID)
            drawUserScreen(canvas)
    except:
        #incase their client cannot join
        message = "Your clientID is wrong so make another user"
        title = "Error"
        tkMessageBox.showinfo(title, message)
        drawHomeScreen(canvas)

#checks if the user exists
def checkIfUserExists(csv, username):
    for row in csv:
        for i, value in enumerate(row):
            if i == 3 and value == username:
                return False
    return True

#adds a user to the database
def SignUPPressed():
    global canvas
    users = pycirrus.Class('pycirrus_users.txt')
    csv = users.csv
    FName = canvas.canvas.data['FName']
    LName = canvas.canvas.data['LName']
    UsernameSU = canvas.canvas.data['UsernameSU']
    PasswordSU = canvas.canvas.data['PasswordSU']
    Client = canvas.canvas.data['Client']
    SignUPValues = [FName.get().strip(),LName.get().strip(),UsernameSU.get().strip(),hash(PasswordSU.get().strip()),Client.get().strip()]
    username = SignUPValues[2]
    if valuesFilled(SignUPValues) == False:
        message = "Looks like you forgot to fill in a field"
        title = "Error"
        tkMessageBox.showinfo(title, message)
        drawHomeScreen(canvas)
    elif checkIfUserExists(csv, username) == False:
        message = "Looks like the username you are using already exists"
        title = "Error"
        tkMessageBox.showinfo(title, message)
        drawHomeScreen(canvas)
    else:
        users.addRow(SignUPValues)
        message = "You can Now Login"
        title = "Message"
        tkMessageBox.showinfo(title, message)
        logOutButtonPressed()

#draws label
def drawLabels(canvas,x,y,textinput):
    global master
    textinput = textinput.split('_')
    textinput = textinput[0]
    L = Label(master ,text=textinput, bg= 'grey',height=2,width=15)
    canvas.create_window(x,y,window = L)
    return L 

#draws the square and toggle button
def drawToggle(canvas,y,value,x= 200):
    global master
    var = IntVar()
    var.set(0)
    c = Checkbutton(master,  variable=var,onvalue=value)
    canvas.create_window(x,y,window = c)
    return var

#draws boolean
def drawBoolean(canvas,x,y,value):
    global master
    variable = StringVar(master)
    variable.set(str(value)) # default value
    w = OptionMenu(master, variable, "True", "False")
    canvas.create_window(x,y,window = w)
    return variable

#draws the text box
def drawEntry(canvas,x,y,value):
    global master
    e = Entry(master,width= 13)
    e.insert(END, str(value)) 
    canvas.create_window(x,y,window = e)
    return e

#draw the inputs 
def drawInputs(canvas,x,y,value,typeOF):
    valueType = str(type(value))
    if valueType == str(typeOF) and valueType == str(type(True)):
        return drawBoolean(canvas,x,y,value)
    else:
        return drawEntry(canvas,x,y,value)

#draws the errod fialog box
class errorDialog(tkSimpleDialog.Dialog):

    def body(self, master):
        global canvas
        message = "tell the type of error you are experience\n be detailed and we will get back right to you."
        Label(master, text=message).grid(row=0,columnspan=2)


        self.e1 = Entry(master)
        self.e1.grid(row=1, column=0,rowspan=2,columnspan=2)


        return self.e1 # initial focus

    def apply(self):
        global canvas
        import time
        user = canvas.canvas.data['user']
        users = pycirrus.Class('errorreports.txt')
        time = time.strftime("%I:%M:%S") + time.strftime("%d/%m/%Y")
        error = str(self.e1.get().strip())
        users.addRow(user,error,time)


#sends error
def SendErrorButtonPressed():
    global canvas
    title = 'Error Report'
    errorDialog(canvas,title)
    refreshButtonPressed()
    
#change settings
def userSettingsButtonPressed():
    global canvas
    currentuser = canvas.canvas.data['user']
    users = pycirrus.Class('pycirrus_users.txt')
    csv = users.csv
    userrow = None
    for i,row in enumerate(csv):
        if currentuser == row[3]:
            userrow = row
    drawUserScreen(canvas)
    saveChangesButton = canvas.data['saveChangesButton']
    canvas.create_window(500,400,window=saveChangesButton)
    canvas.create_text(500, 100, text="Change your Settings.", fill="white", font="verdana 20")

    canvas.create_text(425, 150, text="First Name:", fill="white", font="verdana 20", anchor=E)
    changeFName = canvas.data['changeFName']
    changeFName.insert(END, userrow[1])
    canvas.create_window(500,150,window=changeFName)

    canvas.create_text(425, 200, text="Last Name:", fill="white", font="verdana 20", anchor=E)
    changeLName = canvas.data['changeLName']
    changeLName.insert(END, userrow[2])
    canvas.create_window(500,200,window=changeLName)

    canvas.create_text(425, 250, text="User Name:", fill="white", font="verdana 20", anchor=E)
    changeusername = canvas.data['changeusername']
    changeusername.insert(END, userrow[3])
    canvas.create_window(500,250,window=changeusername)

    canvas.create_text(425, 300, text="Confirm Password:", fill="white", font="verdana 20", anchor=E)
    confirmPassword = canvas.data['confirmPassword']
    canvas.create_window(500,300,window=confirmPassword)

    canvas.create_text(425, 350, text="New Password:", fill="white", font="verdana 20", anchor=E)
    changePassword = canvas.data['changePassword']
    canvas.create_window(500,350,window=changePassword)

#checks if the row is empty
def rowempty(row):
    for item in row:
        if item == '' or item  == 0:
            return True
    return False

#saves any changes
def saveChangesButtonPressed():
    global canvas
    currentuser = canvas.canvas.data['user']
    users = pycirrus.Class('pycirrus_users.txt')
    csv = users.csv
    changeFName = canvas.data['changeFName']
    changeLName = canvas.data['changeLName']
    changeusername = canvas.data['changeusername']
    confirmPassword = canvas.data['confirmPassword']
    changePassword = canvas.data['changePassword']
    userrow = None
    rowlocation = None
    for i,row in enumerate(csv):
        if currentuser == row[3]:
            userrow = row
            rowlocation = i
    newdata = [changeFName.get().strip(),changeLName.get().strip(),changeusername.get().strip() ,hash(confirmPassword.get().strip()),hash(changePassword.get().strip())]
    if rowempty(newdata):
        message = "A value is empty."
        title = "Error"
        tkMessageBox.showinfo(title, message)
    elif newdata[2] not in userrow:
        message = "Your confirmed password is wrong\nmake sure it is your original Password"
        title = "Error"
        tkMessageBox.showinfo(title, message)
    else:
        csv = users.getCSVLIST()
        csv[rowlocation][1] = newdata[0]
        csv[rowlocation][2] = newdata[1]
        csv[rowlocation][3] = newdata[2]
        csv[rowlocation][4] = newdata[4]
        users.saveUpdates(csv)
        drawUserScreen(canvas)

#draws the data
def drawChart(canvas,name):
    empty = "No Class Selected"
    canvas.user.update()
    csv = canvas.user.csv
    dictypes = canvas.user.dictypes
    labels = 0
    m = 115
    w = 50
    if name == empty:
        drawUserScreen(canvas)
    else:
        csv = csv[name]
        dictypes = dictypes[name]
        canvas.data['csv'] = csv
        maxwidth = 300 + m * len(csv[0])
        maxHeight = 200+ w * len(csv)
        #canvas.data['csvInputs']
        drawUserScreen(canvas,maxwidth,maxHeight)
        for i, row in enumerate(csv):
            cols = []
            if i != labels:
                canvas.data['toggleDelete'].append(drawToggle(canvas,200 + w*i,i))
            for j, value in enumerate(row):
                if i == labels:
                    cols.append(drawLabels(canvas,300 + m*j,200+ m*i,value))
                else:
                    cols.append(drawInputs(canvas,300 + m*j,200+ w*i,value,dictypes[j]))
            canvas.data['csvInputs'].append(cols)

#draws the class that is selected
def selectClassPressed():
    global canvas
    classesList = canvas.canvas.data['classesList']
    canvas.canvas.data["ClassSelected"] = classesList.get(ACTIVE)
    drawChart(canvas,canvas.canvas.data["ClassSelected"])

#adds a class
class ClassDialog(tkSimpleDialog.Dialog):

    def body(self, master):

        message = "Name the class but do\n not add any underscores in the \n name '_', and add .txt at the end\n"
        Label(master, text=message).grid(row=0,columnspan=2)

        Label(master, text="Name:").grid(row=1)

        self.e1 = Entry(master)

        self.e1.grid(row=1, column=1)

        return self.e1 # initial focus

    def apply(self):
        first = str(self.e1.get())
        if first.endswith('.txt') == False:
            message = "Dont forget to add the '.txt' "
            title = "Error"
            tkMessageBox.showinfo(title, message)
            return None
        elif first.count('_'):
            message = "You cannont have an underscore '_' "
            title = "Error"
            tkMessageBox.showinfo(title, message)
            return None
        elif first.count(';'):
            message = "You cannont have an semicolon ';' "
            title = "Error"
            tkMessageBox.showinfo(title, message)
            return None
        else:
            global canvas
            canvas.canvas.user.newclass(first)
            canvas.canvas.user.update()

def delClassButtonPressed():
    global canvas
    name = canvas.canvas.data["ClassSelected"]
    canvas.canvas.data["ClassSelected"] = "No Class Selected"
    refreshButtonPressed()
    if name == 'No Class Selected':
        message = "You Have to select a class."
        title = "Error"
        tkMessageBox.showinfo(title, message)
        return None
    message = "Are you sure you want to delete " + name + '?\n the program will terminate in order to delete the file.'
    title = "Delete"
    response = tkMessageBox.askquestion(title, message)
    yes = 'yes'
    if response == yes:
        canvas.canvas.user.deleteClass(name)
        refreshButtonPressed()
    else:
        return None

def CreateClassPressed():
    global canvas
    ClassDialog(canvas)
    refreshButtonPressed()

#all the data the count adds
def init(master,canvas):
    canvas.data['user'] = None
    canvas.data['csv'] = {}
    canvas.data['csvInputs'] = []
    canvas.data['toggleDelete'] = []
    SignIN = Button(canvas, text="Sign In", command=SignINPressed)
    canvas.data["SignIN"] = SignIN
    SignUP = Button(canvas, text="Sign Up", command=SignUPPressed)
    canvas.data["SignUP"] = SignUP
    Instructions = Button(canvas, text="Instructions", command=InstructionsPressed)
    canvas.data["Instructions"] = Instructions
    getpy2 = Button(canvas, text="Get PyCirrus2", command=getpy2Pressed)
    canvas.data["getpy2"] = getpy2
    #SI = Sign In , SU = Sigm UP
    UsernameSI = Entry(canvas)
    canvas.data["UsernameSI"] = UsernameSI
    PasswordSI = Entry(canvas, show="*")
    canvas.data["PasswordSI"] = PasswordSI
    #right side text boxes
    FName = Entry(canvas)
    canvas.data["FName"] = FName
    LName = Entry(canvas)
    canvas.data["LName"] = LName
    UsernameSU = Entry(canvas)
    canvas.data["UsernameSU"] = UsernameSU
    PasswordSU = Entry(canvas, show="*")
    canvas.data["PasswordSU"] = PasswordSU
    Client = Entry(canvas)
    canvas.data["Client"] = Client
    buttons(master,canvas)
    canvas.pack()
    drawHomeScreen(canvas)

#adds buttons to the data
def buttons(master,canvas):
     #logged in user scrolls
    classesList = Listbox(master)
    canvas.data["classesList"] = classesList
    #buttons for class list
    selectClass = Button(canvas, text="Select Class",width = 16,command=selectClassPressed)
    canvas.data["selectClass"] = selectClass
    CreateClass = Button(canvas, text="Create Class",width = 16, command=CreateClassPressed)
    canvas.data["CreateClass"] = CreateClass
    canvas.data["ClassSelected"] = "No Class Selected"
    #scroll
    scrollbar = Scrollbar(canvas)
    canvas.data['scrollbar'] = scrollbar
    #buttons for editing table
    saveButton = Button(canvas, text="Save",width = 10,command=saveButtonPressed)
    canvas.data["saveButton"] = saveButton
    addRowButton = Button(canvas, text="Add Row",width = 10, command=addRowButtonPressed)
    canvas.data["addRowButton"] = addRowButton
    delRowButton = Button(canvas, text="Delete Row(s)",width = 10, command=delRowButtonPressed)
    canvas.data["delRowButton"] = delRowButton
    addColButton = Button(canvas, text="Add Column",width = 10, command=addColButtonPressed)
    canvas.data["addColButton"] = addColButton
    logOutButton = Button(canvas, text="Log Out",width = 10, command=logOutButtonPressed)
    canvas.data["logOutButton"] = logOutButton
    refreshButton = Button(canvas, text="Refresh",width = 10, command=refreshButtonPressed)
    canvas.data["refreshButton"] = refreshButton
    delClassButton = Button(canvas, text="Delete Class",width = 16, command=delClassButtonPressed)
    canvas.data["delClassButton"] = delClassButton
    userSettingsButton = Button(canvas, text="User Settings", width = 16, command = userSettingsButtonPressed)
    canvas.data["userSettingsButton"] = userSettingsButton 
    SendErrorButton = Button(canvas, text="Send Error", width = 16, command = SendErrorButtonPressed)
    canvas.data["SendErrorButton"] = SendErrorButton
    saveChangesButton = Button(canvas, text="Save Changes", width = 16, command = saveChangesButtonPressed)
    canvas.data["saveChangesButton"] = saveChangesButton
    changeFName = Entry(canvas)
    canvas.data["changeFName"] = changeFName
    changeLName = Entry(canvas)
    canvas.data["changeLName"] = changeLName
    confirmPassword = Entry(canvas)
    canvas.data["confirmPassword"] = confirmPassword
    changePassword = Entry(canvas)
    canvas.data["changePassword"] = changePassword
    changeusername = Entry(canvas)
    canvas.data["changeusername"] = changeusername

#deletes files that do nt belong
def ClosingApp():
    ListOfExistingFiles= ['Competitive Analysis.docx','DatabaseFunctions.py','Instructions.pdf','Interface.py','interface3.py','timeSheet.txt','User Stories.pdf','Readme.txt','pycirrus2.py','pycirrus.py','Project Proposal.docx','pycirrus2.pyc','.DS_Store','__boot__.py','__error__.sh','include','PyCirrus.icns','site.pyc','pycirrus.pyc','Main.py']
    currentPath = os.path.dirname(os.path.realpath(__file__))
    onlyfiles = [ f for f in os.listdir(currentPath) if os.path.isfile(os.path.join(currentPath,f)) ]
    filesToDelete = []
    for filesinDirectory in onlyfiles:
        if filesinDirectory not in ListOfExistingFiles:
            filesToDelete.append(filesinDirectory)
    for files in filesToDelete:
        os.remove(files)
    master.destroy()
    master.quit()

#starts the application
def start():
    global master
    master=Tk()
    frame=Frame(master,width=1000,height=600)
    frame.grid(row=0,column=0)
    global canvas
    canvas=Canvas(frame,bg='light blue',width=1000,height=600,scrollregion=(0,0,1000,600))
    hbar=Scrollbar(frame,orient=HORIZONTAL)
    hbar.pack(side=BOTTOM,fill=X)
    hbar.config(command=canvas.xview)
    vbar=Scrollbar(frame,orient=VERTICAL)
    vbar.pack(side=RIGHT,fill=Y)
    vbar.config(command=canvas.yview)
    canvas.config(width=1000,height=600)
    canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    canvas.pack(side=LEFT,expand=True,fill=BOTH)
    master.canvas = canvas.canvas = canvas
    canvas.data = { }
    canvas.user = None
    init(master, canvas)
    master.protocol('WM_DELETE_WINDOW', ClosingApp) 
    master.mainloop()

start()


