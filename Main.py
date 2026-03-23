import wx
import wx.html2

DEFAULT_URL = "https://teams.microsoft.com"


class BrowserFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        style = wx.DEFAULT_FRAME_STYLE | wx.CLIP_CHILDREN
        super().__init__(*args, style=style, **kwargs)

        if not wx.html2.WebView.IsBackendAvailable(wx.html2.WebViewBackendEdge):
            wx.MessageBox(
                "Bu uygulama WebView2 Runtime gerektirmektedir.\n\n"
                "Lütfen Microsoft Edge veya WebView2 Runtime'ı yükleyin.\n"
                "https://developer.microsoft.com/en-us/microsoft-edge/webview2/",
                "WebView2 Bulunamadı",
                wx.ICON_ERROR | wx.OK
            )
            self.Destroy()
            return

        self.browser = wx.html2.WebView.New(
            self,
            backend=wx.html2.WebViewBackendEdge
        )
        self.browser.LoadURL(DEFAULT_URL)
        self.Bind(wx.html2.EVT_WEBVIEW_LOADED, self.OnLoaded)
        self.SetTitle("Yükleniyor...")
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Centre()

    def OnLoaded(self, event):
        title = self.browser.GetCurrentTitle()
        url   = self.browser.GetCurrentURL()
        self.SetTitle(title if title else url)

    def OnClose(self, event):
        self.Destroy()


class App(wx.App):
    def OnInit(self):
        frame = BrowserFrame(
            None,
            title="Launcher",
            size=(1280, 800)
        )
        frame.Show()
        return True


if __name__ == "__main__":
    app = App()
    app.MainLoop()
