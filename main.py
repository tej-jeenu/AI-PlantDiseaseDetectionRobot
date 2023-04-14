### Copyright Michael@bots4all
#%% Load modules
from IPython import get_ipython
import os
import numpy as np
import cv2 as cv
from urllib.request import urlopen
import socket
import sys
import json
import re
import matplotlib.pyplot as plt
import time
import shutil
from ultralytics import YOLO
import cv2
import psycopg2
from datetime import date
import pyautogui
from pynput.keyboard import Key, Controller

keyboard = Controller()


#%% Clear working space
#get_ipython().magic('clear')
#get_ipython().magic('reset -f')
#plt.close('all')

#%% Capture image from camera

conn = psycopg2.connect(user="postgres",
                        password="datta001",
                        host="127.0.0.1",
                        port="5432",
                        database="plantdb")
cursor = conn.cursor()
peoplenotified = []
numbersnotified = []
num = 0
cmd_no = 0


def send_whatsapp_message(msg: str, phonnum: str):
    import pywhatkit
    try:
        pywhatkit.sendwhatmsg_instantly(
            phone_no=phonnum, 
            message=msg,
            tab_close=True
        )
        time.sleep(15)
        pyautogui.click()
        time.sleep(2)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        print("Message sent!")
    except Exception as e:
        print(str(e))

def extractclasses(word):
    identifiedclasses = []
    word = str(word)
    newword = ""
    classes = ['Apple Scab', 'Apple', 'Apple rust', 'Bell_pepper spot', 'Bell_pepper', 'Blueberry', 'Cherry', 'Corn Gray spot', 'Corn blight', 'Corn rust', 'Peach', 'Potato early blight', 'Potato late blight', 'Potato', 'Raspberry', 'Soyabean', 'Soybean', 'Squash Powdery mildew', 'Strawberry', 'Tomato Early blight', 'Tomato Septoria spot', 'Tomato bacterial spot', 'Tomato late blight', 'Tomato mosaic virus', 'Tomato yellow virus', 'Tomato', 'Tomato mold', 'Tomato two spotted spider mites', 'grape black rot', 'grape']
    newword = word.replace("tensor","")
    for char in '()[].':
        newword = newword.replace(char,"")
    if(newword != ""):
        numclasses = newword.split(",")
        for n in numclasses:
            n = int(n)
            identifiedclasses.append(classes[n])
    identifiedclasses = list(dict.fromkeys(identifiedclasses))
    return identifiedclasses

def sentimentanalysis(classes):
    classes = list(classes)
    sentimentlist = []
    diseases = ['Apple Scab', 'Apple rust', 'Bell_pepper spot', 'Corn Gray spot', 'Corn blight', 'Corn rust', 'Potato early blight', 'Potato late blight', 'Squash Powdery mildew', 'Tomato Early blight', 'Tomato Septoria spot', 'Tomato bacterial spot', 'Tomato late blight', 'Tomato mosaic virus', 'Tomato yellow virus', 'Tomato mold', 'Tomato two spotted spider mites', 'grape black rot']
    for c in classes:
        if(c in diseases):
            sentimentlist.append('Disease')
        else:
            sentimentlist.append('Healthy')
    return sentimentlist

def capture():
    global cmd_no
    global num
    cmd_no += 1
    print(str(cmd_no) + ': capture image')
    cam = urlopen('http://192.168.4.1/capture')
    img = cam.read()
    img = np.asarray(bytearray(img), dtype = 'uint8')
    img = cv.imdecode(img, cv.IMREAD_UNCHANGED)
    #cv2.imwrite('pics\\' + str(num) + '.jpg', img)
    #cv.imshow('Camera', img)
    cv.waitKey(1)
    num = num + 1
    return img

