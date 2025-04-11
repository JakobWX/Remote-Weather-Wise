from flask import Flask, request, send_from_directory
import keyboard
import pygetwindow as gw
import pyautogui
import time
import json

with open('config.json') as config_file:
    config = json.load(config_file)

TARGET_WINDOW = config['targetApp']
PASSWORD = config['password']
PORT = config['port'] or 5000

app = Flask(__name__)

def focus_window():
    windows = gw.getWindowsWithTitle(TARGET_WINDOW)
    if windows:
        win = windows[0]
        try:
            win.activate()
            time.sleep(.2)
        except:
            return False
       
        return True
    else:
        return False

@app.route('/')
def index():
    return send_from_directory('.', 'controller.html')


def openRadar():
    keyboard.press('shift')
    keyboard.press_and_release("1")
    keyboard.release('shift')

@app.route('/zoom', methods=['POST'])
def zoom():
    password = request.form.get('password')
    if password != PASSWORD:
        return 'Unauthorized', 401

    if not focus_window():
        return 'No Window', 401

    direction = request.form.get('direction')
    if direction == 'in':
        keyboard.press_and_release('add')

    elif direction == 'out':
        keyboard.press_and_release('subtract')
    elif direction == 'reflectivity': 
        openRadar()
        keyboard.press('shift')
        keyboard.press_and_release("r")
        keyboard.release('shift')
    elif direction == 'velocity':
        openRadar()
        keyboard.press('shift')
        keyboard.press_and_release("v")
        keyboard.release('shift')
    elif direction == "satellite":
        keyboard.press('shift')
        keyboard.press_and_release("2")
        keyboard.release('shift')
    elif direction == "radar":
        openRadar()
    elif direction == "playLoop": 
        keyboard.press_and_release("space")
    return 'OK'

@app.route('/verify', methods=['POST'])
def verify():
    password = request.headers.get('x-password')
    if password == PASSWORD:
        return 'OK', 200
    else:
        return 'Unauthorized', 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)