import wx
import wx.html2
import wx.adv
import json
import os
import sys

DEFAULT_URL = "https://teams.microsoft.com"
PROFILE_DIR = os.path.join(os.environ.get("LOCALAPPDATA", ""), "vdi_teams", "EBWebView")
PREFERENCES = os.path.join(PROFILE_DIR, "Default", "Preferences")

IZIN_ENTRY = {
    "https://teams.microsoft.com:443,*": {
        "last_modified": "13372291992000000",
        "setting": 1
    }
}


def get_resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


def get_icon():
    try:
        path = get_resource_path("microsoft_office_teams_logo_icon_145726(2).ico")
        if os.path.exists(path):
            return wx.Icon(path, wx.BITMAP_TYPE_ICO)
    except Exception:
        pass
    return wx.NullIcon


def set_webview2_permissions():
    if not os.path.exists(PREFERENCES):
        return
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

        icon = get_icon()
        if icon != wx.NullIcon:
            self.SetIcon(icon)

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

        self._init_tray(icon)

    def _init_tray(self, icon):
        self.tray = wx.adv.TaskBarIcon()
        if icon != wx.NullIcon:
            self.tray.SetIcon(icon, "Teams Launcher")
        self.tray.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.OnTrayLeftDClick)
        self.tray.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP,    self.OnTrayRightClick)

    def OnTrayLeftDClick(self, _event):
        self._show_window()

    def OnTrayRightClick(self, _event):
        menu = wx.Menu()
        item_show  = menu.Append(wx.ID_ANY, "Göster")
        item_close = menu.Append(wx.ID_ANY, "Kapat")
        self.tray.Bind(wx.EVT_MENU, lambda e: self._show_window(), item_show)
        self.tray.Bind(wx.EVT_MENU, lambda e: self._exit(),        item_close)
        self.tray.PopupMenu(menu)
        menu.Destroy()

    def _show_window(self):
        self.Iconize(False)
        self.Raise()

    def _exit(self):
        set_webview2_permissions()
        self.tray.RemoveIcon()
        self.tray.Destroy()
        self.Destroy()

    def OnLoaded(self, _event):
        title = self.browser.GetCurrentTitle()
        url   = self.browser.GetCurrentURL()
        self.SetTitle(title if title else url)
        set_webview2_permissions()

    def OnClose(self, _event):
        self.Iconize(True)


class App(wx.App):
    def OnInit(self):
        set_webview2_permissions()
        frame = BrowserFrame(
            None,
            title="Teams Launcher",
            size=(1280, 800)
        )
        frame.Show()
        return True


if __name__ == "__main__":
    app = App()
    app.MainLoop()
