__author__ = 'mbertens'
#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = 'Transponder Service BouquetEntry BouquetService BouquetMarker Bouquet Enigma2'.split()

import bisect
import collections
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib
import urllib2

# ---------------------------------------------------------------------------
# helper functions and global symbols

def _serialise( v ):
    if isinstance( v, list ):
        return list( _serialise( x ) for x in v )
    # end if
    if isinstance( v, JsonSerialisableObjectWithId ):
        return v.id
    # end if
    if isinstance( v, JsonSerialisableObject ):
        return v.data
    else:
        return v
    # end if
# end def

_re_e2decode    = re.compile( '%(..)' )

def _e2decode( x ):
    return _re_e2decode.sub( lambda match: chr( int( match.group( 1 ), 16 ) ), x )
# end def

_re_frombouquet = re.compile( 'FROM BOUQUET "(.*?)"' )
_re_nonalpha    = re.compile( r'\W+', re.UNICODE )

def _get_search_terms( txt ):
    if not txt:
        return ()
    # end if
    txt = txt.strip().lower().replace( "'", "" )
    txt = _re_nonalpha.sub( " ",txt )
    if not txt:
        return ()
    # end if
    return txt.split()
# end def
# ---------------------------------------------------------------------------
# helper classes

class JsonSerialisableObject( object ):
    def __init__( self, **kw ):
        for key in self._json_fields:
            if not hasattr( self, key ):
                setattr( self, key, kw.get( key ) )
            # end if
        # next
    # end def

    @property
    def data( self ):
        fields = ( ( i, getattr( self, i, None ) ) for i in self._json_fields )
        return dict( ( k, _serialise( v ) ) for k, v in fields if v is not None )
    # end def

    def __repr__( self ):
        return '<{0} {1!r}>'.format(self.__class__.__name__, self.data)
    # end def
# end class


class JsonSerialisableObjectWithId( JsonSerialisableObject ):
    def __init__(self, id, **kw):
        self.id = id
        JsonSerialisableObject.__init__( self, **kw )
        return
    # end def

    def __repr__( self ):
        return '<{0} {1!r} {2!r}>'.format( self.__class__.__name__, self.id, self.data )
    # end def
# end class


class Transponder( JsonSerialisableObjectWithId ):
    _json_fields = 'type medium namespace tsid nid freq symbrate pol fec pos inv flags medium modulation rolloff pilot'.split()
    type = 'transponder'

    @staticmethod
    def find( transponders, namespace, tsid, nid ):
        for transponder in transponders.itervalues():
            if ( transponder.namespace == namespace and
                    transponder.tsid == tsid and transponder.nid == nid ):
                return transponder
            # end if
        # next
    # end def

    @property
    def frequency( self ):
        freq_mhz = self.freq / 1000
        freq_khz = self.freq % 1000
        freq_ghz = freq_mhz / 1000
        freq_mhz %= 1000
        return "%i,%03i.%03i %s" % ( freq_ghz, freq_mhz, freq_khz, 'V' if self.pol else 'H' )
    # end def

    @property
    def symbolrate( self ):
        return "%i (%i/%i)" % ( self.symbrate / 1000,
                                self.inv,
                                self.nid )
    # end def

    @property
    def position( self ):
        east_west = 'E'
        if self.pos < 0:
            east_west = 'W'
        # end if
        return "%-2i.%i %s" % ( self.pos / 10, self.pos % 10, east_west )
    # end def
# end class


class SatelliteTransponder( Transponder ):
    def __init__( self, id, medium='s', **kw ):
        Transponder.__init__( self, id, medium=medium, **kw )
        return
    # end def
# end class


class Service( JsonSerialisableObjectWithId ):
    _json_fields = 'type sid transponder servicetype number name extra'.split()
    type = 'service'

    @property
    def cleanname( self ):
        return self.name.replace( u'\x86', '' ).replace( u'\x87', '' )
    # end def

    @property
    def provider( self ):
        return self.extra.split(':')[ 1 ].split( ',' )[ 0 ]
    # end def

    @property
    def transponder_info( self ):
        return "%s %s %s %s" % ( self.transponder.nid,
                                 self.transponder.inv,
                                 self.transponder.tsid,
                                 self.transponder.fec )
    # end def

    @property
    def namespace( self ):
        s = "%X" % ( self.transponder.namespace )
        l = len( s )
        if l % 2 != 0:
            return '0' + s
        # end def
        return s
    # end def

    @staticmethod
    def find( services, sid, namespace, tsid, nid ):
        for service in services.itervalues():
            if service.sid == sid:
                transponder = service.transponder
                if (transponder.namespace == namespace and
                    transponder.tsid == tsid and
                    transponder.nid == nid):
                    return service
                # end if
            # end if
        # next
        return
    # end def
