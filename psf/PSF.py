#!/usr/bin/env python

# PSF Reduction and Manipulation Functions

import os
import sys
import time
import yaml
import pexpect
import numpy
import math
from pyraf import iraf

#class Resample:
#    def __init__(self):
#        self.nbin = 10               # Subsample value using in tinytim
#        self.col = 68                # Size of the cols in PSF for NIC1
#        self.row = 68                # Size of the rows in PSF for NIC1
#
#    def GoGoGo(self, **kwargs):
#
#        print "\n" + "#" * 60 + "\n"
#
#        iraf.images()
#        iraf.dataio()
#        iraf.dataio.setParam("wtextimage.header","no")
#        iraf.dataio.setParam("wtextimage.format","15.8g")
#        iraf.dataio.setParam("wtextimage.maxlinelen","20")
#        InputList = self.GetPSFList()
#	LogFile = open('ResamplePSF.log','w')
#
#        for InputLine in InputList:
#
#	    print "Creating Cylon Model:\t\t\t\t\t[" + InputLine['PrimaryOut'][5:7] + "]\r",
#	    sys.stdout.flush()								# Flush the stdout buffer
#
#            WTextIn = os.getcwd() + "/" + str(InputLine['WTextIn'])
#            WTextOut = os.getcwd() + "/" + str(InputLine['WTextOut'])
#            iraf.wtextimage(WTextIn, WTextOut)
#
#	    LogFile.write("%s ---> %s / %s" % (InputLine['WTextOut'],InputLine['PrimaryOut'],InputLine['SecondaryOut']))
#	    LogFile.flush()
#
#            InputPSF = numpy.zeros((self.col*self.nbin,self.row*self.nbin))         # Array for input PSF
#            PSFValue = open(InputLine['WTextOut'], 'r')                             # Open the infile with the PSF
#
#            # Loop through the number of columns and rows for the InputPSF and put those values in a matrix array
#            for j in range(1,InputLine['nrow']+1):                                  # Loop through each row (Y)
#                for i in range(1,InputLine['ncol']+1):                              # Loop through each column (X)
#                    InputPSF[i,j] = float(PSFValue.readline())                      # Read the next line in the file and assign it to an array element
#
#            InputSum = numpy.add.reduce(numpy.add.reduce(InputPSF))                 # Total of all InputPSF values
#
#            xdim = InputLine['ncol'] // self.nbin                                   # X and Y dimentions of output PSF
#            ydim = InputLine['nrow'] // self.nbin                                   # Use Floor Division so this will work in Python 3+
#
#            OutputPSF = numpy.zeros((self.col,self.row))                                    # Array for output PSF
#
#	    # Loop through the number of columns and rows for the OutputPSF
#            for j in range(1, ydim + 1):
#                for i in range(1, xdim + 1):
#
#                    nxcount = self.nbin*i                                   # Low x value of array slice
#                    nxlow = nxcount-(self.nbin-1)                           # High x value of array slice
#                    nycount = self.nbin*j                                   # Low y value of array slice
#                    nylow = nycount-(self.nbin-1)                           # High y value of array slice
#
#                    # Slice off a 10 x 10 part of the InputPSF and make it one pixel of the OutputPSF
#                    OutputPSF[i,j] = numpy.add.reduce(numpy.add.reduce(InputPSF[nxlow:nxcount+1,nylow:nycount+1]))
#
#            OutputSum = numpy.add.reduce(numpy.add.reduce(OutputPSF))               # Total of all OutputPSF values
#
#	    if "primary" in kwargs:
#	        PrimaryOutputFile = open(InputLine['PrimaryOut'], 'w')                                     # Open the output file for writing
#
#	        for j in range(1, ydim + 1):							# Loop through the columns and rows for the OutputPSF
#        	    for i in range(1, xdim + 1):
#                        PrimaryOutputFile.write(str(OutputPSF[i,j]) + '\n')		# write each value to the output file
#
#		PrimaryOutputFile.close()
#		LogFile.write("%s ---> %s (%f, %f)\n" % (InputLine['WTextOut'],InputLine['PrimaryOut'],InputSum, OutputSum))
#
#	    if "secondary" in kwargs:
#	        SecondaryOutputFile = open(InputLine['SecondaryOut'], 'w')
#
#                for j in range(1, ydim + 1):							 # Loop through the columns and rows for the OutputPSF
#                    for i in range(1, xdim + 1):
#                        SecondaryOutputFile.write(str(OutputPSF[i,j]) + '\n')		# write each value to the output file
#                        
#                SecondaryOutputFile.close()
#                LogFile.write("%s ---> %s (%f, %f)\n" % (InputLine['WTextOut'],InputLine['SecondaryOut'],InputSum, OutputSum))
#                                
#	    LogFile.flush()
#	    os.remove(WTextOut)								# Save Space And Remove The FITS File
#
#            LogFile.write(" (%f, %f)\n" % (InputSum, OutputSum))                             # Print some status information to the screen
#
#	LogFile.close()
#	print "Creating Cylon Model:\t\t\t\t\t[OK]\n"
#	print "#" * 60 	
#
#    def GetPSFList(self):
#
#        # This Works for NIC1 Filters:  F090M, F108N, F110M, F110W, F113N, F145M, F165M, F170M
#        PSFList = [     {'WTextIn' : 'object00.fits[2:680,2:680]', 'WTextOut' : 'object.001', 'PrimaryOut' : 'prim.00.psf', 'SecondaryOut' : 'sec.00.psf', 'ncol' : 679, 'nrow' : 679},
#                        {'WTextIn' : 'object00.fits[2:680,3:680]', 'WTextOut' : 'object.002', 'PrimaryOut' : 'prim.01.psf', 'SecondaryOut' : 'sec.01.psf', 'ncol' : 679, 'nrow' : 678},
#                        {'WTextIn' : 'object00.fits[2:680,4:680]', 'WTextOut' : 'object.003', 'PrimaryOut' : 'prim.02.psf', 'SecondaryOut' : 'sec.02.psf', 'ncol' : 679, 'nrow' : 677},
#                        {'WTextIn' : 'object00.fits[2:680,5:680]', 'WTextOut' : 'object.004', 'PrimaryOut' : 'prim.03.psf', 'SecondaryOut' : 'sec.03.psf', 'ncol' : 679, 'nrow' : 676},
#                        {'WTextIn' : 'object00.fits[2:680,6:680]', 'WTextOut' : 'object.005', 'PrimaryOut' : 'prim.04.psf', 'SecondaryOut' : 'sec.04.psf', 'ncol' : 679, 'nrow' : 675},
#                        {'WTextIn' : 'object00.fits[2:680,7:680]', 'WTextOut' : 'object.006', 'PrimaryOut' : 'prim.05.psf', 'SecondaryOut' : 'sec.05.psf', 'ncol' : 679, 'nrow' : 674},
#                        {'WTextIn' : 'object00.fits[2:680,8:680]', 'WTextOut' : 'object.007', 'PrimaryOut' : 'prim.06.psf', 'SecondaryOut' : 'sec.06.psf', 'ncol' : 679, 'nrow' : 673},
#                        {'WTextIn' : 'object00.fits[2:680,9:680]', 'WTextOut' : 'object.008', 'PrimaryOut' : 'prim.07.psf', 'SecondaryOut' : 'sec.07.psf', 'ncol' : 679, 'nrow' : 672},
#                        {'WTextIn' : 'object00.fits[2:680,10:680]', 'WTextOut' : 'object.009', 'PrimaryOut' : 'prim.08.psf', 'SecondaryOut' : 'sec.08.psf', 'ncol' : 679, 'nrow' : 671}, 
#                        {'WTextIn' : 'object00.fits[2:680,11:680]', 'WTextOut' : 'object.010', 'PrimaryOut' : 'prim.09.psf', 'SecondaryOut' : 'sec.09.psf', 'ncol' : 679, 'nrow' : 670},
#                        {'WTextIn' : 'object00.fits[3:680,2:680]', 'WTextOut' : 'object.011', 'PrimaryOut' : 'prim.10.psf', 'SecondaryOut' : 'sec.10.psf', 'ncol' : 678, 'nrow' : 679},
#                        {'WTextIn' : 'object00.fits[3:680,3:680]', 'WTextOut' : 'object.012', 'PrimaryOut' : 'prim.11.psf', 'SecondaryOut' : 'sec.11.psf', 'ncol' : 678, 'nrow' : 678},
#                        {'WTextIn' : 'object00.fits[3:680,4:680]', 'WTextOut' : 'object.013', 'PrimaryOut' : 'prim.12.psf', 'SecondaryOut' : 'sec.12.psf', 'ncol' : 678, 'nrow' : 677},
#                        {'WTextIn' : 'object00.fits[3:680,5:680]', 'WTextOut' : 'object.014', 'PrimaryOut' : 'prim.13.psf', 'SecondaryOut' : 'sec.13.psf', 'ncol' : 678, 'nrow' : 676},
#                        {'WTextIn' : 'object00.fits[3:680,6:680]', 'WTextOut' : 'object.015', 'PrimaryOut' : 'prim.14.psf', 'SecondaryOut' : 'sec.14.psf', 'ncol' : 678, 'nrow' : 675},
#                        {'WTextIn' : 'object00.fits[3:680,7:680]', 'WTextOut' : 'object.016', 'PrimaryOut' : 'prim.15.psf', 'SecondaryOut' : 'sec.15.psf', 'ncol' : 678, 'nrow' : 674},
#                        {'WTextIn' : 'object00.fits[3:680,8:680]', 'WTextOut' : 'object.017', 'PrimaryOut' : 'prim.16.psf', 'SecondaryOut' : 'sec.16.psf', 'ncol' : 678, 'nrow' : 673},
#                        {'WTextIn' : 'object00.fits[3:680,9:680]', 'WTextOut' : 'object.018', 'PrimaryOut' : 'prim.17.psf', 'SecondaryOut' : 'sec.17.psf', 'ncol' : 678, 'nrow' : 672},
#                        {'WTextIn' : 'object00.fits[3:680,10:680]', 'WTextOut' : 'object.019', 'PrimaryOut' : 'prim.18.psf', 'SecondaryOut' : 'sec.18.psf', 'ncol' : 678, 'nrow' : 671},
#                        {'WTextIn' : 'object00.fits[3:680,11:680]', 'WTextOut' : 'object.020', 'PrimaryOut' : 'prim.19.psf', 'SecondaryOut' : 'sec.19.psf', 'ncol' : 678, 'nrow' : 670},
#                        {'WTextIn' : 'object00.fits[4:680,2:680]', 'WTextOut' : 'object.021', 'PrimaryOut' : 'prim.20.psf', 'SecondaryOut' : 'sec.20.psf', 'ncol' : 677, 'nrow' : 679},
#                        {'WTextIn' : 'object00.fits[4:680,3:680]', 'WTextOut' : 'object.022', 'PrimaryOut' : 'prim.21.psf', 'SecondaryOut' : 'sec.21.psf', 'ncol' : 677, 'nrow' : 678},
#                        {'WTextIn' : 'object00.fits[4:680,4:680]', 'WTextOut' : 'object.023', 'PrimaryOut' : 'prim.22.psf', 'SecondaryOut' : 'sec.22.psf', 'ncol' : 677, 'nrow' : 677},
#                        {'WTextIn' : 'object00.fits[4:680,5:680]', 'WTextOut' : 'object.024', 'PrimaryOut' : 'prim.23.psf', 'SecondaryOut' : 'sec.23.psf', 'ncol' : 677, 'nrow' : 676},
#                        {'WTextIn' : 'object00.fits[4:680,6:680]', 'WTextOut' : 'object.025', 'PrimaryOut' : 'prim.24.psf', 'SecondaryOut' : 'sec.24.psf', 'ncol' : 677, 'nrow' : 675},
#                        {'WTextIn' : 'object00.fits[4:680,7:680]', 'WTextOut' : 'object.026', 'PrimaryOut' : 'prim.25.psf', 'SecondaryOut' : 'sec.25.psf', 'ncol' : 677, 'nrow' : 674},
#                        {'WTextIn' : 'object00.fits[4:680,8:680]', 'WTextOut' : 'object.027', 'PrimaryOut' : 'prim.26.psf', 'SecondaryOut' : 'sec.26.psf', 'ncol' : 677, 'nrow' : 673},
#                        {'WTextIn' : 'object00.fits[4:680,9:680]', 'WTextOut' : 'object.028', 'PrimaryOut' : 'prim.27.psf', 'SecondaryOut' : 'sec.27.psf', 'ncol' : 677, 'nrow' : 672},
#                        {'WTextIn' : 'object00.fits[4:680,10:680]', 'WTextOut' : 'object.029', 'PrimaryOut' : 'prim.28.psf', 'SecondaryOut' : 'sec.28.psf', 'ncol' : 677, 'nrow' : 671},
#                        {'WTextIn' : 'object00.fits[4:680,11:680]', 'WTextOut' : 'object.030', 'PrimaryOut' : 'prim.29.psf', 'SecondaryOut' : 'sec.29.psf', 'ncol' : 677, 'nrow' : 670},
#                        {'WTextIn' : 'object00.fits[5:680,2:680]', 'WTextOut' : 'object.031', 'PrimaryOut' : 'prim.30.psf', 'SecondaryOut' : 'sec.30.psf', 'ncol' : 676, 'nrow' : 679},
#                        {'WTextIn' : 'object00.fits[5:680,3:680]', 'WTextOut' : 'object.032', 'PrimaryOut' : 'prim.31.psf', 'SecondaryOut' : 'sec.31.psf', 'ncol' : 676, 'nrow' : 678},
#                        {'WTextIn' : 'object00.fits[5:680,4:680]', 'WTextOut' : 'object.033', 'PrimaryOut' : 'prim.32.psf', 'SecondaryOut' : 'sec.32.psf', 'ncol' : 676, 'nrow' : 677},
#                        {'WTextIn' : 'object00.fits[5:680,5:680]', 'WTextOut' : 'object.034', 'PrimaryOut' : 'prim.33.psf', 'SecondaryOut' : 'sec.33.psf', 'ncol' : 676, 'nrow' : 676},
#                        {'WTextIn' : 'object00.fits[5:680,6:680]', 'WTextOut' : 'object.035', 'PrimaryOut' : 'prim.34.psf', 'SecondaryOut' : 'sec.34.psf', 'ncol' : 676, 'nrow' : 675},
#                        {'WTextIn' : 'object00.fits[5:680,7:680]', 'WTextOut' : 'object.036', 'PrimaryOut' : 'prim.35.psf', 'SecondaryOut' : 'sec.35.psf', 'ncol' : 676, 'nrow' : 674},
#                        {'WTextIn' : 'object00.fits[5:680,8:680]', 'WTextOut' : 'object.037', 'PrimaryOut' : 'prim.36.psf', 'SecondaryOut' : 'sec.36.psf', 'ncol' : 676, 'nrow' : 673},
#                        {'WTextIn' : 'object00.fits[5:680,9:680]', 'WTextOut' : 'object.038', 'PrimaryOut' : 'prim.37.psf', 'SecondaryOut' : 'sec.37.psf', 'ncol' : 676, 'nrow' : 672},
#                        {'WTextIn' : 'object00.fits[5:680,10:680]', 'WTextOut' : 'object.039', 'PrimaryOut' : 'prim.38.psf', 'SecondaryOut' : 'sec.38.psf', 'ncol' : 676, 'nrow' : 671},
#                        {'WTextIn' : 'object00.fits[5:680,11:680]', 'WTextOut' : 'object.040', 'PrimaryOut' : 'prim.39.psf', 'SecondaryOut' : 'sec.39.psf', 'ncol' : 676, 'nrow' : 670},
#                        {'WTextIn' : 'object00.fits[6:680,2:680]', 'WTextOut' : 'object.041', 'PrimaryOut' : 'prim.40.psf', 'SecondaryOut' : 'sec.40.psf', 'ncol' : 675, 'nrow' : 679},
#                        {'WTextIn' : 'object00.fits[6:680,3:680]', 'WTextOut' : 'object.042', 'PrimaryOut' : 'prim.41.psf', 'SecondaryOut' : 'sec.41.psf', 'ncol' : 675, 'nrow' : 678},
#                        {'WTextIn' : 'object00.fits[6:680,4:680]', 'WTextOut' : 'object.043', 'PrimaryOut' : 'prim.42.psf', 'SecondaryOut' : 'sec.42.psf', 'ncol' : 675, 'nrow' : 677},
#                        {'WTextIn' : 'object00.fits[6:680,5:680]', 'WTextOut' : 'object.044', 'PrimaryOut' : 'prim.43.psf', 'SecondaryOut' : 'sec.43.psf', 'ncol' : 675, 'nrow' : 676},
#                        {'WTextIn' : 'object00.fits[6:680,6:680]', 'WTextOut' : 'object.045', 'PrimaryOut' : 'prim.44.psf', 'SecondaryOut' : 'sec.44.psf', 'ncol' : 675, 'nrow' : 675},
#                        {'WTextIn' : 'object00.fits[6:680,7:680]', 'WTextOut' : 'object.046', 'PrimaryOut' : 'prim.45.psf', 'SecondaryOut' : 'sec.45.psf', 'ncol' : 675, 'nrow' : 674},
#                        {'WTextIn' : 'object00.fits[6:680,8:680]', 'WTextOut' : 'object.047', 'PrimaryOut' : 'prim.46.psf', 'SecondaryOut' : 'sec.46.psf', 'ncol' : 675, 'nrow' : 673},
#                        {'WTextIn' : 'object00.fits[6:680,9:680]', 'WTextOut' : 'object.048', 'PrimaryOut' : 'prim.47.psf', 'SecondaryOut' : 'sec.47.psf', 'ncol' : 675, 'nrow' : 672},
#                        {'WTextIn' : 'object00.fits[6:680,10:680]', 'WTextOut' : 'object.049', 'PrimaryOut' : 'prim.48.psf', 'SecondaryOut' : 'sec.48.psf', 'ncol' : 675, 'nrow' : 671},
#                        {'WTextIn' : 'object00.fits[6:680,11:680]', 'WTextOut' : 'object.050', 'PrimaryOut' : 'prim.49.psf', 'SecondaryOut' : 'sec.49.psf', 'ncol' : 675, 'nrow' : 670},
#                        {'WTextIn' : 'object00.fits[7:680,2:680]', 'WTextOut' : 'object.051', 'PrimaryOut' : 'prim.50.psf', 'SecondaryOut' : 'sec.50.psf', 'ncol' : 674, 'nrow' : 679},
#                        {'WTextIn' : 'object00.fits[7:680,3:680]', 'WTextOut' : 'object.052', 'PrimaryOut' : 'prim.51.psf', 'SecondaryOut' : 'sec.51.psf', 'ncol' : 674, 'nrow' : 678},
#                        {'WTextIn' : 'object00.fits[7:680,4:680]', 'WTextOut' : 'object.053', 'PrimaryOut' : 'prim.52.psf', 'SecondaryOut' : 'sec.52.psf', 'ncol' : 674, 'nrow' : 677},
#                        {'WTextIn' : 'object00.fits[7:680,5:680]', 'WTextOut' : 'object.054', 'PrimaryOut' : 'prim.53.psf', 'SecondaryOut' : 'sec.53.psf', 'ncol' : 674, 'nrow' : 676},
#                        {'WTextIn' : 'object00.fits[7:680,6:680]', 'WTextOut' : 'object.055', 'PrimaryOut' : 'prim.54.psf', 'SecondaryOut' : 'sec.54.psf', 'ncol' : 674, 'nrow' : 675},
#                        {'WTextIn' : 'object00.fits[7:680,7:680]', 'WTextOut' : 'object.056', 'PrimaryOut' : 'prim.55.psf', 'SecondaryOut' : 'sec.55.psf', 'ncol' : 674, 'nrow' : 674},
#                        {'WTextIn' : 'object00.fits[7:680,8:680]', 'WTextOut' : 'object.057', 'PrimaryOut' : 'prim.56.psf', 'SecondaryOut' : 'sec.56.psf', 'ncol' : 674, 'nrow' : 673},
#                        {'WTextIn' : 'object00.fits[7:680,9:680]', 'WTextOut' : 'object.058', 'PrimaryOut' : 'prim.57.psf', 'SecondaryOut' : 'sec.57.psf', 'ncol' : 674, 'nrow' : 672},
#                        {'WTextIn' : 'object00.fits[7:680,10:680]', 'WTextOut' : 'object.059', 'PrimaryOut' : 'prim.58.psf', 'SecondaryOut' : 'sec.58.psf', 'ncol' : 674, 'nrow' : 671},
#                        {'WTextIn' : 'object00.fits[7:680,11:680]', 'WTextOut' : 'object.060', 'PrimaryOut' : 'prim.59.psf', 'SecondaryOut' : 'sec.59.psf', 'ncol' : 674, 'nrow' : 670},
#                        {'WTextIn' : 'object00.fits[8:680,2:680]', 'WTextOut' : 'object.061', 'PrimaryOut' : 'prim.60.psf', 'SecondaryOut' : 'sec.60.psf', 'ncol' : 673, 'nrow' : 679},
#                        {'WTextIn' : 'object00.fits[8:680,3:680]', 'WTextOut' : 'object.062', 'PrimaryOut' : 'prim.61.psf', 'SecondaryOut' : 'sec.61.psf', 'ncol' : 673, 'nrow' : 678},
#                        {'WTextIn' : 'object00.fits[8:680,4:680]', 'WTextOut' : 'object.063', 'PrimaryOut' : 'prim.62.psf', 'SecondaryOut' : 'sec.62.psf', 'ncol' : 673, 'nrow' : 677},
#                        {'WTextIn' : 'object00.fits[8:680,5:680]', 'WTextOut' : 'object.064', 'PrimaryOut' : 'prim.63.psf', 'SecondaryOut' : 'sec.63.psf', 'ncol' : 673, 'nrow' : 676},
#                        {'WTextIn' : 'object00.fits[8:680,6:680]', 'WTextOut' : 'object.065', 'PrimaryOut' : 'prim.64.psf', 'SecondaryOut' : 'sec.64.psf', 'ncol' : 673, 'nrow' : 675},
#                        {'WTextIn' : 'object00.fits[8:680,7:680]', 'WTextOut' : 'object.066', 'PrimaryOut' : 'prim.65.psf', 'SecondaryOut' : 'sec.65.psf', 'ncol' : 673, 'nrow' : 674},
#                        {'WTextIn' : 'object00.fits[8:680,8:680]', 'WTextOut' : 'object.067', 'PrimaryOut' : 'prim.66.psf', 'SecondaryOut' : 'sec.66.psf', 'ncol' : 673, 'nrow' : 673},
#                        {'WTextIn' : 'object00.fits[8:680,9:680]', 'WTextOut' : 'object.068', 'PrimaryOut' : 'prim.67.psf', 'SecondaryOut' : 'sec.67.psf', 'ncol' : 673, 'nrow' : 672},
#                        {'WTextIn' : 'object00.fits[8:680,10:680]', 'WTextOut' : 'object.069', 'PrimaryOut' : 'prim.68.psf', 'SecondaryOut' : 'sec.68.psf', 'ncol' : 673, 'nrow' : 671},
#                        {'WTextIn' : 'object00.fits[8:680,11:680]', 'WTextOut' : 'object.070', 'PrimaryOut' : 'prim.69.psf', 'SecondaryOut' : 'sec.69.psf', 'ncol' : 673, 'nrow' : 670},
#                        {'WTextIn' : 'object00.fits[9:680,2:680]', 'WTextOut' : 'object.071', 'PrimaryOut' : 'prim.70.psf', 'SecondaryOut' : 'sec.70.psf', 'ncol' : 672, 'nrow' : 679},
#                        {'WTextIn' : 'object00.fits[9:680,3:680]', 'WTextOut' : 'object.072', 'PrimaryOut' : 'prim.71.psf', 'SecondaryOut' : 'sec.71.psf', 'ncol' : 672, 'nrow' : 678},
#                        {'WTextIn' : 'object00.fits[9:680,4:680]', 'WTextOut' : 'object.073', 'PrimaryOut' : 'prim.72.psf', 'SecondaryOut' : 'sec.72.psf', 'ncol' : 672, 'nrow' : 677},
#                        {'WTextIn' : 'object00.fits[9:680,5:680]', 'WTextOut' : 'object.074', 'PrimaryOut' : 'prim.73.psf', 'SecondaryOut' : 'sec.73.psf', 'ncol' : 672, 'nrow' : 676},
#                        {'WTextIn' : 'object00.fits[9:680,6:680]', 'WTextOut' : 'object.075', 'PrimaryOut' : 'prim.74.psf', 'SecondaryOut' : 'sec.74.psf', 'ncol' : 672, 'nrow' : 675},
#                        {'WTextIn' : 'object00.fits[9:680,7:680]', 'WTextOut' : 'object.076', 'PrimaryOut' : 'prim.75.psf', 'SecondaryOut' : 'sec.75.psf', 'ncol' : 672, 'nrow' : 674},
#                        {'WTextIn' : 'object00.fits[9:680,8:680]', 'WTextOut' : 'object.077', 'PrimaryOut' : 'prim.76.psf', 'SecondaryOut' : 'sec.76.psf', 'ncol' : 672, 'nrow' : 673},
#                        {'WTextIn' : 'object00.fits[9:680,9:680]', 'WTextOut' : 'object.078', 'PrimaryOut' : 'prim.77.psf', 'SecondaryOut' : 'sec.77.psf', 'ncol' : 672, 'nrow' : 672},
#                        {'WTextIn' : 'object00.fits[9:680,10:680]', 'WTextOut' : 'object.079', 'PrimaryOut' : 'prim.78.psf', 'SecondaryOut' : 'sec.78.psf', 'ncol' : 672, 'nrow' : 671}, 
#                        {'WTextIn' : 'object00.fits[9:680,11:680]', 'WTextOut' : 'object.080', 'PrimaryOut' : 'prim.79.psf', 'SecondaryOut' : 'sec.79.psf', 'ncol' : 672, 'nrow' : 670},
#                        {'WTextIn' : 'object00.fits[10:680,2:680]', 'WTextOut' : 'object.081', 'PrimaryOut' : 'prim.80.psf', 'SecondaryOut' : 'sec.80.psf', 'ncol' : 671, 'nrow' : 679},
#                        {'WTextIn' : 'object00.fits[10:680,3:680]', 'WTextOut' : 'object.082', 'PrimaryOut' : 'prim.81.psf', 'SecondaryOut' : 'sec.81.psf', 'ncol' : 671, 'nrow' : 678},
#                        {'WTextIn' : 'object00.fits[10:680,4:680]', 'WTextOut' : 'object.083', 'PrimaryOut' : 'prim.82.psf', 'SecondaryOut' : 'sec.82.psf', 'ncol' : 671, 'nrow' : 677},
#                        {'WTextIn' : 'object00.fits[10:680,5:680]', 'WTextOut' : 'object.084', 'PrimaryOut' : 'prim.83.psf', 'SecondaryOut' : 'sec.83.psf', 'ncol' : 671, 'nrow' : 676},
#                        {'WTextIn' : 'object00.fits[10:680,6:680]', 'WTextOut' : 'object.085', 'PrimaryOut' : 'prim.84.psf', 'SecondaryOut' : 'sec.84.psf', 'ncol' : 671, 'nrow' : 675},
#                        {'WTextIn' : 'object00.fits[10:680,7:680]', 'WTextOut' : 'object.086', 'PrimaryOut' : 'prim.85.psf', 'SecondaryOut' : 'sec.85.psf', 'ncol' : 671, 'nrow' : 674},
#                        {'WTextIn' : 'object00.fits[10:680,8:680]', 'WTextOut' : 'object.087', 'PrimaryOut' : 'prim.86.psf', 'SecondaryOut' : 'sec.86.psf', 'ncol' : 671, 'nrow' : 673},
#                        {'WTextIn' : 'object00.fits[10:680,9:680]', 'WTextOut' : 'object.088', 'PrimaryOut' : 'prim.87.psf', 'SecondaryOut' : 'sec.87.psf', 'ncol' : 671, 'nrow' : 672},
#                        {'WTextIn' : 'object00.fits[10:680,10:680]', 'WTextOut' : 'object.089', 'PrimaryOut' : 'prim.88.psf', 'SecondaryOut' : 'sec.88.psf', 'ncol' : 671, 'nrow' : 671},
#                        {'WTextIn' : 'object00.fits[10:680,11:680]', 'WTextOut' : 'object.090', 'PrimaryOut' : 'prim.89.psf', 'SecondaryOut' : 'sec.89.psf', 'ncol' : 671, 'nrow' : 670},
#                        {'WTextIn' : 'object00.fits[11:680,2:680]', 'WTextOut' : 'object.091', 'PrimaryOut' : 'prim.90.psf', 'SecondaryOut' : 'sec.90.psf', 'ncol' : 670, 'nrow' : 679},
#                        {'WTextIn' : 'object00.fits[11:680,3:680]', 'WTextOut' : 'object.092', 'PrimaryOut' : 'prim.91.psf', 'SecondaryOut' : 'sec.91.psf', 'ncol' : 670, 'nrow' : 678},
#                        {'WTextIn' : 'object00.fits[11:680,4:680]', 'WTextOut' : 'object.093', 'PrimaryOut' : 'prim.92.psf', 'SecondaryOut' : 'sec.92.psf', 'ncol' : 670, 'nrow' : 677},
#                        {'WTextIn' : 'object00.fits[11:680,5:680]', 'WTextOut' : 'object.094', 'PrimaryOut' : 'prim.93.psf', 'SecondaryOut' : 'sec.93.psf', 'ncol' : 670, 'nrow' : 676},
#                        {'WTextIn' : 'object00.fits[11:680,6:680]', 'WTextOut' : 'object.095', 'PrimaryOut' : 'prim.94.psf', 'SecondaryOut' : 'sec.94.psf', 'ncol' : 670, 'nrow' : 675},
#                        {'WTextIn' : 'object00.fits[11:680,7:680]', 'WTextOut' : 'object.096', 'PrimaryOut' : 'prim.95.psf', 'SecondaryOut' : 'sec.95.psf', 'ncol' : 670, 'nrow' : 674},
#                        {'WTextIn' : 'object00.fits[11:680,8:680]', 'WTextOut' : 'object.097', 'PrimaryOut' : 'prim.96.psf', 'SecondaryOut' : 'sec.96.psf', 'ncol' : 670, 'nrow' : 673},
#                        {'WTextIn' : 'object00.fits[11:680,9:680]', 'WTextOut' : 'object.098', 'PrimaryOut' : 'prim.97.psf', 'SecondaryOut' : 'sec.97.psf', 'ncol' : 670, 'nrow' : 672},
#                        {'WTextIn' : 'object00.fits[11:680,10:680]', 'WTextOut' : 'object.099', 'PrimaryOut' : 'prim.98.psf', 'SecondaryOut' : 'sec.98.psf', 'ncol' : 670, 'nrow' : 671},
#                        {'WTextIn' : 'object00.fits[11:680,11:680]', 'WTextOut' : 'object.100', 'PrimaryOut' : 'prim.99.psf', 'SecondaryOut' : 'sec.99.psf', 'ncol' : 670, 'nrow' : 670} ]  
#
#        return PSFList

