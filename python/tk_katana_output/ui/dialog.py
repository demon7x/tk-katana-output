# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created: Tue Jul 16 16:46:31 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(588, 285)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6)
        self.sel_node = QtGui.QLineEdit(Dialog)
        self.sel_node.setObjectName("sel_node")
        self.horizontalLayout_3.addWidget(self.sel_node)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.groupBox_3 = QtGui.QGroupBox(Dialog)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_5 = QtGui.QLabel(self.groupBox_3)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_8.addWidget(self.label_5)
        self.start_frame = QtGui.QLineEdit(self.groupBox_3)
        self.start_frame.setText("")
        self.start_frame.setObjectName("start_frame")
        self.verticalLayout_8.addWidget(self.start_frame)
        self.horizontalLayout.addLayout(self.verticalLayout_8)
        self.verticalLayout_9 = QtGui.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_7 = QtGui.QLabel(self.groupBox_3)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_9.addWidget(self.label_7)
        self.end_frame = QtGui.QLineEdit(self.groupBox_3)
        self.end_frame.setObjectName("end_frame")
        self.verticalLayout_9.addWidget(self.end_frame)
        self.horizontalLayout.addLayout(self.verticalLayout_9)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.sg_check = QtGui.QCheckBox(Dialog)
        self.sg_check.setChecked(True)
        self.sg_check.setObjectName("sg_check")
        self.verticalLayout.addWidget(self.sg_check)
        self.output_btn = QtGui.QPushButton(Dialog)
        self.output_btn.setObjectName("output_btn")
        self.verticalLayout.addWidget(self.output_btn)
        self.farm_btn = QtGui.QPushButton(Dialog)
        self.farm_btn.setObjectName("farm_btn")
        self.verticalLayout.addWidget(self.farm_btn)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "The Current Sgtk Environment", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "Select Nodes", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("Dialog", "Frame Range", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Dialog", "End", None, QtGui.QApplication.UnicodeUTF8))
        self.sg_check.setText(QtGui.QApplication.translate("Dialog", "Publish To Shotgun", None, QtGui.QApplication.UnicodeUTF8))
        self.output_btn.setText(QtGui.QApplication.translate("Dialog", "Output", None, QtGui.QApplication.UnicodeUTF8))
        self.farm_btn.setText(QtGui.QApplication.translate("Dialog", "Output_Farm", None, QtGui.QApplication.UnicodeUTF8))

from . import resources_rc
