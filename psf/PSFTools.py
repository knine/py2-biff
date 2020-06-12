#!/usr/bin/env python

# Tool To Aid PSF Reduction and Manipulation

import os
import statistics as stats

# Astronomy Modules
import astropy.io.fits as pyfits
from pyraf import iraf

# Custom Modules
import PSF

class ConfigFiles:
	"""Setup and create txt files for PSF fitting"""

        def __init__(self):
		self.SciBox = 'binary_box_sci'                                                                  # Sci Box
                self.ErrBox = 'binary_box_err'                                                                  # Err Box
                self.CoordsFile = 'binary.coords.txt'                                                           # Coordinates To Test
                self.InparamFile = 'binary_inparam.txt'                                                         # Input Parameters
                self.BackgroundLogFile = 'Background.log'                                                       # Background Log File

		print "\n" + "#" * 60 + "\n"                                                                    # Text Output

		self.X = int(raw_input("Enter X Coordinate:\t  "))                                              # X Coordinate
                self.Y = int(raw_input("Enter Y Coordinate:\t  "))                                              # Y Coordinate

                FITSFile = raw_input("Enter Image File:\t  ")                             # Image File
                while not os.path.exists(os.path.abspath(FITSFile)) or not FITSFile:
                        print "ERROR!  No Such Image File! %s \n" % FITSFile,
                        FITSFile = raw_input("Enter Image File:\t  ")
                self.FITSFile = os.path.abspath(FITSFile)

                BackgroundFile = raw_input("Enter Background File:\t  ")          # Background File
                while not os.path.exists(os.path.abspath(BackgroundFile)) or not BackgroundFile:
                        print "ERROR!  No Such File!\n",
                        BackgroundFile = raw_input("Enter Background File:\t  ")
                self.BackgroundFile = os.path.abspath(BackgroundFile)

		print "\n" + "#" * 60                                                                    	# Text Output

        def WriteErrBox(self):
		"""Write the text file for NICMOS [ERR] values"""

                print "Writing %s\t\t\t\t\t" % self.ErrBox,							# Text Output

                if os.path.exists(self.ErrBox):									# If The File Already Exists
                        os.remove(self.ErrBox)									# Remove The File

                XMax, XMin, YMax, YMin = str(self.X + 2), str(self.X - 2),  \
					 str(self.Y + 2), str(self.Y - 2)					# Determine Max And Min Values

                iraf.images()											# Load The IRAF Images Package
                iraf.listpixels(self.FITSFile + "[err][" + XMax + ":" + XMin + "," + YMax + ":" + YMin + "]", 	# IRAF listpixels Command
			        wcs="logical", 
			        Stdout=self.ErrBox)

                print "[OK]"											# Text Output

        def WriteSciBox(self):
		"""Write the text file for NICMOS [SCI] values"""

                print "Writing %s\t\t\t\t\t" % self.SciBox,							# Text Output
                
                if os.path.exists(self.SciBox):									# If The File Already Exists
                        os.remove(self.SciBox)									# Remove The File

                XMax, XMin, YMax, YMin = str(self.X + 2), str(self.X - 2), \
					 str(self.Y + 2), str(self.Y - 2)					# Determine Max And Min Values

                iraf.images()											# Load The IRAF Images Package
                iraf.listpixels(self.FITSFile + "[sci][" + XMax + ":" + XMin + "," + YMax + ":" + YMin + "]", 	# IRAF listpixels Command
				wcs="logical", 
				Stdout=self.SciBox)

                print "[OK]"											# Text Output

        def WriteCoordinates(self):
		"""Write the text file for coordinates to test"""

                print "Writing binary.coords.txt\t\t\t\t",							# Text Output

                BinaryCoordsFile = open(self.CoordsFile, 'w')							# Open The File To Write

                BinaryCoordsFile.write("29\n")									# Start Writing The File
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X - 1, self.Y - 1, self.X - 1, self.Y - 1))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X - 1, self.Y - 1, self.X - 1, self.Y))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X - 1, self.Y - 1, self.X, self.Y - 1))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X - 1, self.Y - 1, self.X, self.Y))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X - 1, self.Y, self.X - 1, self.Y))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X - 1, self.Y, self.X - 1, self.Y + 1))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X - 1, self.Y, self.X, self.Y - 1))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X - 1, self.Y, self.X, self.Y))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X - 1, self.Y, self.X, self.Y + 1))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X - 1, self.Y + 1, self.X - 1, self.Y + 1))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X - 1, self.Y + 1, self.X, self.Y))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X - 1, self.Y + 1, self.X, self.Y + 1))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X, self.Y - 1, self.X, self.Y - 1))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X, self.Y - 1, self.X, self.Y))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X, self.Y - 1, self.X + 1, self.Y - 1))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X, self.Y - 1, self.X + 1, self.Y))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X, self.Y, self.X, self.Y))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X, self.Y, self.X, self.Y + 1))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X, self.Y, self.X + 1, self.Y - 1))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X, self.Y, self.X + 1, self.Y))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X, self.Y, self.X + 1, self.Y + 1))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X, self.Y + 1, self.X, self.Y + 1))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X, self.Y + 1, self.X + 1, self.Y))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X, self.Y + 1, self.X + 1, self.Y + 1))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X + 1, self.Y - 1, self.X + 1, self.Y - 1))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X + 1, self.Y - 1, self.X + 1, self.Y))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X + 1, self.Y, self.X + 1, self.Y))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X + 1, self.Y, self.X + 1, self.Y + 1))
                BinaryCoordsFile.write("%i\t%i\t%i\t%i\n" % (self.X + 1, self.Y + 1, self.X + 1, self.Y + 1))

		BinaryCoordsFile.close()									# Close The File

                print "[OK]"											# Text Output

        def WriteInparam(self):
		"""Write the text file for input parameters"""

                print "Writing binary_inparam.txt\t\t\t\t",							# Text Output

                hdulist = pyfits.open(self.FITSFile)								# Open The FITS file
                (Median,Sigma) = self.FindBackground()

                BinaryInparamFile = open(self.InparamFile,'w')							# Open The File To Write

                BinaryInparamFile.write("%i %i %i %i\n" % (self.X - 2, self.X + 2, self.Y - 2, self.Y + 2))	# Box Coordinates
                BinaryInparamFile.write(self.SciBox + "\n")							# Sci Box
                BinaryInparamFile.write("%f\n" % Median)							# Median
                BinaryInparamFile.write("%f\n" % Sigma)								# Sigma
                BinaryInparamFile.write("%s\n" % hdulist[0].header['ORIENTAT'])					# Orientation
                BinaryInparamFile.write(self.CoordsFile + "\n")							# Coordinates To Test

                hdulist.close()											# Close The FITS File

                print "[OK]"											# Text Output

        def FindBackground(self):
		"""Returns the median and sigma of pixel values with anything that is greater or less than 3-sigma removed.  Writes the details to a log file"""

                InputList = open(self.BackgroundFile, 'r').readlines()						# Open The File With Pixel Values
                BackgroundLog = open(self.BackgroundLogFile, 'w')						# Open The Log File

                BackgroundList=[]										# Array To Hold Pixel Values

                for InputLine in InputList:									# Read The Third Number In Each Line Into An Array
                        EachLine = InputLine.split()
                        BackgroundList.append(float(EachLine[2]))

                BackgroundLog.write("Original Number of Values:  %i\n" % len(BackgroundList))			# Print Original Number Of Values To Log File
                BackgroundLog.write("Original Mean:  %f\n" % stats.mean(BackgroundList))			# Print Original Mean To Log File
                BackgroundLog.write("Original Median:  %f\n" % stats.lmedian(BackgroundList))			# Print Original Median To Log File
                BackgroundLog.write("Original Sigma:  %f\n\n" % stats.lstdev(BackgroundList))			# Print Original Sigma To Log File

                while 1:
                        removed = 0										# Number Of Removed This Loop Set To Zero
                        mean = stats.mean(BackgroundList)                       				# Calculate The New Mean
                        sigma = stats.lstdev(BackgroundList)                    				# Calculate The New Sigma

                        for i in range( len(BackgroundList)-1, -1, -1 ):					# Loop Backwards Through The List, Check For Outliers Or Zeros
                                if BackgroundList[i] > mean + (3 * sigma) or BackgroundList[i] < mean - (3 * sigma) or BackgroundList[i] == 0.0:
                                        BackgroundLog.write("Removing %f\n" % BackgroundList[i])		# Print Point To Be Removed To Log File
                                        removed = removed + 1							# Increment The Number Removed
                                        del BackgroundList[i]							# Remove The Point From The List

                        if removed == 0:									# If No Points Were Removed
                                break										# Break Out Of The While Loop

                Median = stats.lmedian(BackgroundList)								# Calculate Final Median
                Sigma = stats.lstdev(BackgroundList)								# Calculate Final Sigma

                BackgroundLog.write("\nFinal Number of Values:  %i\n" % len(BackgroundList))			# Print Final Number Of Values To Log File
                BackgroundLog.write("Final Mean:  %f\n" % stats.mean(BackgroundList))				# Print Final Mean To Log File
                BackgroundLog.write("Final Median:  %f\n" % Median)						# Print Final Mean To Log File
                BackgroundLog.write("Final Sigma:  %f" % Sigma)							# Print Final Sigma To Log File

                BackgroundLog.close()										# Close The Log File

                return (Median,Sigma)										# Return Median and Sigma

        def Write(self):
		"""Creates all configuration files"""

                print "\n" + "#" * 60 + "\n"									# Text Output
                self.WriteInparam()										# Write Inparameter File
                self.WriteSciBox()										# Write Sci Box File
                self.WriteErrBox()										# Write Err Box File
                self.WriteCoordinates()										# Write Coordinates To Text File
                print "\n" + "#" * 60										# Text Output