# end class


class BouquetEntry( JsonSerialisableObject ):
    pass
# end class


class BouquetService( BouquetEntry ):
    _json_fields = 'type name service'.split()
    type = 'service_entry'
# end class


class BouquetMarker( BouquetEntry ):
    _json_fields = 'type name'.split()
    type = 'marker'
# end class


class Bouquet( BouquetEntry ):
    _json_fields = 'type name items filename'.split()
    type = 'bouquet'

    def __init__(self, **kw):
        JsonSerialisableObject.__init__(self, **kw)
        if not getattr( self, 'items', None ):
            self.items = []
        # end if
        if 'toplevel' not in kw:
            self.istoplevel = True
        # end if
        if 'name' not in kw:
            self.name = ''
        # end if
        return
    # end def
# end class
# ---------------------------------------------------------------------------

class Enigma2( object ):
    re_protocol             = re.compile( r'^(\w+)://' )
    dvb_tv_service_types    = frozenset( ( 1, 4, 5, 17, 22, 23, 24, 25, 26, 27, 211 ) )
    dvb_radio_service_types = frozenset( ( 2, 7, 10))

    def __init__(self):
        self.clear()
        return
    # end def

    def clear( self ):
        self.transponders   = {}
        self.services       = {}
        self.bouquets       = {}
        self._searchterms   = []
        self._searchindexes = []
        return
    # end def

    def load( self, location ):
        print( "enigma.load() entry" )
        if self.re_protocol.match( location ):
            Open = lambda filename: urllib2.urlopen( '{0}/{1}'.format( location, filename ) )
        else:
            Open = lambda filename: open( os.path.join( location, filename ) )
        # end if
        ## read lamedb file

        services        = self.services = {}
        transponders    = self.transponders = {}

        f = Open( 'lamedb' )
        assert( f.readline() == 'eDVB services /4/\n' )
        assert( f.readline() == 'transponders\n' )
        while True:
            line = f.readline()
            if not line or line == 'end\n':
                break
            # end if
            line2, line3 = f.readline(), f.readline()
            assert line3 == '/\n'
            info            = line.strip().split( ':' )
            medium, info2   = line2.strip().split()
            info2           = info2.split( ':'s )
            if medium == 's':
                t = SatelliteTransponder(
                    id = 't{0}'.format( len( self.transponders ) ),
                    namespace   = int( info[ 0 ], 16 ),
                    tsid        = int( info[ 1 ], 16 ),
                    nid         = int( info[ 2 ], 16 ),
                    freq        = int( info2[ 0 ] ),
                    symbrate    = int( info2[ 1 ] ),
                    pol         = int( info2[ 2 ] ),
                    fec         = int( info2[ 3 ] ),
                    pos         = int( info2[ 4 ] ),
                    inv         = int( info2[ 5 ] ),
                    flags       = int( info2[ 6 ] ),
                    system      = int( info2[ 7 ] ) if len(info2)>=11 else None,
                    modulation  = int( info2[ 8 ] ) if len(info2)>=11 else None,
                    rolloff     = int( info2[ 9 ] ) if len(info2)>=11 else None,
                    pilot       = int( info2[ 10 ] ) if len(info2)>=11 else None,
                )
            else:
                sys.stderr.write( "Unsupported medium {0!r}\n".format( medium ) )
                continue
            # end if
            self.transponders[ t.id ] = t
        # end while
        assert( f.readline() == 'services\n' )
        while True:
            line = f.readline()
            if not line or line == 'end\n':
                break
            # end if
            line2, line3 = f.readline(), f.readline()
            info = line.strip().split( ':' )
            name = line2.strip().decode( 'utf8' )
            t = Transponder.find( self.transponders,
                                  namespace = int( info[ 1 ], 16 ),
                                  tsid      = int( info[ 2 ], 16),
                                  nid       = int( info[ 3 ], 16 ), )
            if t is None:
                sys.stderr.write('Service {0!r} references undefined transponder\n'.format(name))
                continue
            # end if
            s = Service(
                id          = 's{0}'.format( len( self.services ) ),
                sid         = int( info[ 0 ], 16 ),
                transponder = t,
                servicetype = int( info[ 4 ] ),
                number      = int( info[ 5 ] ),
                name        = name,
                extra       = line3.strip().decode( 'utf8' ),
            )
            self.services[ s.id ] = s
        # end while
        ## bouquets

        self.bouquets = {}
        self.bouquets[ 'tv' ]     = self._read_bouquet( Open, 'bouquets.tv' )
        self.bouquets[ 'radio' ]  = self._read_bouquet( Open, 'bouquets.radio' )
        print( "enigma.load() exit" )
    # end def

    def _read_bouquet(self, Open, filename):
        b = Bouquet(filename=filename)
        try:
            f = Open(filename)
        except Exception:
            sys.stderr.write('Warning: could not open bouquet file {0!r}\n'.format(filename))
            return b
        # end try
        item = None

        for line in f:
            line = line.strip()
            if not line:
                # as seen in Enigma sources: stop reading this file upon empty line
                break
            # end if
            if not line[0]=='#':
                continue
            # end if
            if line.startswith('#SERVICE'):
                item = None
                serv = line[8:]
                serv = (serv[1:] if serv.startswith(':') else serv).strip()
                serv = serv.split(':', 11)
                type = int(serv[0])
                flags = int(serv[1])
                data = tuple(int(x, 16) for x in serv[2:10])
                path = _e2decode(serv[10])
                name = (_e2decode(serv[11]).decode('utf8')) if len(serv)>11 else None

                if flags & 1: # subdirectory
                    if '/' in path:
                        path = path[path.rfind('/')+1:]
                    else:
                        res = _re_frombouquet.search(path)
                        if res:
                            path = res.group(1)
                        else:
                            sys.stderr.write("No path given for bouquet ({0!r})\n".format(line))
                            continue
                        # end if
                        b.items.append(self._read_bouquet(Open, path))
                    # end if
                # end if
                if flags == 0:
                    # regular service
                    service = Service.find(self.services, data[1], data[4], data[2], data[3])
                    if service:
                        item = BouquetService(service = service, name = name if name else None)
                        b.items.append(item)
                    else:
                        sys.stderr.write("Bouquet references unknown service ({0!r})\n".format(line))
                    # end if
                elif flags == 64:
                    # marker
                    b.items.append(BouquetMarker(name=name))
                # end if
            elif line.startswith( '#DESCRIPTION' ):
                desc = line[12:].decode('utf8')
                if item:
                    item.name = (desc[1:] if desc.startswith(':') else desc).strip()
                # end if
            elif line.startswith( '#NAME ' ):
                b.name = line[6:].decode( 'utf8' )
            # end if
        # next
        return b
    # end def

    def set( self, data ):
        self.transponders = {}
        for k, v in data[ 'transponders' ].iteritems():
            medium = v.get( 'medium' )
            if medium == 's':
                self.transponders[ k ] = SatelliteTransponder( id = k, **v )
            else:
                sys.stderr.write( "Unsupported medium {0!r}\n".format( medium ) )
            # end if
        # next
        self.services = dict((k, Service(id=k, **v)) for k, v in data['services'].iteritems())
    # end def

    @property
    def data(self):
        return dict(
            transponders = dict((k, v.data) for k, v in self.transponders.iteritems()),
            services = dict((k, v.data) for k, v in self.services.iteritems()),
            bouquets = dict((k, v.data) for k, v in self.bouquets.iteritems()),
            )
    # end def

    def save(self, location, keep_tempdir = False):
        res = self.re_protocol.match(location)
        ftp_location = None
        if res:
            proto = res.group(1)
            if proto == 'ftp':
                ftp_location = location
                location = tempfile.mkdtemp(prefix='e2-')
            else:
                raise RuntimeError('Protocol not supported for saving ({0!r})\n'.format(res.group(1)))
            # end if
        # end if
        if not os.path.isdir(location):
            raise RuntimeError('Target location does not exist ({0!r})\n'.format(location))
        # end if
        bouquets = []
        objs = list()
        for key, value in self.bouquets.items():
            objs.append(value)
            value.toplevel = key
            value.istoplevel = True
        # next
        while objs:
            obj = objs.pop(0)
            if isinstance(obj, Bouquet):
                bouquets.append(obj)
                for i in obj.items:
                    i.toplevel = obj.toplevel
                    objs.append(i)
                # next
            # end if
        # end while
        bfilenames = set()
        for b in bouquets:
            if b.filename is not None:
                if b.filename in bfilenames:
                    # filename is in use already
                    b.filename = None
                else:
                    bfilenames.add(b.filename)
                # end if
            # end if
        # next
        for b in bouquets:
            if b.filename is None:
                basename = '{0}.{1}'.format(
                    ('bouquets' if getattr( b, 'istoplevel', False ) else 'userbouquet'),
                    urllib.quote( b.name.lower().replace( ' ', '_' ), '' ),
                    )
                filename = '{0}.{1}'.format( basename, b.toplevel )
                ctr = 0
                while filename in bfilenames:
                    filename = '{0}_{1}.{2}'.format( basename, ctr, b.toplevel )
                    ctr += 1
                # end while
                bfilenames.add( filename )
                b.filename = filename
            # end if
        # next
        for b in bouquets:
            out = open( os.path.join( location, b.filename ), 'w' )
            out.write( '#NAME {0}\n'.format( b.name.encode( 'utf8' ) ) )
            markernum = 0
            for i in b.items:
                if isinstance( i, BouquetService ):
                    s = i.service
                    if hasattr( s, 'cleanname' ):
                        cleanname   = ":%s" % ( s.cleanname.encode('ascii',errors='replace' ) )
                    else:
                        cleanname   = ''
                    # end if
                    out.write( '#SERVICE 1:0:{servicetype:X}:{sid:X}:{tsid:X}:{nid:X}:{namespace:X}:0:0:0:{name}\n'.format(
                            servicetype = s.servicetype,
                            sid = s.sid,
                            tsid = s.transponder.tsid,
                            nid = s.transponder.nid,
                            namespace = s.transponder.namespace,
                            name = cleanname
                        ))
                elif isinstance( i, Bouquet ):
                    out.write( '#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "{0}" ORDER BY bouquet\n'.format( i.filename ) )
                elif isinstance( i, BouquetMarker ):
                    markernum += 1
                    out.write( '#SERVICE 1:64:{0:X}:0:0:0:0:0:0:0::{1}\n#DESCRIPTION {1}\n'.format( markernum, i.name.encode( 'ascii', errors='ignore' ) ) )
                # end if
            # next
            del out
        # next
        if ftp_location and 0:
            if subprocess.call( [ 'lftp', '-e', 'open {0} && mput * ; quit'.format( ftp_location ) ], cwd = location ) != 0:
                sys.stderr.write( 'Warning: lftp failed\n' )
            else:
                if not keep_tempdir:
                    shutil.rmtree(location)
                # end if
            # end if
        # end if
    # end def

    def build_search_index( self ):
        searchidx = collections.defaultdict( set )
        for id, service in self.services.iteritems():
            for term in _get_search_terms( service.cleanname ):
                searchidx[ term ].add( id )
            # next
        # next
        self._searchterms   = []
        self._searchindexes = []
        for term, ids in sorted( searchidx.iteritems(), lambda a, b: cmp( a[ 0 ], b[ 0 ] ) ):
            self._searchterms.append( term )
            self._searchindexes.append( frozenset( ids ) )
        # next
        return
    # end def

    def _term2serviceids( self, term ):
        idx = bisect.bisect_left( self._searchterms, term )
        result = set()
        while idx < len( self._searchterms ) and self._searchterms[ idx ].startswith( term ):
            result.update( self._searchindexes[ idx ] )
            idx += 1
        # end while
        return result
    # end def

    def get_matching_serviceids( self, txt ):
        terms = txt and _get_search_terms( txt )
        if terms:
            result = self._term2serviceids( terms[ 0 ] )
            for t in terms[ 1: ]:
                if not result:
                    break
                # end if
                result.intersection_update( self._term2serviceids( t ) )
            # next
            return result
        else:
            return None
        # end if
        return ()
    # end def

    def get_matching_services( self, txt ):
        ids = self.get_matching_serviceids( txt )
        if ids is not None:
            if ids:
                return list( s for s in self.services if s.id in ids )
            else:
                return []
            # end if
        # end if
    # end def

    def get_service_desc( self, s ):
        if isinstance( s, BouquetService ):
            s = s.service
        # end def
        elif not isinstance( s, Service ):
            s = self.service[ s ]
        # end if
        t = s.transponder
        return '1:0:1:{0:X}:{1:X}:{2:X}:{3:X}:0:0:0:'.format( s.sid, t.tsid, t.nid, t.namespace )
    # end def
# end class
