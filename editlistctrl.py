__author__ = 'mbertens'
import sys
import wx
import wx.lib.mixins.listctrl  as  listmix
from bisect import bisect


class TextEditExMixin:
    """
    A mixin class that enables any text in any column of a
    multi-column listctrl to be edited by clicking on the given row
    and column.  You close the text editor by hitting the ENTER key or
    clicking somewhere else on the listctrl. You switch to the next
    column by hiting TAB.

    To use the mixin you have to include it in the class definition
    and call the __init__ function::

        class TestListCtrl(wx.ListCtrl, TextEditMixin):
            def __init__(self, parent, ID, pos=wx.DefaultPosition,
                         size=wx.DefaultSize, style=0):
                wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
                TextEditMixin.__init__(self)


    Authors:     Steve Zatz, Pim Van Heuven (pim@think-wize.com)
    """

    editorBgColour = wx.Colour(255,255,175) # Yellow
    editorFgColour = wx.Colour(0,0,0)       # black

    def __init__(self):
        # editor = wx.TextCtrl(self, -1, pos=(-1,-1), size=(-1,-1),
        #                     style=wx.TE_PROCESS_ENTER|wx.TE_PROCESS_TAB \
        #                     |wx.TE_RICH2)
        # self.editor = self.make_editor()
        self.Bind( wx.EVT_TEXT_ENTER,   self.CloseEditor )
        self.Bind( wx.EVT_LEFT_DOWN,    self.OnLeftDown )
        self.Bind( wx.EVT_LEFT_DCLICK,  self.OnLeftDown )
        self.Bind( wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self )
        self.__editors = {}

        def setter_textctrl( this, control, row, col ):
            """This sets the value from the listctrl to the editor control.
            This the default wx.TextCtrl setter function

            :param this:    listctrl
            :param control: editor
            :param row:     row in the list
            :param col:     column in the list
            :return:        None
            """
            control.SetValue( this.GetItem( row, col ).GetText() )
            control.SetSelection( -1, -1 )
            return
        # end def

        def getter_textctrl( this, control, row, col ):
            """This sets the value from the editor control back to the listctrl control.
            This the default wx.TextCtrl getter function

            :param this:    listctrl
            :param control: editor
            :param row:     row in the list
            :param col:     column in the list
            :return:        the new value
            """
            this.GetItem( row, col ).SetText( control.GetValue() )
            return control.GetValue()
        # end def

        def binder_textctrl( this, control ):
            control.Bind( wx.EVT_CHAR, this.OnTextCtrlChar )
            return
        # end def
        # Set the default editor
        self.SetColumnEditor( -1, wx.TextCtrl,
                              binder_textctrl,
                              setter_textctrl,
                              getter_textctrl,
                              -1, pos=(-1,-1), size=(-1,-1) )
        return
    # end if

    def SetColumnEditor( self, col, control, binder, setter, getter, *args, **kwargs ):
        if binder is None:
            def binder_textctrl( this, control ):
                control.Bind( wx.EVT_CHAR, this.OnTextCtrlChar )
                return
            # end def
            binder = binder_textctrl
        # end def
        self.__editors[ col ] = { 'control': control,
                                  'setter': setter,
                                  'getter': getter,
                                  'binder': binder,
                                  'args': args,
                                  'kwargs': kwargs,
                                  'editor': None,
                                  'col_style': wx.LIST_FORMAT_LEFT }
        editor = self.make_editor( col, self.__editors, *args, **kwargs )
        if col == -1:
            self.editor = editor
        # end def
        return
    # end def

    def make_editor( self, col, controls, *args, **kwargs ):
        print( "make_editor( %i, %s, %s, %s )" % ( col, repr( controls ), repr( args ), repr( kwargs ) ) )
        col_style = controls[ col ][ 'col_style' ]

        style = wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB | wx.TE_RICH2
        style |= { wx.LIST_FORMAT_LEFT:     wx.TE_LEFT,
                   wx.LIST_FORMAT_RIGHT:    wx.TE_RIGHT,
                   wx.LIST_FORMAT_CENTRE :  wx.TE_CENTRE }[ col_style ]
        control = controls[ col ]
        # editor = wx.TextCtrl( self, -1, style=style )
        editor = control[ 'control' ]( self, *args, **kwargs )

        editor.SetBackgroundColour( self.editorBgColour )
        editor.SetForegroundColour( self.editorFgColour )
        font = self.GetFont()
        editor.SetFont( font )
        self.curRow = 0
        self.curCol = 0
        #print( "Hide" )
        editor.Hide()
        control[ 'editor' ]       = editor
        control[ 'col_style' ]    = col_style
        control[ 'binder' ]( self, editor )
        # editor.Bind( wx.EVT_KILL_FOCUS, self.CloseEditor )
        return editor
    # end def

    def OnItemSelected( self, event ):
        print( "OnItemSelected( %s )" % ( event ) )
        self.curRow = event.GetIndex()
        event.Skip()
        return
    # end def

    def OnTextCtrlChar( self, event ):
        ''' Catch the TAB, Shift-TAB, cursor DOWN/UP key code
            so we can open the editor at the next column (if any).'''
        print( "OnTextCtrlChar( %s )" % ( event ) )
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_TAB and event.ShiftDown():
            self.CloseEditor()
            if self.curCol-1 >= 0:
                self.OpenEditor( self.curRow, self.curCol - 1 )
            # end if
        elif keycode == wx.WXK_TAB:
            self.CloseEditor()
            if self.curCol+1 < self.GetColumnCount():
                self.OpenEditor( self.curRow, self.curCol + 1 )
            # end if
        elif keycode == wx.WXK_ESCAPE:
            self.CloseEditor()
        elif keycode == wx.WXK_DOWN:
            self.CloseEditor()
            if self.curRow + 1 < self.GetItemCount():
                self._SelectIndex( self.curRow + 1 )
                self.OpenEditor( self.curRow, self.curCol )
            # end if
        elif keycode == wx.WXK_UP:
            self.CloseEditor()
            if self.curRow > 0:
                self._SelectIndex( self.curRow - 1 )
                self.OpenEditor( self.curRow, self.curCol )
            # end if
        else:
            event.Skip()
        # end if
        return
    # end def

    def OnLeftDown( self, event = None ):
        ''' Examine the click and double
        click events to see if a row has been click on twice. If so,
        determine the current row and columnn and open the editor.'''
        print( "OnLeftDown( %s ) %s" % ( event, self.editor ) )
        if self.editor.IsShown():
            self.CloseEditor()
        # end if
        x,y = event.GetPosition()
        row,flags = self.HitTest( ( x, y ) )

        if row != self.curRow: # self.curRow keeps track of the current row
            print("skip")
            event.Skip()
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
        col = bisect( self.col_locs, x + self.GetScrollPos( wx.HORIZONTAL ) ) - 1
        self.OpenEditor( row, col )
        print("done")
        return
    # end def

    def OpenEditor( self, row, col ):
        ''' Opens an editor at the current position. '''
        print( "OpenEditor( %i, %i )" % ( row, col ) )
        # give the derived class a chance to Allow/Veto this edit.
        evt = wx.ListEvent( wx.wxEVT_COMMAND_LIST_BEGIN_LABEL_EDIT, self.GetId() )
        evt.m_itemIndex = row
        evt.m_col = col
        try:
            setter = self.__editors[ col ][ 'setter' ]
        except:
            setter = self.__editors[ -1 ][ 'setter' ]
        # end try

        item = self.GetItem( row, col )
        evt.m_item.SetId( item.GetId() )
        evt.m_item.SetColumn( item.GetColumn() )
        evt.m_item.SetData( item.GetData() )
        evt.m_item.SetText( item.GetText() )
        ret = self.GetEventHandler().ProcessEvent( evt )
        if ret and not evt.IsAllowed():
            return   # user code doesn't allow the edit.
        # end if
        # if self.GetColumn( col ).m_format != self.col_style:
        try:
            self.editor = self.__editors[ col ][ 'editor' ]
        except:
            self.editor = self.__editors[ -1 ][ 'editor' ]
        # en def
        # end if
        x0 = self.col_locs[ col ]
        x1 = self.col_locs[ col + 1 ] - x0

        scrolloffset = self.GetScrollPos( wx.HORIZONTAL )

        # scroll forward
        if x0 + x1 - scrolloffset > self.GetSize()[ 0 ]:
            if wx.Platform == "__WXMSW__":
                # don't start scrolling unless we really need to
                offset = x0 + x1 - self.GetSize()[ 0 ] - scrolloffset
                # scroll a bit more than what is minimum required
                # so we don't have to scroll everytime the user presses TAB
                # which is very tireing to the eye
                addoffset = self.GetSize()[ 0 ] / 4
                # but be careful at the end of the list
                if addoffset + scrolloffset < self.GetSize()[ 0 ]:
                    offset += addoffset
                # end if
                self.ScrollList( offset, 0 )
                scrolloffset = self.GetScrollPos( wx.HORIZONTAL )
            else:
                # Since we can not programmatically scroll the ListCtrl
                # close the editor so the user can scroll and open the editor
                # again
                setter( self, self.editor, row, col )
                self.curRow = row
                self.curCol = col
                self.CloseEditor()
                return
            # end if
        # end if
        rect = self.GetItemRect( row )
        top = rect[ 1 ]
        left = x0 - scrolloffset
        width = x1
        height = -1
        self.editor.SetDimensions( left, top,  width, height, wx.SIZE_ALLOW_MINUS_ONE )
        setter( self, self.editor, row, col )
        print("Show editor")
        self.editor.Show()
        self.editor.Raise()
        self.editor.Update()
        self.editor.SetFocus()
        self.editor.Raise()
        self.curRow = row
        self.curCol = col
        return
    # end def

    # FIXME: this function is usually called twice - second time because
    # it is binded to wx.EVT_KILL_FOCUS. Can it be avoided? (MW)
    def CloseEditor(self, event = None):
        ''' Close the editor and save the new value to the ListCtrl. '''
        print( "CloseEditor( %s )" % ( event ) )
        if not self.editor.IsShown():
            return
        # end if
        try:
            getter = self.__editors[ self.curCol ][ 'getter' ]
        except:
            getter = self.__editors[ -1 ][ 'getter' ]
        # end try

        text = getter( self, self.editor, self.curRow, self.curCol )
        print( "hide" )
        self.editor.Hide()
        self.SetFocus()

        # post wxEVT_COMMAND_LIST_END_LABEL_EDIT
        # Event can be vetoed. It doesn't has SetEditCanceled(), what would
        # require passing extra argument to CloseEditor()
        evt = wx.ListEvent( wx.wxEVT_COMMAND_LIST_END_LABEL_EDIT, self.GetId() )
        evt.m_itemIndex = self.curRow
        evt.m_col = self.curCol
        item = self.GetItem( self.curRow, self.curCol )
        evt.m_item.SetId( item.GetId() )
        evt.m_item.SetColumn( item.GetColumn() )
        evt.m_item.SetData( item.GetData() )
        evt.m_item.SetText( text )  # should be empty string if editor was canceled
        ret = self.GetEventHandler().ProcessEvent( evt )
        # print( "ret (%s): %s" % ( evt, ret ) )
        if not ret or evt.IsAllowed():
            if self.IsVirtual():
                # replace by whather you use to populate the virtual ListCtrl
                # data source
                self.SetVirtualData( self.curRow, self.curCol, text )
            else:
                self.SetStringItem( self.curRow, self.curCol, text )
            # end if
        # end if
        self.RefreshItem( self.curRow )
        return
    # end def

    def _SelectIndex( self, row ):
        print( "_SelectIndex( %i )" % ( row ) )
        listlen = self.GetItemCount()
        if row < 0 and not listlen:
            return
        # end if
        if row > ( listlen - 1 ):
            row = listlen -1
        # end if
        self.SetItemState( self.curRow, ~wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
        self.EnsureVisible( row )
        self.SetItemState( row, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED )
        return
    # end def
# end class

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
        # self.__checkboxColumn = -1
        # self.__eventHandler = None
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
        if not isinstance( item, wx.ListItem ):
            raise Exception( "Invalid type: item must be wx.ListItem" )
        # end if
        # print( "SetPyData( %s, %s ) = ( %i, %i )" % ( item, data, item.Id, item.Column ) )
        if item.Id in self.__map:
            self.__map[ item.Id ][ item.Column ] = data
        else:
            self.__map[ item.Id ] = { item.Column: data }
        # end if
        return
    # end def

    def GetPyData( self, item ):
        if not isinstance( item, wx.ListItem ):
            raise Exception( "Invalid type: item must be wx.ListItem" )
        # end if
        # print( "GetPyData( %s ) = ( %i, %i )" % ( item, item.Id, item.Column ) )
        if item.Id in self.__map:
            row = self.__map[ item.Id ]
            if item.Column in row:
                return row[ item.Column ]
            # end def
        # end if
        return None
    # end def
# end class

class EditableListCtrl( MyBaseListCtrl, TextEditExMixin ):
    ''' TextEditMixin allows any column to be edited. '''
    #----------------------------------------------------------------------
    def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        """Constructor"""
        MyBaseListCtrl.__init__( self, parent, ID, pos, size, style )
        TextEditExMixin.__init__( self )
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