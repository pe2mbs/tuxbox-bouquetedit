#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#
#
import wx
import gettext
import time
import bouquetedit.mainwnd

class MySplashScreen( wx.SplashScreen ):
    """
Create a splash screen widget.
    """
    def __init__( self, parent = None ):
        # This is a recipe to a the screen.
        # Modify the following variables as necessary.
        self.__parent = parent
        aBitmap = wx.Image( name = "images/tuxbox-logo.png" ).ConvertToBitmap()
        splashStyle = wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT
        splashDuration = 10000 # milliseconds
        # Call the constructor with the above arguments in exactly the
        # following order.
        wx.SplashScreen.__init__( self, aBitmap, splashStyle,
                                  splashDuration, None )
        self.Bind( wx.EVT_CLOSE, self.OnExit )
        self.__parent.mainwindow = bouquetedit.mainwnd.MainWnd( None, wx.ID_ANY, "" )
        wx.Yield()
        return
    # end def

    def OnExit( self, evt ):
        self.Hide()
        # MyFrame is the main frame.
        self.__parent.SetTopWindow( self.__parent.mainwindow )
        self.__parent.mainwindow.Show( True )
        # The program will freeze without this line.
        evt.Skip()  # Make sure the default handler runs too...
        return
    # end def
# end class

class MyApp( wx.App ):
    def OnInit( self ):
        self.mainwindow = None
        MySplashScreen( self )
        # MySplash.Show()
        return True
    # end def
# end class

if __name__ == "__main__":
    gettext.install( "app" ) # replace with the appropriate catalog name
    app = MyApp( redirect=False, filename = "demo.log" )
    app.MainLoop()
# end def