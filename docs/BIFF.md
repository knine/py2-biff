# BIFF - BInary Fitting Facility - Installing

## Operating System

Distributions tested:
* Ubuntu 18.04

## Installing

This document assumes: 
* The user is running a compatible Linux distribution.
* PyRAF / IRAF with Python 2.7 have been installed.

Chose an appropriate directory location to save the files that will be accessible as needed.

Single User Example:
```
cd ~
mkdir knine && cd knine
git clone https://github.com/knine/py2-biff.git
```

For the above example, the main BIFF program will be located at `~/knine/py2-biff/biff.py`

## Command Alias

Create an alias to easily access the BIFF program. For example in Ubuntu 18.04 create or edit `~/.bash_aliases` file.

Example line to add:
```
alias biff='/home/<USERNAME>/knine/py2-biff/biff.py'
```

Replace `<USERNAME>` and modify paths as needed.

The current shell will need to be restarted for the alias to be recognized.

## Usage and Configuration

Create a directory to do the research work.
```
cd ~
mkdir MyResearch && cd MyResearch
```

* After changing to the research directory and run `mkiraf` to generate a default `login.cl` file.
```
mkiraf
```
Inside the research directory, create a file called `biff.yaml` and create the required default data.

```
biff:
  path: '/home/<USERNAME>/knine/py2-biff'

tinytim:
  path: '/home/<USERNAME>/opt/tinytim'
  outfile: 'nicmos1.par'
```

Replace `<USERNAME>` and modify paths as needed.

* biff:path - Full directory path to base BIFF files.

* tinytim:path - Full directory path to Tiny Tim files. This will automatically set the required TINYTIM environment variable in BIFF when needed.
* tinytim:outfile - Name of the parameter file which tiny1 writes and tiny2 reads. Can be named as desired.

