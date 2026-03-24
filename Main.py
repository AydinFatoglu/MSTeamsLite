import wx
import wx.html2
import json
import os
DEFAULT_URL = "https://teams.microsoft.com"
PROFILE_DIR = os.path.join(os.environ.get("LOCALAPPDATA", ""), "vdi_teams", "EBWebView")
PREFERENCES  = os.path.join(PROFILE_DIR, "Default", "Preferences")
IZIN_ENTRY = {
    "https://teams.microsoft.com:443,*": {
        "last_modified": "13372291992000000",
        "setting": 1
    }
}
def set_webview2_permissions():
    if not os.path.exists(PREFERENCES):
        return  # Henüz oluşmamış, ilk açılışta oluşacak
    try:
        with open(PREFERENCES, "r", encoding="utf-8") as f:
            data = json.load(f)
        exceptions = data["profile"]["content_settings"]["exceptions"]
        exceptions["media_stream_camera"] = IZIN_ENTRY
        exceptions["media_stream_mic"]    = IZIN_ENTRY
        exceptions["sound"]               = IZIN_ENTRY
        exceptions["speaker_selection"]   = IZIN_ENTRY
        with open(PREFERENCES, "w", encoding="utf-8") as f:
            json.dump(data, f, separators=(",", ":"))
    except Exception:
        pass
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
        # Sayfa yüklendikten sonra izinleri yaz (WebView2 o an dosyayı bırakmış olur)
        set_webview2_permissions()
    def OnClose(self, event):
        # Kapanırken de yaz — bir sonraki açılış için garantile
        set_webview2_permissions()
        self.Destroy()
class App(wx.App):
    def OnInit(self):
        # Başlamadan önce varsa yaz
        set_webview2_permissions()
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
