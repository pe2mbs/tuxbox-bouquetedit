import wx
from lxml import etree
# begin wxGlade: dependencies
import gettext
# end wxGlade
import gui

__author__ = 'mbertens'

class Preferences( gui.Preferences ):
    HOSTNAME_COLUMN = 0
    PROTOCOL_COLUMN = 1
    PATH_COLUMN     = 2
    USERNAME_COLUMN = 3
    PASSWORD_COLUMN = 4
    CHECKBOX_COLUMN = 5
    def __init__( self, parent, *args, **kwds ):
        gui.Preferences.__init__( self, *args, **kwds )
        self.__parent = parent
        self.Config = parent.Config
        self.receivers.SetSize( ( 777, 337 ) )
        self.receivers.InsertColumn(   self.HOSTNAME_COLUMN, _('Hostname') )
        self.receivers.InsertColumn(   self.PROTOCOL_COLUMN, _('Protocol') )
        self.receivers.InsertColumn(   self.PATH_COLUMN, _('Path') )
        self.receivers.InsertColumn(   self.USERNAME_COLUMN, _('Username') )
        self.receivers.InsertColumn(   self.PASSWORD_COLUMN, _('Password') )
        self.receivers.InsertColumn(   self.CHECKBOX_COLUMN, _('Auto load') )
        self.receivers.SetColumnWidth( self.CHECKBOX_COLUMN, 77 )

        def password_setter( this, editor, row, col ):
            print( "password_setter( %s, %s, %i, %i )" % ( this, editor, row, col ) )
            item = self.receivers.GetItem( row, col )
            element = self.receivers.GetPyData( item )
            print( "password_setter.value: %s" % ( element.text ) )
            editor.SetValue( element.text )
            editor.SetSelection( -1, -1 )
            return
        # end def

        def password_getter( this, editor, row, col ):
            print( "password_getter( %s, %s, %i, %i )" % ( this, editor, row, col ) )
            item = self.receivers.GetItem( row, col )
            element = self.receivers.GetPyData( item )
            element.text = editor.GetValue()
            print( "password_getter.value: %s" % ( element.text ) )
            return "*" * len( item.GetText() )
        # end def

        def choice_setter( this, editor, row, col ):
            print( "choice_setter( %s, %s, %i, %i )" % ( this, editor, row, col ) )
            item = self.receivers.GetItem( row, col )
            print( 'choice_setter (%s): %s' % ( editor, item.GetText() ) )
            editor.SetSelection( editor.FindString( item.GetText() ) )
            return
        # end def

        def choice_getter( this, editor, row, col ):
            print( "choice_getter( %s, %s, %i, %i )" % ( this, editor, row, col ) )
            item = self.receivers.GetItem( row, col )
            text = editor.GetString( editor.GetCurrentSelection() )
            print( 'choice_getter (%s): %s' % ( editor, text ) )
            element = this.GetPyData( item )
            element.text = text
            return text
        # end def

        self.ProtocolSelectListBox = None
        def choice_binder( this, editor ):
            editor.Bind( wx.EVT_CHOICE, self.OnProtocolSelectListBox )
            self.ProtocolSelectListBox = editor
            return
        # end def

        def autoload_setter( this, editor, row, col ):
            return
        # end def

        def autoload_getter( this, editor, row, col ):
            return ''
        # end def

        self.receivers.SetColumnEditor( self.PROTOCOL_COLUMN,
                                        wx.ComboBox,
                                        choice_binder,
                                        choice_setter,
                                        choice_getter,
                                        id = wx.ID_ANY,
                                        choices = [ _("FTP"), _("SFTP") ],
                                        style = wx.CB_DROPDOWN )

        self.receivers.SetColumnEditor( self.PASSWORD_COLUMN,
                                        wx.TextCtrl,
                                        None,
                                        password_setter,
                                        password_getter,
                                        id = wx.ID_ANY, style = wx.TE_PASSWORD )

        self.receivers.SetColumnEditor( self.CHECKBOX_COLUMN,
                                        wx.CheckBox,
                                        None,
                                        autoload_setter,
                                        autoload_getter,
                                        id = wx.ID_ANY )
        # setup language choices
        languages = self.__parent.SupportedLanguages()
        for lang in languages:
            lang = languages[ lang ]
            idx = self.languages.Append( lang[ 'info' ].Description, lang[ 'info' ] )
        # next
        self.load()
        self.sizeColumns()
        # self.receivers.setCheckboxColumn( self.CHECKBOX_COLUMN, self.OnCheckBoxColumn )
        return
    # end def

    def sizeColumns( self ):
        self.receivers.SetColumnWidth( self.HOSTNAME_COLUMN, 150 )
        self.receivers.SetColumnWidth( self.PATH_COLUMN, 150 )
        self.receivers.SetColumnWidth( self.PROTOCOL_COLUMN, 100 )
        self.receivers.SetColumnWidth( self.USERNAME_COLUMN, 150 )
        self.receivers.SetColumnWidth( self.PASSWORD_COLUMN, 150 )
        self.receivers.SetColumnWidth( self.CHECKBOX_COLUMN, 80 )
        size = ( sum( [ self.receivers.GetColumnWidth( i ) for i in ( 0, 1, 2, 3, 4, 5 ) ] ), -1 )
        self.receivers.SetSize( size )
        self.receivers.SetMinSize( size )
        self.receivers.Update()
        return
    # end def

    def OnProtocolSelectListBox( self, event ):
        self.ProtocolSelectListBox.SetSelection( event.GetInt() )
        return
    # end def

    def load( self ):
        self.receivers.DeleteAllItems()
        row = self.receivers.GetItemCount()
        items = self.Config.get_x_path( '/config/Preferences/wxListCtrl[@name="receivers"]/wxListItem' )
        for xml_item in items:
            self.receivers.InsertStringItem( row, xml_item.attrib[ 'text' ] )
            self.receivers.SetPyData( self.receivers.GetItem( row, 0 ), xml_item )
            for element in xml_item:
                id = int( element.attrib[ 'id' ] )
                if id == self.PASSWORD_COLUMN:
                    self.receivers.SetStringItem( row, id, "*" * len( element.text ) )
                else:
                    self.receivers.SetStringItem( row, id, element.text )
                # end if
                self.receivers.SetPyData( self.receivers.GetItem( row, id ), element )
            # next
            litem = wx.ListItem()
            litem.SetMask( litem.GetMask( ) | wx.LIST_MASK_IMAGE )
            litem.SetColumn( self.CHECKBOX_COLUMN )
            litem.SetId( row )
            litem.SetImage( self.receivers.IMG_CHECKED_BOX if xml_item.attrib[ 'autoload' ] == 'True' else self.receivers.IMG_UNCHECKED_BOX )
            self.receivers.SetItem( litem )
            self.receivers.SetPyData( litem, xml_item )
            row += 1
        # next
        checkbox = self.Config.get_x_path( '/config/Preferences/wxCheckBox[@name="hideEmptyServices"]', False )
        if checkbox is not None:
            self.hideEmptyServices.Value = bool( checkbox.text )
        # end if
        checkbox = self.Config.get_x_path( '/config/Preferences/wxCheckBox[@name="hideDotServices"]', False )
        if checkbox is not None:
            self.hideDotServices.Value = bool( checkbox.text )
        # end if
        choice = self.Config.get_x_path( '/config/Preferences/wxChoice[@name="language"]', False )
        if choice is not None:
            try:
                # print( "Set language: %s" % ( choice.text ) )
                for idx in range( self.languages.GetCount() ):
                    info = self.languages.GetClientData( idx )
                    if info.CanonicalName == choice.text:
                        # print( "Set language index: %i" % ( idx ) )
                        self.languages.SetSelection( idx )
                    # end if
                # next
            except:
                print( "Could not set language: %s" % ( choice.text ) )
                pass
            # end try
        else:
            # Here we set de default
            pass
        # end if
        # TODO: Fix loading all settings

        return
    # end def


    def save( self ):
        num_items = self.receivers.GetItemCount()
        receivers = self.Config.get_x_path( '/config/Preferences/wxListCtrl[@name="receivers"]', False )
        for idx in range( num_items ):
            hItem   = self.receivers.GetItem( idx, 0 )
            item    = self.receivers.GetPyData( hItem )
            if item is not None:
                # Handle existing entry
                item.attrib[ 'text' ] = hItem.GetText()
                cItem = self.receivers.GetItem( idx, self.CHECKBOX_COLUMN )
                item.attrib[ 'autoload' ] = "True" if cItem.GetImage() == self.receivers.IMG_CHECKED_BOX else "False"
                for element in item:
                    id = int( element.attrib[ 'id' ] )
                    lItem = self.receivers.GetItem( idx, id )
                    if id != self.PASSWORD_COLUMN: # for the password column the data is already in the xml element
                        element.text = lItem.Text
                    # end if
                # next
            else:
                # Handle NEW entry
                child = etree.SubElement( receivers, "wxListItem" )
                self.receivers.SetPyData( hItem )
                child.attrib[ 'text' ] = hItem.GetText()
                cItem = self.receivers.GetItem( idx, self.CHECKBOX_COLUMN )
                child.attrib[ 'autoload' ] = "True" if cItem.GetImage() == self.receivers.IMG_CHECKED_BOX else "False"
                for col in range( self.PATH_COLUMN, self.CHECKBOX_COLUMN ):
                    child1 = etree.SubElement( child, "Column" )
                    child1.attrib[ 'id' ] = str( col )
                    lItem = self.receivers.GetItem( idx, col )
                    if col != self.PASSWORD_COLUMN: # for the password column the data is already in the xml element
                        child1.text = lItem.Text
                    else:
                        element = self.receivers.GetPyData( self.receivers.GetItem( idx, id ) )
                        child1.text = element.text
                    # end if
                # next
            # end if
        # next
        checkbox = self.Config.get_x_path( '/config/Preferences/wxCheckBox[@name="hideEmptyServices"]', False )
        if checkbox is not None:
            checkbox.text = str( self.hideEmptyServices.Value )
        # end if
        checkbox = self.Config.get_x_path( '/config/Preferences/wxCheckBox[@name="hideDotServices"]', False )
        if checkbox is not None:
            checkbox.text = str( self.hideDotServices.Value )
        # end if
        choice = self.Config.get_x_path( '/config/Preferences/wxChoice[@name="language"]', False )
        if choice is not None:
            info = self.languages.GetClientData( self.languages.GetSelection() )
            choice.text = info.CanonicalName
        # end if
        # TODO: Fix saveing all settings
        self.Config.save()
        return
    # end def

    def __clearCheckboxes( self ):
        num_items = self.receivers.GetItemCount()
        for idx in range( num_items ):
            cItem = self.receivers.GetItem( idx, self.CHECKBOX_COLUMN )
            cItem.SetMask( cItem.GetMask( ) | wx.LIST_MASK_IMAGE )
            cItem.SetImage( self.receivers.IMG_UNCHECKED_BOX )
            self.receivers.SetItem( cItem )
        # next
        return
    # end def

    def OnCheckBoxColumn( self, item ):
        self.__clearCheckboxes()
        item.SetImage( self.receivers.IMG_CHECKED_BOX )
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


        self.receivers.SetStringItem( num_items, self.PROTOCOL_COLUMN, self.protocol.GetItems()[ self.protocol.GetSelection() ] )
        self.receivers.SetStringItem( num_items, self.PATH_COLUMN, self.path.Value )
        self.receivers.SetStringItem( num_items, self.USERNAME_COLUMN, self.username.Value )
        self.receivers.SetStringItem( num_items, self.PASSWORD_COLUMN, "*" * len( self.password.Value ) )
        litem = wx.ListItem()
        litem.SetMask( litem.GetMask( ) | wx.LIST_MASK_IMAGE )
        litem.SetColumn( self.CHECKBOX_COLUMN )
        litem.SetId( num_items )
        litem.SetImage( self.receivers.IMG_CHECKED_BOX if self.autoload.Value else self.receivers.IMG_UNCHECKED_BOX )
        self.receivers.SetItem( litem )
        # Mark new element
        self.receivers.SetPyData( litem, None )
        passwd = etree.Element( 'password' )
        passwd.text = self.password.Value
        self.receivers.SetPyData( self.receivers.GetItem( num_items,
                                                          self.PASSWORD_COLUMN ),
                                  passwd )
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
