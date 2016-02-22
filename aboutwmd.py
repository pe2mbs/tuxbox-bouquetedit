import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade
import bouquetedit.gui

__author__ = 'mbertens'

class AboutWnd( bouquetedit.gui.AboutWnd ):
    def __init__(self, *args, **kwds):
        bouquetedit.gui.AboutWnd.__init__( self, *args, **kwds )
        self.Bind( wx.EVT_BUTTON, self.clickClose, self.button_13 )
        return
    # end def

    def clickClose( self, event ):
        self.EndModal(0)
        return
    # end def
# end class