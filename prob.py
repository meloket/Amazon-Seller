#An examnple of the use of threading to allow simultaneous operations in a
#tkinter gui (which is locked to a single thread)


import threading
import Tkinter as tk
from Tkinter import *
import ttk
import os
import subprocess


class Progress():
    """ threaded progress bar for tkinter gui """
    def __init__(self, parent, row, column, columnspan):
        self.maximum = 100
        self.interval = 10
        self.progressbar = ttk.Progressbar(parent, orient=tk.HORIZONTAL,
                                           mode="indeterminate",
                                           maximum=self.maximum)
        self.progressbar.grid(row=row, column=column,
                              columnspan=columnspan, sticky="we")
        self.thread = threading.Thread()
        self.thread.__init__(target=self.progressbar.start(self.interval),
                             args=())
        self.thread.start()

    def pb_stop(self):
        """ stops the progress bar """
        if not self.thread.isAlive():
            VALUE = self.progressbar["value"]
            self.progressbar.stop()
            self.progressbar["value"] = VALUE

    def pb_start(self):
        """ starts the progress bar """

        p = subprocess.Popen('scrapy crawl xmlparser', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        retval = p.wait()
        # p = subprocess.Popen('scrapy crawl xmlparser -o edata.csv -t csv', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # # for line in p.stdout.readlines():
        #     # text.insert(0, line)
        #     # print line,
        # retval = p.wait()
        if not self.thread.isAlive():
            print()
            VALUE = self.progressbar["value"]
            self.progressbar.configure(mode="indeterminate",
                                       maximum=self.maximum,
                                       value=VALUE)
            self.progressbar.start(self.interval)

    def pb_clear(self):
        """ stops the progress bar """
        if not self.thread.isAlive():
            self.progressbar.stop()
            self.progressbar.configure(mode="determinate", value=0)

    def pb_complete(self):
        """ stops the progress bar and fills it """
        if not self.thread.isAlive():
            self.progressbar.stop()
            self.progressbar.configure(mode="determinate",
                                       maximum=self.maximum,
                                       value=self.maximum)

def printmsg():
    """ prints a message in a seperate thread to tkinter """
    print("proof a seperate thread is running")


class AppGUI(tk.Frame):
    """ class to define tkinter GUI"""
    def __init__(self, parent,):
        tk.Frame.__init__(self, master=parent)

        # text = Entry(parent)
        # text.pack(side=LEFT,fill=BOTH, expand=1)

        prog_bar = Progress(parent, row=0, column=0, columnspan=2)
        # Button 1
        start_button = ttk.Button(parent, text="start",
                                  command=prog_bar.pb_start)
        start_button.grid(row=1, column=0)
        # Button 2
        stop_button = ttk.Button(parent, text="stop",
                                 command=prog_bar.pb_stop)
        stop_button.grid(row=1, column=1)
        # Button 3
        complete_button = ttk.Button(parent, text="complete",
                                     command=prog_bar.pb_complete)
        complete_button.grid(row=2, column=0)
        # Button 4
        clear_button = ttk.Button(parent, text="clear",
                                  command=prog_bar.pb_clear)
        clear_button.grid(row=2, column=1)
        # Button 5
        test_print_button = ttk.Button(parent, text="thread test",
                                       command=printmsg)
        test_print_button.grid(row=3, column=0, columnspan=2, sticky="we")


ROOT = tk.Tk()
APP = AppGUI(ROOT)
ROOT.mainloop()
