import os
from datetime import date, datetime

from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener

filePath = ''
eventDict = {}
startTime = 0
logPeriodMinutes = 1  # file log will happen once per minute at most

def on_press(key):
    global eventDict
    eventDict['keyPresses'] += 1  # one more event encountered

    captureInfo()

    #print("Key pressed: {0}".format(key))


def on_release(key):
    global eventDict
    eventDict['keyReleases'] += 1  # one more event encountered

    captureInfo()

    #print("Key released: {0}".format(key))


def on_move(x, y):
    global eventDict
    eventDict['mouseMoves'] += 1  # one more event encountered

    captureInfo()

    #print("Mouse moved to ({0}, {1})".format(x, y))


def on_click(x, y, button, pressed):
    global eventDict

    if pressed:
        eventDict['mousePresses'] += 1  # one more event encountered
        #print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
    else:
        eventDict['mouseReleases'] += 1  # one more event encountered
        #print('Mouse released at ({0}, {1}) with {2}'.format(x, y, button))

    captureInfo()


def on_scroll(x, y, dx, dy):
    global eventDict
    eventDict['mouseScrolls'] += 1  # one more event encountered

    captureInfo()

    #print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))


def reset_eventDict():
    global eventDict
    eventDict = {'keyPresses': 0, 'keyReleases': 0, 'mouseMoves': 0, 'mousePresses': 0, 'mouseReleases': 0,
                 'mouseScrolls': 0}

def updateStartTime():
    global startTime
    startTime = datetime.now()


def checkTimeLapseInMinutes():
    global startTime
    diffTime = (datetime.now() - startTime).seconds / 60
    return diffTime


def logEventsToFile():
    global filePath, eventDict

    with open(filePath, 'a', encoding='utf-8') as f:
        today = date.today()
        dateStr = today.strftime("%b_%d_%Y")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        f.write(f"Record {dateStr} at {current_time}\n")
        f.write(f"Key presses: {eventDict['keyPresses']}\
        Key releases: {eventDict['keyReleases']}\
        Mouse moves: {eventDict['mouseMoves']}\
        Mouse presses: {eventDict['mousePresses']}\
        Mouse releases: {eventDict['mouseReleases']}\
        Mouse scrolls: {eventDict['mouseScrolls']}\n\n")

def captureInfo():
    global logPeriodMinutes

    diffTime = checkTimeLapseInMinutes()
    if diffTime >= logPeriodMinutes:
        logEventsToFile()
        reset_eventDict()
        updateStartTime()

def monitor_activity():
    global filePath

    reset_eventDict()  # initializes eventDict at start
    target_folder="C:\\temp\keymouseLogs"  # subfolder where all activity will be logged

    today = date.today()
    dateStr = today.strftime("%b_%d_%Y")
    logFileName = "activityLog_" + dateStr + ".txt"

    if os.path.exists(target_folder):
        # Subfolder exists. Create log file.
        filePath=os.path.join(target_folder, logFileName)
    else:
        # Subfolder does NOT exists. Create logfile with the folder
        os.mkdir(target_folder)
        filePath=os.path.join(target_folder, logFileName)

    with open(filePath, 'a', encoding='utf-8') as f:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        f.write(f"Logging after power cycle {today} at {current_time}\n")

    updateStartTime()  # capture current time as reference

    # Setup the listener threads
    keyboard_listener = KeyboardListener(on_press=on_press, on_release=on_release)
    mouse_listener = MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)

    # Start the threads and join them so the script doesn't end early
    keyboard_listener.start()
    mouse_listener.start()
    keyboard_listener.join()
    mouse_listener.join()


