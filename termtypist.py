import time
from curses import wrapper
import curses
from collections import deque

input = ''
latestWpm = deque([], 10)
initTime = time.time()

class GameOver(Exception): pass
class Exit(Exception): pass

def main(stdscr):
    stdscr.clear()

    try:
        while True:
            startGame(stdscr)
    except Exit:
        pass


def startGame(stdscr):
    global input
    global initTime

    input = ''
    stdscr.clear()

    try:
        while True:
            char = stdscr.getkey()
            startTimer()

            if char == '\\':
                getCommand(stdscr)
            elif char == '\x7f':
                backspace(stdscr)
            elif char == '\n':
                submitInput(stdscr)
            elif len(char) == 1:
                input += char
                stdscr.addch(char)
            stdscr.refresh()
    except GameOver:
        pass

def getCommand(stdscr):
    global input
    global initTime
    command = stdscr.getkey()

    if command == 'q':
        raise Exit
    elif command == 'n':
        startGame(stdscr)
    # elif command == 'c':
    #     latestWpm = deque([], 10)

def submitInput(stdscr):
    global input
    global initTime
    endTime = time.time()
    wpm = calculateWpm(endTime)

    stdscr.addstr('\n' + wpm + '\n\n')
    addLatestWpmPanel(stdscr)
    stdscr.addstr(3, 0, '')

    char = stdscr.getkey()

    if char == '\\':
        getCommand(stdscr)
    else:
        raise GameOver

def backspace(stdscr):
    global input

    input = input[:-1]
    reloadWindow(stdscr)

def startTimer():
    global initTime

    if len(input) == 0:
        initTime = time.time()

def calculateWpm(endTime):
    global latestWpm

    finalTimeInMinutes = (endTime - initTime) / 60
    grossWpm = int((len(input) / 5) / finalTimeInMinutes)
    # netWpm = int((grossWpm - errors) / finalTimeInMinutes)
    # prettyNetWpm = str(netWpm if netWpm > 0 else 0) + ' WPM'
    prettyGrossWpm = str(grossWpm) + ' WPM'

    latestWpm.appendleft(grossWpm)

    return prettyGrossWpm

def addLatestWpmPanel(stdscr):
    height = 0
    width = stdscr.getmaxyx()[1] - 20

    stdscr.addstr(0, width - 20, 'Average WPM')
    stdscr.addstr(1, width - 20, str(averageWpm()) + ' WPM')
    stdscr.addstr(height, width, 'Latest results')
    height += 1

    for wpm in latestWpm:
        stdscr.addstr(height, width, str(wpm) + ' WPM')
        height += 1

def averageWpm():
    average = 0

    for wpm in latestWpm:
        average += wpm

    return (average / len(latestWpm)) if len(latestWpm) > 0 else 0

def reloadWindow(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 0, input)


wrapper(main)