#%% Send a command and receive a response
off = [0.007,  0.022,  0.091,  0.012, -0.011, -0.05]
def cmd(sock, do, what = '', where = '', at = ''):
    global cmd_no
    cmd_no += 1
    msg = {"H":str(cmd_no)} # dictionary
    if do == 'move':
        msg["N"] = 3
        what = ' car '
        if where == 'forward':
            msg["D1"] = 3
        elif where == 'back':
            msg["D1"] = 4
        elif where == 'left':
            msg["D1"] = 1
        elif where == 'right':
            msg["D1"] = 2
        msg["D2"] = at # at is speed here
        where = where + ' '
    elif do == 'stop':
        msg.update({"N":1,"D1":0,"D2":0,"D3":1})
        what = ' car'
    elif do == 'rotate':
        msg.update({"N":5,"D1":1,"D2":at}) # at is an angle here
        what = ' ultrasonic unit'
        where = ' '
    elif do == 'measure':
        if what == 'distance':
            msg.update({"N":21,"D1":2})
        elif what == 'motion':
            msg["N"] = 6
        what = ' ' + what
    elif do == 'check':
        msg["N"] = 23
        what = ' off the ground'
    msg_json = json.dumps(msg)
    print(str(cmd_no) + ': ' + do + what + where + str(at), end = ': ')
    try:
        sock.send(msg_json.encode())
    except:
        print('Error: ', sys.exc_info()[0])
        sys.exit()
    while 1:
        res = sock.recv(1024).decode()
        if '_' in res:
            break
    res = re.search('_(.*)}', res).group(1)
    if res == 'ok' or res == 'true':
        res = 1
    elif res == 'false':
        res = 0
    else:
        res = int(res)
    print(res)
    return res

def makeprediction(num):
    num = int(num)
    model = YOLO("50epochplantmodel.pt")
    classlist = []
    for i in range(num):
           img = capture()
           result = model.predict(source=img, show=True, conf=0.8)
           print(result[0].boxes.cls)
           classlist.extend(extractclasses(str(result[0].boxes.cls)))
           print(classlist)
    classlist = list(dict.fromkeys(classlist))
    return classlist


def movehalfmetre(num):
    num = int(num)
    for i in range(num):
       cmd(car, do = 'move', where = 'forward', at = '100')
    stopcar(0.1)

def rotatecar(direction):
    if(direction == "l"):
        cmd(car, do = 'move', where = 'left', at = '10')
    if(direction == "r"):
        cmd(car, do = 'move', where = 'right', at = '10')

def stopcar(duration):
    duration = int(duration)
    cmd(car, do='stop')
    time.sleep(duration)

def measuredistance():
    distance = 0
    distance = cmd(car, do = 'measure', what = 'distance')
    return distance

def rotatecamera(direction):
    distance = 0
    if(direction == "l"):
        cmd(car, do = 'rotate', at = '160')
    if(direction == "r"):
        cmd(car, do = 'rotate', at = '0')
    if(direction == "m"):
        cmd(car, do = 'rotate', at = '90')

#sql methods
def regx(pattern, word):
    word = str(word)
    for char in pattern:
        word = word.replace(char,"")
    return word

def addfarmer():
    f = open("command.txt", "r")
    data = str(f.readline())
    components = data.split("-")
    print(str(components))
    phonenum = ""
    phonenum = regx("()\n", components[3])
    cursor.execute("SELECT MAX(farmer_id) FROM farmers")
    num = regx("[](),",cursor.fetchall())
    if(num == "None"):
        num = 0
    else:
        num = int(num)
        num = num + 1
        num = str(num)
    cursor.execute("INSERT INTO farmers(farmer_id,farmer_name,farmer_jobkeywords,farmer_phonenumber) VALUES (%s,%s,%s,%s)",[num,components[1],phonenum,components[2]])
    conn.commit()
    retrieveandupdatetasks("addfarmer")