class FocusTest (PSF.Tiny):
	"""Automated setup and run of NIC1 focus tests"""

        def __init__(self, Min, Max):
		self.MinFocus = Min										# Minimum Focus To Try
		self.MaxFocus = Max										# Maximum Focus To Try
		self.WorkingDirectory = os.getcwd()								# Get The Current Working Directory
		PSF.Tiny.__init__(self)										# Get Object Parameters from PSF.Tiny

        def Setup(self, **kwargs):
		"""
			- Create TinyTim parameter file with tiny1
			- Setup Directories of focus tests
			- Writes new parameter files for each directory
			- Creates the resampled model PSFs in each directory
			- Runs single PSF fit in each directory
		"""
	
		self.Tiny1()											# Run tiny1 To Create The Tiny Tim Parameter File

                Files = ConfigFiles()										# Object To Write Configuration Files
                Resample = PSF.Resample()									# Object To Resample PSFs
	
		FocusLog = open("FocusLog.txt",'w')

                for i in range(self.MinFocus,self.MaxFocus):							# Loop Through Range Of Values
                        NewDirectory = 'test' + str(i)								# New Directory To Be Created
                        PSFFile = open(self.ParameterFile,'r').readlines()                              	# Open The Tiny Tim Parameter File
                        linecount = 0                                                                   	# Line Counter For List

                        for line in PSFFile:									# Loop Through Tiny Tim Parameter File Lines
                                if (line.find('# Z4 : Focus') != -1):                                   	# Line We Are Looking For
                                        focus = line.split()[0]                                         	# Get Default Focus
                                        newfocus = float(focus) + 0.01100 * i                           	# Calculate New Test Focus
                                        if i < 0:
                                                newline = '%0.5f # Z4 : Focus\n' % (newfocus)           	# Negative
                                        else:
                                                newline = '%0.6f # Z4 : Focus\n' % (newfocus)           	# Positive
                                        PSFFile[linecount] = newline                                    	# Set New Focus

                                linecount = linecount + 1							# Increment The Line Count

                        os.mkdir(NewDirectory)									# Create The New Directory
                        os.chdir(NewDirectory)									# Move To The New Directory

                        NewPSFFile = open(self.ParameterFile,'w')						# Open A New Tiny Tim Parameter File For Writing
                        for printline in PSFFile:								# Loop Though The List
                                NewPSFFile.write(printline)							# Write The File
                        NewPSFFile.close()									# Close The File

                        self.Tiny2()										# Run tiny2 On New Parameter File, Create Model PSF
                        Files.Write()										# Write The Binary Configuration Files
                        Resample.GoGoGo(primary='true',secondary='true')					# Resample Model PSF

			if "single" in kwargs:
                        	Fit = PSF.SingleFit()								# Run A Single PSF Solution
				FocusLog.write("%i\t%1.10f\t%s\t%1.9f\n" % (i,Fit.MinChi,Fit.BestModel[5:7],Fit.Flux))
				FocusLog.flush()

			if "binary" in kwargs:
				BinaryFit = PSF.BinaryFit()								
				BinaryFit.Run()									# Run A Binary PSF Solution
			
                        os.chdir(self.WorkingDirectory)								# Move Back To The Working Directory

		FocusLog.close()


