import wx
import wx.gizmos

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

class SaveTreeItem( object ):
    def __init__( self, parent ):
        self.__parent                   = parent
        self.__childeren                = []
        self.__label                    = ''
        self.__data                     = None
        self.__icon_normal              = -1
        self.__icon_selected            = -1
        self.__icon_expanded            = -1
        self.__icon_selectedexpanded    = -1
        self.__font                     = None
        self.__expanded                 = False
        self.__background               = None
        self.__color                    = None
        return
    # end def

    def GetText( self ):
        return self.__label
    # end def

    def SetText( self, text ):
        self.__label = text
        return
    # end def

    def GetPyData( self ):
        return self.__data
    # end def

    def SetPyData( self, data ):
        self.__data = data
        return
    # end def

    def GetImage( self, type_icon ):
        if type_icon == wx.TreeItemIcon_Normal:
            return self.__icon_normal
        elif type_icon == wx.TreeItemIcon_Selected:
            return self.__icon_selected
        elif type_icon == wx.TreeItemIcon_Expanded:
            return self.__icon_expanded
        elif type_icon == wx.TreeItemIcon_SelectedExpanded:
            return self.__icon_selectedexpanded
        # end def
        return None
    # end def

    def SetImage( self, type_icon, icon ):
        if type_icon == wx.TreeItemIcon_Normal:
            self.__icon_normal          = icon
        elif type_icon == wx.TreeItemIcon_Selected:
            self.__icon_selected        = icon
        elif type_icon == wx.TreeItemIcon_Expanded:
            self.__icon_expanded        = icon
        elif type_icon == wx.TreeItemIcon_SelectedExpanded:
            self.__icon_selectedexpanded = icon
        # end def
        return
    # end def

    def GetFont( self ):
        return self.__font
    # end def

    def SetFont( self, font ):
        self.__font = font
        return
    # end def

    def IsExpanded( self ):
        return self.__expanded
    # end def

    def SetExpanded( self, expanded = True ):
        self.__expanded = expanded
        return
    # end def

    def GetTextColour( self ):
        return self.__color
    # end def

    def SetTextColour( self, color ):
        self.__color    = color
        return
    # end def

    def GetBackgroundColour( self ):
        return self.__background
    # end def

    def SetBackgroundColour( self, color ):
        self.__background   = color
        return
    # end def

    def GetTreeCtrl( self ):
        return self.__parent
    # end def

    def Copy( self, node, recursive = True ):
        ''' Generates a python object representation of the tree (or a branch of it),
            composed of a object:
            label:                  the text that the tree item had
            font:
            icon-normal
            icon-selected
            icon-expanded
            icon-selectedexpanded
            color:
            background-color:
            data:                   the node's data, returned from GetItemPyData(node)
            children:               a list containing the node's children (one of these dictionaries for each)
        '''
        self.__label                    = self.__parent.GetItemText( node )
        self.__data                     = self.__parent.GetItemPyData( node )
        self.__icon_normal              = self.__parent.GetItemImage( node, wx.TreeItemIcon_Normal )
        self.__icon_selected            = self.__parent.GetItemImage( node, wx.TreeItemIcon_Selected )
        self.__icon_expanded            = self.__parent.GetItemImage( node, wx.TreeItemIcon_Expanded )
        self.__icon_selectedexpanded    = self.__parent.GetItemImage( node, wx.TreeItemIcon_SelectedExpanded )
        self.__font                     = self.__parent.GetItemFont( node )
        self.__color                    = self.__parent.GetItemTextColour( node )
        self.__expanded                 = self.__parent.IsExpanded( node )
        self.__background               = self.__parent.GetItemBackgroundColour( node )
        if recursive:
            nc = self.__parent.GetChildrenCount( node, 0 )
            child, cookie = self.__parent.GetFirstChild( node )
            # In wxPython 2.5.4, GetFirstChild only takes 1 argument
            for i in xrange( nc ):
                item = SaveTreeItem( self.__parent )
                item.Copy( child, recursive )
                child, cookie = self.__parent.GetNextChild( node, cookie )
                self.__childeren.append( item )
            # next
        # end if
        return
    # end def

    def GetChildrenCount( self ):
        return len( self.__childeren )
    # end def

    def GetChild( self, idx ):
        return self.__childeren[ idx ]
    # end def

    def InsertInto( self, parent, nodes ):
        self.InsertItemsFromList( nodes, parent, appendafter = True )
        return
    # end def

    def InsertBefore( self, parent, nodes ):
        self.InsertItemsFromList( nodes, parent )
        return
    # end def

    def InsertAfter( self, parent, after, nodes ):
        self.InsertItemsFromList( nodes, parent, insertafter = after )
    # end def

    def Append( self, parent, nodes ):
        self.InsertItemsFromList( nodes, parent, appendafter = True )
        return
    # end def

    def InsertItemsFromList( self, parent, insertafter = None, appendafter = False ):
        ''' Takes a list, 'itemslist', generated by SaveTreeItem.Copy(), and inserts
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
        if insertafter:
            node = self.__parent.InsertItem( parent, insertafter, self.__label )
        elif appendafter:
            node = self.__parent.AppendItem( parent, self.__label )
        else:
            node = self.__parent.PrependItem( parent, self.__label )
        # end if
        self.__parent.SetItemPyData( node, self.__data )
        self.__parent.SetItemImage( node, self.__icon_normal, wx.TreeItemIcon_Normal )
        self.__parent.SetItemImage( node, self.__icon_selected, wx.TreeItemIcon_Selected )
        self.__parent.SetItemImage( node, self.__icon_expanded, wx.TreeItemIcon_Expanded )
        self.__parent.SetItemImage( node, self.__icon_selectedexpanded, wx.TreeItemIcon_SelectedExpanded )
        self.__parent.SetItemFont( node, self.__font )
        self.__parent.SetItemTextColour( node, self.__color )
        self.__parent.SetItemBackgroundColour( node, self.__background )
        if len( self.__childeren ) > 0:
            for item in self.__childeren:
                item.InsertItemsFromList( node, appendafter = True )
            # next
        # end if
        if self.__expanded:
            self.__parent.Expand( node )
        # end if
        return node
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
        childitem   = SaveTreeItem( self )
        childitem.Copy( treeItem )
        if not previous.IsOk():
            child = childitem.InsertItemsFromList( self.GetItemParent( treeItem ) )
        else:
            child = childitem.InsertItemsFromList( self.GetItemParent( treeItem ), previous )
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
        childitem   = SaveTreeItem( self )
        childitem.Copy( treeItem )
        child = childitem.InsertItemsFromList( parent, next )
        self.Delete( treeItem )
        self.SelectItem( child )
        return
    # end def

    def InsertBefore( self, treeItem, text ):
        # self.PrependItem( treeItem, text ) ???
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
# end class

class ExtTreeListCtrl( wx.gizmos.TreeListCtrl, ContextMenu ):
    def __init__( self, parent, *args, **kwargs ):
        super( ExtTreeListCtrl, self).__init__( parent, *args, **kwargs )
        ContextMenu.__init__( self )
        return
    # end def

    def ExpandAllChildren( self, *args, **kwargs ):
        return

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
        childitem = SaveTreeItem( self )
        childitem.Copy( treeItem )
        if not previous.IsOk():
            child = childitem.InsertItemsFromList( self.GetItemParent( treeItem ) )
        else:
            child = childitem.InsertItemsFromList( self.GetItemParent( treeItem ), previous )
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
        childitem = SaveTreeItem( self )
        childitem.Copy( treeItem, True )
        child = childitem.InsertItemsFromList( parent, next )
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
# end class