def removefarmer():
    global peoplenotified
    global numbersnotified
    f = open("command.txt", "r")
    data = str(f.readline())
    components = data.split("-")
    print(str(components))
    name = ""
    name = regx("\n", components[1])
    cursor.execute("DELETE FROM farmers WHERE farmer_name = %s",[name])
    conn.commit()
    retrieveandupdatetasks("deletefarmer")
    if(name in peoplenotified):
        time.sleep(5)
        index = peoplenotified.index(name)
        send_whatsapp_message("Hi " + name.split()[0] + ", your job role was removed recently, sorry if this caused any disruption",numbersnotified[index])
        peoplenotified.remove(peoplenotified[index])
        numbersnotified.remove(numbersnotified[index])


def addassoctreatmenttasks(twodimclasses):
    cursor.execute('TRUNCATE tasks')
    conn.commit()
    twodimclasses = list(twodimclasses)
    classes = ['Apple Scab', 'Apple', 'Apple rust', 'Bell_pepper spot', 'Bell_pepper', 'Blueberry', 'Cherry', 'Corn Gray spot', 'Corn blight', 'Corn rust', 'Peach', 'Potato early blight', 'Potato late blight', 'Potato', 'Raspberry', 'Soyabean', 'Soybean', 'Squash Powdery mildew', 'Strawberry', 'Tomato Early blight', 'Tomato Septoria spot', 'Tomato bacterial spot', 'Tomato late blight', 'Tomato mosaic virus', 'Tomato yellow virus', 'Tomato', 'Tomato mold', 'Tomato two spotted spider mites', 'grape black rot', 'grape']
    flattenedclasses = []
    for plantlist in twodimclasses:
        for plant in plantlist:
            flattenedclasses.append(plant)
    
    flattenedclasses = list(dict.fromkeys(flattenedclasses)) # removed repeats here
    for plant in flattenedclasses:
        cursor.execute('SELECT treatment_id,treatment_repeats FROM treatments WHERE plant_id = %s',[classes.index(plant)])
        treatmentvalues = cursor.fetchall()
        for valuetuple in treatmentvalues:
            cursor.execute('INSERT INTO tasks(task_treatment,task_nextdate,task_repeatsleft) VALUES (%s,%s,%s)',[int(valuetuple[0]),date.today(),int(valuetuple[1])])
            conn.commit()

def retrieveandupdatetasks(mode: str):
    classes = ['Apple Scab', 'Apple', 'Apple rust', 'Bell_pepper spot', 'Bell_pepper', 'Blueberry', 'Cherry', 'Corn Gray spot', 'Corn blight', 'Corn rust', 'Peach', 'Potato early blight', 'Potato late blight', 'Potato', 'Raspberry', 'Soyabean', 'Soybean', 'Squash Powdery mildew', 'Strawberry', 'Tomato Early blight', 'Tomato Septoria spot', 'Tomato bacterial spot', 'Tomato late blight', 'Tomato mosaic virus', 'Tomato yellow virus', 'Tomato', 'Tomato mold', 'Tomato two spotted spider mites', 'grape black rot', 'grape']
    cursor.execute('SELECT treatment_id,treatment_name,treatment_intervaldays,plant_id FROM tasks INNER JOIN treatments ON task_treatment = treatment_id WHERE task_nextdate = CURRENT_DATE')
    taskinfo = cursor.fetchall()
    oldlinesinfile = []
    linesinfile = []
    for tasktuple in taskinfo:
        linestring = ""
        linestring = "->  " + tasktuple[1] + " to any " + classes[int(tasktuple[3])] + " plants"
        oldlinestring = tasktuple[1] + " to any " + classes[int(tasktuple[3])] + " plants"
        linesinfile.append(linestring)
        oldlinesinfile.append(oldlinestring)
    
    cursor.execute('SELECT farmer_name,farmer_jobkeywords,farmer_phonenumber FROM farmers')
    farmerinfo = cursor.fetchall()
    
    twodimfarmerlist = []
    twodimwhatsapplist = []
    for line in linesinfile:
        personlist = []
        whatsapplist = []
        for farmertuple in farmerinfo:
            addperson = False
            keywordlist = str(farmertuple[1]).split(",")
            print(str(keywordlist))
            for keyword in keywordlist:
                if(keyword in str(line)):
                    addperson = True
            if(addperson == True):
                personlist.append(farmertuple[0])
                print(personlist)
                whatsapplist.append(farmertuple[2])
        twodimfarmerlist.append(personlist)
        twodimwhatsapplist.append(whatsapplist)
    
    jobrolesfilelines = []
    for farmertuple in farmerinfo:
        jobrolesfilelines.append(farmertuple[0] + "  role_keywords: " + farmertuple[1] + "  phone_number: " + farmertuple[2] + "\n")
    
    newlinesinfile = linesinfile
    for i in range(len(linesinfile)):
        newlinesinfile[i] = linesinfile[i] + " " + regx("'",str(twodimfarmerlist[i])) + '\n'
    
    with open("todaytasks.txt", "w") as file:
            file.writelines(newlinesinfile)
    file.close()
    with open("jobroles.txt", "w") as file:
            file.writelines(jobrolesfilelines)
    file.close()
    
    time.sleep(10)
    sendwhatsappmessages(twodimfarmerlist, twodimwhatsapplist, oldlinesinfile)

