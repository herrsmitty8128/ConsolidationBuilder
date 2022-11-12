
import sys
from PyQt5 import QtWidgets
from ConsolidationMainWindow import ConsolidationMainWindow



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ConsolidationMainWindow(app)
    window.show()
    sys.exit(app.exec_())