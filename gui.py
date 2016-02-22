#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.6.8 on Sun Feb 21 15:56:35 2016
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
CMD_HELP            = wx.NewId()
CMD_OPEN_LOCATION   = wx.NewId()
CMD_OPEN_RECEIVER   = wx.NewId()
CMD_SAVE            = wx.NewId()
CMD_SAVEAS_LOCATION = wx.NewId()
CMD_SAVEAS_RECEIVER = wx.NewId()
CMD_PREFERENCES     = wx.NewId()
CMD_ABOUT           = wx.NewId()
CMD_CLOSE           = wx.NewId()
CMD_NEW_ENTRY       = wx.NewId()
CMD_DELETE_ENTRY    = wx.NewId()
CMD_PRINT           = wx.NewId()
CMD_PRINT_SETUP     = wx.NewId()
from bouquetedit.extendtreectrl import ExtendedTreeCtrl
from bouquetedit.editlistctrl import VirtualListCtrl
from bouquetedit.editlistctrl import EditableListCtrl
# end wxGlade


class BouquetEditMainWnd(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: BouquetEditMainWnd.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.window_1 = wx.SplitterWindow(self, wx.ID_ANY, style=wx.SP_3D | wx.SP_BORDER)
        self.window_1_pane_1 = wx.Panel(self.window_1, wx.ID_ANY)
        self.services = VirtualListCtrl(self.window_1_pane_1, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_VIRTUAL | wx.LC_SINGLE_SEL | wx.LC_HRULES | wx.LC_VRULES | wx.SUNKEN_BORDER)
        self.filter = wx.TextCtrl(self.window_1_pane_1, wx.ID_ANY, "")
        self.button_4 = wx.Button(self.window_1_pane_1, wx.ID_ANY, _("Apply"))
        self.button_3 = wx.Button(self.window_1_pane_1, wx.ID_ANY, _("Clear"))
        self.window_1_pane_2 = wx.Panel(self.window_1, wx.ID_ANY)
        self.button_6 = wx.Button(self.window_1_pane_2, wx.ID_ANY, _(">>"))
        self.button_7 = wx.Button(self.window_1_pane_2, wx.ID_ANY, _("<<"))
        self.bouquet_choice = wx.Choice(self.window_1_pane_2, wx.ID_ANY, choices=[])
        self.bouquets = ExtendedTreeCtrl(self.window_1_pane_2, wx.ID_ANY, style=wx.TR_HAS_BUTTONS | wx.TR_NO_LINES | wx.TR_LINES_AT_ROOT | wx.TR_FULL_ROW_HIGHLIGHT | wx.TR_HIDE_ROOT | wx.TR_ROW_LINES | wx.TR_DEFAULT_STYLE | wx.SUNKEN_BORDER | wx.WANTS_CHARS | wx.FULL_REPAINT_ON_RESIZE)
        self.button_8 = wx.Button(self.window_1_pane_2, wx.ID_ANY, _("UP"))
        self.button_9 = wx.Button(self.window_1_pane_2, wx.ID_ANY, _("DN"))
        
        # Menu Bar
        self.frame_2_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu_sub = wx.Menu()
        wxglade_tmp_menu_sub.Append(CMD_OPEN_RECEIVER, _("Receiver"), "", wx.ITEM_NORMAL)
        wxglade_tmp_menu_sub.Append(CMD_OPEN_LOCATION, _("Folder"), "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendMenu(wx.ID_ANY, _("Open"), wxglade_tmp_menu_sub, "")
        wxglade_tmp_menu.Append(CMD_SAVE, _("Save"), _("Save to receiver"), wx.ITEM_NORMAL)
        wxglade_tmp_menu_sub = wx.Menu()
        wxglade_tmp_menu_sub.Append(CMD_SAVEAS_RECEIVER, _("Receiver"), "", wx.ITEM_NORMAL)
        wxglade_tmp_menu_sub.Append(CMD_SAVEAS_LOCATION, _("Folder"), "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendMenu(wx.ID_ANY, _("Save as"), wxglade_tmp_menu_sub, "")
        wxglade_tmp_menu.Append(CMD_CLOSE, _("Close"), _("Close the bouquet"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendSeparator()
        wxglade_tmp_menu.Append(CMD_PRINT, _("Print"), _("Print the bouquets"), wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(CMD_PRINT_SETUP, _("Print setup"), "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendSeparator()
        wxglade_tmp_menu.Append(wx.ID_EXIT, _("Exit"), _("Exit the application"), wx.ITEM_NORMAL)
        self.frame_2_menubar.Append(wxglade_tmp_menu, _("File"))
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(CMD_PREFERENCES, _("Preferences"), _("Application preferences"), wx.ITEM_NORMAL)
        self.frame_2_menubar.Append(wxglade_tmp_menu, _("Options"))
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(CMD_HELP, _("Help"), "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.Append(CMD_ABOUT, _("About"), _("About this application"), wx.ITEM_NORMAL)
        self.frame_2_menubar.Append(wxglade_tmp_menu, _("Help"))
        self.SetMenuBar(self.frame_2_menubar)
        # Menu Bar end
        
        # Tool Bar
        self.frame_2_toolbar = wx.ToolBar(self, -1)
        self.SetToolBar(self.frame_2_toolbar)
        self.frame_2_toolbar.AddLabelTool(CMD_OPEN_LOCATION, _("Open folder"), wx.Bitmap("/home/mbertens/python/Icons/openfile.ico", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "", _("Open folder"))
        self.frame_2_toolbar.AddLabelTool(CMD_OPEN_RECEIVER, _("Open receiver"), wx.Bitmap("/home/mbertens/python/Icons/new CERTO client.ico", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "", _("Open receiver"))
        self.frame_2_toolbar.AddLabelTool(CMD_SAVE, _("Save"), wx.Bitmap("/home/mbertens/python/Icons/Save.ico", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "", _("Save bouquets"))
        self.frame_2_toolbar.AddSeparator()
        self.frame_2_toolbar.AddLabelTool(CMD_NEW_ENTRY, _("New"), wx.Bitmap("/home/mbertens/python/Icons/New.Item.ico", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "", _("New bouquet"))
        self.frame_2_toolbar.AddLabelTool(CMD_DELETE_ENTRY, _("Delete"), wx.Bitmap("/home/mbertens/python/Icons/delete.ico", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "", _("Delete bouquest / entry"))
        self.frame_2_toolbar.AddSeparator()
        self.frame_2_toolbar.AddLabelTool(CMD_HELP, _("Help"), wx.Bitmap("/home/mbertens/python/Icons/Help.ico", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "", _("Show help"))
        # Tool Bar end
        self.frame_2_statusbar = self.CreateStatusBar(4, 0)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_LIST_KEY_DOWN, self.keyDownService, self.services)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.clickServiceColumn, self.services)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.clickAcivateService, self.services)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.clickRightService, self.services)
        self.Bind(wx.EVT_TEXT_ENTER, self.clickApplyFilter, self.filter)
        self.Bind(wx.EVT_BUTTON, self.clickApplyFilter, self.button_4)
        self.Bind(wx.EVT_BUTTON, self.clickClearFilter, self.button_3)
        self.Bind(wx.EVT_BUTTON, self.clickAddToBouquet, self.button_6)
        self.Bind(wx.EVT_BUTTON, self.clickRemoveFromBouquet, self.button_7)
        self.Bind(wx.EVT_CHOICE, self.clickMakeBouquetChoice, self.bouquet_choice)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.clickSelectBouquetEntry, self.bouquets)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.clickActivateBouquetEntry, self.bouquets)
        self.Bind(wx.EVT_TREE_KEY_DOWN, self.keyDownBouquetEntry, self.bouquets)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.endLabelEdit, self.bouquets)
        self.Bind(wx.EVT_BUTTON, self.clickMoveEntryUp, self.button_8)
        self.Bind(wx.EVT_BUTTON, self.clickMoveEntryDown, self.button_9)
        self.Bind(wx.EVT_MENU, self.clickMenuOpenReceiver, id=CMD_OPEN_RECEIVER)
        self.Bind(wx.EVT_MENU, self.clickMenuOpenFolder, id=CMD_OPEN_LOCATION)
        self.Bind(wx.EVT_MENU, self.clickMenuSave, id=CMD_SAVE)
        self.Bind(wx.EVT_MENU, self.clickMenuSaveAsReceiver, id=CMD_SAVEAS_RECEIVER)
        self.Bind(wx.EVT_MENU, self.clickMenuSaveAsFolder, id=CMD_SAVEAS_LOCATION)
        self.Bind(wx.EVT_MENU, self.clickMenuClose, id=CMD_CLOSE)
        self.Bind(wx.EVT_MENU, self.clickMenuPrint, id=CMD_PRINT)
        self.Bind(wx.EVT_MENU, self.clickMenuPrintSetup, id=CMD_PRINT_SETUP)
        self.Bind(wx.EVT_MENU, self.clickMenuExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.clickMenuPreferences, id=CMD_PREFERENCES)
        self.Bind(wx.EVT_MENU, self.clickMenuHelp, id=CMD_HELP)
        self.Bind(wx.EVT_MENU, self.clickMenuAbout, id=CMD_ABOUT)
        self.Bind(wx.EVT_TOOL, self.clickMenuOpenFolder, id=CMD_OPEN_LOCATION)
        self.Bind(wx.EVT_TOOL, self.clickMenuOpenReceiver, id=CMD_OPEN_RECEIVER)
        self.Bind(wx.EVT_TOOL, self.clickMenuSave, id=CMD_SAVE)
        self.Bind(wx.EVT_TOOL, self.clickMenuNewEntry, id=CMD_NEW_ENTRY)
        self.Bind(wx.EVT_TOOL, self.clickMenuDeleteEntry, id=CMD_DELETE_ENTRY)
        self.Bind(wx.EVT_TOOL, self.clickMenuHelp, id=CMD_HELP)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: BouquetEditMainWnd.__set_properties
        self.SetTitle(_("TuxBox - bouquet  editor"))
        self.button_6.SetMinSize((32, 32))
        self.button_7.SetMinSize((32, 32))
        self.button_8.SetMinSize((32, 32))
        self.button_9.SetMinSize((32, 32))
        self.window_1.SetMinSize((982, 742))
        self.frame_2_toolbar.Realize()
        self.frame_2_statusbar.SetStatusWidths([-1, 150, 150, 100])
        # statusbar fields
        frame_2_statusbar_fields = ["", "", _("Idle"), _("Modified")]
        for i in range(len(frame_2_statusbar_fields)):
            self.frame_2_statusbar.SetStatusText(frame_2_statusbar_fields[i], i)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: BouquetEditMainWnd.__do_layout
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_3 = wx.FlexGridSizer(4, 1, 20, 20)
        sizer_9 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_2 = wx.FlexGridSizer(4, 1, 20, 20)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(1, 3, 0, 10)
        sizer_6.Add(self.services, 1, wx.EXPAND | wx.FIXED_MINSIZE, 0)
        grid_sizer_1.Add(self.filter, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(self.button_4, 0, 0, 0)
        grid_sizer_1.Add(self.button_3, 0, 0, 0)
        grid_sizer_1.AddGrowableCol(0)
        sizer_6.Add(grid_sizer_1, 0, wx.EXPAND, 0)
        self.window_1_pane_1.SetSizer(sizer_6)
        grid_sizer_2.Add((20, 20), 0, 0, 0)
        grid_sizer_2.Add(self.button_6, 0, 0, 0)
        grid_sizer_2.Add(self.button_7, 0, 0, 0)
        grid_sizer_2.Add((20, 20), 0, 0, 0)
        grid_sizer_2.AddGrowableRow(0)
        grid_sizer_2.AddGrowableRow(3)
        sizer_8.Add(grid_sizer_2, 0, wx.EXPAND, 0)
        sizer_9.Add(self.bouquet_choice, 0, wx.EXPAND, 0)
        sizer_9.Add(self.bouquets, 1, wx.EXPAND | wx.FIXED_MINSIZE, 0)
        sizer_8.Add(sizer_9, 1, wx.EXPAND, 0)
        grid_sizer_3.Add((20, 20), 0, 0, 0)
        grid_sizer_3.Add(self.button_8, 0, 0, 0)
        grid_sizer_3.Add(self.button_9, 0, 0, 0)
        grid_sizer_3.Add((20, 20), 0, 0, 0)
        grid_sizer_3.AddGrowableRow(0)
        grid_sizer_3.AddGrowableRow(3)
        sizer_8.Add(grid_sizer_3, 0, wx.EXPAND, 0)
        self.window_1_pane_2.SetSizer(sizer_8)
        self.window_1.SplitVertically(self.window_1_pane_1, self.window_1_pane_2)
        sizer_5.Add(self.window_1, 1, wx.EXPAND | wx.FIXED_MINSIZE, 0)
        self.SetSizer(sizer_5)
        sizer_5.Fit(self)
        self.Layout()
        # end wxGlade

    def keyDownService(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'keyDownService' not implemented!"
        event.Skip()

    def clickServiceColumn(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickServiceColumn' not implemented!"
        event.Skip()

    def clickAcivateService(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickAcivateService' not implemented!"
        event.Skip()

    def clickRightService(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickRightService' not implemented!"
        event.Skip()

    def clickApplyFilter(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickApplyFilter' not implemented!"
        event.Skip()

    def clickClearFilter(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickClearFilter' not implemented!"
        event.Skip()

    def clickAddToBouquet(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickAddToBouquet' not implemented!"
        event.Skip()

    def clickRemoveFromBouquet(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickRemoveFromBouquet' not implemented!"
        event.Skip()

    def clickMakeBouquetChoice(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMakeBouquetChoice' not implemented!"
        event.Skip()

    def clickSelectBouquetEntry(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickSelectBouquetEntry' not implemented!"
        event.Skip()

    def clickActivateBouquetEntry(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickActivateBouquetEntry' not implemented!"
        event.Skip()

    def keyDownBouquetEntry(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'keyDownBouquetEntry' not implemented!"
        event.Skip()

    def endLabelEdit(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'endLabelEdit' not implemented!"
        event.Skip()

    def clickMoveEntryUp(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMoveEntryUp' not implemented!"
        event.Skip()

    def clickMoveEntryDown(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMoveEntryDown' not implemented!"
        event.Skip()

    def clickMenuOpenReceiver(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMenuOpenReceiver' not implemented!"
        event.Skip()

    def clickMenuOpenFolder(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMenuOpenFolder' not implemented!"
        event.Skip()

    def clickMenuSave(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMenuSave' not implemented!"
        event.Skip()

    def clickMenuSaveAsReceiver(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMenuSaveAsReceiver' not implemented!"
        event.Skip()

    def clickMenuSaveAsFolder(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMenuSaveAsFolder' not implemented!"
        event.Skip()

    def clickMenuClose(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMenuClose' not implemented!"
        event.Skip()

    def clickMenuPrint(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMenuPrint' not implemented!"
        event.Skip()

    def clickMenuPrintSetup(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMenuPrintSetup' not implemented!"
        event.Skip()

    def clickMenuExit(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMenuExit' not implemented!"
        event.Skip()

    def clickMenuPreferences(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMenuPreferences' not implemented!"
        event.Skip()

    def clickMenuHelp(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMenuHelp' not implemented!"
        event.Skip()

    def clickMenuAbout(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMenuAbout' not implemented!"
        event.Skip()

    def clickMenuNewEntry(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMenuNewEntry' not implemented!"
        event.Skip()

    def clickMenuDeleteEntry(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMenuDeleteEntry' not implemented!"
        event.Skip()

# end of class BouquetEditMainWnd

class Preferences(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: Preferences.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        self.notebook_2 = wx.Notebook(self, wx.ID_ANY, style=0)
        self.notebook_2_pane_1 = wx.Panel(self.notebook_2, wx.ID_ANY)
        self.receivers = EditableListCtrl(self.notebook_2_pane_1, wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.label_1 = wx.StaticText(self.notebook_2_pane_1, wx.ID_ANY, _("Hostname"))
        self.label_2 = wx.StaticText(self.notebook_2_pane_1, wx.ID_ANY, _("Username"))
        self.label_3 = wx.StaticText(self.notebook_2_pane_1, wx.ID_ANY, _("Password"))
        self.hostname = wx.TextCtrl(self.notebook_2_pane_1, wx.ID_ANY, _("ftp://dm7020hd/etc/enigma2"))
        self.username = wx.TextCtrl(self.notebook_2_pane_1, wx.ID_ANY, _("root"))
        self.password = wx.TextCtrl(self.notebook_2_pane_1, wx.ID_ANY, _("5701mb"), style=wx.TE_PASSWORD)
        self.button_10 = wx.Button(self.notebook_2_pane_1, wx.ID_ANY, _("Add"))
        self.autoload = wx.CheckBox(self.notebook_2_pane_1, wx.ID_ANY, _("Auto load receiver"))
        self.button_16 = wx.Button(self.notebook_2_pane_1, wx.ID_ANY, _("Save"))
        self.button_15 = wx.Button(self.notebook_2_pane_1, wx.ID_ANY, _("Cancel"))
        self.notebook_2_pane_2 = wx.Panel(self.notebook_2, wx.ID_ANY)
        self.hideEmptyServices = wx.CheckBox(self.notebook_2_pane_2, wx.ID_ANY, _("Hide empty services"))
        self.hideDotServices = wx.CheckBox(self.notebook_2_pane_2, wx.ID_ANY, _("Hide services with only '.'"))
        self.panel_1 = wx.Panel(self.notebook_2_pane_2, wx.ID_ANY)
        self.notebook_2_pane_3 = wx.Panel(self.notebook_2, wx.ID_ANY)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.clickReceiverSelected, self.receivers)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.clickReceiverAcivated, self.receivers)
        self.Bind(wx.EVT_LIST_KEY_DOWN, self.keyDownReceiver, self.receivers)
        self.Bind(wx.EVT_BUTTON, self.clickAddHost, self.button_10)
        self.Bind(wx.EVT_BUTTON, self.clickSave, self.button_16)
        self.Bind(wx.EVT_BUTTON, self.clickCancel, self.button_15)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: Preferences.__set_properties
        self.SetTitle(_("Preferences"))
        self.username.SetMinSize((150, 25))
        self.password.SetMinSize((150, 25))
        self.hideEmptyServices.SetValue(1)
        self.hideDotServices.SetValue(1)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: Preferences.__do_layout
        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_5 = wx.FlexGridSizer(10, 1, 0, 0)
        sizer_11 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_9 = wx.FlexGridSizer(2, 4, 10, 10)
        grid_sizer_4 = wx.FlexGridSizer(2, 4, 0, 20)
        sizer_11.Add(self.receivers, 1, wx.EXPAND, 0)
        grid_sizer_4.Add(self.label_1, 0, 0, 0)
        grid_sizer_4.Add(self.label_2, 0, 0, 0)
        grid_sizer_4.Add(self.label_3, 0, 0, 0)
        grid_sizer_4.Add((20, 20), 0, 0, 0)
        grid_sizer_4.Add(self.hostname, 0, wx.EXPAND, 0)
        grid_sizer_4.Add(self.username, 0, 0, 0)
        grid_sizer_4.Add(self.password, 0, 0, 0)
        grid_sizer_4.Add(self.button_10, 0, 0, 0)
        grid_sizer_4.AddGrowableCol(0)
        sizer_11.Add(grid_sizer_4, 0, wx.EXPAND, 0)
        grid_sizer_9.Add(self.autoload, 0, 0, 0)
        grid_sizer_9.Add((10, 10), 0, 0, 0)
        grid_sizer_9.Add((10, 10), 0, 0, 0)
        grid_sizer_9.Add((10, 10), 0, 0, 0)
        grid_sizer_9.Add((20, 20), 0, 0, 0)
        grid_sizer_9.Add(self.button_16, 0, 0, 0)
        grid_sizer_9.Add(self.button_15, 0, 0, 0)
        grid_sizer_9.Add((10, 40), 0, 0, 0)
        grid_sizer_9.AddGrowableCol(0)
        sizer_11.Add(grid_sizer_9, 0, wx.EXPAND, 0)
        self.notebook_2_pane_1.SetSizer(sizer_11)
        grid_sizer_5.Add(self.hideEmptyServices, 0, 0, 0)
        grid_sizer_5.Add(self.hideDotServices, 0, 0, 0)
        sizer_12.Add(grid_sizer_5, 1, wx.EXPAND, 0)
        sizer_12.Add(self.panel_1, 1, wx.EXPAND, 0)
        self.notebook_2_pane_2.SetSizer(sizer_12)
        self.notebook_2.AddPage(self.notebook_2_pane_1, _("Receivers"))
        self.notebook_2.AddPage(self.notebook_2_pane_2, _("Services"))
        self.notebook_2.AddPage(self.notebook_2_pane_3, _("Bouquets"))
        sizer_10.Add(self.notebook_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_10)
        sizer_10.Fit(self)
        self.Layout()
        # end wxGlade

    def clickReceiverSelected(self, event):  # wxGlade: Preferences.<event_handler>
        print "Event handler 'clickReceiverSelected' not implemented!"
        event.Skip()

    def clickReceiverAcivated(self, event):  # wxGlade: Preferences.<event_handler>
        print "Event handler 'clickReceiverAcivated' not implemented!"
        event.Skip()

    def keyDownReceiver(self, event):  # wxGlade: Preferences.<event_handler>
        print "Event handler 'keyDownReceiver' not implemented!"
        event.Skip()

    def clickAddHost(self, event):  # wxGlade: Preferences.<event_handler>
        print "Event handler 'clickAddHost' not implemented!"
        event.Skip()

    def clickSave(self, event):  # wxGlade: Preferences.<event_handler>
        print "Event handler 'clickSave' not implemented!"
        event.Skip()

    def clickCancel(self, event):  # wxGlade: Preferences.<event_handler>
        print "Event handler 'clickCancel' not implemented!"
        event.Skip()

# end of class Preferences

class OpenReceiver(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: OpenReceiver.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.label_4 = wx.StaticText(self, wx.ID_ANY, _("Hostname"))
        self.hostname = wx.TextCtrl(self, wx.ID_ANY, _("ftp://dm7020hd/etc/enigma2"))
        self.label_5 = wx.StaticText(self, wx.ID_ANY, _("Username"))
        self.username = wx.TextCtrl(self, wx.ID_ANY, "")
        self.label_6 = wx.StaticText(self, wx.ID_ANY, _("Password"))
        self.password = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PASSWORD)
        self.saveInPreferences = wx.CheckBox(self, wx.ID_ANY, _("Save in Preferences"))
        self.button_12 = wx.Button(self, wx.ID_ANY, _("Open"))
        self.button_11 = wx.Button(self, wx.ID_ANY, _("Cancel"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.clickOpen, self.button_12)
        self.Bind(wx.EVT_BUTTON, self.clickCancel, self.button_11)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: OpenReceiver.__set_properties
        self.SetTitle(_("Open receiver"))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: OpenReceiver.__do_layout
        grid_sizer_6 = wx.FlexGridSizer(6, 2, 5, 20)
        grid_sizer_7 = wx.FlexGridSizer(1, 3, 0, 20)
        grid_sizer_6.Add(self.label_4, 0, 0, 0)
        grid_sizer_6.Add(self.hostname, 0, wx.EXPAND, 0)
        grid_sizer_6.Add(self.label_5, 0, 0, 0)
        grid_sizer_6.Add(self.username, 0, wx.EXPAND, 0)
        grid_sizer_6.Add(self.label_6, 0, 0, 0)
        grid_sizer_6.Add(self.password, 0, wx.EXPAND, 0)
        grid_sizer_6.Add((20, 20), 0, 0, 0)
        grid_sizer_6.Add(self.saveInPreferences, 0, wx.ALL, 1)
        grid_sizer_6.Add((20, 20), 0, 0, 0)
        grid_sizer_7.Add((20, 20), 0, 0, 0)
        grid_sizer_7.Add(self.button_12, 0, 0, 0)
        grid_sizer_7.Add(self.button_11, 0, 0, 0)
        grid_sizer_7.AddGrowableCol(0)
        grid_sizer_6.Add(grid_sizer_7, 1, wx.EXPAND, 0)
        grid_sizer_6.Add((20, 20), 0, 0, 0)
        grid_sizer_6.Add((20, 20), 0, 0, 0)
        self.SetSizer(grid_sizer_6)
        grid_sizer_6.Fit(self)
        grid_sizer_6.AddGrowableCol(1)
        self.Layout()
        # end wxGlade

    def clickOpen(self, event):  # wxGlade: OpenReceiver.<event_handler>
        print "Event handler 'clickOpen' not implemented!"
        event.Skip()

    def clickCancel(self, event):  # wxGlade: OpenReceiver.<event_handler>
        print "Event handler 'clickCancel' not implemented!"
        event.Skip()

# end of class OpenReceiver

class AboutWnd(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: AboutWnd.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.label_7 = wx.StaticText(self, wx.ID_ANY, _("TUXBOX Bouquet editor"))
        self.label_8 = wx.StaticText(self, wx.ID_ANY, _("version: 1.0.0"))
        self.label_9 = wx.StaticText(self, wx.ID_ANY, _("Author: Marc Bertens"))
        self.label_10 = wx.StaticText(self, wx.ID_ANY, _("email: pe2mbs@pe2mbs.nl"))
        self.label_11 = wx.StaticText(self, wx.ID_ANY, _("Libraries: wxWidgets"))
        self.button_13 = wx.Button(self, wx.ID_ANY, _("Close"))

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: AboutWnd.__set_properties
        self.SetTitle(_("About"))
        self.SetSize((400, 220))
        self.label_7.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))
        self.button_13.SetFocus()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: AboutWnd.__do_layout
        grid_sizer_8 = wx.FlexGridSizer(10, 1, 0, 0)
        grid_sizer_8.Add((10, 10), 0, 0, 0)
        grid_sizer_8.Add(self.label_7, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        grid_sizer_8.Add(self.label_8, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        grid_sizer_8.Add((20, 20), 0, 0, 0)
        grid_sizer_8.Add(self.label_9, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        grid_sizer_8.Add(self.label_10, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        grid_sizer_8.Add(self.label_11, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        grid_sizer_8.Add((20, 20), 0, 0, 0)
        grid_sizer_8.Add((20, 20), 0, 0, 0)
        grid_sizer_8.Add(self.button_13, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.SetSizer(grid_sizer_8)
        grid_sizer_8.AddGrowableCol(0)
        self.Layout()
        # end wxGlade

# end of class AboutWnd
if __name__ == "__main__":
    gettext.install("app") # replace with the appropriate catalog name

    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = (None, wx.ID_ANY, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()