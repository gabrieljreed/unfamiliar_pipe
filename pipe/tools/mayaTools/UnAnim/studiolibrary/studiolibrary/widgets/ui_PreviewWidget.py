# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PreviewWidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Frame(object):
    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        Frame.resize(160, 479)
        Frame.setMinimumSize(QSize(160, 0))
        Frame.setFrameShape(QFrame.NoFrame)
        Frame.setFrameShadow(QFrame.Plain)
        Frame.setLineWidth(0)
        self.verticalLayout_2 = QVBoxLayout(Frame)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.titleFrame = QFrame(Frame)
        self.titleFrame.setObjectName(u"titleFrame")
        self.titleFrame.setMinimumSize(QSize(0, 24))
        self.titleFrame.setFrameShape(QFrame.NoFrame)
        self.titleFrame.setFrameShadow(QFrame.Plain)
        self.titleFrame.setLineWidth(0)
        self.horizontalLayout_3 = QHBoxLayout(self.titleFrame)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")

        self.verticalLayout_2.addWidget(self.titleFrame)

        self.iconTitleFrame = QFrame(Frame)
        self.iconTitleFrame.setObjectName(u"iconTitleFrame")
        self.iconTitleFrame.setMinimumSize(QSize(0, 16))
        self.iconTitleFrame.setStyleSheet(u"")
        self.iconTitleFrame.setFrameShape(QFrame.NoFrame)
        self.iconTitleFrame.setFrameShadow(QFrame.Plain)
        self.iconTitleFrame.setLineWidth(0)
        self.verticalLayout_7 = QVBoxLayout(self.iconTitleFrame)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(4, 2, 4, 2)

        self.verticalLayout_2.addWidget(self.iconTitleFrame)

        self.iconGroup = QFrame(Frame)
        self.iconGroup.setObjectName(u"iconGroup")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iconGroup.sizePolicy().hasHeightForWidth())
        self.iconGroup.setSizePolicy(sizePolicy)
        self.iconGroup.setMaximumSize(QSize(5000, 5000))
        self.iconGroup.setFrameShape(QFrame.NoFrame)
        self.iconGroup.setFrameShadow(QFrame.Plain)
        self.iconGroup.setLineWidth(0)
        self.horizontalLayout = QHBoxLayout(self.iconGroup)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.iconFrame = QFrame(self.iconGroup)
        self.iconFrame.setObjectName(u"iconFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.iconFrame.sizePolicy().hasHeightForWidth())
        self.iconFrame.setSizePolicy(sizePolicy1)
        self.iconFrame.setMinimumSize(QSize(50, 50))
        self.iconFrame.setMaximumSize(QSize(5000, 5000))
        self.iconFrame.setStyleSheet(u"")
        self.iconFrame.setFrameShape(QFrame.NoFrame)
        self.iconFrame.setFrameShadow(QFrame.Plain)
        self.iconFrame.setLineWidth(0)
        self.verticalLayout_5 = QVBoxLayout(self.iconFrame)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(4, 2, 4, 2)

        self.horizontalLayout.addWidget(self.iconFrame)


        self.verticalLayout_2.addWidget(self.iconGroup)

        self.formFrame = QFrame(Frame)
        self.formFrame.setObjectName(u"formFrame")
        sizePolicy.setHeightForWidth(self.formFrame.sizePolicy().hasHeightForWidth())
        self.formFrame.setSizePolicy(sizePolicy)
        self.formFrame.setMinimumSize(QSize(0, 15))
        self.formFrame.setFrameShape(QFrame.NoFrame)
        self.formFrame.setFrameShadow(QFrame.Plain)
        self.formFrame.setLineWidth(0)
        self.verticalLayout_4 = QVBoxLayout(self.formFrame)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(4, 2, 4, 2)

        self.verticalLayout_2.addWidget(self.formFrame)

        self.spacer = QFrame(Frame)
        self.spacer.setObjectName(u"spacer")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.spacer.sizePolicy().hasHeightForWidth())
        self.spacer.setSizePolicy(sizePolicy2)
        self.spacer.setFrameShape(QFrame.NoFrame)
        self.spacer.setFrameShadow(QFrame.Plain)
        self.spacer.setLineWidth(0)

        self.verticalLayout_2.addWidget(self.spacer)

        self.buttonGroup = QFrame(Frame)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.setFrameShape(QFrame.NoFrame)
        self.buttonGroup.setFrameShadow(QFrame.Plain)
        self.buttonGroup.setLineWidth(0)
        self.horizontalLayout_2 = QHBoxLayout(self.buttonGroup)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.acceptButton = QPushButton(self.buttonGroup)
        self.acceptButton.setObjectName(u"acceptButton")
        self.acceptButton.setMinimumSize(QSize(32, 32))
        self.acceptButton.setMaximumSize(QSize(96, 96))
        font = QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.acceptButton.setFont(font)

        self.horizontalLayout_2.addWidget(self.acceptButton)


        self.verticalLayout_2.addWidget(self.buttonGroup)


        self.retranslateUi(Frame)

        QMetaObject.connectSlotsByName(Frame)
    # setupUi

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
        self.acceptButton.setText(QCoreApplication.translate("Frame", u"Accept", None))
    # retranslateUi