def taskscompleted():
    cursor.execute('SELECT treatment_id,treatment_intervaldays FROM tasks INNER JOIN treatments ON task_treatment = treatment_id WHERE task_nextdate = CURRENT_DATE')
    taskinfo = cursor.fetchall()
    for tasktuple in taskinfo:
        cursor.execute('UPDATE tasks SET task_nextdate = task_nextdate + %s,task_repeatsleft = task_repeatsleft - 1 WHERE task_treatment = %s',[tasktuple[1],int(tasktuple[0])])
        conn.commit() 
    cursor.execute('DELETE FROM tasks WHERE task_repeatsleft = -1')
    conn.commit()

def sendwhatsappmessages(twodimfarmerlist,twodimwhatsapplist,linesinfile):
    global peoplenotified
    global numbersnotified
    twodimfarmerlist = list(twodimfarmerlist)
    twodimwhatsapplist = list(twodimwhatsapplist)
    linesinfile = list(linesinfile)

    twodimmsgcontents = []
    flattenedfarmerlist = []
    flattenedwhatsapplist = []

    #here we are going to flatten the farmerlist and whatsapplist
    for farmers in twodimfarmerlist:
        for farmer in farmers:
            flattenedfarmerlist.append(farmer)
    
    for whatsappnumbers in twodimwhatsapplist:
        for whatsappnumber in whatsappnumbers:
            flattenedwhatsapplist.append(whatsappnumber)
    
    #we will then remove repeats in the flattenedfarmerlist
    newflattenedfarmerlist = list(dict.fromkeys(flattenedfarmerlist))

    for farmer in newflattenedfarmerlist:
        msgcontents = []
        for i in range(len(twodimfarmerlist)):
            if(farmer in twodimfarmerlist[i]):
                msgcontents.append(linesinfile[i])
        twodimmsgcontents.append(msgcontents)

    for i in range(len(newflattenedfarmerlist)):
        if(len(twodimmsgcontents[i]) > 1):
            stringmsg = "Hi " + str(newflattenedfarmerlist[i]).split()[0] + ", Please can you do the following tasks today: \n \n"
            for msg in twodimmsgcontents[i]:
                stringmsg = stringmsg + "-" + msg + "\n"
            #sendwhatsappmessagehere
            if(newflattenedfarmerlist[i] not in peoplenotified):
                send_whatsapp_message(stringmsg, flattenedwhatsapplist[flattenedfarmerlist.index(newflattenedfarmerlist[i])])
                peoplenotified.append(newflattenedfarmerlist[i])
                numbersnotified.append(flattenedwhatsapplist[flattenedfarmerlist.index(newflattenedfarmerlist[i])])
            #print(stringmsg + flattenedwhatsapplist[flattenedfarmerlist.index(newflattenedfarmerlist[i])])
        else:
            stringmsg = "Hi " + str(newflattenedfarmerlist[i]).split()[0] + ", Please can you " + twodimmsgcontents[i][0]
            #sendwhatsappmsghere
            if(newflattenedfarmerlist[i] not in peoplenotified):
                send_whatsapp_message(stringmsg, flattenedwhatsapplist[flattenedfarmerlist.index(newflattenedfarmerlist[i])])
                peoplenotified.append(newflattenedfarmerlist[i])
                numbersnotified.append(flattenedwhatsapplist[flattenedfarmerlist.index(newflattenedfarmerlist[i])])
            #print(stringmsg + flattenedwhatsapplist[flattenedfarmerlist.index(newflattenedfarmerlist[i])])
    

