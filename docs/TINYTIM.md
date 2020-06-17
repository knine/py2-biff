# BIFF - BInary Fitting Facility - TINYTIM Prerequisites

BIFF requires that [Tiny Tim](https://github.com/spacetelescope/tinytim) be available on the system.

## Operating System

This document assumes the user is running a compatible Linux distribution.

Distributions tested:
* Ubuntu 18.04

## Installing

Download Tiny Tim from the link above either as a tarball or using `git`.

Chose an appropriate directory location to save the files that will be accessible as needed.

Single User Example:
```
cd ~
mkdir stsci && cd stsci
git clone https://github.com/spacetelescope/tinytim.git
```

Tiny Tim needs to be compiled with a C compiler which may need to be installed on the system.

As of this is writing in the year 2020, pretty much all systems have multiprocessors. Compile Tiny Tim for multiple processors:
```
cd tinytim
make threadedlinux
```

See the Tiny Tim documentation for more information.

## BIFF Configuration

To make BIFF aware of Tiny Tim, edit biff.yaml. For example:
```
tinytim:
  path: '/home/jake/stsci/tinytim'
  outfile: 'nicmos1.par'
```

* path: Full directory path to Tiny Tim files. This will automatically set the required TINYTIM environment variable in BIFF when needed.
* outfile: Name of the parameter file which tiny1 writes and tiny2 reads. Can be named as desired.

## Archive Copy

A copy of the [Tiny Tim repository](https://github.com/knine/tinytim) has been archived in the same user profile as BIFF.
