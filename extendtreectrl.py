import wx

__author__ = 'mbertens'


class ContextMenu(object):
    def __init__(self):
        super( ContextMenu, self).__init__()
        self._menu = None
        self.__updateHandler = None
        self.Bind( wx.EVT_CONTEXT_MENU, self.OnContextMenu )
        return
    # end def

    def SetContextMenuHandler( self, handler ):
        self.__updateHandler = handler
        return
    # end def

    def OnContextMenu( self, event ):
        if self._menu is None:
            self.CreateContextMenu( self._menu )
        # end if
        if self.__updateHandler is not None:
            self.__updateHandler( self._menu )
        # end def
        self.PopupMenu( self._menu )
        return
    # end def

    def CreateContextMenu( self, menu ):
        raise NotImplementedError
    # end def

    def SetPopupMenu( self, menu ):
        self._menu = menu
        return
    # end def

# end class

class ExtendedTreeCtrl( wx.TreeCtrl, ContextMenu ):
    def __init__( self, parent, *args, **kwargs ):
        super( ExtendedTreeCtrl, self).__init__( parent, *args, **kwargs )
        ContextMenu.__init__( self )
        return
    # end def

    def CreateContextMenu( self, menu ):
        self._menu.Append( wx.ID_ADD )
        self._menu.Append( wx.ID_DELETE )
        self._menu.Append( wx.ID_EDIT )
        return
    # end def

    def MoveUp( self, treeItem ):
        previous    = self.GetPrevSibling( treeItem )
        if not previous.IsOk():
            return
        # end if
        previous    = self.GetPrevSibling( previous )
        childitems = self.SaveItemsToList( treeItem )
        if not previous.IsOk():
            child = self.InsertItemsFromList( childitems,
                                              self.GetItemParent( treeItem ) )[ 0 ]
        else:
            child = self.InsertItemsFromList( childitems,
                                              self.GetItemParent( treeItem ), previous )[ 0 ]
        # end if
        self.Delete( treeItem )
        self.SelectItem( child )
        return
    # end def

    def MoveDown( self, treeItem ):
        next        = self.GetNextSibling( treeItem )
        parent      = self.GetItemParent( treeItem )
        if not next.IsOk():
            return
        # end if
        childitems = self.SaveItemsToList( treeItem )
        child = self.InsertItemsFromList( childitems, parent, next )[ 0 ]
        self.Delete( treeItem )
        self.SelectItem( child )
        return
    # end def

    def InsertBefore( self, treeItem, text ):
        treeItem    = self.GetPrevSibling( treeItem )
        parent      = self.GetItemParent( treeItem )
        if not treeItem.IsOk():
            child = self.InsertItemBefore( parent, 0, text )
        else:
            child = self.InsertItem( parent, treeItem, text )
        # end if
        return child
    # end def

    def Traverse( self, func, startNode ):
        """Apply 'func' to each node in a branch, beginning with 'startNode'. """
        def TraverseAux( node, depth, func ):
            nc = self.GetChildrenCount( node, 0 )
            child, cookie = self.GetFirstChild( node )
            # In wxPython 2.5.4, GetFirstChild only takes 1 argument
            for i in xrange( nc ):
                func( child, depth )
                TraverseAux( child, depth + 1, func )
                child, cookie = self.GetNextChild( node, cookie )
            # next
        # end if
        func( startNode, 0 )
        TraverseAux( startNode, 1, func )
        return
    # end def

    def ItemIsChildOf( self, item1, item2 ):
        ''' Tests if item1 is a child of item2, using the Traverse function '''
        self.result = False
        def test_func( node, depth ):
            if node == item1:
                self.result = True
            # end if
            return
        # end def
        self.Traverse( test_func, item2 )
        return self.result
    # end def

    def SaveItemsToList( self, startnode ):
        ''' Generates a python object representation of the tree (or a branch of it),
            composed of a list of dictionaries with the following key/values:
            label:      the text that the tree item had
            data:       the node's data, returned from GetItemPyData(node)
            children:   a list containing the node's children (one of these dictionaries for each)
        '''
        global list
        list = []

        def save_func( node, depth ):
            tmplist = list
            for x in range( depth ):
                if type( tmplist[ -1 ] ) is not dict:
                    tmplist.append( {} )
                # end if
                tmplist = tmplist[ -1 ].setdefault( 'children', [] )
            # next
            item = {}
            item[ 'label' ] = self.GetItemText(node)
            item[ 'data' ] = self.GetItemPyData(node)
            item[ 'icon-normal' ] = self.GetItemImage(node, wx.TreeItemIcon_Normal)
            item[ 'icon-selected' ] = self.GetItemImage(node, wx.TreeItemIcon_Selected)
            item[ 'icon-expanded' ] = self.GetItemImage(node, wx.TreeItemIcon_Expanded)
            item[ 'icon-selectedexpanded' ] = self.GetItemImage(node, wx.TreeItemIcon_SelectedExpanded)
            item[ 'font' ] = self.GetItemFont( node )
            item[ 'color' ] = self.GetItemTextColour( node )
            item[ 'expanded' ] = self.IsExpanded( node )
            item[ 'background' ] = self.GetItemBackgroundColour( node )
            tmplist.append( item )
            return
        # end def
        self.Traverse( save_func, startnode )
        return list
    # end def

    def InsertItemsFromList( self, itemlist, parent, insertafter = None, appendafter = False ):
        ''' Takes a list, 'itemslist', generated by SaveItemsToList, and inserts
            it in to the tree. The items are inserted as children of the
            treeitem given by 'parent', and if 'insertafter' is specified, they
            are inserted directly after that treeitem. Otherwise, they are put at
            the beginning.

            If 'appendafter' is True, each item is appended. Otherwise it is prepended.
            In the case of children, you want to append them to keep them in the same order.
            However, to put an item at the start of a branch that has children, you need to
            use prepend. (This will need modification for multiple inserts. Probably reverse
            the list.)

            Returns a list of the newly inserted treeitems, so they can be
            selected, etc..'''
        newitems = []
        for item in itemlist:
            if insertafter:
                node = self.InsertItem( parent, insertafter, item[ 'label' ] )
            elif appendafter:
                node = self.AppendItem( parent, item[ 'label' ] )
            else:
                node = self.PrependItem(parent, item[ 'label' ] )
            # end if
            self.SetItemPyData( node, item[ 'data' ] )
            self.SetItemImage( node, item[ 'icon-normal' ], wx.TreeItemIcon_Normal )
            self.SetItemImage( node, item[ 'icon-selected' ], wx.TreeItemIcon_Selected )
            self.SetItemImage( node, item[ 'icon-expanded' ], wx.TreeItemIcon_Expanded )
            self.SetItemImage( node, item[ 'icon-selectedexpanded' ], wx.TreeItemIcon_SelectedExpanded )
            self.SetItemFont( node, item[ 'font' ] )
            self.SetItemTextColour( node, item[ 'color' ] )
            self.SetItemBackgroundColour( node, item[ 'background' ] )
            newitems.append( node )
            if 'children' in item:
                self.InsertItemsFromList(item[ 'children' ], node, appendafter = True )
            # end if
            if item[ 'expanded' ]:
                self.Expand( node )
            # end if
        # next
        return newitems
    # end def
# end class