Generic Makefile system for NewGRFs
-----------------------------------

Contents:

1 About
2 Setting up a repository
  2.1 Enabling support for using layered graphics files as source
3 Installation and dependencies
  3.1 Update from old Makefile revisions
4 Usage
  4.1 Speed issues
5 License
6 Credits



-------
1 About
-------

This NewGRF build system aims at NewGRF authors for OpenTTD and TTDPatch
who want to employ an easy-to-use system in order to generate their NewGRFS.

Name of this Repo:  Example NewGRF project
Repository version: 289



-------------------------
2 Setting up a repository
-------------------------

If you already have the necessary devlopment tools (see chapter 3 for
requirements), here is how to get a new project going:

If you have obtained a bundle from
http://bundles.openttdcoop.org/newgrf_makefile/
it is very simple to get a newgrf going: 
1) after unzip rename the resulting directory into one which makes sense
   for your new newgrf
2) initialize a mercurial repository within that directory using 'hg init'
   and add all files to the project, but do not yet commit. Currently the
   makefile does not satisfactorily work without mercurial repository
3) In order to adopt the project to your needs, you'll need to adjust a
   few files:
   - Makefile.config
   - .hgignore
   - docs/changelog.ptxt
   - docs/readme.ptxt
   - docs/license.ptxt (you may choose GPL v2 or newer, if you use this
     template newgrf and build system)
4) Make your initial commit to your repository, adding the build framework
5) Start editing your newgrf.
6) Optionally: enable building pngs from psd (photoshop) or xcf (gimp) 
   layered source files

If you checked out the repository for the example newgrf makefile from
http://hg.openttdcoop.org/projects/example_makefile
then build the example directories using 'make' and copy the resulting
directory example-newgrf-nightly-rXXX-nfo or ...-nml (whatever type of
project you plan to take on) to a place and name where you want to develop
your newgrf. Continue with step 2) as above.

A few general rules:
   The main source file has to differ from the desired grf name only by the
   file extension. If your newgrf is called example.grf, your main source
   file is called
      sprites/nfo/example.pnfo (NFO project)
      src/example.pnml         (NML project)
   The example setup takes care of that, just mind this rule when giving your
   NewGRF a unique name.

optional: 
   use {{GRF_ID}} and {{GRF_TITLE}} in your action 08 of your
   newgrf as done in the supplied example (sprites/nfo/00header.pnfo) to
   have the newgrf always display the correct version.

Further it can be recommended to use the hgeol extension of mercurial
(for versions newer than 1.5.4).
See http://mercurial.selenic.com/wiki/EolExtension for details. Using
the default configuration is often fine, just edit your .hgrc and add
this extension:

[extensions]
eol =

2.1 Enabling support for using layered graphics files as source
---------------------------------------------------------------
If you use layered image files to create, say, sprites of the same vehicle
with just different cargos, this makefile can use this layered file directly
as source and write the resulting pngs from your psd (photoshop) or
xcf (gimp) source files. But as gimp support is not enabled by default, some
additional changes are needed:
a) Edit your Makefile.config and look for 
   # GRAPHICS_SOURCE_LIST_FILE := src/png_source_list
   uncomment that line (remove the #) and replace the filename by the filename
   you want to use.
b) Create that file you chose in step a) and add the png files which you like
   to create from your source images, one png file per line:
   png filename<TAB>source filename<TAB>layers separated by space
   for example:
   sprites/graphics/tree_01.png 	sprites/graphics/trees.xcf		0 1 3
   Note that you'll have to give the path relative to the repository's main
   directory.
d) Make sure that you have gimp installed and within your path



-------------------------------
3 Installation and dependencies
-------------------------------

This Makefile system is easiest to setup if you employ a certain
directory structure for your NewGRF project. Clone this project and fill
in your NewGRF content. Make sure to adopt Makefile.config to your needs.

Requirements for running this Makefile successfully:
	grfcodec (only nfo-stylee project)
	nforenum (only nfo-stylee project)
	NML (only nml-style project)
	gcc
	md5sum (or md5 on Mac)
	make
    mercurial (recommended)
    python (recommended)
	gimp (optional, see chapter 2.1)
If you want to bundle the grf, you'll need additionally
	tar
	zip
	bzip2
	unix2dos (optional)
Windows only:
On Windows systems this means that you'll need to install MinGW and MSys
in order to obtain a posix compatible environment. Then the makefile can
be called the very same way as it is on linux and mac systems.
MinGW/MSys contain the above mentioned programmes (except renum and
grfcodec of course) and can be obtained from http://www.mingw.org/ That
site also features an excellent walk-through o how to install it.

