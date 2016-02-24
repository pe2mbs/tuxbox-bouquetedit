__author__ = 'mbertens'

import wx

def BindEx( control, event ):
    def postbind( func ):
        control.Bind( event, func )
        return func
    return postbind

def AfterEx( *ar, **kwar ):
    def postafter( func ):
        wx.CallAfter( func, *ar, **kwar )
        return func
    return postafter

app= wx.PySimpleApp()
frame= wx.Frame( None, title= "App" )
sizer= wx.BoxSizer( wx.VERTICAL )
list1= wx.ListCtrl( frame, style=
wx.LC_REPORT| wx.LC_EDIT_LABELS )

for i in range( 4 ):
    list1.InsertColumn( i, 'col %i'% i )

for i in range( 200 ):
    list1.InsertStringItem( 0, [ "what", "who" ][ i% 2 ] ) #-1

sizer.Add( list1, 1, wx.EXPAND )
frame.SetSizer( sizer )
frame.Show()
combo1= wx.ComboBox( list1, value= 'who',
style= wx.CB_DROPDOWN, choices= 'who when where'.split() )
combo1.Hide()

@BindEx( list1, wx.EVT_LIST_BEGIN_LABEL_EDIT )
def onedit( e ):
    item= e.GetItem()
    rect= list1.GetItemRect( item.GetId() )
    rect.OffsetXY( 0, -2 )
    if not list1.GetRect().ContainsRect( rect ):
        #frame thinner than listbox
        rect= rect.Intersect( list1.GetRect() )
        #simplified scrollbar compensate
        rect.SetWidth( rect.GetWidth()- 22 )
        @AfterEx( rect )
        def postedit( rect ):
            combo1.SetRect( rect )
            combo1.SetFocus() #picky order .
            combo1.Show()
            combo1.Raise()

        @BindEx( combo1, wx.EVT_KILL_FOCUS )
        def onlostfocus( e ):
            combo1.Hide()

app.MainLoop()