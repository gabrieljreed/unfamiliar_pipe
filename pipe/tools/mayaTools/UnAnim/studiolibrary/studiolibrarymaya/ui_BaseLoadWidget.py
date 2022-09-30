# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'BaseLoadWidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(160, 560)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(160, 560))
        Form.setMaximumSize(QSize(16777215, 16777215))
        Form.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.titleFrame = QFrame(Form)
        self.titleFrame.setObjectName(u"titleFrame")
        self.titleFrame.setMinimumSize(QSize(0, 24))
        self.titleFrame.setFrameShape(QFrame.StyledPanel)
        self.titleFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.titleFrame)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")

        self.verticalLayout.addWidget(self.titleFrame)

        self.mainFrame = QFrame(Form)
        self.mainFrame.setObjectName(u"mainFrame")
        self.mainFrame.setFrameShape(QFrame.NoFrame)
        self.mainFrame.setFrameShadow(QFrame.Plain)
        self.mainFrame.setLineWidth(0)
        self.verticalLayout_2 = QVBoxLayout(self.mainFrame)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(4, 2, 4, 2)
        self.iconTitleFrame = QFrame(self.mainFrame)
        self.iconTitleFrame.setObjectName(u"iconTitleFrame")
        self.iconTitleFrame.setMinimumSize(QSize(0, 16))
        self.iconTitleFrame.setFrameShape(QFrame.NoFrame)
        self.iconTitleFrame.setFrameShadow(QFrame.Plain)
        self.iconTitleFrame.setLineWidth(0)
        self.verticalLayout_6 = QVBoxLayout(self.iconTitleFrame)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")

        self.verticalLayout_2.addWidget(self.iconTitleFrame)

        self.iconFrame = QFrame(self.mainFrame)
        self.iconFrame.setObjectName(u"iconFrame")
        self.iconFrame.setFrameShape(QFrame.NoFrame)
        self.iconFrame.setFrameShadow(QFrame.Plain)
        self.iconFrame.setLineWidth(0)
        self.verticalLayout_3 = QVBoxLayout(self.iconFrame)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.iconFrame2 = QFrame(self.iconFrame)
        self.iconFrame2.setObjectName(u"iconFrame2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.iconFrame2.sizePolicy().hasHeightForWidth())
        self.iconFrame2.setSizePolicy(sizePolicy1)
        self.iconFrame2.setStyleSheet(u"")
        self.iconFrame2.setFrameShape(QFrame.NoFrame)
        self.iconFrame2.setFrameShadow(QFrame.Plain)
        self.iconFrame2.setLineWidth(0)
        self.verticalLayout_8 = QVBoxLayout(self.iconFrame2)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.thumbnailLayout = QHBoxLayout()
        self.thumbnailLayout.setSpacing(0)
        self.thumbnailLayout.setObjectName(u"thumbnailLayout")
        self.thumbnailLayout.setContentsMargins(-1, 0, -1, 0)
        self.thumbnailFrame = QFrame(self.iconFrame2)
        self.thumbnailFrame.setObjectName(u"thumbnailFrame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(1)
        sizePolicy2.setHeightForWidth(self.thumbnailFrame.sizePolicy().hasHeightForWidth())
        self.thumbnailFrame.setSizePolicy(sizePolicy2)
        self.thumbnailFrame.setMinimumSize(QSize(50, 50))
        self.thumbnailFrame.setMaximumSize(QSize(150, 150))
        self.thumbnailFrame.setStyleSheet(u"")
        self.thumbnailFrame.setFrameShape(QFrame.NoFrame)
        self.thumbnailFrame.setFrameShadow(QFrame.Plain)
        self.thumbnailFrame.setLineWidth(0)
        self.verticalLayout_4 = QVBoxLayout(self.thumbnailFrame)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 4, 0, 2)

        self.thumbnailLayout.addWidget(self.thumbnailFrame)


        self.verticalLayout_8.addLayout(self.thumbnailLayout)


        self.verticalLayout_3.addWidget(self.iconFrame2)


        self.verticalLayout_2.addWidget(self.iconFrame)

        self.formFrame = QFrame(self.mainFrame)
        self.formFrame.setObjectName(u"formFrame")
        self.formFrame.setMinimumSize(QSize(0, 16))
        self.formFrame.setFrameShape(QFrame.NoFrame)
        self.formFrame.setFrameShadow(QFrame.Plain)
        self.formFrame.setLineWidth(0)
        self.verticalLayout_14 = QVBoxLayout(self.formFrame)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")

        self.verticalLayout_2.addWidget(self.formFrame)


        self.verticalLayout.addWidget(self.mainFrame)

        self.customWidgetFrame = QFrame(Form)
        self.customWidgetFrame.setObjectName(u"customWidgetFrame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.customWidgetFrame.sizePolicy().hasHeightForWidth())
        self.customWidgetFrame.setSizePolicy(sizePolicy3)
        self.customWidgetFrame.setFrameShape(QFrame.NoFrame)
        self.customWidgetFrame.setFrameShadow(QFrame.Raised)
        self.customWidgetFrame.setLineWidth(0)
        self.verticalLayout_9 = QVBoxLayout(self.customWidgetFrame)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")

        self.verticalLayout.addWidget(self.customWidgetFrame)

        self.previewButtons = QFrame(Form)
        self.previewButtons.setObjectName(u"previewButtons")
        self.previewButtons.setFrameShape(QFrame.NoFrame)
        self.previewButtons.setFrameShadow(QFrame.Plain)
        self.previewButtons.setLineWidth(0)
        self.horizontalLayout_6 = QHBoxLayout(self.previewButtons)
        self.horizontalLayout_6.setSpacing(1)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.acceptButton = QPushButton(self.previewButtons)
        self.acceptButton.setObjectName(u"acceptButton")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.acceptButton.sizePolicy().hasHeightForWidth())
        self.acceptButton.setSizePolicy(sizePolicy4)
        self.acceptButton.setMinimumSize(QSize(80, 35))
        self.acceptButton.setMaximumSize(QSize(125, 35))
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.acceptButton.setFont(font)
        self.acceptButton.setStyleSheet(u"")

        self.horizontalLayout_2.addWidget(self.acceptButton)

        self.selectionSetButton = QPushButton(self.previewButtons)
        self.selectionSetButton.setObjectName(u"selectionSetButton")
        sizePolicy.setHeightForWidth(self.selectionSetButton.sizePolicy().hasHeightForWidth())
        self.selectionSetButton.setSizePolicy(sizePolicy)
        self.selectionSetButton.setMinimumSize(QSize(35, 35))
        self.selectionSetButton.setMaximumSize(QSize(35, 16777215))
        icon = QIcon()
        icon.addFile(u"icons/selectionSet2.png", QSize(), QIcon.Normal, QIcon.Off)
        self.selectionSetButton.setIcon(icon)
        self.selectionSetButton.setIconSize(QSize(25, 25))

        self.horizontalLayout_2.addWidget(self.selectionSetButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.horizontalLayout_6.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addWidget(self.previewButtons)

        self.labelSpacer = QFrame(Form)
        self.labelSpacer.setObjectName(u"labelSpacer")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(2)
        sizePolicy5.setHeightForWidth(self.labelSpacer.sizePolicy().hasHeightForWidth())
        self.labelSpacer.setSizePolicy(sizePolicy5)
        self.labelSpacer.setFrameShape(QFrame.NoFrame)
        self.labelSpacer.setFrameShadow(QFrame.Plain)
        self.labelSpacer.setLineWidth(0)

        self.verticalLayout.addWidget(self.labelSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
#if QT_CONFIG(tooltip)
        self.acceptButton.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.acceptButton.setText(QCoreApplication.translate("Form", u"Apply", None))
        self.selectionSetButton.setText("")
    # retranslateUi

