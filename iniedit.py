import sys
import configparser
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg


class FileHandler():
    def __init__(self):
        self.openFile = ''
        self.parser = configparser.ConfigParser()

    def fileOpen(self, filepath):
        self.parser.read(filepath)
        self.openFile = filepath

    def fileSave(self, filepath):
        pass

    def fileNew(self, filepath):
        pass

    def getSections(self):
        if not self.openFile:
            return []

        return self.parser.sections()


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()

        self.app = App()
        self.setCentralWidget(self.app)

        self.setWindowTitle('Ini Editor')
        self.setGeometry(10, 10, 600, 400)

        self.fileHandler = FileHandler()

        menubar = self.menuBar()
        self.populateMenuBar(menubar)

        self.center()
        self.show()

    def populateMenuBar(self, menubar):
        newAction = qtw.QAction("&New", self)
        newAction.setStatusTip("Create a file")
        newAction.triggered.connect(self.fileNew)
        newAction.setShortcut('Ctrl+N')

        openAction = qtw.QAction("&Open", self)
        openAction.setStatusTip("Open a file")
        openAction.triggered.connect(self.fileOpen)
        openAction.setShortcut('Ctrl+O')

        saveAction = qtw.QAction("&Save", self)
        saveAction.setStatusTip("Save a file")
        saveAction.triggered.connect(self.fileSave)
        saveAction.setShortcut('Ctrl+S')

        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)

    def fileOpen(self):
        fileToOpen = qtw.QFileDialog.getOpenFileName(self, "Select a file", "", "Configuration Files (*.ini)")
        fileToOpen = str(fileToOpen[0])
        if fileToOpen:
            self.fileHandler.fileOpen(fileToOpen)
            self.app.populateSections(self.fileHandler.getSections())

    def fileSave(self):
        pass

    def fileNew(self):
        pass

    def center(self):
        frameGeometry = self.frameGeometry()
        center = qtw.QDesktopWidget().availableGeometry().center()
        frameGeometry.moveCenter(center)
        self.move(frameGeometry.topLeft())


class App(qtw.QWidget):
    def __init__(self):
        super().__init__()

# left sections
        self.leftBox = qtw.QVBoxLayout()
        self.leftBox.setSizeConstraint(qtw.QLayout.SetMinAndMaxSize)
        self.leftBox.setContentsMargins(0, 0, 0, 0)
        self.leftBox.setGeometry(qtc.QRect(0,0,50,50))

        self.sections = qtw.QListWidget(self)
        self.sections.setGeometry(0,0,50,50)

        self.leftBox.addWidget(self.sections)

# right values
        self.rightBox = qtw.QVBoxLayout()
        self.rightBox.setSizeConstraint(qtw.QLayout.SetMinAndMaxSize)
        self.rightBox.setContentsMargins(0, 0, 0, 0)
        self.rightBox.setAlignment(qtc.Qt.AlignTop)

        lab = qtw.QLabel()
        lab.setText("we are")
        self.rightBox.addWidget(lab)

#main display
        self.mainLayout = qtw.QHBoxLayout()
        self.mainLayout.setAlignment(qtc.Qt.AlignLeft)

        self.mainLayout.addLayout(self.leftBox)
        self.mainLayout.addLayout(self.rightBox)

        self.setLayout(self.mainLayout)

    def populateSections(self, sections):
        if not sections:
            return

        for section in sections:
            #listwidgetitem = qtw.QListWidgetItem(section)
            self.sections.addItem(section)

        self.sections.itemClicked.connect(self.sectionClicked)

    def sectionClicked(self, chosenSection):
        print(chosenSection.text())


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

