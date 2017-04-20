# Zave2Pdf

_Zave2Pdf_ is a Python script that, converts a zave file into a pdf file, by using [reportlab](https://pypi.python.org/pypi/reportlab), [pdfrw](https://github.com/pmaupin/pdfrw/) and Python xml library. To use this script, reportlab and pdfrw should be installed. And pdfrw requires a patch before install.

__IMPORTANT__: Script requires to apply [developer's patch](https://github.com/pmaupin/pdfrw/pull/63) to pdfrw, because related pull request hasn't merged to master repository. For detailed information and application steps look at __Prepare pdfrw__ title.

##Running Script

Zave2Pdf work with two parameters; __-zave__ to indicate zave file and __-s__ to indicate (optional) output pdf file.

Usage;

     Zave2Pdf.py -zave /Path/of/ZaveFile.zave

Indicating the save path and file name(optional);

     Zave2Pdf.py -zave /Path/of/ZaveFile.zave -s /Save/Directory/FileName.pdf


##Prepare pdfrw

###Download pdfrw
Original git repository of pdfrw master is [pmaupin/pdfrw/](https://github.com/pmaupin/pdfrw/). And clone url can be found from _Clone or Download_ button as [https://github.com/pmaupin/pdfrw.git](https://github.com/pmaupin/pdfrw.git)

And related patch file can be found as [https://github.com/pmaupin/pdfrw/pull/63.patch](https://github.com/pmaupin/pdfrw/pull/63.patch)

First go your local folder

	cd /Users/user_name/Downloads/
	
An get pdfrw master,
	
	git clone https://github.com/pmaupin/pdfrw.git
	
Master is here. Now go into folder,
	
	cd pdfrw

Create .patch file by _curl_, from github's patch file url ([_pmaupin/pdfrw/pull/63.patch_](https://patch-diff.githubusercontent.com/raw/pmaupin/pdfrw/pull/63.patch)) which can be found at [63rd pull request page.](https://github.com/pmaupin/pdfrw/pull/63)

	curl -0 https://patch-diff.githubusercontent.com/raw/pmaupin/pdfrw/pull/63.patch
	
And apply patch file,

	git apply 63.patch

After patch, pdfrw is ready!

###Install pdfrw

	python setup.py build
	sudo python setup.py install
     
##Some Notes

- Zave files can consist scrollable contents. But pdfs can't, in traditional ways. Zave2Pdf adds scrollable content as following page and prints a message into scroll area as "You can view the content at the following page"
- This script based on zave files which contains pdf and png files. This kind of zave files is the majortiy of zave files. When any problems occured, please use issues or send an e-mail to me.