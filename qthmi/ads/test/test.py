"""
Created on 25.03.2013
@author: lehmann

"""
import sys
import pyads
from PyQt5.QtWidgets import QDialog, QCheckBox, QVBoxLayout, QApplication


class MainForm(QDialog):

    def _initADS(self):
        self.adsPort = pyads.open_port()
        self.adsAdr = pyads.get_local_address()
        self.adsAdr.port = 5000

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        # ADS initialisieren
        self._initADS()

        # Elemente
        bit1CheckBox = QCheckBox("Bit1")
        (errCode, bit1) = pyads.read(
            self.adsAdr, pyads.INDEXGROUP_MEMORYBIT, 100 * 8 + 0,
            pyads.PLCTYPE_BOOL
        )

        if errCode == 0:
            bit1CheckBox.setChecked(bit1)

        bit2CheckBox = QCheckBox("Bit2")
        (errCode, bit2) = pyads.read(
            self.adsAdr, pyads.INDEXGROUP_MEMORYBIT, 100 * 8 + 1,
            pyads.PLCTYPE_BOOL
        )

        if errCode == 0:
            bit2CheckBox.setChecked(bit2)

        bit3CheckBox = QCheckBox("Bit3")
        (errCode, bit3) = pyads.read(
            self.adsAdr, pyads.INDEXGROUP_MEMORYBIT, 100 * 8 + 2,
            pyads.PLCTYPE_BOOL
        )

        if errCode == 0:
            bit3CheckBox.setChecked(bit3)

        bit4CheckBox = QCheckBox("Bit4")
        (errCode, bit4) = pyads.read(
            self.adsAdr, pyads.INDEXGROUP_MEMORYBIT, 100 * 8 + 3,
            pyads.PLCTYPE_BOOL
        )

        if errCode == 0:
            bit4CheckBox.setChecked(bit4)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(bit1CheckBox)
        layout.addWidget(bit2CheckBox)
        layout.addWidget(bit3CheckBox)
        layout.addWidget(bit4CheckBox)
        self.setLayout(layout)

        # Signale
        self.bit1CheckBox.stateChanged.connect(self.bit1CheckBox_stateChanged)
        self.bit2CheckBox.stateChanged.connect(self.bit2CheckBox_stateChanged)
        self.bit3CheckBox.stateChanged.connect(self.bit3CheckBox_stateChanged)
        self.bit4CheckBox.stateChanged.connect(self.bit4CheckBox_stateChanged)

    def __del__(self):
        pyads.close_port()

    def bit1CheckBox_stateChanged(self, state):
        pyads.write(self.adsAdr, pyads.INDEXGROUP_MEMORYBIT,
                    100 * 8 + 0, state, pyads.PLCTYPE_BOOL)

    def bit2CheckBox_stateChanged(self, state):
        pyads.write(self.adsAdr, pyads.INDEXGROUP_MEMORYBIT,
                    100 * 8 + 1, state, pyads.PLCTYPE_BOOL)

    def bit3CheckBox_stateChanged(self, state):
        pyads.write(self.adsAdr, pyads.INDEXGROUP_MEMORYBIT,
                    100 * 8 + 2, state, pyads.PLCTYPE_BOOL)

    def bit4CheckBox_stateChanged(self, state):
        pyads.write(self.adsAdr, pyads.INDEXGROUP_MEMORYBIT,
                    100 * 8 + 3, state, pyads.PLCTYPE_BOOL)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    frm = MainForm()
    frm.show()
    app.exec_()
