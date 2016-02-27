# Tuxbox / Engima2 Bouquet Editor

Why another Bouquet Editor, there are several bouquet editors some are Windows only, some are web based to run on the receiver it self, 
and Linux / multi platform. Most of these don't work like they should be therefore another was desired. 

This Bouquet editor uses the wxWidgets 2.8 library and is written in Python. All through the application not complete (see todo) 
I like to get some feedback on how the application experienced is at this time. 

I thank "spacedentist" and his project enigma2-bouqueteditor, the enigma2.py module, I used this to do all the parsing and building 
the service list and bouquets. 

All through this is build on a Linux system, it should run on Windows and Mac.  
The gui is designed with wxGlade.


# Usage:
When starting the application and a receiver is set to autoload, the application will load the channels and bouquets from the receiver.

## Keys
###	Service list
	UP						move up an item.
	DOWN					move down an item.
	ENTER / Double click	start mplayer.
	Q / q					terminate mplayer process.
	Button >>				Add a high light service into the selected bouquet.
	Button <<				Remove a high light service from the bouquet.

### Bouquet tree
	UP						move up an item.
	DOWN					move down an item.
	ENTER / Double click	start mplayer.
	Q / q					terminate mplayer process.
	Button UP				move item up in the tree.
	Button DOWN				move item down in the tree.

	CTRL-UP					move item up in the tree.
	CTRL-DOWN				move item down in the tree.
	DELETE					Remove item from the list.
	
# Last updates
1.	Now Save As bouquets to folder works.
2.	Now Save bouquets to folder works.
3.	Some improvements to the preferences dialog where made, but still not complete.
4.	Radio channels now implemented
5.	Solved the issue "Sometimes in filter mode on ASC mode services disappear"
6.	Added help system
7.  Multi language support added.
8.	Moved language class to language module and improved setting user language

# Todo
1.	Save bouquets (receiver) it must be tested, it should work already.
2.	Save As bouquets (receiver) it must be tested, it should work already.
3.	Bouquet "Drag and Drop". 
4.	"Drag and Drop" service to bouquet.
5.	Printer setup and print.
6.  Help system contents must be added.
7.  Improve further the preferences dialog

# Issues

 
