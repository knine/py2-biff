# BIFF - BInary Fitting Facility - Python 2

BIFF was originally a set of routines I developed around 2007 - 2008 while in graduate school to aid in modeling point spread functions to search for binary brown dwarfs in archive Hubble Space Telescope data archive.

Now it is 2020. This is my attempt to make it work again.

## Getting Started

* Install a basic minimal installation of Ubuntu 18.04.
* Update the system and install recommended libraries for 32-bit IRAF.
```
sudo apt-get update && sudo apt-get upgrade && sudo apt-get dist-upgrade
sudo apt install libc6:i386 libz1:i386 libncurses5:i386 libbz2-1.0:i386 libuuid1:i386 libxcb1:i386 libxmu6:i386
```
* Download and install Python 3.7 64-bit [Miniconda](https://docs.conda.io/en/latest/miniconda.html) for Linux.
* Add the AstroConda channel:
```
conda config --add channels http://ssb.stsci.edu/astroconda
```
* Install the [Legacy Software Stack](https://astroconda.readthedocs.io/en/latest/installation.html#iraf-install)
```
conda create -n iraf27 python=2.7 iraf-all pyraf-all stsci
conda install -c astroconda -n iraf27 statistics termcolor
```

### Prerequisites

* [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
* [AstroConda](https://astroconda.readthedocs.io/en/latest/getting_started.html)
* [Tiny Tim](https://github.com/spacetelescope/tinytim)

### Installing

* [Install Tiny Tim](docs/TINYTIM.md)
* [Install and Configure BIFF](docs/BIFF.md)

## Built With

* [Python 2.7](https://www.python.org/download/releases/2.7/) - Primary programming language.
* [PyRAF](https://pypi.org/project/pyraf/) - Support libraries.

## Authors

* [Jacob Albretsen](https://github.com/knine)

See also the list of [contributors](https://github.com/knine/py2-biff/contributors) who participated in this project.

## License

This project is licensed under the GNU General Public License Version 3 - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

* Special thanks to my PhD adviser, Dr. Denise Stephens.
~                 
