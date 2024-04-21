import psutil
from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout,QComboBox,QCheckBox,QSpinBox,QLabel,QPushButton
from PyQt5.QtCore import Qt,QEventLoop,QTimer
import keyboard
import qdarkstyle
from time import sleep
# handle = win32process.OpenProcess(win32process.PROCESS_ALL_ACCESS, False, 12824)
def get_process_id_by_name(name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == name:
            return proc.info['pid']
    return None

pid = get_process_id_by_name("RobloxPlayerBeta.exe")

def main():
    app = QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    window = QWidget()
    window.setWindowFlags(Qt.WindowType.WindowCloseButtonHint)
    window.setWindowTitle("Freeze Switch V2")

    layout = QVBoxLayout()
    text = QComboBox()
    label = QLabel()
    label.setText("Seconds Default 7, 0 to disable. this waits a set amount of time and unfreezes")
    cooldown = QSpinBox()
    cooldown.setValue(7)
    text.addItems(["`","1","2","3","4","5","6","7","8","9","0","-","=","q","e","r","t","y","u","i","o","p"])
    text.setCurrentText("`")
    button = QCheckBox("Freeze Roblox!")
    button.clicked.connect(lambda: toggle(button.isChecked(),cooldown.value(),button))
    keyboard.hook(lambda event: Toggletoggle(button,text.currentText(),cooldown.value()))
    layout.addWidget(button)
    layout.addWidget(text)
    layout.addWidget(label)
    layout.addWidget(cooldown)
    window.setLayout(layout)
    window.show()
    window.setGeometry(638,218,149,104)
    app.exec_()


def Toggletoggle(button: QCheckBox, key, cd):
    #global pid  # Added global declaration
    if keyboard.is_pressed(key) and button.isEnabled() and cd > 0:
        button.setChecked(not button.isChecked())
        toggle(button.isChecked(),cd,button)
    elif keyboard.is_pressed(key) and button.isEnabled() and cd == 0:
        button.setChecked(not button.isChecked())
        toggle(button.isChecked(),cd,button)

        
def toggle(checked, cd, button: QCheckBox):
    pid = globals()["pid"]
  # Added global declaration
    print(pid)
    if (checked):
        if pid != None:
            try:
                process = psutil.Process(pid)
                process.suspend()
            except:
                print("user closed program")
        else:
            globals()["pid"] = get_process_id_by_name("RobloxPlayerBeta.exe")
            pid = globals()["pid"]
            if pid != None:
                try:
                    process = psutil.Process(pid)
                    process.suspend()
                except:
                    print("user closed program")
        if cd > 0:
            button.setDisabled(True)
            loop = QEventLoop()
            QTimer.singleShot(cd * 1000, loop.quit)
            loop.exec_()
            button.setDisabled(False)
            if pid != None:
                try:
                    process = psutil.Process(pid)
                    process.resume()
                except:
                    print("user closed program")
            button.setChecked(False)
    else:
        if pid != None:
            try:
                process = psutil.Process(pid)
                process.resume()
                pid = None
            except:
                print("user closed program")
        else:
            pid = get_process_id_by_name("RobloxPlayerBeta.exe")
            if pid != None:
                try:
                    process = psutil.Process(pid)
                    process.resume()
                except:
                    print("user closed program")
if __name__ == "__main__":
    main()
