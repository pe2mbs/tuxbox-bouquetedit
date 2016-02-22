__author__ = 'mbertens'
import sys
import wx
import wx.lib.mixins.listctrl  as  listmix
from bisect import bisect


class MyBaseListCtrl( wx.ListCtrl,
                      listmix.ListRowHighlighter,
                      listmix.ListCtrlAutoWidthMixin ):
    images=[ 'images/squareunchecked.ico',
             'images/squarechecked.ico',
             'images/sort-down.ico',
             'images/sort-up.ico' ]
    IMG_UNCHECKED_BOX   = 0
    IMG_CHECKED_BOX     = 1
    IMG_SORT_DESCENDING = 2
    IMG_SORT_ASCENDING  = 3

    def __init__( self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0 ):
        wx.ListCtrl.__init__( self, parent, ID, pos, size, style )
        listmix.ListRowHighlighter.__init__( self )
        listmix.ListCtrlAutoWidthMixin.__init__( self )
        self.il = wx.ImageList( 16, 16, True )
        self.__checkboxColumn = -1
        self.__eventHandler = None
        self.setResizeColumn( 1 )
        self.resizeColumn( 200 )
        self.__id = -sys.maxint
        self.__map = {}
        for i in self.images:
            self.il.Add( wx.Bitmap( i ) )
        # next
        # self.SetImageList( self.il, wx.IMAGE_LIST_NORMAL )
        self.SetImageList( self.il, wx.IMAGE_LIST_SMALL )
        # self.SetImageList( self.il, wx.IMAGE_LIST_STATE )
        self.SetAutoLayout( True )
        return
    # end def

    def SetPyData( self, item, data ):
        self.__map[ self.__id ] = data
        self.SetItemData( item, self.__id )
        self.__id += 1
        return
    # end def

    def GetPyData( self, item ):
        id = self.GetItemData( item )
        print( 'GetPyData().id = %i' % ( id ) )
        if id != 0:
            return self.__map[ id ]
        # end if
        return None
    # end def

    def setCheckboxColumn( self, col, eventHandler ):
        if type( col ) is int:
            self.__checkboxColumn = [ col ]
        else:
            self.__checkboxColumn = col
        # end if
        self.__eventHandler = eventHandler
        return
    # end def

    def OnCheckBoxColumn( self, item ):
        self.__eventHandler( item )
        return
    # end def

    def OnLeftDown(self, evt=None):
        ''' Examine the click and double
        click events to see if a row has been click on twice. If so,
        determine the current row and columnn and open the editor.'''

        if self.editor.IsShown():
            self.CloseEditor()
        # end if
        x,y = evt.GetPosition()
        row,flags = self.HitTest((x,y))

        if row != self.curRow: # self.curRow keeps track of the current row
            evt.Skip()
            return
        # end if
        # the following should really be done in the mixin's init but
        # the wx.ListCtrl demo creates the columns after creating the
        # ListCtrl (generally not a good idea) on the other hand,
        # doing this here handles adjustable column widths

        self.col_locs = [ 0 ]
        loc = 0
        for n in range( self.GetColumnCount() ):
            loc = loc + self.GetColumnWidth( n )
            self.col_locs.append( loc )
        # next

        col = bisect(self.col_locs, x+self.GetScrollPos(wx.HORIZONTAL)) - 1
        if col in self.__checkboxColumn:
            item = self.GetItem( row, col )
            self.OnCheckBoxColumn( item )
        else:
            listmix.TextEditMixin.OnLeftDown( self, evt )
        # end if
        return
    # end def

# end class

class EditableListCtrl( MyBaseListCtrl, listmix.TextEditMixin ):
    ''' TextEditMixin allows any column to be edited. '''
    #----------------------------------------------------------------------
    def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        """Constructor"""
        MyBaseListCtrl.__init__( self, parent, ID, pos, size, style )
        listmix.TextEditMixin.__init__( self )
        self.Refresh()
        return
    # end def
# end class

class VirtualListCtrl( MyBaseListCtrl ):
    #----------------------------------------------------------------------
    def __init__( self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition,
                  size=wx.DefaultSize, style=0):
        """Constructor"""
        MyBaseListCtrl.__init__( self, parent, ID, pos, size, style )
        self.__OnGetItemText    = None
        self.__OnGetItemAttr    = None
        self.normalAttr = [ wx.ListItemAttr(), wx.ListItemAttr() ]
        self.Refresh()
        return
    # end def

    def SetHighlightColor(self, color):
        """Set the color used to highlight the rows. Call L{RefreshRows} after
        this if you wish to update all the rows highlight colors.
        @param color: wx.Color or None to set default

        """
        self._color = color
        self.normalAttr[ 1 ].SetBackgroundColour( color )
    # end def

    def VirtualItemText( self, OnGetItemText ):
        self.__OnGetItemText = OnGetItemText
        return
    # end def

    def VirtualItemAttr( self, OnGetItemAttr ):
        self.__OnGetItemAttr = OnGetItemAttr
        return
    # end def

    def OnGetItemImage( self, item ):
        return -1
    # end def

    def OnGetItemText( self, item, col ):
        if self.__OnGetItemText:
            return self.__OnGetItemText( item, col )
        # end if
        return ''
    # end def

    def OnGetItemAttr( self, row ):
        if self.__OnGetItemAttr:
            return self.__OnGetItemAttr( row )
        # end if
        return self.normalAttr[ row % 2 ]
    # end def
# end class