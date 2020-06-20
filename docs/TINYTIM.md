# BIFF - BInary Fitting Facility - TINYTIM Install

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

See the [Tiny Tim documentation](https://github.com/spacetelescope/tinytim/blob/master/tinytim.pdf) for more information.

## BIFF Configuration

To make BIFF aware of Tiny Tim, edit biff.yaml. For see [BIFF install](https://github.com/knine/py2-biff/docs/BIFF.md) document for details.

## Archive Copy

A copy of the [Tiny Tim repository](https://github.com/knine/tinytim) has been archived in the same user profile as BIFF.
