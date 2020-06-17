#!/usr/bin/env python

import os
import sys
import time
import yaml

from functools import partial
from termcolor import colored

from biff.tinytim import Resample,TinyTim

class core:
    def __init__(self):

        try:
            with open(r'biff.yaml') as file:
                parameters = yaml.load(file, Loader=yaml.FullLoader)
                self.biffParam = parameters['biff']
                self.tinyParam = parameters['tinytim']
        except IOError:
            sys.exit(colored('ERROR: biff.yaml could not be found.\n',"red"))

        while 1:
            os.system('clear')
            self.PrintMenu()

            Run = { '10' : self.Tiny1,
                    '11' : self.Tiny2,
                    '12' : partial(self.Resample,primary='true',secondary='true'),
                    '13' : partial(self.Resample,primary='true'),
                    '14' : partial(self.Resample,secondary='true'),
                    'q'  : self.Exit }

            Option = raw_input(colored("Selection:  ","green"))
            Run.get(Option,self.PrintError)()

    def EndTime(self):
        self.endtime = time.strftime('%A, %B %d, %Y %X %Z' ,time.localtime())
        print(colored("\nStarted at:\t %s","green")) % (self.starttime)
        print(colored("Finished at:\t %s \n","green")) % (self.endtime)
        GoOn = raw_input("Press Enter To Continue...")

    def Exit(self):
        sys.exit(colored("\nThank You for Using BIFF\n","green"))

    def PrintError(self):
        print(colored("\nSelected input is not an option!\n","red"))
        GoOn = raw_input(colored("Press Enter To Continue...","green"))

    def PrintMenu(self):
        print colored("\n BIFF - BInary Fitting Facility ","green")
        print colored("=" * 32 + "\n","green")

        #print colored(" Automated Reductions ","green")
        #print colored("-" * 22,"green")
        #print colored(" 1 - Run A Single and Binary PSF Reduction -- NOT TESTED!!","red")
        #print colored(" 2 - Run A Single PSF Reduction -- NOT TESTED!!","red")
        #print colored(" 3 - Run A Binary PSF Reduction -- NOT TESTED!!","red")

        #print colored("\n Focus Testing ","green")
        #print colored("-" * 15,"green")
        #print colored(" 4 - Run Single and Binary PSF Focus Tests (-5 to 5 microns)","red")
        #print colored(" 5 - Run Single PSF Focus Tests (-20 to 20 microns)","red")
        #print colored(" 6 - Run Binary PSF Focus Tests (-5 to 5 microns)","red")

        print colored("\n Model PSFs ","green")
        print colored("-" * 12,"green")
        print colored("10 - Run Tiny1","green")
        print colored("11 - Run Tiny2","green")
        print colored("12 - Resample Model PSF (Primary and Secondary)","green")
        print colored("13 - Resample Model PSF (Primary Only)","green")
        print colored("14 - Resample Model PSF (Secondary Only)","green")

        #print colored("\n Individual Tasks ","green")
        #print colored("-" * 18,"green")
        #print colored("20 - Make Binary Configuration Files (5x5 pixels)","red")
        #print colored("21 - Find Background -- NOT TESTED!!","red")
        #print colored("22 - Find Best Single Model","red")
        #print colored("23 - Find Best Binary Model","red")
                
        print colored("\nq - Quit the Program\n","green")

    def Resample(self, **kwargs):
        self.StartTime()
        Run = Resample(self.biffParam)
        Run.WritePSFs(**kwargs)
        self.EndTime()

    def Tiny1(self):
        Tiny = TinyTim(self.tinyParam)
        Tiny.tiny1()

    def Tiny2(self):
        Tiny = TinyTim(self.tinyParam)
        Tiny.tiny2()

    def StartTime(self):
        self.starttime = time.strftime('%A, %B %d, %Y %X %Z' ,time.localtime())

DoingResearch = core()
