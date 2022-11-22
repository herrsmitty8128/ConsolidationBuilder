# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1003, 767)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.entityName = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.entityName.setObjectName("entityName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.entityName)
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.beginningBalanceDate = QtWidgets.QDateEdit(self.verticalLayoutWidget)
        self.beginningBalanceDate.setObjectName("beginningBalanceDate")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.beginningBalanceDate)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.endingBalanceDate = QtWidgets.QDateEdit(self.verticalLayoutWidget)
        self.endingBalanceDate.setObjectName("endingBalanceDate")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.endingBalanceDate)
        self.verticalLayout.addLayout(self.formLayout)
        self.tabWidget = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.EntitiesTab = QtWidgets.QWidget()
        self.EntitiesTab.setObjectName("EntitiesTab")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.EntitiesTab)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Entities = QtWidgets.QTableView(self.EntitiesTab)
        self.Entities.setAlternatingRowColors(True)
        self.Entities.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.Entities.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.Entities.setSortingEnabled(True)
        self.Entities.setObjectName("Entities")
        self.horizontalLayout_2.addWidget(self.Entities)
        self.tabWidget.addTab(self.EntitiesTab, "")
        self.CostCentersTab = QtWidgets.QWidget()
        self.CostCentersTab.setObjectName("CostCentersTab")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.CostCentersTab)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.Cost_Centers = QtWidgets.QTableView(self.CostCentersTab)
        self.Cost_Centers.setAlternatingRowColors(True)
        self.Cost_Centers.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.Cost_Centers.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.Cost_Centers.setSortingEnabled(True)
        self.Cost_Centers.setObjectName("Cost_Centers")
        self.horizontalLayout_3.addWidget(self.Cost_Centers)
        self.tabWidget.addTab(self.CostCentersTab, "")
        self.AccountsTab = QtWidgets.QWidget()
        self.AccountsTab.setObjectName("AccountsTab")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.AccountsTab)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.Accounts = QtWidgets.QTableView(self.AccountsTab)
        self.Accounts.setAlternatingRowColors(True)
        self.Accounts.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.Accounts.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.Accounts.setSortingEnabled(True)
        self.Accounts.setObjectName("Accounts")
        self.horizontalLayout_4.addWidget(self.Accounts)
        self.tabWidget.addTab(self.AccountsTab, "")
        self.TrialBalanceTab = QtWidgets.QWidget()
        self.TrialBalanceTab.setObjectName("TrialBalanceTab")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.TrialBalanceTab)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Trial_Balance = QtWidgets.QTableView(self.TrialBalanceTab)
        self.Trial_Balance.setAlternatingRowColors(True)
        self.Trial_Balance.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.Trial_Balance.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.Trial_Balance.setSortingEnabled(True)
        self.Trial_Balance.setObjectName("Trial_Balance")
        self.verticalLayout_2.addWidget(self.Trial_Balance)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        self.tabWidget.addTab(self.TrialBalanceTab, "")
        self.AdjustmentsTab = QtWidgets.QWidget()
        self.AdjustmentsTab.setObjectName("AdjustmentsTab")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.AdjustmentsTab)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.Adjustments = QtWidgets.QTableView(self.AdjustmentsTab)
        self.Adjustments.setAlternatingRowColors(True)
        self.Adjustments.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.Adjustments.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.Adjustments.setSortingEnabled(True)
        self.Adjustments.setObjectName("Adjustments")
        self.horizontalLayout_6.addWidget(self.Adjustments)
        self.tabWidget.addTab(self.AdjustmentsTab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.errorTextEdit = QtWidgets.QTextEdit(self.splitter)
        self.errorTextEdit.setObjectName("errorTextEdit")
        self.horizontalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1003, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuImport = QtWidgets.QMenu(self.menuEdit)
        self.menuImport.setObjectName("menuImport")
        self.menuExport = QtWidgets.QMenu(self.menuEdit)
        self.menuExport.setObjectName("menuExport")
        self.menuConsolidation = QtWidgets.QMenu(self.menubar)
        self.menuConsolidation.setObjectName("menuConsolidation")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSaveAs = QtWidgets.QAction(MainWindow)
        self.actionSaveAs.setObjectName("actionSaveAs")
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionBuild = QtWidgets.QAction(MainWindow)
        self.actionBuild.setObjectName("actionBuild")
        self.actionAudit = QtWidgets.QAction(MainWindow)
        self.actionAudit.setObjectName("actionAudit")
        self.actionImportEntities = QtWidgets.QAction(MainWindow)
        self.actionImportEntities.setObjectName("actionImportEntities")
        self.actionImportCostCenters = QtWidgets.QAction(MainWindow)
        self.actionImportCostCenters.setObjectName("actionImportCostCenters")
        self.actionImportAccounts = QtWidgets.QAction(MainWindow)
        self.actionImportAccounts.setObjectName("actionImportAccounts")
        self.actionImportTrialBalance = QtWidgets.QAction(MainWindow)
        self.actionImportTrialBalance.setObjectName("actionImportTrialBalance")
        self.actionImportAdjustments = QtWidgets.QAction(MainWindow)
        self.actionImportAdjustments.setObjectName("actionImportAdjustments")
        self.actionExportEntities = QtWidgets.QAction(MainWindow)
        self.actionExportEntities.setObjectName("actionExportEntities")
        self.actionExportCostCenters = QtWidgets.QAction(MainWindow)
        self.actionExportCostCenters.setObjectName("actionExportCostCenters")
        self.actionExportAccounts = QtWidgets.QAction(MainWindow)
        self.actionExportAccounts.setObjectName("actionExportAccounts")
        self.actionExportTrialBalance = QtWidgets.QAction(MainWindow)
        self.actionExportTrialBalance.setObjectName("actionExportTrialBalance")
        self.actionExportAdjustments = QtWidgets.QAction(MainWindow)
        self.actionExportAdjustments.setObjectName("actionExportAdjustments")
        self.actionRollforward = QtWidgets.QAction(MainWindow)
        self.actionRollforward.setObjectName("actionRollforward")
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuImport.addAction(self.actionImportEntities)
        self.menuImport.addAction(self.actionImportCostCenters)
        self.menuImport.addAction(self.actionImportAccounts)
        self.menuImport.addAction(self.actionImportTrialBalance)
        self.menuImport.addAction(self.actionImportAdjustments)
        self.menuExport.addAction(self.actionExportEntities)
        self.menuExport.addAction(self.actionExportCostCenters)
        self.menuExport.addAction(self.actionExportAccounts)
        self.menuExport.addAction(self.actionExportTrialBalance)
        self.menuExport.addAction(self.actionExportAdjustments)
        self.menuEdit.addAction(self.menuImport.menuAction())
        self.menuEdit.addAction(self.menuExport.menuAction())
        self.menuConsolidation.addAction(self.actionBuild)
        self.menuConsolidation.addAction(self.actionAudit)
        self.menuConsolidation.addAction(self.actionRollforward)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuConsolidation.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(4)
        self.actionNew.triggered.connect(MainWindow.new_menu_item)  # type: ignore
        self.actionOpen.triggered.connect(MainWindow.open_menu_item)  # type: ignore
        self.actionClose.triggered.connect(MainWindow.close_menu_item)  # type: ignore
        self.actionSave.triggered.connect(MainWindow.save_menu_item)  # type: ignore
        self.actionSaveAs.triggered.connect(MainWindow.save_as_menu_item)  # type: ignore
        self.actionQuit.triggered.connect(MainWindow.quit_menu_item)  # type: ignore
        self.actionBuild.triggered.connect(MainWindow.build_menu_item)  # type: ignore
        self.actionImportEntities.triggered.connect(MainWindow.import_menu_item)  # type: ignore
        self.actionImportCostCenters.triggered.connect(MainWindow.import_menu_item)  # type: ignore
        self.actionImportAccounts.triggered.connect(MainWindow.import_menu_item)  # type: ignore
        self.actionImportTrialBalance.triggered.connect(MainWindow.import_menu_item)  # type: ignore
        self.actionImportAdjustments.triggered.connect(MainWindow.import_menu_item)  # type: ignore
        self.actionExportEntities.triggered.connect(MainWindow.export_menu_item)  # type: ignore
        self.actionExportCostCenters.triggered.connect(MainWindow.export_menu_item)  # type: ignore
        self.actionExportAccounts.triggered.connect(MainWindow.export_menu_item)  # type: ignore
        self.actionExportTrialBalance.triggered.connect(MainWindow.export_menu_item)  # type: ignore
        self.actionExportAdjustments.triggered.connect(MainWindow.export_menu_item)  # type: ignore
        self.actionRollforward.triggered.connect(MainWindow.rollforward_menu_item)  # type: ignore
        self.actionAudit.triggered.connect(MainWindow.audit_menu_item)  # type: ignore
        self.entityName.textEdited['QString'].connect(MainWindow.set_entity_name)  # type: ignore
        self.beginningBalanceDate.dateChanged['QDate'].connect(MainWindow.set_beginning_date)  # type: ignore
        self.endingBalanceDate.dateChanged['QDate'].connect(MainWindow.set_ending_date)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Consolidation Station"))
        self.label.setText(_translate("MainWindow", "Entity Name"))
        self.label_2.setText(_translate("MainWindow", "Beginning Balance Date:"))
        self.beginningBalanceDate.setDisplayFormat(_translate("MainWindow", "M/d/yyyy"))
        self.label_3.setText(_translate("MainWindow", "Ending Balance Date:"))
        self.endingBalanceDate.setDisplayFormat(_translate("MainWindow", "M/d/yyyy"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.EntitiesTab), _translate("MainWindow", "Entities"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.CostCentersTab), _translate("MainWindow", "Cost Centers"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.AccountsTab), _translate("MainWindow", "Accounts"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TrialBalanceTab), _translate("MainWindow", "Trial Balance"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.AdjustmentsTab), _translate("MainWindow", "Adjustments"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Data"))
        self.menuImport.setTitle(_translate("MainWindow", "Import"))
        self.menuExport.setTitle(_translate("MainWindow", "Export"))
        self.menuConsolidation.setTitle(_translate("MainWindow", "Consolidation"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setToolTip(_translate("MainWindow", "Create a new consolidation workbook"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setToolTip(_translate("MainWindow", "Open a consolidation workbook file"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setToolTip(_translate("MainWindow", "Save the current consolidation workbook"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSaveAs.setText(_translate("MainWindow", "Save As"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionClose.setToolTip(_translate("MainWindow", "Close the current consolidation workbook"))
        self.actionClose.setShortcut(_translate("MainWindow", "Ctrl+W"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionBuild.setText(_translate("MainWindow", "Build"))
        self.actionAudit.setText(_translate("MainWindow", "Audit"))
        self.actionImportEntities.setText(_translate("MainWindow", "Entities"))
        self.actionImportCostCenters.setText(_translate("MainWindow", "Cost Centers"))
        self.actionImportAccounts.setText(_translate("MainWindow", "Accounts"))
        self.actionImportTrialBalance.setText(_translate("MainWindow", "Trial Balance"))
        self.actionImportAdjustments.setText(_translate("MainWindow", "Adjustments"))
        self.actionExportEntities.setText(_translate("MainWindow", "Entities"))
        self.actionExportCostCenters.setText(_translate("MainWindow", "Cost Centers"))
        self.actionExportAccounts.setText(_translate("MainWindow", "Accounts"))
        self.actionExportTrialBalance.setText(_translate("MainWindow", "Trial Balance"))
        self.actionExportAdjustments.setText(_translate("MainWindow", "Adjustments"))
        self.actionRollforward.setText(_translate("MainWindow", "Rollforward Year"))
