import wx
import os
import locale
import gettext

__author__ = 'mbertens'

class wxLanguageSupport( object ):
    __wxLanguages       = {}
    def __init__( self, set_language = None ):
        for dirname, dirnames, filenames in os.walk( './locale' ):
            language = dirname.split('/')[ -1 ]
            if "LC_MESSAGES" in dirnames:
                # Found locate directory
                info = wx.Locale.FindLanguageInfo( language )
                lang = { 'class': gettext.translation( "bouqueteditor",
                                                        "./locale",
                                                        languages = [ language ],
                                                        fallback = False ),
                         'info': info }
                self.__wxLanguages[ language ] = lang
            # end if
        # next
        if set_language is not None:
            self.ActivateLanguage( set_language )
        # end if
        return
    # end def

    def ActivateLanguage( self, language ):
        langObject = self.__wxLanguages[ language ]
        langObject[ 'class' ].install()
        self.locale = wx.Locale( langObject[ 'info' ].Language )
        locale.setlocale( locale.LC_ALL, language + ".utf8" )
        return
    # end def

    def SupportedLanguages( self ):
        return self.__wxLanguages
    # end def
# end class
