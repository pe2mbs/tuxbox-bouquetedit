from lxml import etree
import time
import os

__author__ = 'mbertens'

class Config( object ):
    def __init__( self, filename ):
        self.tree = None
        self.filename = filename
        self.load( filename )
        return
    # end def

    def load( self, filename = None ):
        if filename is None:
            filename = self.filename
        # end if
        try:
            fp = open( os.path.join( os.path.expanduser( "~" ), '.bouquetedit', filename ) )
        except:
            try:
                # Load the default config
                fp = open( filename )
            except:
                raise Exception( 'Could not load configuration.' )
            # end try
        # end try
        self.tree = etree.parse( fp )
        return
    # end def

    def save( self, filename = None ):
        if filename is None:
            filename = self.filename
        # end if
        dir = os.path.join( os.path.expanduser( "~" ), '.bouquetedit' )
        if not os.path.isdir( dir ):
            os.mkdir( dir )
        # end if
        fp = open( os.path.join( dir, filename ), 'w' )
        item = self.tree.find( 'SaveTime' )
        if item is not None:
            item.text = time.strftime( '%Y-%m-%d %H:%M:%S', time.gmtime() )
        else:
            print( "not updating timestamp" )
        # end if
        fp.write( etree.tostring( self.tree,
                                  xml_declaration = True,
                                  encoding='utf8',
                                  pretty_print = True ) )
        fp.close()
        return
    # end def

    def get_x_path( self, xpath, listitems = True ):
        result = self.tree.xpath( xpath )
        if len( result ) == 1 and not listitems:
            return result[ 0 ]
        # end if
        return result
    # end def

    def getAutoLoadReceiver( self ):
        item = self.tree.xpath( '/config/Preferences/wxListCtrl[@name="receivers"]/wxListItem[@autoload="True"]' )
        if item:
            if len( item ) == 1:
                item = item[ 0 ]
            # end if
            passwd      = ''
            username    = ''
            for element in item:
                if element.attrib[ 'id' ] == '1' and element.text:
                    username = element.text
                elif element.attrib[ 'id' ] == '2' and element.text:
                    passwd = element.text
                # end if
            # next
            return ( item.attrib[ 'text' ], username, passwd )
        return None
    # end def
# end class