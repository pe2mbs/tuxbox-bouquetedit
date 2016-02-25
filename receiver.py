import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade
import gui

__author__ = 'mbertens'

class OpenReceiver( gui.OpenReceiver ):
    def __init__(self, *args, **kwds):
        gui.OpenReceiver.__init__( self, *args, **kwds )
        return
    # end def

    def OpenLocation( self ):
        self.Title = 'Open receiver...'
        self.saveInPreferences.Show()
        if self.ShowModal() == wx.ID_OK:
            return True
        # end def
        return False

    def SaveAsLocation( self ):
        self.Title = 'Save to receiver...'
        self.saveInPreferences.Hide()
        if self.ShowModal() == wx.ID_OK:
            return True
        # end def
        return False
    # end def

    def GetHostInfo( self ):
        hostinfo = {}
        hostinfo[ 'protocol' ]  = self.protocol.GetLabelText()
        hostinfo[ 'username' ]  = self.username.Value
        hostinfo[ 'password' ]  = self.password.Value
        hostinfo[ 'hostname' ]  = self.hostname.Value
        hostinfo[ 'path' ]      = self.path.Value
        return hostinfo
    # end def

    def clickOpen( self, event ):
        if self.protocol.GetSelection() == 0:   # FTP   port 21
            from ftplib import FTP
            try:
                ftp = FTP( self.hostname.Value )
                ftp.login( self.username.Value, self.password.Value )
                ftp.close()
            except Exception, exc:
                if exc.message == '':
                    wx.MessageBox( exc.strerror, 'Error', wx.ID_OK )
                else:
                    wx.MessageBox( exc.message, 'Error', wx.ID_OK )
                # end if
                return
            # end try
        elif self.protocol.GetSelection() == 1: # SSH/SFTP port 22
            from ftplib import FTP_TLS
            try:
                ftps = FTP_TLS( self.hostname.Value )
                ftps.login( self.username.Value, self.password.Value )
                ftps.prot_p()
                ftps.close()
            except Exception, exc:
                if exc.message == '':
                    wx.MessageBox( exc.strerror, 'Error', wx.ID_OK )
                else:
                    wx.MessageBox( exc.message, 'Error', wx.ID_OK )
                # end if
                return
            # end try
        else:
            wx.MessageBox( 'Invalid protocol selected', 'Error', wx.ID_OK )
            return
        # end def
        if self.saveInPreferences.IsShown() and self.saveInPreferences.IsChecked():
            pass
        # end if
        self.EndModal( wx.ID_OK )
        return
    # end def

    def clickCancel( self, event ):
        self.EndModal( wx.ID_CANCEL )
        return
    # end def
# end class
