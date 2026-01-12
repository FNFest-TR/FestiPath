# 🎵 FN Festival Path Overlay

**[English]** A lightweight, transparent Python overlay for **Fortnite Festival**. It reads the game logs in real-time to detect the currently playing song and instrument, then fetches and displays the optimal Overdrive path data directly on your screen.

**[Türkçe]** **Fortnite Festival** modu için geliştirilmiş hafif ve şeffaf bir Python katmanı (overlay). Oyun loglarını gerçek zamanlı okuyarak çalan şarkıyı ve enstrümanı algılar, ardından optimal "Overdrive" yol verilerini ekrana yansıtır.

---

## 🌟 Features / Özellikler

### English
* **Real-time Detection:** Automatically detects the song and instrument via `FortniteGame.log`.
* **Live Path Display:** Shows when to activate Overdrive using color-coded text (R, G, Y, B, O).
* **Customizable UI:**
    * Adjust font size and window opacity.
    * Toggle background darkening for better readability.
    * Draggable window (Click & Drag).
* **Dual Language:** Supports English and Turkish interfaces.
* **Always on Top:** Stays over the game window (Borderless Fullscreen recommended).

### Türkçe
* **Gerçek Zamanlı Algılama:** `FortniteGame.log` üzerinden şarkıyı ve enstrümanı otomatik algılar.
* **Canlı Yol Gösterimi:** Overdrive'ın ne zaman basılacağını renk kodlarıyla (R, G, Y, B, O) gösterir.
* **Özelleştirilebilir Arayüz:**
    * Yazı boyutu ve şeffaflık ayarı.
    * Okunabilirlik için arka planı koyulaştırma seçeneği.
    * Sürüklenebilir pencere (Tıkla & Sürükle).
* **Çift Dil Desteği:** Türkçe ve İngilizce arayüz seçenekleri.
* **Her Zaman Üstte:** Oyun penceresinin üzerinde durur (Penceresiz Tam Ekran önerilir).

---

## 🛠️ Installation & Usage / Kurulum ve Kullanım

### Requirements / Gereksinimler
* Windows OS
* Python 3.x
* Game running in **Windowed Fullscreen** or **Windowed** mode.

### Setup / Kurulum

1.  **Clone or Download** this repository.
    * Projeyi indirin veya klonlayın.
2.  **Install Dependencies:**
    * Gerekli kütüphaneyi yükleyin:
    ```bash
    pip install requests
    ```
3.  **Image Assets (Optional):**
    * Create a folder named `img` in the script directory.
    * Add icons named: `lead.png`, `drums.png`, `vocals.png`, `bass.png`, `proguitar.png`, `probass.png`.
    * *(Opsiyonel)* Scriptin olduğu yere `img` klasörü açın ve içine enstrüman ikonlarını ekleyin.
4.  **Run the Script:**
    * Scripti çalıştırın:
    ```bash
    python path.pyw
    ```

### Controls / Kontroller
* **Left Click & Drag:** Move the overlay.
* **Right Click:** Open Settings / Close App.
* **Sol Tık & Sürükle:** Pencerenin yerini değiştirir.
* **Sağ Tık:** Ayarlar menüsünü açar / Uygulamayı kapatır.

---

## ⚠️ Disclaimer / Yasal Uyarı

**[EN]** This tool is an external overlay that only reads local log files (`FortniteGame.log`) and fetches public data from the internet. It does **not** inject code into the game memory or modify game files. However, use it at your own risk. The developer is not responsible for any bans or penalties.

**[TR]** Bu araç, sadece yerel log dosyalarını (`FortniteGame.log`) okuyan ve internetten veri çeken harici bir katmandır. Oyun hafızasına (memory) müdahale etmez veya oyun dosyalarını değiştirmez. Yine de kullanım riski size aittir. Geliştirici, olası yasaklanma veya cezalardan sorumlu değildir.

---

## 🙏 Credits

Data provided by [fnfpaths](https://fnfpaths.github.io/).