class FocusTestAAA (PSF.Tiny):
        """Automated setup and run of NIC1 focus tests"""

        def __init__(self, Min, Max):
                self.MinFocus = Min                                                                             # Minimum Focus To Try
                self.MaxFocus = Max                                                                             # Maximum Focus To Try
                self.WorkingDirectory = os.getcwd()                                                             # Get The Current Working Directory
                PSF.Tiny.__init__(self)                                                                         # Get Object Parameters from PSF.Tiny

        def Setup(self, **kwargs):
                Resample = PSF.Resample()                                                                       # Object To Resample PSFs

                for i in range(self.MinFocus,self.MaxFocus):                                                    # Loop Through Range Of Values
                        NewDirectory = 'test' + str(i)                                                          # New Directory To Be Created
                        PSFFile = open(self.ParameterFile,'r').readlines()                                      # Open The Tiny Tim Parameter File
                        linecount = 0                                                                           # Line Counter For List

                        for line in PSFFile:                                                                    # Loop Through Tiny Tim Parameter File Lines
                                if (line.find('# Z4 : Focus') != -1):                                           # Line We Are Looking For
                                        focus = line.split()[0]                                                 # Get Default Focus
                                        newfocus = float(focus) + 0.01100 * i                                   # Calculate New Test Focus
                                        if i < 0:
                                                newline = '%0.5f # Z4 : Focus\n' % (newfocus)                   # Negative
                                        else:
                                                newline = '%0.6f # Z4 : Focus\n' % (newfocus)                   # Positive
                                        PSFFile[linecount] = newline                                            # Set New Focus

                                linecount = linecount + 1                                                       # Increment The Line Count

                        os.chdir(NewDirectory)                                                                  # Move To The New Directory

                        NewPSFFile = open(self.ParameterFile,'w')                                               # Open A New Tiny Tim Parameter File For Writing
                        for printline in PSFFile:                                                               # Loop Though The List
                                NewPSFFile.write(printline)                                                     # Write The File
                        NewPSFFile.close()                                                                      # Close The File

                        self.Tiny2()                                                                            # Run tiny2 On New Parameter File, Create Model PSF
                        Resample.GoGoGo(primary='true',secondary='true')                                        # Resample Model PSF

                        if "binary" in kwargs:
                                BinaryFit = PSF.BinaryFit()
                                BinaryFit.Run()                                                                 # Run A Binary PSF Solution
				os.system('/usr/local/bin/SortF113n')

                        os.chdir(self.WorkingDirectory)                                                         # Move Back To The Working Directory

