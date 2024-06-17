# imports
import psutil
from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout,QComboBox,QCheckBox,QSpinBox,QLabel,QPushButton,QMessageBox
from PyQt5.QtCore import Qt,QEventLoop,QTimer
from PyQt5.QtGui import QFont,QFontDatabase,QIcon
import keyboard
import qdarkstyle
import urllib.request, json 
import webbrowser
import sys,os
from time import sleep
# imports end
#gets pid from the name
def get_process_id_by_name(name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == name:
            return proc.info['pid']
    return None
# try to see if roblox is open and if it is set it
pid = get_process_id_by_name("RobloxPlayerBeta.exe")

version = "https://github.com/LukeDevsE/FreezeSwitchV2/releases/tag/v2.0.3"
basedir = os.path.dirname(__file__)
#main ui code
def main():
    #initialize app
    app = QApplication([])
    #set cool dark theme
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    #make window
    window = QWidget()
    # make it so theres only the x
    window.setWindowFlags(Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowStaysOnTopHint)
    window.setWindowOpacity(0.75)
    window.setWindowIcon(QIcon(os.path.join(basedir, 'icon.png')))
    #qt5 is pretty cool, but this just sets the title of the window to Freeze Switch V2, kinda obv
    window.setWindowTitle("Freeze Switch V2")
    idofthis = QFontDatabase.addApplicationFont(os.path.join(basedir, 'Geologica-Medium.ttf'))
    font = QFont("Geologica Roman Medium",8)
    
    #basically it puts stuff up to down
    layout = QVBoxLayout()
    #this is the key picker
    text = QComboBox()
    #label for the cooldown
    label = QLabel()
    label.setText("Seconds Default 0, 0 to disable. This waits a set amount of time and unfreezes")
    label.setFont(font)
    
    #cooldown number
    cooldown = QSpinBox()
    #default number
    cooldown.setValue(0)
    #make a max, since anything above 9, will just kick you from the game for no internet
    cooldown.setMaximum(9)
    #add all the keys to the key picker
    text.addItems(["`","1","2","3","4","5","6","7","8","9","0","-","=","q","e","r","t","y","u","i","o","p"])
    #set default to `
    text.setCurrentText("`")
    #the main freeze button
    button = QCheckBox("Freeze Roblox!")
    button.setFont(font)
    #when freeze button clickeed, call toggle function and give the state of the button (checked), the cooldown number, and the button itself.
    button.clicked.connect(lambda: toggle(button.isChecked(),cooldown.value(),button))
    #main keyboard function where if you press a key, it freezes. it passes in, the button its self, the key you picked, and the cooldown value
    keyboard.hook(lambda event: Toggletoggle(button,text.currentText(),cooldown.value()))
    # adds all the ui to the layout
    layout.addWidget(button)
    layout.addWidget(text)
    layout.addWidget(label)
    layout.addWidget(cooldown)
    window.setLayout(layout)
    #shows the window
    window.show()
    #sets the size
    window.setGeometry(638,218,149,104)
    window.setFixedSize(window.size())
    try:
        with urllib.request.urlopen("https://api.github.com/repos/LukeDevsE/FreezeSwitchV2/releases") as url:
            try:
                data = json.load(url)
                if version != data[0]['html_url']:
                    messagebox = QMessageBox()
                    messagebox.setText("There is a new update, pressing yes will send you to the download page (github)")
                    messagebox.setWindowTitle("New Update!")
                    messagebox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    messagebox.setWindowIcon(QIcon(os.path.join(basedir, 'icon.png')))
                    messagebox.setFont(font)
                    btn = messagebox.exec_()
                if btn == QMessageBox.Yes:
                    webbrowser.open(data[0]['html_url'], new=0, autoraise=True)
            except:
                print("error getting update")
    except:
        print("offline")
    #and executes the app
    app.exec_()

#this gets called when you press the key to turn on the freeze (default is `)
def Toggletoggle(button: QCheckBox, key, cd):
    #check if your pressing that key, and the checkbox is enabled and the cooldown is above 0 (because it gets disabled if its zero)
    if keyboard.is_pressed(key) and button.isEnabled() and cd > 0:
        #toggles the button checked
        button.setChecked(not button.isChecked())
        #and calls the toggle function (the same one when you click the toggle)
        toggle(button.isChecked(),cd,button)
    elif keyboard.is_pressed(key) and button.isEnabled() and cd == 0:
        # same code as the other one but instead this runs if cd is disabled
        button.setChecked(not button.isChecked())
        toggle(button.isChecked(),cd,button)

        
def toggle(checked, cd, button: QCheckBox):
    # we get the global variable (if you edit a variable in here, it will only set the value in here)
    pid = globals()["pid"]
    # print it for debugging
    print(pid)
    # if its enabled do some more code
    if (checked):
        if pid != None:
            try:
                process = psutil.Process(pid)
                process.suspend()
            except:
                print("user closed program")
                globals()["pid"] = get_process_id_by_name("RobloxPlayerBeta.exe")
                pid = globals()["pid"]
                if pid != None:
                    process = psutil.Process(pid)
                    process.suspend()
        else:
            globals()["pid"] = get_process_id_by_name("RobloxPlayerBeta.exe")
            pid = globals()["pid"]
            if pid != None:
                try:
                    process = psutil.Process(pid)
                    process.suspend()
                except:
                    print("user closed program")
                    globals()["pid"] = get_process_id_by_name("RobloxPlayerBeta.exe")
                    pid = globals()["pid"]
                    if pid != None:
                        process = psutil.Process(pid)
                        process.suspend()
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
                    globals()["pid"] = get_process_id_by_name("RobloxPlayerBeta.exe")
                    pid = globals()["pid"]
                    if pid != None:
                        process = psutil.Process(pid)
                        process.resume()
            button.setChecked(False)
    else:
        if pid != None:
            try:
                process = psutil.Process(pid)
                process.resume()
            except:
                print("user closed program")
                globals()["pid"] = get_process_id_by_name("RobloxPlayerBeta.exe")
                pid = globals()["pid"]
                if pid != None:
                    process = psutil.Process(pid)
                    process.resume() 
        else:
            pid = get_process_id_by_name("RobloxPlayerBeta.exe")
            if pid != None:
                try:
                    process = psutil.Process(pid)
                    process.resume()
                except:
                    print("user closed program")
                    globals()["pid"] = get_process_id_by_name("RobloxPlayerBeta.exe")
                    pid = globals()["pid"]
                    if pid != None:
                        process = psutil.Process(pid)
                        process.resume()
if __name__ == "__main__":
    main()
