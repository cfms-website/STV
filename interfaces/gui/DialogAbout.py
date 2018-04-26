import wx.adv


class DialogAbout:
    def __init__(self, parent):
        about_info = wx.adv.AboutDialogInfo()
        about_info.SetName("CFMS Election Tabulator")
        about_info.SetVersion("1.0")
        about_info.SetDescription("Displays and tabulates voter ballots utilizing a single transferable vote system\n"
                                  "with support for custom election configurations and dynamic ballot format parsing.")
        about_info.SetCopyright("This software is derived from the work of UCSB AS and is intended for internal CFMS "
                                "use only.")
        about_info.SetWebSite("https://www.cfms.org/")
        about_info.AddDeveloper("Pavel Yarmak <it@cfms.org>")

        wx.adv.AboutBox(about_info, parent)