#shutil.rmtree('C:\\Users\\jeenu\\Desktop\\python programs\\PlantCheckerProject\\pics') #deletes pictures which were taken in the folder
#car movement controlled here

movementiters = 15
frames = 30
condition = False
while 1:
    rawcommand = ""
    if os.path.exists("command.txt"):
        f = open("command.txt", "r")
        rawcommand = f.read()
    if("PATH" in rawcommand):
        cv.namedWindow('Camera')
        cv.moveWindow('Camera', 0, 0)

        ip = "192.168.4.1"
        port = 100
        print('Connect to {0}:{1}'.format(ip, port))
        car = socket.socket()
        try:
          car.connect((ip, port))
        except:
          print('Error: ', sys.exc_info()[0])
          sys.exit()
        print('Connected!')

        print('Receive from {0}:{1}'.format(ip, port))
        try:
          data = car.recv(1024).decode()
        except:
          print('Error: ', sys.exc_info()[0])
          sys.exit()
        print('Received: ', data)

        f = open("pathdetails.txt", "r")
        repeats = int(f.read())
        twodimclasses = []
        twodimsentiment = []
        for i in range(repeats + 1): #extra 1 for calibrating motion
           print(i)
           rotatecamera("l") #in relation to positioning the camera
           movehalfmetre(movementiters)
           if(i > 0):
              classlist = []
              sentimentlist = []
              classlist = makeprediction(frames)
              sentimentlist = sentimentanalysis(classlist)
              twodimclasses.append(classlist)
              twodimsentiment.append(sentimentlist)
              print(str(twodimclasses))
              print(str(twodimsentiment))
        addassoctreatmenttasks(twodimclasses)
        #any file writing takes place here
        car.close()
        linesinfile = []
        n = 0.5
        for c in twodimclasses:
            collection = str(c)
            for char in "[]'":
                collection = collection.replace(char,"")
            if(collection == ""):
                collection = "no plants here"
            linesinfile.append(str(n) + "m: " + collection + "\n")
            n = n + 0.5
        with open("generalmap.txt", "w") as file:
            file.writelines(linesinfile)
        file.close()
        linesinfile = []
        n = 0.5
        Row = "|"
        Secondrow = "|"
        for d in twodimsentiment:
            if('Disease' in d):
                Row = Row + " X |"
            else:
                Row = Row + " - |"
            Secondrow = Secondrow + str(n) + "|"
            n = n + 0.5
        Row = Row + '\n'
        Secondrow = Secondrow + '\n'
        Thirdrow = "'| X |' implies diseased plants in that cell" +'\n'
        linesinfile = [Row, Secondrow, Thirdrow]
        with open("diseasemap.txt", "w") as file:
            file.writelines(linesinfile)
        file.close()         
        g = open("command.txt", "w")
        g.write("NONE")
        g.close()
    if("TASKINFO" in rawcommand):
        retrieveandupdatetasks("")
        g = open("command.txt", "w")
        g.write("NONE")
        g.close()
    elif("ADD" in rawcommand):
        addfarmer()
        g = open("command.txt", "w")
        g.write("NONE")
        g.close()
    elif("REMOVE" in rawcommand):
        removefarmer()
        g = open("command.txt", "w")
        g.write("NONE")
        g.close()
    elif("EXIT" in rawcommand):
        taskscompleted()
        g = open("command.txt", "w")
        g.write("NONE")
        g.close()
        quit()
    #general processing stuff 

    