If you use for OpenTTD data folder a non-default path or Windows with a
non-English localization make sure to copy Makefile.local.sample to
Makefile.local and edit the line with
	INSTALLDIR =
accordingly so that it shows the full path to your OpenTTD / TTDP data
directory.

3.1 Update from old Makefile versions
-------------------------------------
Note that some changes were introduced between 0.4.0 and 0.4.1 Makefile
versions which require you additionally to make changes to your
Makefile.config:

USE_NFO := 1 ; for nfo-style projects
USE_NML := 1 ; for nml-style projects
USE_OBG := 1 ; additionally for base graphics sets

MAIN_TARGET and GRF_FILES became obsolete. It is replaced by the common
variable TARGET_FILES

DOC_FILES now lists all required documentation files in their final form
(*.txt). This is also true for text files which require pre-processing,
you just specify the desired output filename here. The individual
variables README_FILENAME etc are obsolete and unused.



-------
4 Usage
-------

Before this build system can be applied to a newgrf, you have to adopt a
few lines in Makefile.config, mainly you'll have to replace "mynewgrf"
by the actual name of your newgrf. Also make sure to change that in the
.hgignore file.

If the Makefile is too slow, you may try different dependency checks or
skip those completely. Available options for dependency generation are:
mdep:   uses a python script. Default when used in a hg repository
normal: uses gcc and bash to scan for dependencies
none:   disable the dependency generation (mostly)
Makefile.local allows to choose the method via the declaration of
DEP_CHECK_TYPE.

The Makefile offers different targets. A brief overview is given here:

all:
	This is the default target, if also no parameter is given to
	make. It will simply build the grf file, if it needs building

depend:
	Re-run the dependency check. Usually not manually needed.

docs:
	Build the documentation files

bundle:
	This target will create a directory called "<name>-nightly" and
	copy the grf file there and the documentation files, readme.txt,
	changelog.txt and license.txt

bundle_zip
	This will zip the bundle directory into one zip for distribution

bundle_tar
	This will tar the bundle directory into a tar archive for
	distribution or upload to bananas

bundle_src
	Creates a source bundle

install:
	This will create a tar archive (like bundle_tar) and copy it
	into the INSTALLDIR as specified in Makefile.local (or the
	default dir, if that isn't defined). Don't rely on a good
	detection of the default installation directory. It's
	especially bound to fail on windows machines.

distclean:
	This phony target cleans everything from a source bundle which
	wasn't shipped.

clean:
	This phony target will delete all files which this Makefile will
	create

mrproper:
	This phony target will delete also all directories created by
	different Makefile targets

remake:
	It's a shortcut for first cleaning the dir and then making the
	grf anew.

addcheck:
	Check whether there are some files required but not part of the
	repository.

check:
	Check the md5sum of the built newgrf against the supplied md5sum
	(Intended to be used when building from tar balls)


4.1 Speed issues
----------------

A note concerning the speed of the makefile:
It seems that the required tools using MinGW and / or msys are thoroughly
slow on windows. A few example run times for OpenGFX, same processor type
(both core 2 duo, 2.26GHz for the windows machine, 2.0 GHz for the OSX
machine). Note that the values given are the 'real' time. Even though
this varies more and is dependent on the processor load, that's what you
have to wait for; the 'user' times are quite low on the windows machine
(~16s), but that by no means reflects the build time. Times are from
OpenGFX r539 with makefile r199.

DEP_CHECK_TYPE         windows               bash native
                 native       in VM            (OSX)
none            1m23.360s      -             0m32.781s
mdep            1m54.484s   0m30.164s        0m33.807s
normal          2m37.857s      -             0m36.528s



---------
5 License
---------

This generic NewGRF Makefile was written by Ingo von Borstel (aka
planetmaker) and is free to use for anyone under the terms of the GNU
Pulic License v2 or higher. See license.txt.

The source code can be obtained from the #openttdcoop DevZone at
http://dev.openttdcoop.org/projects/newgrf-makefile or via mercurial
checkout
hg clone http://hg.openttdcoop.org/newgrf-makefile



---------
6 Credits
---------

Author: Ingo von Borstel (aka planetmaker)

Special thanks to #openttdcoop and especially Ammler who provides and
works a lot on maintaining the Development Zone where this repository is
hosted and who also frequently gives much valuable input. Thanks also to
Alberth, Terkhen Yexo, Rubidium and Ammler who frequently give valuable
input in form of advice and patches to this project. Last but not least
thanks to all the NewGRF authors whose NewGRFs can be my playground for
this project.