class BinaryFit:
    #def __init__(self):
	
    def Run(self):
        print "\n" + "#" * 60 + "\n"
        print "Running Binary PSF Fits (FORTRAN Version)\n"

	starttime = time.strftime('%A, %B %d, %Y %X %Z' ,time.localtime())
        os.system('nice -19 /usr/local/bin/BinaryFitPSF')
	endtime = time.strftime('%A, %B %d, %Y %X %Z' ,time.localtime())

	LogFile = open("BinaryFitPSF.log", 'w')
	LogFile.write("\n" + "#" * 60 + "\n")
        LogFile.write("\nStarted at:\t %s\n" % (starttime))
        LogFile.write("Finished at:\t %s\n" % (endtime))
        LogFile.write("\n" + "#" * 60)                                  
        LogFile.close()

        print "\n" + "#" * 60

class SingleFit:
        def __init__(self):
                # Open file with Real PSF information and assign the values

                Xmin, Xmax, Ymin, Ymax, RealPSFFile, Background, Sigma, Orientation, Coords = open("binary_inparam.txt", 'r').read().split()
                self.Background = float(Background)                                     # Cast background to float (global)
                self.Sigma = float(Sigma)                                               # Cast sigma to float (global)

                self.MakeRealPSF()                                                      # Read in the Real PSF file, etc
                self.MakeRealPSFError()                                                 # Read in the Real PSF Error file

                OutputFile = open("SingleFitPSF.out", 'w')                              # Open new output file for writing
                OutputFile.write("\n" + "#" * 60)                                       # Write beginning message
                OutputFile.write("\n\nBeginning Best Single PSF Models\n\n")
                OutputFile.close()                                                      # Close the output file

                print "\n" + "#" * 60                                                   # Text Output
                print "\nBeginning Best Single PSF Models\n"

                starttime = time.strftime('%A, %B %d, %Y %X %Z' ,time.localtime())

                #self.FindBestModel('ChiWeighted')                                       # Find best ChiWeighted Model
                self.FindBestModel('ChiReduced')                                        # Find best ChiReduced Model
                #self.FindBestModel('GoodnessOfFit')                                     # Find best Goodness-of-fit Model

                endtime = time.strftime('%A, %B %d, %Y %X %Z' ,time.localtime())

                OutputFile = open("SingleFitPSF.out", 'a')                              # Open new output file for appending
		OutputFile.write("Started at:\t %s\n" % (starttime))			# Log Start Time
                OutputFile.write("Finished at:\t %s\n" % (endtime))			# Log End Time
                OutputFile.write("\n" + "#" * 60)                                       # Write ending message
                OutputFile.close()                                                      # Close the output file

                print "#" * 60

        def BestPSF(self,Statistic):
                D = {}                                                                  # Dictionary to hold minimum chi
                ModelPSFList = self.GetPrimaryList()                                    # Get list of model filenames

                for ModelPSFFile in ModelPSFList:                                       # Loop through all the models
                        self.MakeModelPSF(ModelPSFFile)                                 # Make the model PSF

                        # Create the array to hold the scaled PSF
                        ScalePSF = numpy.zeros((self.RealPSFArraySize+1,self.RealPSFArraySize+1))
                        ScalePSF = self.ModelPSF * self.Flux                            # Model PSF scaled

                        # Determine and do the desired statistic
                        if Statistic == 'ChiWeighted':                                  # Chi Weighted
                                chi = numpy.add.reduce(numpy.add.reduce(self.RealPSFWeight*(self.RealPSF-ScalePSF)**2))
                        elif Statistic == 'ChiReduced':                                 # Chi Reduced
                                chi = self.FindChiReduced(self.Flux)
                        elif Statistic == 'GoodnessOfFit':                              # Goodness-of-fit
                                chi = self.FindGoodnessOfFit(self.Flux)
                        else:
                                sys.exit("BestPSF:  Bad Chi Statistic Given")           # Bad statistic given

                        # If Chi not assigned or is less than previous calculation
                        if not D.has_key('MinChi') or chi < D['MinChi']:
                                D['MinChi']=chi                                         # Assign a miniumum chi
                                self.BestModel = ModelPSFFile                           # Assign the best model

        def FindBestModel(self,Statistic):
                icount = 1                                                              # Number of tries
                scale = 1.0
                self.Flux = scale * self.Base                                           # Assign flux to base at first

                OutputFile = open("SingleFitPSF.out", 'a')                              # Open the output file for appending
                OutputFile.write("Try\tFlux\t\tBest Model\t" + Statistic +"\n")         # Write the column titles

                print "Try\tFlux\t\tBest Model\t" + Statistic                           # Print column titles
                
                while 1:
                        Comp = self.Flux                                                # Flux to compare after models
                        self.BestPSF(Statistic)                                         # Find the best model
                        self.ScaleBestPSF(Statistic)                                    # Find the best flux for the model
                        self.Flux = self.Flux * self.Base                               # New scaled flux

                        # Output to file and screen
                        print "%i\t%1.9f\t%s\t%1.10f" % (icount, self.Flux, self.BestModel, self.MinChi)
                        OutputFile.write("%i\t%1.9f\t%s\t%1.10f\n" % (icount, self.Flux, self.BestModel, self.MinChi))

                        # Compare previous solution to see if the same, stop trying after 10 times
                        if self.Flux == Comp  or icount > 10:
                                break
                        icount = icount+1
                print ""                                                                # Print line
                OutputFile.write("\n")
                OutputFile.close()                                                      # Close file

        def FindChiReduced(self,Flux):
                # Define an array for the errors and calculate errors
                RealPSFErr = numpy.zeros((self.RealPSFArraySize+1,self.RealPSFArraySize+1))
                RealPSFErr[1:,1:] = self.RealPSFError[1:,1:]**2  + self.Sigma**2

                # Define an array for the chi reduced statistics, calculate, and return the value
                ChiReducedPSF = numpy.zeros((self.RealPSFArraySize+1,self.RealPSFArraySize+1))
                ChiReducedPSF[1:,1:] = (self.RealPSF[1:,1:] - (self.ModelPSF[1:,1:] * Flux))**2 / RealPSFErr[1:,1:]
                return numpy.add.reduce(numpy.add.reduce(ChiReducedPSF[1:,1:]))

        def FindGoodnessOfFit(self,Flux):
                # Define an array for the chi goodness-of-fit statistics, calculate, and return the value
                ChiReducedPSF = numpy.zeros((self.RealPSFArraySize+1,self.RealPSFArraySize+1))
                ChiReducedPSF[1:,1:] = (self.RealPSF[1:,1:] - (self.ModelPSF[1:,1:] * Flux))**2 / self.ModelPSF[1:,1:]
                return numpy.add.reduce(numpy.add.reduce(ChiReducedPSF[1:,1:]))

        def GetPrimaryList(self):
                PrimaryList = ( 'prim.00.psf', 'prim.01.psf', 'prim.02.psf', 'prim.03.psf', 'prim.04.psf',
                                'prim.05.psf', 'prim.06.psf', 'prim.07.psf', 'prim.08.psf', 'prim.09.psf',
                                'prim.10.psf', 'prim.11.psf', 'prim.12.psf', 'prim.13.psf', 'prim.14.psf',
                                'prim.15.psf', 'prim.16.psf', 'prim.17.psf', 'prim.18.psf', 'prim.19.psf',
                                'prim.20.psf', 'prim.21.psf', 'prim.22.psf', 'prim.23.psf', 'prim.24.psf',
                                'prim.25.psf', 'prim.26.psf', 'prim.27.psf', 'prim.28.psf', 'prim.29.psf',
                                'prim.30.psf', 'prim.31.psf', 'prim.32.psf', 'prim.33.psf', 'prim.34.psf',
                                'prim.35.psf', 'prim.36.psf', 'prim.37.psf', 'prim.38.psf', 'prim.39.psf',
                                'prim.40.psf', 'prim.41.psf', 'prim.42.psf', 'prim.43.psf', 'prim.44.psf',
                                'prim.45.psf', 'prim.46.psf', 'prim.47.psf', 'prim.48.psf', 'prim.49.psf',
                                'prim.50.psf', 'prim.51.psf', 'prim.52.psf', 'prim.53.psf', 'prim.54.psf',
                                'prim.55.psf', 'prim.56.psf', 'prim.57.psf', 'prim.58.psf', 'prim.59.psf',
                                'prim.60.psf', 'prim.61.psf', 'prim.62.psf', 'prim.63.psf', 'prim.64.psf',
                                'prim.65.psf', 'prim.66.psf', 'prim.67.psf', 'prim.68.psf', 'prim.69.psf',
                                'prim.70.psf', 'prim.71.psf', 'prim.72.psf', 'prim.73.psf', 'prim.74.psf',
                                'prim.75.psf', 'prim.76.psf', 'prim.77.psf', 'prim.78.psf', 'prim.79.psf',
                                'prim.80.psf', 'prim.81.psf', 'prim.82.psf', 'prim.83.psf', 'prim.84.psf',
                                'prim.85.psf', 'prim.86.psf', 'prim.87.psf', 'prim.88.psf', 'prim.89.psf',
                                'prim.90.psf', 'prim.91.psf', 'prim.92.psf', 'prim.93.psf', 'prim.94.psf',
                                'prim.95.psf', 'prim.96.psf', 'prim.97.psf', 'prim.98.psf', 'prim.99.psf')
                return PrimaryList

        def MakeModelPSF(self, Filename):
                ModelPSFData = open(Filename, 'r')                                      # Open file with PSF Values
                ModelPSFBase = numpy.zeros((68,68))                                     # Array to hold entire PSF image

                # Loop through size of PSF image, assign values
                for j in range(1,68):
                        for i in range(1,68):
                                ModelPSFBase[i,j] = float(ModelPSFData.readline())

                # Array to hold section of PSF
                self.ModelPSF = numpy.zeros((self.RealPSFArraySize+1,self.RealPSFArraySize+1))

                # Assign the section of the PSF desired
                size = int(self.RealPSFArraySize // 2)                                  # Size of model based on real PSF
                self.ModelPSF[1:,1:] = ModelPSFBase[34-size:34+size+1,34-size:34+size+1]

        def MakeRealPSF(self):
                RealPSFFile = "binary_box_sci"                                          # File containing Real PSF values
                RealPSFInfo = []                                                        # List to hold Real PSF error values

                RealPSFLines = open(RealPSFFile, 'r').readlines()                       # Open file with Real PSF pixel values
                for RealPSFLine in RealPSFLines:                                        # Loop through lines, create List
                        RealPSFInfo.append(RealPSFLine.split())

                ArraySize = math.sqrt(len(RealPSFInfo))                                 # Determine size needed for array
                if ArraySize % 2 == 0:
                        sys.exit("Size of Real PSF File Is Not Odd")
                else:
                        self.RealPSF = numpy.zeros((ArraySize+1,ArraySize+1))           # Real PSF pixel array (Global)
                        self.RealPSFWeight = numpy.zeros((ArraySize+1,ArraySize+1))     # Weight array (Global)
                        self.RealPSFArraySize = ArraySize                               # Size needed for array (Global)

                self.Base = 0.0                                                         # Base flux (Global)

                for Values in RealPSFInfo:                                              # Loop through list
                        i = int(Values[0][:-1])                                         # x values from listpix
                        j = int(Values[1][:-1])                                         # y values from listpix

                        self.RealPSF[i,j] = float(Values[2]) - self.Background          # Assign pixel values

                        if self.RealPSF[i,j] < 0:                                       # If pixel is less than zero
                                self.RealPSF[i,j] = 0.0                                 # Assign to zero

                        self.Base = self.Base + self.RealPSF[i,j]                       # Add to base flux

                        # Assign weight value
                        self.RealPSFWeight[i,j] = math.sqrt(math.fabs(self.RealPSF[i,j]))

                        if self.RealPSF[i,j] < self.Sigma:                              # If pixel is less than sigma
                                self.RealPSFWeight[i,j] = 0.0                           # No weight

        def MakeRealPSFError(self):
                RealPSFErrorFile = "binary_box_err"                                     # File containing Real PSF error values
                RealPSFErrorInfo = []                                                   # List to hold Real PSF error values

                RealPSFErrorLines = open(RealPSFErrorFile, 'r').readlines()             # Open file with Real PSF error pixel values
                for RealPSFErrorLine in RealPSFErrorLines:                              # Loop through lines, create List
                        RealPSFErrorInfo.append(RealPSFErrorLine.split())

                ArraySize = math.sqrt(len(RealPSFErrorInfo))                            # Determine size needed for array
                if ArraySize % 2 == 0:
                        sys.exit("Size of Real PSF Error File Is Not Odd")
                else:
                        self.RealPSFError = numpy.zeros((ArraySize+1,ArraySize+1))      # Real PSF Error pixel array (Global)

                for Values in RealPSFErrorInfo:                                         # Loop through list
                        i = int(Values[0][:-1])                                         # x values from listpix
                        j = int(Values[1][:-1])                                         # y values from listpix

                        self.RealPSFError[i,j] = float(Values[2])                       # Assign pixel values

        def ScaleBestPSF(self,Statistic):
                D = {}                                                                  # Dictionary to hold minimum chi
                self.MakeModelPSF(self.BestModel)                                       # Make the model PSF

                # Loop through 0.0001 increments of the flux
                for k in range(1, 100000):
                        scale = k * 0.0001                                              # Scale increment

                        # Create the array to hold the scaled PSF
                        ScalePSF = numpy.zeros((self.RealPSFArraySize+1,self.RealPSFArraySize+1))
                        ScalePSF = self.ModelPSF * scale * self.Base

                        # Determine and do the desired statistic
                        if Statistic == 'ChiWeighted':                                  # Chi Weighted
                                chi = numpy.add.reduce(numpy.add.reduce(self.RealPSFWeight*(self.RealPSF-ScalePSF)**2))
                        elif Statistic == 'ChiReduced':                                 # Chi Reduced
                                chi = self.FindChiReduced(scale*self.Base)
                        elif Statistic == 'GoodnessOfFit':                              # Goodness-of-fit
                                chi = self.FindGoodnessOfFit(scale*self.Base)
                        else:
                                sys.exit("ScaleBestPSF:  Bad Chi Statistic Given")      # Bad statistic given
                       
                        # If Chi not assigned or is less than previous calculation
                        if not D.has_key('MinChi') or chi < D['MinChi']:
                                D['MinChi']=chi                                         # Assign the minimum chi
                                self.Flux = scale                                       # Assign the best scale

                self.MinChi = D['MinChi']                                               # Assign the global minimum chi

#class Tiny:
#    def __init__(self):
#        try:
#            with open(r'biff.yaml') as file:
#                param = yaml.load(file, Loader=yaml.FullLoader)
#                os.environ["TINYTIM"] = param['biff']['tinytim']['path']
#                self.ParameterFile = param['biff']['tinytim']['outfile']
#        except IOError:
#            print('ERROR: biff.yaml could not be found.\n')
#            GoOn = raw_input("Press Enter To Continue...")
#
#    def Tiny1(self):
#        print("\n" + "#" * 60 + "\n")
#        print("Running tiny1...")
#        os.system('env tiny1 ' + self.ParameterFile)
#        print("\n" + "#" * 60)
#        GoOn = raw_input("Press Enter To Continue...")
#
#    def Tiny2(self):
#        print("\n" + "#" * 60 + "\n")
#        print("Running tiny2 On Parameter File...\n")
#        os.system('env tiny2 ' + self.ParameterFile)
#        print("\n" + "#" * 60)
#        GoOn = raw_input("Press Enter To Continue...")

