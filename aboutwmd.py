import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade
import gui
import version

__author__ = 'mbertens'

class AboutWnd( gui.AboutWnd ):
    def __init__(self, *args, **kwds):
        gui.AboutWnd.__init__( self, *args, **kwds )
        verstr = "%i.%02i.%04i (%s)" % ( version.MAJOR_VERSION,
                                         version.MINOR_VERSION,
                                         version.BUILD_NUMBER,
                                         version.BUILD_DATE )
        self.label_8.SetLabel( _("Version: %s") % ( verstr ) )
        self.Bind( wx.EVT_BUTTON, self.clickClose, self.button_13 )
        return
    # end def

    def clickClose( self, event ):
        self.EndModal(0)
        return
    # end def
# end class