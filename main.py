# This Python file uses the following encoding: utf-8
import sys
import time
from functools import partial
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QThread
from PySide6.QtCore import QThread, QTime
from PySide6.QtWidgets import *
from datetime import datetime
from playsound import playsound


class StopWatch(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.h = 0
        self.m = 0
        self.s = 0

    def reset(self):
        self.h = 0
        self.m = 0
        self.s = 0

    def increase(self):
        self.s += 1
        if self.s >= 60:
            self.s = 0
            self.m += 1
        if self.m >= 60:
            self.m = 0
            self.h += 1

    def run(self):
        while True:
            self.increase()
            window.ui.lbl_stopwatch.setText(f"{'%0.2d' % self.h}:{'%0.2d' % self.m}:{'%0.2d' % self.s}")
            time.sleep(1)


class Timer(QThread):
    def __init__(self, h, m, s):
        QThread.__init__(self)
        self.hh = h
        self.mm = m
        self.ss = s

    def reset(self):
        self.hh = 0
        self.mm = 0
        self.ss = 0

    def decrease(self):

        if self.ss == 0 and self.mm == 0 and self.hh == 0:
            return
        if self.ss <= 0:
            self.mm -= 1
            self.ss += 60
        if self.mm < 0:
            self.hh -= 1
            self.mm += 60
        self.ss -= 1

    def run(self):
        while True:
            self.decrease()
            window.ui.lbl_timer.setText(f"{'%0.2d' % self.hh}:{'%0.2d' % self.mm}:{'%0.2d' % self.ss}")
            time.sleep(1)


class Alarm(QThread):
    def __init__(self, h, m):
        QThread.__init__(self)
        self.hhh = int('%0.2d' % h)
        self.mmm = int('%0.2d' % m)

    def run(self):

        while True:
            self.time = datetime.now()
            self.hour = int(self.time.strftime("%H"))
            self.minute = int(self.time.strftime("%M"))
            self.second = int(self.time.strftime("%S"))
            a = Timer(int(self.hhh - self.hour), (self.mmm - self.minute), (00 - self.second))
            a.decrease()
            window.ui.lbl_alarm.setText(f"{'%0.2d' % a.hh}:{'%0.2d' % a.mm}"
                                        f":{'%0.2d' % a.ss}")
            if self.hour == self.hhh:
                if self.minute == self.mmm:
                    print("Wake Up!")
                    playsound('Alarm.wav')
                    break
            time.sleep(1)


class Main(QWidget):
    def __init__(self):
        super(Main, self).__init__()

        loader = QUiLoader()
        self.ui = loader.load("form.ui")
        self.setWindowTitle("Clock")
        self.ui.btn_stopwatch_start.clicked.connect(self.startStopWatch)
        self.ui.btn_stopwatch_pause.clicked.connect(self.pasueStopWatch)
        self.ui.btn_stopwatch_stop.clicked.connect(self.stopStopWatch)
        self.ui.btn_stopwatch_lap.clicked.connect(self.lapStopWatch)
        self.ui.btn_timer_start.clicked.connect(self.startTimer)
        self.ui.btn_timer_pause.clicked.connect(self.pasueTimer)
        self.ui.btn_timer_stop.clicked.connect(self.stopTimer)
        self.ui.btn_alarm_start.clicked.connect(self.startAlarm)
        self.ui.btn_alarm_stop.clicked.connect(self.stopAlarm)
        self.stop = StopWatch()

        self.ui.show()

    def pasueStopWatch(self):
        self.stop.terminate()

    def stopStopWatch(self):
        self.stop.terminate()
        self.ui.lbl_stopwatch.setText("00:00:00")
        self.stop.reset()

    def startStopWatch(self):
        self.stop.start()

    def lapStopWatch(self):
        label = QLabel()
        label.setText(self.ui.lbl_stopwatch.text())
        self.ui.lap_stopwatch.addWidget(label)

    def pasueTimer(self):
        self.timer.terminate()

    def stopTimer(self):
        self.timer.terminate()
        self.ui.lbl_timer.setText("00:00:00")
        self.timer.reset()

    def startTimer(self):
        self.timer = Timer(self.ui.spin_hour.value(), self.ui.spin_minute.value(), self.ui.spin_second.value())
        self.timer.start()

    def stopAlarm(self):
        self.alarm.terminate()
        self.ui.lbl_alarm.setText("00:00:00")

    def startAlarm(self):
        self.alarm = Alarm(self.ui.spin_hour_alarm.value(), self.ui.spin_minute_alarm.value())
        self.alarm.start()


if __name__ == "__main__":
    app = QApplication([])
    window = Main()
    sys.exit(app.exec())
