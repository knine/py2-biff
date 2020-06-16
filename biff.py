#!/usr/bin/env python

import os
import sys
import time
from termcolor import colored
import yaml

from biff.tinytim import Resample,TinyTim
from psf import PSF
#from psf import PSFTools

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

            Run = { '1' : self.ReductionAll,
                    '2' : self.ReductionSingle,
                    '3' : self.ReductionBinary,
                    '4' : self.FocusTestsAll,
                    '5' : self.FocusTestsSingle,
                    '6' : self.FocusTestsBinary,
                    '10' : self.Tiny1,
                    '11' : self.Tiny2,
                    '12' : self.ResamplePSFAll,
                    '13' : self.ResamplePrimary,
                    '14' : self.ResampleSecondary,
                    '20' : self.MakeConfigFiles,
                    '21' : self.FindBackground,
                    '22' : self.BestSingle,
                    '23' : self.BestBinary,
                    'q'  : self.Exit,
                    '99' : self.AAA }

            Option = raw_input(colored("Selection:  ","green"))
            Run.get(Option,self.PrintError)()

    def AAA(self):
        self.StartTime()

        Focus = PSFTools.FocusTestAAA(Min=-20,Max=21)                   # Create New Focus Object
        Focus.Setup(binary="true")                                      # Run the Binary Focus Tests

        self.EndTime()

    def BestBinary(self):
        self.StartTime()
        Run = PSF.BinaryFit()
        Run.Run()
        self.EndTime()

    def BestSingle(self):
        self.StartTime()
        Run = PSF.SingleFit()
        self.EndTime()

    def EndTime(self):
        self.endtime = time.strftime('%A, %B %d, %Y %X %Z' ,time.localtime())
        print "\nStarted at:\t %s" % (self.starttime)
        print "Finished at:\t %s \n" % (self.endtime)
        GoOn = raw_input("Press Enter To Continue...")

    def Exit(self):
        sys.exit(colored("\nThank You for Using BIFF\n","green"))

    def FindBackground(self):
        self.StartTime()
        Run = PSFTools.ConfigFiles()
        print Run.FindBackground()
        self.EndTime()

    def FocusTestsAll(self):
        self.StartTime()
        Focus = PSFTools.FocusTest(Min=-5,Max=6)                    # Create New Focus Object
        Focus.Setup(single="true",binary="true")                    # Run The Single And Binary Focus Tests
        self.EndTime()

    def FocusTestsBinary(self):
        self.StartTime()
        Focus = PSFTools.FocusTest(Min=-5,Max=6)                    # Create New Focus Object
        Focus.Setup(binary="true")                                  # Run the Binary Focus Tests
        self.EndTime()
    
    def FocusTestsSingle(self):
        self.StartTime()
        Focus = PSFTools.FocusTest(Min=-20,Max=21)                  # Create New Focus Object
        Focus.Setup(single="true")                                  # Run The Single Focus Tests
        self.EndTime()

    def MakeConfigFiles(self):
        self.StartTime()
        Files = PSFTools.ConfigFiles()                              # Create New Configuration Files Object
        Files.Write()                                               # Automatically Generate The Files
        self.EndTime()

    def PrintError(self):
        print "\nSelected input is not an option!"
        GoOn = raw_input("Press Enter To Continue...")

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

    def ReductionAll(self):                                                             # Perform Single and Binary PSF Full Reduction
        self.StartTime()
        #Focus = float(raw_input("Focus Adjustment (0 For None):  "))                    # Get Focus Adjustment
        #print Focus
        print "\nFitAll:  This feature is not done yet"
        self.EndTime()

    def ReductionBinary(self):                                                          # Perform A Binary PSF Full Reduction
        self.StartTime()
        #Focus = float(raw_input("Focus Adjustment (0 For None):  "))                    # Get Focus Adjustment
        #print Focus
        print "\nFitBinary:  This feature is not done yet"
        self.EndTime()

    def ReductionSingle(self):                                                          # Perform A Single PSF Full Reduction
        self.StartTime()
        #Focus = float(raw_input("Focus Adjustment (0 For None):  "))                    # Get Focus Adjustment
        #print Focus
        print "FitSingle:  This feature is not done yet"
        self.EndTime()

    def ResampleAll(self):
        self.StartTime()
        Run = Resample()
        Run.GoGoGo(primary='true',secondary='true')
        self.EndTime()

    def ResamplePrimary(self):
        self.StartTime()
        Run = Resample(self.biffParam)
        Run.WritePSFs(primary='true')
        self.EndTime()

    def ResampleSecondary(self):
        self.StartTime()
        Run = Resample(self.biffParam)
        Run.WritePSFs(secondary='true')
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
