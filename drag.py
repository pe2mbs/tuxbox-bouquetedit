import wx

__author__ = 'mbertens'

class ServiceDataObject( wx.PyTextDataObject ):
    def __init__( self, text, obj ):
        self.__obj = obj
        wx.PyTextDataObject.__init__( self, text )
        return
    # end def

    def GetObject( self ):
        return self.__obj
    # end def

    def SetObject( self, obj ):
        self.__obj = obj
        return
    # en def
# end class


class ServiceDropTarget( wx.TextDropTarget ):
    def __init__( self, object ):
        wx.TextDropTarget.__init__( self )
        self.object = object
        return
    # end def

    def OnData( self, x, y, obj ):
        print( "x=%i, y=%i = %s" % ( x, y, repr( obj ) ) )
        return
    # end def

    def OnDropText( self, x, y, data ):
        print( "x=%i, y=%i = %s" % ( x, y, repr( data ) ) )
        #self.object.InsertStringItem( 0, data )
        return
    # end def

# end class
