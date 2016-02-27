import wx
from wx import Printer as wxPrinter
from wx.html import HtmlEasyPrinting

__author__ = 'mbertens'

class HtmlPrinter( HtmlEasyPrinting ):
    def __init__(self):
        HtmlEasyPrinting.__init__( self )
        self.printer_config = wx.PrintData()
        self.printer_config.SetPaperId( wx.PAPER_A4 )
        self.printer_config.SetOrientation( wx.PORTRAIT )
        return
    # end def

    def GetHtmlText( self, text ):
        "Simple conversion of text.  Use a more powerful version"
        html_text = text.replace( '\n\n','<P>' ).replace( '\n', '<BR>' )
        return html_text
    # end def

    def Print( self, text, doc_name ):
        self.SetHeader( doc_name )
        self.PrintText( self.GetHtmlText( text ), doc_name )
        return
    # end def

    def PrintHtml( self, text, doc_name ):
        self.SetHeader( doc_name )
        self.PrintText( text, doc_name )
        return
    # end def

    def PreviewText( self, text, doc_name ):
        self.SetHeader( doc_name )
        HtmlEasyPrinting.PreviewText( self, text )
        return
    # end def
# end class

class Printer( wx.Printout ):
    def __init__( self, frame, text = "", name = "" ):
        "Prepares the Printing object.  Note: change current_y for 1, 1.5, 2 spacing for lines."
        wx.Printout.__init__( self )
        self.printer_config = wx.PrintData()
        self.printer_config.SetPaperId( wx.PAPER_A4 )
        self.printer_config.SetOrientation( wx.LANDSCAPE )
        self.frame      = frame
        self.doc_text   = text
        self.doc_name   = name
        self.current_y = 15  #y should be either (15, 22, 30)
        if self.current_y == 15:
            self.num_lines_per_page = 50
        elif self.current_y == 22:
            self.num_lines_per_page = 35
        else:
            self.num_lines_per_page = 25
        # end if
        return
    # end def

    def Print( self, text, doc_name ):
        "Prints the given text.  Currently doc_name logic doesn't exist.  E.g. might be useful for a footer.."
        self.doc_text = text
        self.doc_name = doc_name
        pdd = wx.PrintDialogData()
        pdd.SetPrintData( self.printer_config )
        printer = wxPrinter( pdd )
        if not printer.Print( self.frame,self ):
            wx.MessageBox("Unable to print the document.")
        else:
            self.printer_config = printer.GetPrintDialogData().GetPrintData()
        # end if
        return
    # end def

    def PreviewText(self, text, doc_name):
        "This function displays the preview window for the text with the given header."
        #try:
        self.doc_name = doc_name
        self.doc_text = text

        #Destructor fix by Peter Milliken -- with change to Printer.__init__()
        print1 = Printer(self.frame, text = self.doc_text, name = self.doc_name)
        print2 = Printer(self.frame, text = self.doc_text, name = self.doc_name)
        preview = wx.PrintPreview(print1, print2, self.printer_config)

        if not preview.Ok():
            wx.MessageBox("Unable to display preview of document.")
            return
        # end if
        preview_window = wx.PreviewFrame(preview, self.frame, \
                                        "Print Preview - %s" % doc_name)
        preview_window.Initialize()
        preview_window.SetPosition(self.frame.GetPosition())
        preview_window.SetSize(self.frame.GetSize())
        preview_window.MakeModal(True)
        preview_window.Show(True)
        #except:
        #    wx.MessageBox(GetErrorText())
        return
    # end def

    def PageSetup(self):
        "This function handles displaying the Page Setup window and retrieving the user selected options."
        config_dialog = wx.PageSetupDialog(self.frame)   #replaces PrintDialog
        config_dialog.GetPageSetupData()
        print self.printer_config
        config_dialog.ShowModal()
        self.printer_config = config_dialog.GetPageSetupData()
        print self.printer_config
        config_dialog.Destroy()
    # end def

    def OnBeginDocument(self,start,end):
        "Do any end of document logic here."
        wx.Printout.OnBeginDocument(self,start,end)
    # end def

    def OnEndDocument(self):
        "Do any end of document logic here."
        wx.Printout.OnEndDocument(self)
    # end def

    def OnBeginPrinting(self):
        "Do printing initialization logic here."
        wx.Printout.OnBeginPrinting(self)
    # end def

    def OnEndPrinting(self):
        "Do any post printing logic here."
        wx.Printout.OnEndPrinting(self)
    # end def

    def OnPreparePrinting(self):
        "Do any logic to prepare for printing here."
        wx.Printout.OnPreparePrinting(self)
    # end def

    def HasPage( self, page_num ):
        "This function is called to determine if the specified page exists."
        return len(self.GetPageText(page_num)) > 0
    # end def

    def GetPageInfo( self ):
        """
        This returns the page information: what is the page range available, and what is the selected page range.
        Currently the selected page range is always the available page range.  This logic should be changed if you need
        greater flexibility.
        """

        minPage = 1
        maxPage = int(len(self.doc_text.split('\n'))/self.num_lines_per_page)
        fromPage, toPage = minPage, maxPage
        return (minPage,maxPage,fromPage,toPage)
    # end def

    def OnPrintPage(self, page_num):
        "This function / event is executed for each page that needs to be printed."
        dc = self.GetDC()
        x,y = 25, self.current_y
        if not self.IsPreview():
            y *=4
        line_count = 1
        for line in self.GetPageText(page_num):
            dc.DrawText(line, x, y*line_count)
            line_count += 1
        # next
        return True
    # end def

    def GetPageText(self, page_num):
        "This function returns the text to be displayed for the given page number."
        lines = self.doc_text.split('\n')
        lines_for_page = lines[(page_num -1)*self.num_lines_per_page: page_num*(self.num_lines_per_page-1)]
        return lines_for_page
    # end def
# end class