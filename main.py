# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 23:03:14 2023
@author: tooth
"""
import pygetwindow
import pyautogui
import traceback
import Levenshtein
import pytesseract
import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QRadioButton
from PyQt5 import uic
import sys
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
import json
from ctypes import windll
import random


def empty():
    pass


# cv2.namedWindow('TrackBar')
# cv2.resizeWindow('TrackBar', 640, 320)
# cv2.createTrackbar('Hue Min', 'TrackBar', 0, 255, empty)
# cv2.createTrackbar('Hue Max', 'TrackBar', 179, 255, empty)
# cv2.createTrackbar('Sat Min', 'TrackBar', 0, 255, empty)
# cv2.createTrackbar('Sat Max', 'TrackBar', 255, 255, empty)
# cv2.createTrackbar('Val Min', 'TrackBar', 0, 255, empty)
# cv2.createTrackbar('Val Max', 'TrackBar', 255, 255, empty)


def screenshot(mode):
    window = pygetwindow.getWindowsWithTitle('umamusume')[0]
    h = windll.user32.FindWindowA(b'Shell_TrayWnd', None)

    left = window.left
    top = window.top
    # print(window.size)

    # if window.width < window.height and (top != 0 or (window.height != 1900)):
    if window.width < window.height and (top != 0 or (window.height != 1047)):
        windll.user32.ShowWindow(h, 9)
        # window.resizeTo(1080, 1900)
        window.resizeTo(583, 1047)
        window.moveTo(left, 0)
    elif window.width > window.height:
        windll.user32.ShowWindow(h, 0)
        window.resizeTo(1940, 1120)
        window.moveTo(-10, -30)

    top = window.top
    left = window.left

    img = pyautogui.screenshot(region=(left + 10, top + 30, window.width - 20, window.height - 45))
    open_cv_image = np.array(img)
    open_cv_image = open_cv_image[:, :, ::-1].copy()
    data = processScreenshot(open_cv_image, mode)
    return data


def jsonProcess(skill, mode):
    if mode == 0:
        data = open('./js/female_event_datas.json', 'r', encoding="utf-8")
        data = json.load(data)
        choice = []
        tmp = None

        for i in skill:
            print("skill:--------------" + i + "---end")
            choRule = round(len(i) / 2) - 1
            if len(i) <= 3:
                choRule = 1
            for j in data:

                for k in j["choices"]:
                    if len(skill) == len(j["choices"]):
                        if len(i) - 2 <= len(k['n']) <= len(i) + 2:
                            distance2 = Levenshtein.distance(i, k['n'])
                            if distance2 <= choRule:
                                j["distance2"] = distance2
                                if j not in choice:
                                    choice.append(j)
        if len(choice) >= 1:
            for i in range(len(choice)):
                for j in range(i + 1, len(choice)):
                    if choice[j]["distance2"] < choice[i]["distance2"]:
                        tmp = choice[i]
                        choice[i] = choice[j]
                        choice[j] = tmp
                    elif choice[j]["distance2"] == choice[i]["distance2"]:
                        tmpA = 0
                        tmpB = 0
                        for l in range(len(choice[i]["choices"])):
                            # print("--------skill----------")
                            # print(skill[l])
                            # print("-----------------------")

                            # print("--------target----------")
                            # print(choice[i]["choices"][l]["n"])
                            # print("-----------------------")
                            tmpA += Levenshtein.distance(choice[i]["choices"][l]["n"], skill[l])
                            # print(tmpA)
                        for k in range(len(choice[j]["choices"])):
                            # print("--------skill----------")
                            # print(skill[k])
                            # print("-----------------------")

                            # print("--------target----------")
                            # print(choice[j]["choices"][k]["n"])
                            # print("-----------------------")
                            tmpB += Levenshtein.distance(choice[j]["choices"][k]["n"], skill[k])
                            # print(tmpB)

                        if tmpB < tmpA:
                            tmp = choice[i]
                            choice[i] = choice[j]
                            choice[j] = tmp

        if len(choice) >= 1:
            # print(choice)
            tmp = choice[0]
        # print (tmp)
        return tmp
    else:
        data = open('./js/skill_bak.json', 'r', encoding="utf-8")
        data = json.load(data)
        final = []

        for i in skill:
            for j in range(len(data)):

                tmp = Levenshtein.distance(data[j]["skill"], i)
                if len(data[j]["skill"]) <= 5:
                    if tmp < 2:
                        if data[j] not in final:
                            final.append(data[j])
                elif tmp < 2:
                    # print(tmp)
                    # print(data[j]["skill"], )
                    if data[j] not in final:
                        final.append(data[j])

                    # print(tmp)
        return final


def processScreenshot(image, mode):
    data = None

    # title=cv2Process(image,0)
    skill = cv2Process(image, 1, mode)

    try:
        if mode == 0:
            if 2 <= len(skill) <= 6:
                data = jsonProcess(skill, mode)
        else:
            data = jsonProcess(skill, mode)
    except Exception as e:
        tryEx(e)
    return data


def cv2Process(img, type, mode):
    # img = cv2.imread('GGG.PNG')
    dimensions = img.shape
    # h_min = cv2.getTrackbarPos('Hue Min', 'TrackBar')
    # h_max = cv2.getTrackbarPos('Hue Max', 'TrackBar')
    # s_min = cv2.getTrackbarPos('Sat Min', 'TrackBar')
    # s_max = cv2.getTrackbarPos('Sat Max', 'TrackBar')
    # v_min = cv2.getTrackbarPos('Val Min', 'TrackBar')
    # v_max = cv2.getTrackbarPos('Val Max', 'TrackBar')
    # print(h_min, h_max, s_min, s_max, v_min, v_max)

    if mode == 0:

        count = 0
        if type == 0:
            img = img[round(dimensions[0] * 0.18):round(dimensions[0] / 3), round(dimensions[1] * 0.15):dimensions[1]]
        else:
            img = img[round(dimensions[0] / 4):round(dimensions[0] * 0.9),
                  round(dimensions[1] * 0.1):round(dimensions[1] * 0.8)]
        copy = img.copy()

        alpha = 1.7
        beta = 0
        adjusted = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
        img = cv2.cvtColor(adjusted, cv2.COLOR_RGB2GRAY)

        if type == 0:
            kernel = np.ones((2, 2), np.uint8)
            binary = cv2.erode(img, kernel, iterations=1)
            ret, binary = cv2.threshold(binary, 240, 255, cv2.THRESH_BINARY)

        else:
            kernel = np.ones((1, 1), np.uint8)
            binary = cv2.dilate(img, kernel, iterations=2)
            ret, binary = cv2.threshold(binary, 240, 255, cv2.THRESH_BINARY)

        dim = binary.shape

        img = cv2.resize(binary, (dim[1], dim[0]))

        if type == 1:
            counter, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(copy, counter, -1, (0, 0, 255), 3)

            for i in counter:
                # print( cv2.contourArea(i))
                if cv2.contourArea(i) > 18000:
                    count += 1
        if count >= 2:
            data = (pytesseract.image_to_string(img, lang="jpn", config='--psm 6 --oem 3'))
        else:
            data = ""
        if type == 0:
            data = data.replace(" ", "")
            data = data.split("\n")
            data.pop()
        else:
            data = data.split("\n")
            data.pop()
            if len(data) < count & count <= 7:
                while len(data) != count:
                    data.append("null")

        # cv2.imshow('My Image', copy)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # print(count)
        # print(len(data))
        # print(data)
        if count != len(data):
            return []
        else:
            return data

    else:
        img = img[round(dimensions[0] / 2.7):round(dimensions[0] * 0.79),
              round(dimensions[1] * 0.18):round(dimensions[1] * 0.69)]
        copy = img.copy()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower = np.array([0, 0, 0])
        upper = np.array([179, 255, 244])
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(img, img, mask=mask)
        # 0 179 0 255 0 244
        count = 0

        # cv2.imshow('img', img)
        # cv2.imshow('hsv', hsv)
        # cv2.imshow('mask', mask)
        # cv2.imshow('reslut', result)

        alpha = 1.7
        beta = 0
        adjusted = cv2.convertScaleAbs(result, alpha=alpha, beta=beta)
        img = cv2.cvtColor(adjusted, cv2.COLOR_RGB2GRAY)

        kernel = np.ones((1, 1), np.uint8)
        binary = cv2.erode(img, kernel, iterations=1)
        ret, binary = cv2.threshold(binary, 0, 255, cv2.THRESH_BINARY)

        dim = binary.shape

        img = cv2.resize(binary, (dim[1], dim[0]))

        counter, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(copy, counter, -1, (0, 0, 255), 1)
        data = []
        for i in counter:

            x, y, w, h = cv2.boundingRect(i)
            if cv2.contourArea(i) > 35000:
                skillCut = copy[y:y + h - 100, x:x + w]

                # cv2.imshow(str(count), skillCut)
                count += 1

                imgC = cv2.resize(skillCut, (0, 0), fx=2, fy=2)
                hsv = cv2.cvtColor(imgC, cv2.COLOR_BGR2HSV)

                # lowerS = np.array([h_min, s_min, v_min])
                # upperS = np.array([h_max, s_max, v_max])
                lowerS = np.array([0, 150, 73])
                upperS = np.array([24, 213, 152])
                # 0 24 150 213 73 152
                maskS = cv2.inRange(hsv, lowerS, upperS)

                heightMS, widthMS = maskS.shape

                if heightMS < 100:
                    # print(pytesseract.image_to_string(maskS, lang="jpn"))
                    skillO = pytesseract.image_to_string(maskS, lang="jpn")
                    skillO = skillO.replace(" ", "")
                    skillO = skillO.split("\n")
                    data.append(skillO[0])
                    resultS = cv2.bitwise_and(imgC, imgC, mask=maskS)

                    # cv2.imshow(str(count)+'img', imgC)
                    # cv2.imshow(str(count) + 'mask', maskS)
                    # cv2.imshow(str(count) + 'res', resultS)
                    # cv2.waitKey(1)

        print(data)
        return data



def randomColor():
    color = "#" + ''.join([random.choice('3456789ABC') for j in range(6)])

    return color


class skillWindow(QMainWindow):
    def __init__(self, parent=None):
        try:
            super(skillWindow, self).__init__(parent)
            uic.loadUi("skill.ui", self)
            self.vbox = self.findChild(QVBoxLayout, "vbox")
            self.dataHistory = []
            pass
        except Exception as e:
            tryEx(e)

    def generate(self, data):
        # print(1)
        # print(self.vbox)

        for i in data:
            if i not in self.dataHistory:
                self.dataHistory.append(i)

        for i in reversed(range(self.vbox.count())):
            self.vbox.itemAt(i).widget().setParent(None)
        for i in self.dataHistory:
            labelStr = i["skill"] + "    " + i["zhSkill"] + "\r\n" + i["cond"]
            labelStr = labelStr.replace("  ", "\r\n")
            labelStr = labelStr.replace("<hr>", "\r\n")
            lb = QLabel(labelStr, self)
            lb.setFixedHeight(140)

            lb.setStyleSheet('background-color:' + ' #67a8da' + '; color:white; font-size:12px;')
            lb.setAlignment(QtCore.Qt.AlignCenter)
            self.vbox.addWidget(lb)
        pass


class UI(QMainWindow):
    def __init__(self):

        config = open('config.json', 'r', encoding="utf-8")
        config = json.load(config)
        checkApp = 0

        super(UI, self).__init__(parent=None)
        self.setFixedSize(390, 570)
        self.checkMode = 0
        uic.loadUi("gui.ui", self)
        self.alert = self.findChild(QLabel, "alert")
        self.vbox = self.findChild(QVBoxLayout, "vbox")
        self.skillMode = self.findChild(QRadioButton, "skillMode")
        self.eventMode = self.findChild(QRadioButton, "eventMode")
        self.eventMode.setChecked(True)
        self.skillMode.toggled.connect(lambda: self.changeMode(self.skillMode))
        self.eventMode.toggled.connect(lambda: self.changeMode(self.eventMode))

        try:
            screenshot(self.checkMode)
        except Exception as e:
            checkApp = 1
            tryEx(e)

        if checkApp == 1:
            self.alert.setText("找不到程式 umamusume")
        else:
            self.alert.setText("偵測到程式")
        self.qTimer = QTimer()

        self.qTimer.setInterval(config["decetTime"])
        self.qTimer.timeout.connect(self.getSensorValue)
        self.qTimer.start()
        self.skillWindow = skillWindow(self)
        self.show()

    def getSensorValue(self):
        data = None
        checkApp = 0

        try:
            data = screenshot(self.checkMode)
        except Exception as e:
            tryEx(e)
            checkApp = 1
        if data is not None and self.checkMode == 0:
            title = data["e"]
            choice = data["choices"]
            for i in reversed(range(self.vbox.count())):
                self.vbox.itemAt(i).widget().setParent(None)
            for i in choice:
                lb = QLabel(i["t"], self)
                if len(i["t"]) > 30:
                    i["t"] = i["t"].replace("  ", "\r\n")
                    i["t"] = i["t"].replace("<hr>", "\r\n")
                    lb = QLabel(i["t"], self)
                    lb.setFixedHeight(110)
                else:
                    lb.setFixedHeight(50)
                lb.setStyleSheet('background-color:' + randomColor() + '; color:white; font-size:12px;')
                lb.setAlignment(QtCore.Qt.AlignCenter)
                self.vbox.addWidget(lb)
            if len(title) > 10:
                self.alert.setFont(QFont('微軟正黑體 Light', 15))
            else:
                self.alert.setFont(QFont('微軟正黑體 Light', 20))
            self.alert.setText(title)

        elif data is not None and self.checkMode == 1:

            skillWindow.generate(self.skillWindow, data)

            pass

        else:
            if checkApp != 1:
                self.alert.setText("檢測中...")
            else:
                self.alert.setText("找不到程式 umamusume")

            for i in reversed(range(self.vbox.count())):
                self.vbox.itemAt(i).widget().setParent(None)

    def changeMode(self, b):
        if b.text() == "事件模式":
            if b.isChecked():
                self.checkMode = 0
                self.skillWindow.close()
        else:
            if b.isChecked():
                self.checkMode = 1
                self.skillWindow.show()


def loadUi():
    app = QApplication(sys.argv)
    UIWindow = UI()
    UIWindow.show()
    app.exec_()


def tryEx(e):
    error_class = e.__class__.__name__  # 取得錯誤類型
    detail = e.args[0]  # 取得詳細內容
    cl, exc, tb = sys.exc_info()  # 取得Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
    fileName = lastCallStack[0]  # 取得發生的檔案名稱
    lineNum = lastCallStack[1]  # 取得發生的行號
    funcName = lastCallStack[2]  # 取得發生的函數名稱
    errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
    print(errMsg)


if __name__ == '__main__':
    loadUi()
