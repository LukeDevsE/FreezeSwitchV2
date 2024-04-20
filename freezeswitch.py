import psutil
from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout,QComboBox,QCheckBox
from PyQt5.QtCore import Qt
import keyboard
import qdarkstyle
# handle = win32process.OpenProcess(win32process.PROCESS_ALL_ACCESS, False, 12824)




def get_process_id_by_name(name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == name:
            return proc.info['pid']
    return None
def main():
    app = QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    window = QWidget()
    window.setWindowFlags(Qt.WindowType.WindowCloseButtonHint)
    window.setWindowTitle("Freeze Switch V2")

    layout = QVBoxLayout()
    text = QComboBox()
    text.addItems(["`","1","2","3","4","5","6","7","8","9","0","-","=","q","e","r","t","y","u","i","o","p"])
    text.setCurrentText("`")
    button = QCheckBox("Freeze Roblox!")
    button.clicked.connect(lambda: toggle(button.isChecked()))
    keyboard.hook(lambda event: Toggletoggle(button,text.currentText()))
    layout.addWidget(button)
    layout.addWidget(text)
    window.setLayout(layout)
    window.show()
    window.setGeometry(638,218,149,104)
    app.exec_()


def Toggletoggle(button: QCheckBox, key):
    if keyboard.is_pressed(key):
        button.setChecked(not button.isChecked())
        toggle(button.isChecked())
def toggle(checked):
    if (checked):
        pid = get_process_id_by_name("RobloxPlayerBeta.exe")
        if pid != None:
            process = psutil.Process(pid)
            process.suspend()
    else:
        pid = get_process_id_by_name("RobloxPlayerBeta.exe")
        if pid != None:
            process = psutil.Process(pid)
            process.resume()
if __name__ == "__main__":
    main()
