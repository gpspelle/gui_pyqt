#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


import os
from PyQt5 import QtCore
from PyQt5.QtCore import QDateTime, Qt, QTime
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QFileDialog, QFormLayout)


class SelectStreams(QDialog):
    def __init__(self, parent=None):
        super(SelectStreams, self).__init__(parent)

        self.originalPalette = QApplication.palette()

        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        #self.createTopLeftGroupBox()
        #self.createTopRightGroupBox()
        #self.createBottomLeftTabWidget()
        self.createBottomRightGroupBox()
        #self.createProgressBar()

        styleComboBox.activated[str].connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        #disableWidgetsCheckBox.toggled.connect(self.topLeftGroupBox.setDisabled)
        #disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)
        #disableWidgetsCheckBox.toggled.connect(self.bottomLeftTabWidget.setDisabled)
        disableWidgetsCheckBox.toggled.connect(self.bottomRightGroupBox.setDisabled)

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)
        topLayout.addWidget(disableWidgetsCheckBox)

        mainLayout = QGridLayout()
        #mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        #mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        #mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        #mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
        mainLayout.addWidget(self.bottomRightGroupBox)
        #mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        #mainLayout.setRowStretch(1, 1)
        #mainLayout.setRowStretch(2, 1)
        #mainLayout.setColumnStretch(0, 1)
        #mainLayout.setColumnStretch(1, 1)

        self.streams = []

        extractButton = QPushButton("Extract")
        extractButton.setCheckable(True)
        extractButton.clicked.connect(lambda:self.extractPressed())
        mainLayout.addWidget(extractButton)

        self.setLayout(mainLayout)
        
        self.setWindowTitle("Extract Features")
        self.changeStyle('Windows')

    def clickBox1(self, state):

        if state == QtCore.Qt.Checked:
            self.streams.append('temporal')
        else:
            self.streams.remove('temporal')
    
    def clickBox2(self, state):

        if state == QtCore.Qt.Checked:
            self.streams.append('spatial')
        else:
            self.streams.remove('spatial')

    def clickBox3(self, state):

        if state == QtCore.Qt.Checked:
            self.streams.append('pose')
        else:
            self.streams.remove('pose')

    def clickBox4(self, state):

        if state == QtCore.Qt.Checked:
            self.streams.append('ritmo')
        else:
            self.streams.remove('ritmo')

    def extractPressed(self):

        if len(self.fileDialog.selectedFiles()) > 1:
            print("ERROR! Select only one file")
            self.close()

        cat_streams = ''

        for i in self.streams:
            cat_streams += (i + ' ')
           
        class_ = str(self.classComboBox.currentText()).replace('/', '')

        id = str(self.idEdit.text())
        data_folder = self.fileDialog.selectedFiles()[0]

        #os.system("python3 streams_fextractor.py -streams " + cat_streams + " -id " + .id + " -data " + data_folder + " -class " + class_)
        print("python3 streams_fextractor.py -streams " + cat_streams + " -id " + id + " -data " + data_folder + " -class " + class_)

        self.close()

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)

    def advanceprogressbar(self):
        curval = self.progressbar.value()
        maxval = self.progressbar.maximum()
        self.progressbar.setvalue(curval + (maxval - curval) / 100)

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Streams")

        checkButton1 = QCheckBox("Temporal")
        checkButton2 = QCheckBox("Spatial")
        checkButton3 = QCheckBox("Pose")
        checkButton4 = QCheckBox("Ritmo visual")

        checkButton1.stateChanged.connect(self.clickBox1)
        checkButton2.stateChanged.connect(self.clickBox2)
        checkButton3.stateChanged.connect(self.clickBox3)
        checkButton4.stateChanged.connect(self.clickBox4)

        #checkBox = QCheckBox("Tri-state check box")
        #checkBox.setTristate(True)
        #checkBox.setCheckState(Qt.PartiallyChecked)

        layout = QVBoxLayout()
        layout.addWidget(checkButton1)
        layout.addWidget(checkButton2)
        layout.addWidget(checkButton3)
        layout.addWidget(checkButton4)
        #layout.addWidget(checkBox)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)    

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Group 2")

        defaultPushButton = QPushButton("Default Push Button")
        defaultPushButton.setDefault(True)

        togglePushButton = QPushButton("Toggle Push Button")
        togglePushButton.setCheckable(True)
        togglePushButton.setChecked(True)

        flatPushButton = QPushButton("Flat Push Button")
        flatPushButton.setFlat(True)

        layout = QVBoxLayout()
        layout.addWidget(defaultPushButton)
        layout.addWidget(togglePushButton)
        layout.addWidget(flatPushButton)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    def createBottomLeftTabWidget(self):
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Ignored)

        tab1 = QWidget()
        tableWidget = QTableWidget(10, 10)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QTextEdit()

        textEdit.setPlainText("Twinkle, twinkle, little star,\n"
                              "How I wonder what you are.\n" 
                              "Up above the world so high,\n"
                              "Like a diamond in the sky.\n"
                              "Twinkle, twinkle, little star,\n" 
                              "How I wonder what you are!\n")

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.bottomLeftTabWidget.addTab(tab1, "&Table")
        self.bottomLeftTabWidget.addTab(tab2, "Text &Edit")

    def createBottomRightGroupBox(self):
        self.bottomRightGroupBox = QGroupBox("Extract Features")

        checkButton1 = QCheckBox("Temporal")
        checkButton2 = QCheckBox("Spatial")
        checkButton3 = QCheckBox("Pose")
        checkButton4 = QCheckBox("Ritmo visual")

        checkButton1.stateChanged.connect(self.clickBox1)
        checkButton2.stateChanged.connect(self.clickBox2)
        checkButton3.stateChanged.connect(self.clickBox3)
        checkButton4.stateChanged.connect(self.clickBox4)

        #checkBox = QCheckBox("Tri-state check box")
        #checkBox.setTristate(True)
        #checkBox.setCheckState(Qt.PartiallyChecked)
        
        hBox = QHBoxLayout()

        hBox.addWidget(checkButton1)
        hBox.addWidget(checkButton2)
        hBox.addWidget(checkButton3)
        hBox.addWidget(checkButton4)

        self.classComboBox = QComboBox()
        self.classComboBox.addItems(['Falls /NotFalls', 'Violence /NotViolence'])

        vBox = QVBoxLayout()
        vBox.addWidget(self.classComboBox)
        vBox.addSpacing(10)

        idLabel = QLabel("Id:")
        self.idEdit = QLineEdit()

        formLayout = QFormLayout()
        formLayout.addRow(idLabel, self.idEdit)
        formLayout.addRow(QLabel("Streams"), hBox)
        formLayout.addRow(QLabel("Class"), vBox)

        selectFolderLabel = QLabel("Select your data's folder")
        selectFolderLabel.setAlignment(Qt.AlignCenter)
        formLayout.addWidget(selectFolderLabel)
        fileButton = QPushButton("Select")
        fileButton.setCheckable(True)
        fileButton.clicked.connect(lambda:self.filePressed())
        formLayout.addWidget(fileButton)

        self.bottomRightGroupBox.setLayout(formLayout)

    def filePressed(self):

        self.fileDialog = QFileDialog(self)
        self.fileDialog.setFileMode(QFileDialog.DirectoryOnly)
        self.fileDialog.show()

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)

