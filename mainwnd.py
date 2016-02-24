import wx
import os
import subprocess
# begin wxGlade: dependencies
import gettext
# end wxGlade
import gui
import preferencies
import receiver
import aboutwmd
import config
import enigma

__author__ = 'mbertens'

class MainWnd( gui.BouquetEditMainWnd ):
    COLUMN_SERVICE_NAME             = 0
    COLUMN_SERVICE_PROVIDER         = 1
    COLUMN_SERVICE_POSITION         = 2
    COLUMN_SERVICE_FREQUENCY        = 3
    COLUMN_SERVICE_SYMBOLRATE       = 4
    COLUMN_SERVICE_NAMESPACE        = 5
    COLUMN_SERVICE_TRANSPONDER      = 6
    POPUP_MENU_ALL                  = wx.NewId()
    BOUQUET_ITEM_MARKER_INS_BEFORE  = wx.NewId()
    BOUQUET_ITEM_MARKER_INS_AFTER   = wx.NewId()
    BOUQUET_ITEM_MARKER_ADD         = wx.NewId()
    BOUQUET_ITEM_REMOVE             = wx.NewId()
    BOUQUET_ITEM_MARKER_EDIT        = wx.NewId()
    BOUQUET_EDIT                    = wx.NewId()
    BOUQUET_INS_AFTER               = wx.NewId()
    BOUQUET_INS_BEFORE              = wx.NewId()
    BOUQUET_ADD                     = wx.NewId()

    def __init__(self, *args, **kwds):
        gui.BouquetEditMainWnd.__init__( self, *args, **kwds )
        # Read the configuration of the application
        self.Config         = config.Config( 'config.xml' )
        self.COLUMNS        = []
        self.Preferences    = None
        self.bouquetMenu    = wx.Menu()
        markerMenu          = wx.Menu()
        markerMenu.Append( self.BOUQUET_ITEM_MARKER_EDIT, 'Edit' )
        markerMenu.Append( self.BOUQUET_ITEM_MARKER_INS_BEFORE, 'Insert before' )
        markerMenu.Append( self.BOUQUET_ITEM_MARKER_INS_AFTER, 'Insert after' )
        markerMenu.Append( self.BOUQUET_ITEM_MARKER_ADD, 'Add' )
        self.bouquetMenu.AppendMenu( wx.NewId(), 'Marker', markerMenu )
        createMenu          = wx.Menu()
        createMenu.Append( self.BOUQUET_EDIT, 'Edit' )
        createMenu.Append( self.BOUQUET_INS_BEFORE, 'Insert before' )
        createMenu.Append( self.BOUQUET_INS_AFTER, 'Insert after' )
        createMenu.Append( self.BOUQUET_ADD, 'Add' )
        self.bouquetMenu.AppendMenu( wx.NewId(), 'Bouquet', createMenu )
        self.bouquetMenu.AppendSeparator()
        self.bouquetMenu.Append( self.BOUQUET_ITEM_REMOVE, 'Remove' )
        self.bouquets.SetPopupMenu( self.bouquetMenu )
        self.bouquets.Bind( wx.EVT_MENU, self.PopupMenuBouquet )
        self.bouquets.SetContextMenuHandler( self.PopupUpdateMenuBouquet )
        self.listMenu       = wx.Menu()
        showMenu            = wx.Menu()
        showMenu.Append( self.POPUP_MENU_ALL, 'All' )
        showMenu.AppendSeparator()
        try:
            width, height = self.Config.get_x_path( '/config/MainWnd/wxSize', False ).text.split( ',' )
            self.Size = ( int( width ), int( height ) )
            columns = self.Config.get_x_path( '/config/MainWnd/Services/Column' )
            total_width = 20
            for column in columns:
                colnum  = int( column.attrib[ 'id' ] )
                width   = int( column.attrib[ 'width' ] )
                name    = column.attrib[ 'name' ]
                show    = column.attrib[ 'show' ] == 'True'
                newId   = wx.NewId()
                self.services.InsertColumn( colnum, name )
                if show:
                    self.services.SetColumnWidth( colnum, width )
                    total_width += width
                else:
                    self.services.SetColumnWidth( colnum, 0 )
                # end if
                item = showMenu.AppendCheckItem( newId, name )
                item.Check( show )
                self.COLUMNS.append( ( colnum, name, width, newId ) )
            # next
            self.window_1.SashPosition = total_width
        except Exception, exc:
            print( "Setup services: %s" % ( exc ) )
        # end try
        self.services.Bind( wx.EVT_MENU, self.PopupMenuServices )
        self.Bind( wx.EVT_CLOSE, self.OnClose )
        self.listMenu.AppendMenu( wx.NewId(), 'Show/Hide Columns', showMenu )

        self.services.VirtualItemText( self.OnGetItemText )
        self.services.SetHighlightColor( 'yellow' )
        self.engima = enigma.Enigma2()
        self.__reverse = False
        self.__sortColumn = -1
        self.__items = []
        self.__filterEmptyTransponder   = True
        self.__filterDotTransponder     = True
        self.mplayer_process    = None
        try:
            self.__filterEmptyTransponder   = self.Config.get_x_path( '/config/Preferences/wxCheckBox[@name="hideEmptyServices"]', False ).text == 'True'
            self.__filterDotTransponder     = self.Config.get_x_path( '/config/Preferences/wxCheckBox[@name="hideDotServices"]', False ).text == 'True'
        except Exception, exc:
            print( "loading settings: %s" % ( exc ) )
        # end try
        autoload = self.Config.getAutoLoadReceiver()
        if autoload:
            self.__streaming_host = autoload[ 'hostname' ]
            self.Populate( autoload )
        # end if
        return
    # end def

    def clickMoveEntryUp( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        self.bouquets.MoveUp( self.bouquets.GetSelection() )
        return
    # end def

    def clickMoveEntryDown( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        self.bouquets.MoveDown( self.bouquets.GetSelection() )
        return
    # end def

    def clickMenuDeleteEntry( self, event ):
        treeItem    = self.bouquets.GetSelection()
        if treeItem.IsOk():
            e = self.bouquets.GetItemPyData( treeItem )
            if e.type == 'bouquet':
                idx = self.bouquet_choice.FindString( e.name )
                self.bouquet_choice.Delete( idx )

            # end if
            self.bouquets.Delete( treeItem )
            self.Save()
        # end if
        return
    # end def

    def clickMenuNewEntry( self, event ):
        child = self.bouquets.AppendItem( self.bouquets.GetRootItem(), 'New bouquet' )
        child_e = enigma.Bouquet()
        if child_e is not None:
            self.bouquets.SetItemPyData( child, child_e )
            if child_e.type == 'bouquet':
                self.bouquets.SetItemBackgroundColour( child, "red" )
                self.bouquets.SetItemTextColour( child, "white" )

            elif child_e.type == 'marker':
                self.bouquets.SetItemBackgroundColour( child, "blue" )
                self.bouquets.SetItemTextColour( child, "white" )

            else:
                self.bouquets.SetItemBackgroundColour( child, "white" )
                self.bouquets.SetItemTextColour( child, "black" )

            # end if
        # end if
        self.Save()
        self.bouquets.Refresh()
        self.bouquets.SelectItem( child )
        self.bouquets.EditLabel( child )
        return
    # end def

    def PopupUpdateMenuBouquet( self, menu ):
        treeItem    = self.bouquets.GetSelection()
        if treeItem.IsOk():
            e = self.bouquets.GetItemPyData( treeItem )
            menu.Enable( self.BOUQUET_ITEM_MARKER_EDIT, e.type == 'marker' )
            menu.Enable( self.BOUQUET_ITEM_MARKER_INS_BEFORE, e.type != 'bouquet' )
            menu.Enable( self.BOUQUET_ITEM_MARKER_INS_AFTER, e.type != 'bouquet' )
            menu.Enable( self.BOUQUET_ITEM_MARKER_ADD, e.type == 'bouquet' )
            menu.Enable( self.BOUQUET_EDIT, e.type == 'bouquet' )
            menu.Enable( self.BOUQUET_INS_AFTER, e.type == 'bouquet' )
            menu.Enable( self.BOUQUET_INS_BEFORE, e.type == 'bouquet' )
        # end if
        return
    # end def

    def PopupMenuBouquet( self, event ):
        treeItem    = self.bouquets.GetSelection()
        parent      = self.bouquets.GetItemParent( treeItem )
        if treeItem.IsOk():
            e = self.bouquets.GetItemPyData( treeItem )
            child_e = None
            if event.Id == self.BOUQUET_ITEM_MARKER_INS_BEFORE:
                child = self.bouquets.InsertBefore( treeItem, 'New marker' )
                if child.IsOk():
                    child_e = enigma.BouquetMarker()
                else:
                    raise Exception( "Invalid child on BOUQUET_ITEM_MARKER_INS_BEFORE" )
                # end if

            elif event.Id == self.BOUQUET_ITEM_MARKER_INS_AFTER:
                child = self.bouquets.InsertItem( parent, treeItem, 'New marker' )
                child_e = enigma.BouquetMarker()

            elif event.Id == self.BOUQUET_ITEM_MARKER_ADD:
                child = self.bouquets.AppendItem( parent, 'New marker' )
                child_e = enigma.BouquetMarker()

            elif event.Id == self.BOUQUET_ITEM_REMOVE:
                if e.type == 'bouquet':
                    idx = self.bouquet_choice.FindString( e.name )
                    self.bouquet_choice.Delete( idx )

                # end if
                self.bouquets.Delete( treeItem )
                self.Save()
                return
            elif event.Id == self.BOUQUET_ITEM_MARKER_EDIT:
                if e.type == 'marker':
                    self.bouquets.EditLabel( treeItem )
                    return
                # end if
            elif event.Id == self.BOUQUET_EDIT:
                if e.type == 'bouquet':
                    self.bouquets.EditLabel( treeItem )
                    return
                # end if
            elif event.Id == self.BOUQUET_INS_BEFORE:
                child = self.bouquets.InsertBefore( treeItem, 'New bouquet' )
                if child.IsOk():
                    child_e = enigma.Bouquet()

                else:
                    raise Exception( "Invalid child on BOUQUET_ITEM_MARKER_INS_BEFORE" )
                # end if

            elif event.Id == self.BOUQUET_INS_AFTER:
                child = self.bouquets.InsertItem( parent, treeItem, 'New bouquet' )
                child_e = enigma.Bouquet()

            elif event.Id == self.BOUQUET_ADD:
                child = self.bouquets.AppendItem( self.bouquets.GetRootItem(), 'New bouquet' )
                child_e = enigma.Bouquet()

            else:
                raise Exception( "Invalid event from PopupMenuBouquet()" )
            # end if
            if child_e is not None:
                self.bouquets.SetItemPyData( child, child_e )
                if child_e.type == 'bouquet':
                    self.bouquets.SetItemBackgroundColour( child, "red" )
                    self.bouquets.SetItemTextColour( child, "white" )

                elif child_e.type == 'marker':
                    self.bouquets.SetItemBackgroundColour( child, "blue" )
                    self.bouquets.SetItemTextColour( child, "white" )

                else:
                    self.bouquets.SetItemBackgroundColour( child, "white" )
                    self.bouquets.SetItemTextColour( child, "black" )

                # end if
            # end if
            self.Save()
            self.bouquets.Refresh()
            self.bouquets.SelectItem( child )
            self.bouquets.EditLabel( child )

        else:
            raise Exception( "Invalid selection from PopupMenuBouquet()" )
        # end if
        return
    # end def

    def PopupMenuServices( self, event ):
        print( "PopupMenuEvent" )
        print( event.Id )
        if event.Id == self.POPUP_MENU_ALL:
            for colnum, name, width, id in self.COLUMNS:
                item = self.listMenu.FindItemById( id )
                item.Check( True )
                self.services.SetColumnWidth( colnum, width )
                column = self.Config.get_x_path( '/config/MainWnd/Services/Column[@id="%i"]' % ( colnum ), False )
                if column is not None:
                    column.attrib[ 'show' ] = 'True'
                    # We do the save on exit
                    # self.Config.save()
                # end if
            # next
        else:
            for colnum, name, width, id in self.COLUMNS:
                if id == event.Id:
                    item = self.listMenu.FindItemById( id )
                    if item.IsChecked():
                        self.services.SetColumnWidth( colnum, width )
                    else:
                        self.services.SetColumnWidth( colnum, 0 )
                    # end if
                    column = self.Config.get_x_path( '/config/MainWnd/Services/Column[@id="%i"]' % ( colnum ), False )
                    if column is not None:
                        column.attrib[ 'show' ] = '%s' % ( item.IsChecked() )
                        # We do the save on exit
                        # self.Config.save()
                    # end if
                    return
                # end if
            # next
        # end if
        return
    # end def

    def OnGetItemText( self, item, col ):
        if col == self.COLUMN_SERVICE_NAME:
            return self.__items[ item ].cleanname
        elif col == self.COLUMN_SERVICE_PROVIDER:
            return self.__items[ item ].provider
        elif col == self.COLUMN_SERVICE_POSITION:
            return self.__items[ item ].transponder.position
        elif col == self.COLUMN_SERVICE_FREQUENCY:
            return self.__items[ item ].transponder.frequency
        elif col == self.COLUMN_SERVICE_SYMBOLRATE:
            return self.__items[ item ].transponder.symbolrate
        elif col == self.COLUMN_SERVICE_NAMESPACE:
            return self.__items[ item ].namespace
        elif col == self.COLUMN_SERVICE_TRANSPONDER:
            return self.__items[ item ].transponder_info
        # end if
        return 'unknown'
    # end def

    def Populate( self, hostinfo ):
        print( "Loading from %s://%s%s with user %s:%s" % ( hostinfo[ 'protocol' ],
                                                            hostinfo[ 'hostname' ],
                                                            hostinfo[ 'path' ],
                                                            hostinfo[ 'username' ],
                                                            hostinfo[ 'password' ] ) )
        self.frame_2_statusbar.PushStatusText( "Host: %s" % ( self.__streaming_host ), 1 )
        self.frame_2_statusbar.PushStatusText( "Loading", 2 )
        # read the LAMEDB for all services and bouquets
        self.engima.load( "%s://%s:%s@%s%s" % ( hostinfo[ 'protocol' ],
                                               hostinfo[ 'username' ],
                                               hostinfo[ 'password' ],
                                               hostinfo[ 'hostname' ],
                                               hostinfo[ 'path' ] ) )
        # populate the list control
        self.__sortColumn = self.COLUMN_SERVICE_NAME
        self.clickClearFilter( None )
        # populate the tree control and choice control
        self.bouquet_choice.Append( 'All bouquets' )
        for e in self.engima.bouquets[ 'tv' ].items:
            if e.type == 'bouquet':
                self.bouquet_choice.Append( e.name )
            # end if
        # end def
        self.bouquet_choice.SetSelection( 0 )
        item = self.bouquets.AddRoot( 'root' )
        self.bouquets.SetItemPyData( item, self.engima.bouquets[ 'tv' ] )
        self.__bouquets = self.engima.bouquets[ 'tv' ]
        self.__add_bouquet_entry( self.__bouquets,
                                  self.bouquets.GetRootItem(),
                                  self.bouquet_choice.GetLabelText() )


        return
    # end def

    def __add_bouquet_entry( self, b, tree, selected = '' ):
        for e in b.items:
            if e.type == 'bouquet' and ( self.bouquet_choice.GetSelection() == 0 or selected == e.name ):
                item = self.bouquets.AppendItem( tree, e.name )
                self.bouquets.SetItemBackgroundColour( item, "red" )
                self.bouquets.SetItemTextColour( item, "white" )

                self.bouquets.SetPyData( item, e )
                self.__add_bouquet_entry( e, item, selected )
                self.bouquets.ExpandAllChildren( item )
            elif e.type == 'service_entry' and ( self.bouquet_choice.GetSelection() == 0 or selected == b.name ):
                item = self.bouquets.AppendItem( tree, e.service.cleanname )
                self.bouquets.SetPyData( item, e )
            elif e.type == 'marker' and ( self.bouquet_choice.GetSelection() == 0 or selected == b.name ):
                item = self.bouquets.AppendItem( tree, e.name )
                self.bouquets.SetItemBackgroundColour( item, "blue" )
                self.bouquets.SetItemTextColour( item, "white" )
                self.bouquets.SetPyData( item, e )
            # end if
        # next
        return
    # end def

    def Save(self):
        self.__bouquets = enigma.Bouquet()
        self.__put_bouquet_entry( self.__bouquets,
                                  self.bouquets.GetRootItem() )
        for item in self.__bouquets.items:
            print( "Bouquet: %s" % ( item.name ) )
            for bouquetitem in item.items:
                if bouquetitem.type == 'service_entry':
                    print( "   %s" % ( repr( bouquetitem.service.name ) ) )
                elif bouquetitem.type == 'marker':
                    print( "   %s" % ( repr( bouquetitem.name ) ) )
            # next
        # next
        return
    # end def

    def __put_bouquet_entry( self, b, parent ):
        child, cookie = self.bouquets.GetFirstChild( parent )
        last = self.bouquets.GetLastChild( parent )
        while child.IsOk():
            e = self.bouquets.GetItemPyData( child )
            if isinstance( e, enigma.Bouquet ):
                e.name = self.bouquets.GetItemText( child )
                print( "Add Bouquet: %s %s" % ( e.name, e ) )
                # Make sure that the BouquetService/BouquetMarker list is empty
                e.items = []
                b.items.append( e )
                self.__put_bouquet_entry( e, child )
            elif isinstance( e, enigma.BouquetMarker ):
                print( "Add BouquetMarker: %s %s" % ( e.name, e ) )
                b.items.append( e )
            elif isinstance( e, enigma.BouquetService ):
                print( "Add BouquetService: %s %s" % ( e.name, e ) )
                b.items.append( e )
            elif isinstance( e, enigma.Service ):
                print( "Add Service: %s %s" % ( e.name, e ) )
                b.items.append( enigma.BouquetService( service = e ) )
            # end if
            if child == last:
                return
            # end if
            child = self.bouquets.GetNextSibling( child )
        # next
        return
    # end def

    def clickSelectBouquetEntry( self, event ):
        service = self.bouquets.GetPyData( event.Item )
        if service.type == 'service_entry':
            # Find the Service in the service list
            for idx, item in enumerate( self.__items ):
                if item == service.service:
                    self.services.Focus( idx )
                    self.services.Select( idx )
                    return
                # end if
            # next
        # end if
        return
    # end def

    def keyDownService(self, event):  # wxGlade: BouquetEditMainWnd.<event_handler>
        if self.mplayer_process and event.KeyCode in [ ord('Q'),ord('q') ]:
            self.mplayer_process.terminate()
            os.system( 'killall mplayer' )
        # end if
        return
    # end def

    def SortItems( self, column ):
        self.frame_2_statusbar.PushStatusText( "Sorting", 2 )
        if self.__sortColumn == column:
            self.__reverse = not self.__reverse
            if self.__reverse:
                self.services.SetColumnImage( column, self.services.IMG_SORT_DESCENDING )
            else:
                self.services.SetColumnImage( column, self.services.IMG_SORT_ASCENDING )
            # end if
        else:
            self.__reverse = False
            self.services.SetColumnImage( self.__sortColumn, -1 )
            self.services.SetColumnImage( column, self.services.IMG_SORT_ASCENDING )
            self.__sortColumn = column
        # end if
        if column == self.COLUMN_SERVICE_NAME:
            key = lambda k: k.cleanname
        elif column == self.COLUMN_SERVICE_PROVIDER:
            key = lambda k: k.provider
        elif column == self.COLUMN_SERVICE_POSITION:
            key = lambda k: k.transponder.position
        elif column == self.COLUMN_SERVICE_FREQUENCY:
            key = lambda k: k.transponder.frequency
        elif column == self.COLUMN_SERVICE_SYMBOLRATE:
            key = lambda k: k.transponder.symbolrate
        elif column == self.COLUMN_SERVICE_NAMESPACE:
            key = lambda k: k.namespace
        elif column == self.COLUMN_SERVICE_TRANSPONDER:
            key = lambda k: k.transponder_info
        else:
            return
        # end if
        self.__items = sorted( self.__items, key = key, reverse = self.__reverse )
        self.frame_2_statusbar.PushStatusText( "Idle", 2 )
        return
    # end def

    def clickServiceColumn( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        # re-Sort the list
        self.SortItems( event.Column )
        # redraw the list
        self.Refresh()
        return
    # end def

    def clickApplyFilter( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        some = self.filter.Value
        self.__items = []
        count = 0
        self.services.SetItemCount( count )
        for service in self.engima.services:
            service = self.engima.services[ service ]
            if ( some in service.cleanname or
                        some in service.provider or
                        some in service.namespace or
                        some in service.transponder.frequency or
                        some in service.transponder.position ):
                if ( ( self.__filterEmptyTransponder and service.cleanname == '' ) or
                     ( self.__filterDotTransponder and service.cleanname == '.' ) ):
                    pass
                else:
                    self.__items.append( service )
                # end id
                self.__items.append( service )
                count += 1
            # end if
        # next
        self.services.SetItemCount( count )
        self.__reverse = not self.__reverse
        self.SortItems( self.__sortColumn )
        self.frame_2_statusbar.PushStatusText( "Filter", 2 )
        self.Refresh()
        return
    # end def

    def clickClearFilter( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        self.filter.Value = ''
        self.__items = []
        for service in self.engima.services:
            service = self.engima.services[ service ]
            if ( ( self.__filterEmptyTransponder and service.cleanname == '' ) or
                 ( self.__filterDotTransponder   and service.cleanname == '.' ) ):
                pass
            else:
                self.__items.append( service )
            # end if
        # next
        self.services.SetItemCount( len( self.__items ) )
        self.__reverse = not self.__reverse
        self.SortItems( self.__sortColumn )
        self.frame_2_statusbar.PushStatusText( "Idle", 2 )
        self.Refresh()
        return
    # end def

    def clickAcivateService( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        if self.__streaming_host:
            if self.mplayer_process:
                self.mplayer_process.terminate()
                os.system( 'killall mplayer' )
            # end if
            service = self.__items[ event.Index ]
            self.mplayer_process = subprocess.Popen( [ 'mplayer',
                                                       '-quiet',
                                                       '-really-quiet',
                                                       '-cache',
                                                       '128',
                                'http://{0}:8001/{1}'.format( self.__streaming_host,
                                            self.engima.get_service_desc( service ) ) ] )

        return
    # end def

    def clickRightService( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        self.services.PopupMenu( self.listMenu, event.GetPoint() )
        return
    # end def

    def clickAddToBouquet( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        selected    = self.services.GetFirstSelected()
        treeItem    = self.bouquets.GetSelection()
        if selected == -1 or not treeItem.IsOk():
            return
        # end if
        e = self.bouquets.GetItemPyData( treeItem )
        s = self.__items[ selected ]
        if e.type in [ 'service_entry', 'marker' ]:
            child = self.bouquets.InsertItem( self.bouquets.GetItemParent( treeItem ),
                                              treeItem,
                                              s.cleanname )
            self.bouquets.SetItemPyData( child,
                                         enigma.BouquetService( service = s ) )

        elif e.type == 'bouquet':
            child = self.bouquets.AppendItem( treeItem, s.cleanname )
            self.bouquets.SetItemPyData( child,
                                         enigma.BouquetService( service = s ) )

        # end if
        return
    # end def

    def clickRemoveFromBouquet( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        treeItem    = self.bouquets.GetSelection()
        e = self.bouquets.GetItemPyData( treeItem )
        if e.type == 'service_entry':
            self.bouquets.Delete( treeItem )
            self.Save()
        # end if
        return
    # end def

    def clickMakeBouquetChoice( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        self.bouquets.DeleteAllItems()
        item = self.bouquets.AddRoot( 'root' )
        self.__add_bouquet_entry( self.__bouquets, self.bouquets.GetRootItem(),
                                  event.String )
        return
    # end def

    def endLabelEdit( self, event ):
        # Need to update the descriptor
        service = self.bouquets.GetPyData( event.Item )
        if service.type == 'marker':
            service.name = self.bouquets.GetEditControl().Value
        # end if
        return

    def clickActivateBouquetEntry( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        if self.__streaming_host:
            service = self.bouquets.GetPyData( event.Item )
            if service.type == 'service_entry':
                if self.mplayer_process:
                    self.mplayer_process.terminate()
                    os.system( 'killall mplayer' )
                # end if
                self.mplayer_process = subprocess.Popen( [ 'mplayer',
                                                           '-quiet',
                                                           '-really-quiet',
                                                            '-cache',
                                                            '128',
                                    'http://{0}:8001/{1}'.format( self.__streaming_host,
                                                self.engima.get_service_desc( service ) ) ] )
            elif service.type == 'marker':
                # Go into edit mode
                self.bouquets.EditLabel( event.Item )
            # end if
        # end if
        return
    # end def

    def keyDownBouquetEntry( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        keyCode = event.GetKeyCode()
        control = event.GetKeyEvent().ControlDown()
        print( 'keyDownBouquetEntry( event.keyCode = %i )' % ( keyCode ) )
        treeItem    = self.bouquets.GetSelection()
        if keyCode == 127 and treeItem.IsOk():
            self.bouquets.Delete( treeItem )
        elif control and keyCode == 315:    # up
            self.clickMoveEntryUp( event )
        elif control and keyCode == 317:    # down
            self.clickMoveEntryDown( event )
        elif keyCode == 314 and self.bouquets.IsExpanded( treeItem ):    # left
            self.bouquets.Collapse( treeItem )
        elif self.mplayer_process and event.KeyCode in [ ord('Q'),ord('q') ]:
            self.mplayer_process.terminate()
            os.system( 'killall mplayer' )
        else:
            event.Skip()
        # end if
        return
    # end def

    def clickMenuOpenFolder( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMenuOpen' not implemented!"
        event.Skip()

    def clickMenuOpenReceiver( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMenuOpen' not implemented!"
        wmd = receiver.OpenReceiver( self, wx.ID_ANY )
        if wmd.ShowModal() == wx.ID_OK:
            # make sure that its closed
            self.clickMenuClose( event )
            # Open the receiver box
            self.__streaming_host = wmd.hostname.Value.split( '//' )[ 1 ].split('/')[ 0 ]
            self.Populate( ( wmd.hostname.Value,
                             wmd.username.Value,
                             wmd.password.Value ) )
        # end if
        return
    # end def

    def clickMenuSave( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMenuSave' not implemented!"
        event.Skip()

    def clickMenuSaveAsFolder( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMenuSaveAs' not implemented!"
        event.Skip()

    def clickMenuSaveAsReceiver( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMenuSaveAs' not implemented!"
        wmd = receiver.OpenReceiver( self, wx.ID_ANY )
        if wmd.ShowModal() == wx.ID_OK:
            # Open the receiver box
            pass
        # end if
        return
    # end def

    def clickMenuClose( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMenuClose' implemented!"
        self.services.SetItemCount( 0 )
        self.bouquets.DeleteAllItems()
        self.__items = []
        self.engima.clear()
        return
    # end def

    def clickMenuPrint( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMenuPrint' not implemented!"
        return
    # end def

    def clickMenuPrintSetup( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMenuPrintSetup' not implemented!"
        return
    # end def

    def OnClose( self, event ):
        dlg = wx.MessageDialog(self,
              "Do you really want to close this application?",
              "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            size = self.Config.get_x_path( '/config/MainWnd/wxSize', False )
            size.text = "%i,%i" % ( self.Size.width, self.Size.height )
            self.Config.save()
            self.Destroy()
        # end if
        return
    # end def

    def clickMenuExit( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        self.Close()
        return
    # end def

    def clickMenuPreferences( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        if self.Preferences is None:
            self.Preferences = preferencies.Preferences( self.Config, self, wx.ID_ANY )
        # end if
        self.Preferences.ShowModal()
        return
    # end def

    def clickMenuHelp( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        print "Event handler 'clickMenuHelp' not implemented!"
        return
    # end def

    def clickMenuAbout( self, event ):  # wxGlade: BouquetEditMainWnd.<event_handler>
        wnd = aboutwmd.AboutWnd( self, wx.ID_ANY )
        wnd.ShowModal()
        del wnd
        return
    # end def
# end class
