

# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 23:03:14 2023
@author: tooth
"""

def screenshot():
    import pygetwindow    
    import pyautogui    
    import numpy as np
    from ctypes import windll
    
    window = pygetwindow.getWindowsWithTitle('umamusume')[0]
    h = windll.user32.FindWindowA(b'Shell_TrayWnd', None)
    
    left=window.left
    top=window.top
    #print(window.size)
    
    
    if window.width <window.height and (top !=0 or (window.height!=1047) ):
        windll.user32.ShowWindow(h, 9)
        window.resizeTo(583,1047)
        window.moveTo(left,0)
    elif window.width >window.height:
        windll.user32.ShowWindow(h, 0)
        window.resizeTo(1940,1120)
        window.moveTo(-10,-30)
        
        
    top=window.top
    left=window.left
    img = pyautogui.screenshot(region=(left+10,top+30,window.width-20,window.height-45))
    open_cv_image = np.array(img)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    data=processScreenshot(open_cv_image)
    
    return data

def jsonProcess(skill,type):
    
    import Levenshtein
    import json
    
    if type==0:
        data = open('./js/female_event_datas.json','r',encoding="utf-8")
    else:
        data = open('./js/male_event_datas.json','r',encoding="utf-8")
    data = json.load(data)
    choice=[]
    tmp=None
    
    


    for i in skill:        
        print("skill:--------------"+i+"---end")
        choRule=round(len(i)/2)-1
        if(len(i)<=3):
            choRule=1
        for j in data:
           
            for k in j["choices"]:
                if len(skill)==len(j["choices"]):
                    if len(k['n'])>=len(i)-2 and len(k['n'])<=len(i)+2:
                        distance2 = Levenshtein.distance(i,k['n'])
                        if(distance2<=choRule):
                            j["distance2"]=distance2
                            if j not in choice:
                                choice.append(j)
    if(len(choice)>=1):
        for i in range(len(choice)):
            for j in range(i+1,len(choice)):
                if choice[j]["distance2"]<choice[i]["distance2"]:
                    tmp=choice[i]
                    choice[i]=choice[j]
                    choice[j]=tmp
                elif choice[j]["distance2"]==choice[i]["distance2"]:
                    tmpA=0
                    tmpB=0
                    for l in range(len(choice[i]["choices"])):
                        # print("--------skill----------")
                        # print(skill[l])
                        # print("-----------------------")
                        
                        # print("--------target----------")
                        # print(choice[i]["choices"][l]["n"])
                        # print("-----------------------")
                        tmpA += Levenshtein.distance(choice[i]["choices"][l]["n"],skill[l])
                        #print(tmpA)
                    for k in range(len(choice[j]["choices"])):
                        # print("--------skill----------")
                        # print(skill[k])
                        # print("-----------------------")
                        
                        # print("--------target----------")
                        # print(choice[j]["choices"][k]["n"])
                        # print("-----------------------")
                        tmpB += Levenshtein.distance(choice[j]["choices"][k]["n"],skill[k])
                        #print(tmpB)

                    if tmpB<tmpA:
                        tmp=choice[i]
                        choice[i]=choice[j]
                        choice[j]=tmp
                        
    if len(choice)>=1:
        #print(choice)
        tmp=choice[0]
    #print (tmp)
    return tmp
    

def processScreenshot(image):
    
    #title=cv2Process(image,0)
    skill=cv2Process(image,1)
    data=None
    try :
        if(len(skill)>=2 and len(skill)<=6):            
            data=jsonProcess(skill,0)
    except Exception as e:
        tryEx(e)
        data=None
    return(data)


def cv2Process(img,type):
    import pytesseract
    import cv2
    import numpy as np  
    #img = cv2.imread('GGG.PNG')
    
    
    
    dimensions = img.shape
    count=0
    if(type==0):
        img = img[round(dimensions[0]*0.18):round(dimensions[0]/3),round(dimensions[1]*0.15):dimensions[1]]
    else:
        img = img[round(dimensions[0]/4):round(dimensions[0]*0.9),round(dimensions[1]*0.1):round(dimensions[1]*0.8)]
    copy=img.copy()
    alpha=1.7
    beta=0
    adjusted=cv2.convertScaleAbs(img,alpha=alpha,beta=beta)    
    img= cv2.cvtColor(adjusted,cv2.COLOR_RGB2GRAY)

    if type==0:
        kernel=np.ones((2,2),np.uint8)
        binary=cv2.erode(img,kernel,iterations=1)
        ret,binary=cv2.threshold(binary,240,255,cv2.THRESH_BINARY)

    else: 
        kernel=np.ones((1,1),np.uint8)
        binary=cv2.dilate(img,kernel,iterations=2)
        ret,binary=cv2.threshold(binary,240,255,cv2.THRESH_BINARY)
        
    
    dim = binary.shape 
    
    
    img = cv2.resize(binary, (dim[1], dim[0]))
    
    if type==1:
        counter,hierarchy=cv2.findContours(binary,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(copy,counter,-1,(0,0,255),3)
        
        for i in counter:
            #print( cv2.contourArea(i))
            if cv2.contourArea(i)>18000:
                count+=1
    if count>=2:
        data=(pytesseract.image_to_string(img,lang="jpn",config='--psm 6 --oem 3'))
    else:
        data=""
    if(type==0):
        data=data.replace(" ","")
        data=data.split("\n")
        data.pop()
    else:
        data=data.split("\n")
        data.pop()
        if (len(data)<count&count<=7):
            while(len(data)!=count):
                data.append("null")
                
    # cv2.imshow('My Image', copy)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # print(count)
    # print(len(data))
    # print(data)
    if count!=len(data):
        return []
    else:
        return data

def randomColor():
    import random
    
    color = "#"+''.join([random.choice('3456789ABC') for j in range(6)])    
    
    return color

def loadui():
    from PyQt5.QtWidgets import QMainWindow,QApplication,QLabel,QVBoxLayout
    from PyQt5 import uic
    import sys
    from PyQt5.QtCore import QTimer
    from PyQt5 import QtCore    
    from PyQt5.QtGui import QFont
    import json

    config=open('config.json','r',encoding="utf-8")
    config=json.load(config)
    
    class UI(QMainWindow):
        def __init__(self):
            
            checkApp=0
            super(UI,self).__init__()
            self.setFixedSize(390, 489)
            uic.loadUi("gui.ui",self)
            self.alert=self.findChild(QLabel,"alert")
            self.vbox=self.findChild(QVBoxLayout,"vbox")
            try: 
                screenshot()
            except Exception as e:
                checkApp=1
                tryEx(e) 
                
            if checkApp==1:
                self.alert.setText("找不到程式 umamusume")
            else:
                self.alert.setText("偵測到程式")
            self.qTimer = QTimer()

            
            self.qTimer.setInterval(config["decetTime"]) 
            self.qTimer.timeout.connect(self.getSensorValue)
            self.qTimer.start()
            self.show()
            
        def getSensorValue(self):
            data=None
            checkApp=0
            try: 
                data=screenshot()
            except Exception as e:
                tryEx(e)
                checkApp=1
            if data!=None:
                title=data["e"]
                choice=data["choices"]
                for i in reversed(range(self.vbox.count())): 
                    self.vbox.itemAt(i).widget().setParent(None)
                for i in choice:
                    lb = QLabel(i["t"], self)
                    if len(i["t"])>30:                        
                        i["t"]=i["t"].replace("  ","\r\n")
                        i["t"]=i["t"].replace("<hr>","\r\n")
                        lb = QLabel(i["t"], self)                        
                        lb.setFixedHeight(110)
                    else:
                        lb.setFixedHeight(50)
                    lb.setStyleSheet('background-color:'+randomColor()+'; color:white; font-size:12px;')
                    lb.setAlignment(QtCore.Qt.AlignCenter)
                    self.vbox.addWidget(lb)
                if len(title)>10:
                    self.alert.setFont(QFont('微軟正黑體 Light', 15))
                else:
                    self.alert.setFont(QFont('微軟正黑體 Light', 20))
                self.alert.setText(title)
            else:
                if checkApp!=1:
                    self.alert.setText("檢測中...")
                else :
                    self.alert.setText("找不到程式 umamusume")
                    
                    
                    
                for i in reversed(range(self.vbox.count())):
                   self.vbox.itemAt(i).widget().setParent(None)
    app=QApplication(sys.argv)
    UIWindow=UI()
    UIWindow.show()
    app.exec_()
    
def tryEx(e):
    import sys
    import traceback
    
    error_class = e.__class__.__name__ #取得錯誤類型
    detail = e.args[0] #取得詳細內容
    cl, exc, tb = sys.exc_info() #取得Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
    fileName = lastCallStack[0] #取得發生的檔案名稱
    lineNum = lastCallStack[1] #取得發生的行號
    funcName = lastCallStack[2] #取得發生的函數名稱
    errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
    print(errMsg)

if __name__ == '__main__':
    loadui()


