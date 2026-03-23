# MSTeamsLite

VDI Teams Launcher, kurumsal sanal masaüstü (VDI) ortamlarında Microsoft Teams'i doğrudan ve hafif bir pencere içinde açmak için geliştirilmiş bir araçtır.
 
Uygulama, Microsoft'un modern web motoru olan WebView2 (Edge/Chromium) üzerine inşa edilmiştir. Bu sayede Teams, ayrı ve ağır bir uygulama kurulumu gerektirmeden, tam işlevsel bir tarayıcı motoru üzerinden çalışır. Giriş bilgileri ve oturum verileri WebView2'nin izole profil alanında saklandığından kullanıcılar her açılışta yeniden giriş yapmak zorunda kalmaz.
 
Uygulama açılırken önce sistemde WebView2 Runtime'ın yüklü olup olmadığını kontrol eder. Eğer bulunamazsa kullanıcıyı bilgilendirerek kapatılır. WebView2, Windows 11 ve güncel Windows 10 sistemlerinde zaten yüklü geldiğinden kurumsal ortamlarda ek bir kurulum adımı gerekmez.
 
Mikrofon ve kamera izinleri WebView2 tarafından native olarak yönetilir. İlk kullanımda sistem izin popup'ı gösterir, kullanıcı onayladıktan sonra bu tercih kalıcı olarak kaydedilir.
 
Uygulama tek bir Python dosyasından oluşur, bağımlılıkları minimumdur ve PyInstaller ile kolayca EXE formatına dönüştürülebilir.
