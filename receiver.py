import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade
import bouquetedit.gui

__author__ = 'mbertens'

class OpenReceiver( bouquetedit.gui.OpenReceiver ):
    def __init__(self, *args, **kwds):
        bouquetedit.gui.OpenReceiver.__init__( self, *args, **kwds )
        return
    # end def

    def clickOpen( self, event ):
        try:
            protocol, hosturl = self.hostname.Value.split(':')
            if hosturl[0:2] != u'//':
                raise Exception( 'incorrect format: // before hostname missing' )
            # end if
            hosturl = hosturl[ 2 : ]
            hostname, folder = hosturl.split( '/', 1 )
        except Exception, exc:
            wx.MessageBox( 'hostname must have to following format:\n'
                           '<protocol>://<hostname>/<path>\n%s' % ( exc.message ),
                           'Error', wx.ID_OK )
            return
        # end try
        if protocol == 'ftp':   # FTP   port 21
            from ftplib import FTP
            try:
                ftp = FTP( hostname )
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
        elif protocol == 'smb': # samba port ?
            pass
        elif protocol == 'sftp': # SSH/SFTP port 22
            from ftplib import FTP_TLS
            try:
                ftps = FTP_TLS( hostname )
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
        if self.saveInPreferences.IsChecked():
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
