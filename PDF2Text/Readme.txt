If you don't have pdfminer3k module, the easiest way to install is to use pip in cmd below:

	pip install pdfminer3k 

*pdfminer3k is for python 3.x

Note: Some PDF has already encrypted, but password is blank space.

Inorder to decrypt, you need to download 'qpdf'and below is download link:

	https://sourceforge.net/projects/qpdf/

And set an environment variable to your system.

	example: make sure qpdf.exe exist in path like C:\qpdf-5.1.2\bin and copy path.
		 Next, go to system properties > advanced > environment variable,
		       PATH, click edit then paste.

Finally, use sentance below in your .py file.

from subprocess import call
call('qpdf --password=%s --decrypt %s %s' % ('', input_file, output_file), shell=True) 


2017/6/1