class Initialize(QDialog):
    def __init__(self, streams, ind, parent=None):
        super(Initialize, self).__init__(parent)

        self.streams = streams
        self.originalPalette = QApplication.palette()

        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        self.createTopRightGroupBox(ind)
        self.createProgressBar()

        styleComboBox.activated[str].connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        
        disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)
        topLayout.addWidget(disableWidgetsCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)

        createButton = QPushButton("Create")
        createButton.setCheckable(True)
        createButton.clicked.connect(lambda:self.createPressed(ind))
        mainLayout.addWidget(createButton)


        fileButton = QPushButton("Select file")
        fileButton.setCheckable(True)
        fileButton.clicked.connect(lambda:self.filePressed(ind))
        mainLayout.addWidget(fileButton)


        self.setLayout(mainLayout)
        
        self.setWindowTitle("Extract Features")
        self.changeStyle('Windows')

    def createPressed(self, ind):
        if len(self.fileDialog.selectedFiles()) > 1:
            print("ERROR! Select only one file")
            self.close()

        os.system('python3 multi-stream-vgg16.py -streams ' + self.streams[ind] + ' -weight ' + self.fileDialog.selectedFiles()[0])
        
        ind += 1

        if ind >= len(self.streams):
            sys.exit(app.exec_()) 

        window_ = Initialize(self.streams, ind)
        window_.show()
        self.close()
    
    def filePressed(self, ind):

        self.fileDialog = QFileDialog(self)
        self.fileDialog.show()

    def createTopRightGroupBox(self, ind):
        stream = self.streams[ind]
        self.topRightGroupBox = QGroupBox("Select initialization weights to " + stream)

        layout = QVBoxLayout()
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1)

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
     

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window_ = SelectStreams()
    window_.show()
    sys.exit(app.exec_()) 
