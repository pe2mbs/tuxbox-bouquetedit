__author__ = 'mbertens'

import codecs

class HtmlConverter( object ):
    def __init__( self ):
        return
    # end def

    def generate_service( self, services, title ):
        doc = u"""<html>
    <head>
        <style>
body
{
    font-family: "Times New Roman", Times, serif;
    font-size:      10px;
    font-weight:    normal;
}

table
{
    width: 100%%;
}

table, th, td
{
    text-align:     left;
    vertical-align: top;
}

th
{
    border-top:  1px solid black;
    border-bottom:  1px solid black;
}

tr:nth-child(even)
{
    background-color: #f2f2f2
}

#service
{
    border-left:  1px solid black;
    border-bottom:  1px solid black;
    width: 5%%;
}
#name
{
    border-left:  1px solid black;
    border-bottom:  1px solid black;
    width: 10%%;
}
#type
{
    border-left:  1px solid black;
    border-bottom:  1px solid black;
    width: 10%%;
}
#provider
{
    border-left:  1px solid black;
    border-bottom:  1px solid black;
    width: 40%%;
}
#cardinfo
{
    border-left:  1px solid black;
    border-bottom:  1px solid black;
    width: 10%%;
}
#transponder
{
    border-left:  1px solid black;
    border-bottom:  1px solid black;
    width: 20%%;
}
#service
{
    border-left:  1px solid black;
    border-bottom:  1px solid black;
    width: 5%%;
}
#sid
{
    border-left:  1px solid black;
    border-right:  1px solid black;
    border-bottom:  1px solid black;
    width: 5%%;
    text-align: right;
}
        </style>
    </head>"""
        doc += u"""
    <body>
    <h1>{title}</h1>
    <table>
        <tr>
            <th id="service">Service Id</th>
            <th id="name">Name</th>
            <th id="type">Type</th>
            <th id="provider">Provider</th>
            <th id="cardinfo">Card info</th>
            <th id="transponder">Transponder</th>
            <th id="sid">SID</th>
        </tr>""".format( title = title )

        for service in services:
            # print( service )
            if service.type == 'service':
                if service.servicetype == 1:
                    servicetype = 'Television'
                elif service.servicetype == 2:
                    servicetype = 'Radio'
                else:
                    servicetype = 'Type: %s' % ( service.servicetype )
                # end if
                provider = service.extra.split(',')
                transponder = u"""<table><tr><td>Id</td><td>{id}</td></tr>
    <tr><td>Position</td><td>{pos}</td></tr>
    <tr><td>Frequency</td><td>{freq}</td></tr>
    <tr><td>Symbol rate</td><td>{symrate}</td></tr>
</table>""".format( id = service.transponder.id,
                    pos = service.transponder.position,
                    freq = service.transponder.frequency,
                    symrate = service.transponder.symbolrate )

                item = u"""<tr><td id="service">{name}</td>
                              <td id="name">{channel}</td>
                              <td id="type">{type}</td>
                              <td id="provider">{extra}</td>
                              <td id="cardinfo">{cardinfo}</td>
                              <td id="transponder">{transponder}</td>
                              <td id="sid">{sid}</td>
                            </tr>\n""".format(
                        name        = service.id,
                        channel     = '<br/>('.join( service.cleanname.split('(') ),
                        type        = servicetype,
                        extra       = provider[ 0 ].split(':')[ 1 ],
                        cardinfo    = '<br/>'.join( provider[ 1: ] ),
                        transponder = transponder,
                        sid         = service.sid )
                doc += item
            # end if
        # next
        doc += u"</table>\n</body>\n</html>\n"
        # codecs.open( 'temp.html', 'w', 'utf8' ).write( doc )
        # print doc.encode( 'ascii', errors = 'ignore' )
        return doc
    # end def

    def generate_bouquets( self, bouquet, title ):
        print( title )
        for service in bouquet.items:
            print( service )
        # next
        return
    # end def
# end class