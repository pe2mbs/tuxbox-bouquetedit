import sys
import wx
from lxml import etree
# begin wxGlade: dependencies
import gettext
# end wxGlade
import bouquetedit.gui

__author__ = 'mbertens'

class Preferences( bouquetedit.gui.Preferences ):
    CHECKBOX_COLUMN = 3
    def __init__(self, config, *args, **kwds):
        bouquetedit.gui.Preferences.__init__( self, *args, **kwds )
        self.Config = config
        self.receivers.SetSize( ( 777, 337 ) )
        self.receivers.InsertColumn( 0, 'Hostname' )
        self.receivers.SetColumnWidth( 0, 400 )
        self.receivers.InsertColumn( 1, 'Username' )
        self.receivers.SetColumnWidth( 1, 150 )
        self.receivers.InsertColumn( 2, 'Password' )
        self.receivers.SetColumnWidth( 2, 150 )
        self.receivers.InsertColumn( self.CHECKBOX_COLUMN, 'Auto load' )
        self.receivers.SetColumnWidth( self.CHECKBOX_COLUMN, 77 )
        self.load()
        self.sizeColumns()
        self.receivers.setCheckboxColumn( self.CHECKBOX_COLUMN, self.OnCheckBoxColumn )
        return
    # end def

    def sizeColumns( self ):
        self.receivers.SetColumnWidth( 0, 400 )
        self.receivers.SetColumnWidth( 1, 150 )
        self.receivers.SetColumnWidth( 2, 150 )
        self.receivers.SetColumnWidth( self.CHECKBOX_COLUMN, 80 )
        size = ( sum( [ self.receivers.GetColumnWidth( i ) for i in ( 0, 1, 2 ) ] ), -1 )
        self.receivers.SetSize( size )
        self.receivers.SetMinSize( size )
        self.receivers.Update()
        return
    # end def

    def load( self ):
        self.receivers.DeleteAllItems()
        num_items = self.receivers.GetItemCount()
        items = self.Config.get_x_path( '/config/Preferences/wxListCtrl[@name="receivers"]/wxListItem' )
        for item in items:

            self.receivers.InsertStringItem( num_items, item.attrib[ 'text' ] )
            for element in item:
                id = int( element.attrib[ 'id' ] )
                if id < 3 and element.text:
                    self.receivers.SetStringItem( num_items, id, element.text )
                # end if
            # next
            litem = wx.ListItem()
            litem.SetMask( litem.GetMask( ) | wx.LIST_MASK_IMAGE )
            litem.SetColumn( self.CHECKBOX_COLUMN )
            litem.SetId( num_items )
            litem.SetImage( self.receivers.IMG_CHECKED_BOX if item.attrib[ 'autoload' ] == 'True' else self.receivers.IMG_UNCHECKED_BOX )
            self.receivers.SetItem( litem )
            self.receivers.SetPyData( num_items, item )
            num_items += 1
        # next
        return
    # end def


    def save( self ):
        num_items = self.receivers.GetItemCount()
        receivers = self.Config.get_x_path( '/config/Preferences/wxListCtrl[@name="receivers"]', False )
        for idx in range( num_items ):
            item = self.receivers.GetPyData( idx )
            if item is not None:
                # Handle existing entry
                item.attrib[ 'text' ] = self.receivers.GetItemText( idx )
                cItem = self.receivers.GetItem( idx, self.CHECKBOX_COLUMN )
                item.attrib[ 'autoload' ] = "True" if cItem.GetImage() == self.receivers.IMG_CHECKED_BOX else "False"
                for element in item:
                    id = int( element.attrib[ 'id' ] )
                    lItem = self.receivers.GetItem( idx, id )
                    element.text = lItem.Text
                # next
            else:
                # Handle NEW entry
                child = etree.SubElement( receivers, "wxListItem" )
                self.receivers.SetPyData( idx, child )
                child.attrib[ 'text' ] = self.receivers.GetItemText( idx )
                cItem = self.receivers.GetItem( idx, self.CHECKBOX_COLUMN )
                child.attrib[ 'autoload' ] = "True" if cItem.GetImage() == self.receivers.IMG_CHECKED_BOX else "False"
                for col in range( 1, 3 ):
                    child1 = etree.SubElement( child, "Column" )
                    child1.attrib[ 'id' ] = str( col )
                    lItem = self.receivers.GetItem( idx, col )
                    child1.text = lItem.Text
                # next
            # end if
        # next
        self.Config.save()
        return
    # end def

    def __clearCheckboxes( self ):
        num_items = self.receivers.GetItemCount()
        for idx in range( num_items ):
            cItem = self.receivers.GetItem( idx, self.CHECKBOX_COLUMN )
            cItem.SetMask( cItem.GetMask( ) | wx.LIST_MASK_IMAGE )
            cItem.SetImage( 0 )
            self.receivers.SetItem( cItem )
        # next
        return
    # end def

    def OnCheckBoxColumn( self, item ):
        self.__clearCheckboxes()
        item.SetImage( 1 )
        item.SetMask( item.GetMask( ) | wx.LIST_MASK_IMAGE )
        self.receivers.SetItem( item )
        return
    # end def

    def clickReceiverSelected( self, event ):  # wxGlade: Preferences.<event_handler>
        return
    # end def

    def keyDownReceiver( self, event ):  # wxGlade: Preferences.<event_handler>
        if event.KeyCode == 127 and event.Index != -1:
            item = self.receivers.GetPyData( event.Index )
            if item:
                parent = item.getparent()
                parent.remove( item )
            # end if
            self.receivers.DeleteItem( event.Index )
        # end if
        return
    # end def

    def clickAddHost( self, event ):  # wxGlade: Preferences.<event_handler>
        if self.autoload.Value:
            self.__clearCheckboxes()
        # end if
        num_items = self.receivers.GetItemCount()
        self.receivers.InsertStringItem( num_items, self.hostname.Value )
        self.receivers.SetStringItem( num_items, 1, self.username.Value )
        self.receivers.SetStringItem( num_items, 2, self.password.Value )

        litem = wx.ListItem()
        litem.SetMask( litem.GetMask( ) | wx.LIST_MASK_IMAGE )
        litem.SetColumn( self.CHECKBOX_COLUMN )
        litem.SetId( num_items )
        litem.SetImage( self.receivers.IMG_CHECKED_BOX if self.autoload.Value else self.receivers.IMG_UNCHECKED_BOX )
        self.receivers.SetItem( litem )
        # Mark new element
        self.receivers.SetPyData( num_items, None )
        return
    # end def

    def clickSave( self, event ):  # wxGlade: Preferences.<event_handler>
        if self.Config is not None:
            self.save()
            self.EndModal( 0 )
        # end if
        return
    # end def

    def clickCancel( self, event ):  # wxGlade: Preferences.<event_handler>
        self.EndModal( 0 )
        return
    # end def
# end class