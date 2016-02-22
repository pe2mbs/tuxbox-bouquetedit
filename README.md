# Tuxbox / Engima2 Bouquet Editor

Why another Bouquet Editor, there are several bouquet editors some are Windows only, some are web based to run on the receiver it self, 
and Linux / multi platform. Most of these don't work like they should be therefore another was desired. 

This Bouquet editor uses the wxWidgets 2.8 library and is written in Python. All through the application not complete (see todo) 
I like to get some feedback on how the application experienced is at this time. 


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
	

# Todo
1.	Save bouquets (receiver/folder).
2.	Save As bouquets (receiver/folder).
3.	Bouquet "Drag and Drop". 
4.	"Drag and Drop" service to bouquet.
5.	Handle radio channels.
6.	Printer setup and print.
7.  Help system.
8.  Improve the preferences dialog

# Issues
1.	Sometimes in filter mode on ASC mode services disapear
 
