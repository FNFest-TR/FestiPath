import tkinter as tk
from tkinter import ttk, font
import threading
import time
import os
import re
import requests
import sys
import configparser

# --- SABİTLER ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.expandvars(r'%localappdata%\FortniteGame\Saved\Logs\FortniteGame.log')
DATA_URL = "https://fnfpaths.github.io/fnfp.js"
CONFIG_FILE = os.path.join(BASE_DIR, 'config.ini')
IMG_DIR = os.path.join(BASE_DIR, 'img')

# --- DİL VERİTABANI ---
LANGUAGES = {
    'tr': {
        'app_title': 'FN Festival Path Overlay',
        'waiting': 'Şarkı Bekleniyor...',
        'ready': 'Hazır',
        'settings': 'Ayarlar',
        'font_size': 'Font Boyutu',
        'opacity': 'Şeffaflık',
        'bg_visible': 'Arka Planı Koyulaştır',
        'language': 'Dil / Language',
        'close': 'Kapat',
        'no_data': 'Veri Yok',
        'path_not_found': 'Yol verisi bulunamadı.',
        'internet_error': 'İnternet Yok',
        'server_error': 'Sunucu Hatası',
        'log_reading': 'Log Okunuyor...',
        'system_starting': 'Sistem Başlatılıyor...'
    },
    'en': {
        'app_title': 'FN Festival Path Overlay',
        'waiting': 'Waiting for song...',
        'ready': 'Ready',
        'settings': 'Settings',
        'font_size': 'Font Size',
        'opacity': 'Opacity',
        'bg_visible': 'Darken Background',
        'language': 'Language',
        'close': 'Close',
        'no_data': 'No Data',
        'path_not_found': 'Path data not found.',
        'internet_error': 'No Internet',
        'server_error': 'Server Error',
        'log_reading': 'Reading Log...',
        'system_starting': 'System Starting...'
    }
}

# Enstrüman Kod Haritası
INSTRUMENT_MAP = {
    'Drums': 'd', 'Drum': 'd',
    'Bass': 'b',
    'Vocals': 'v', 'Vocal': 'v',
    'Guitar': 'l', 'Lead': 'l',   
    'PlasticGuitar': 'g', 'ProGuitar': 'g', 
    'PlasticBass': 'm', 'ProBass': 'm'      
}

# Görünen İsim Haritası
DISPLAY_NAME_MAP = {
    'Guitar': 'Lead', 'Lead': 'Lead',
    'PlasticGuitar': 'Pro Guitar', 'ProGuitar': 'Pro Guitar',
    'PlasticBass': 'Pro Bass', 'ProBass': 'Pro Bass',
    'Bass': 'Bass', 'Drums': 'Drums', 'Vocals': 'Vocals'
}

# İkon Dosyaları
ICON_FILES = {
    'Lead': 'lead.png', 'Pro Guitar': 'proguitar.png',
    'Pro Bass': 'probass.png', 'Bass': 'bass.png',
    'Drums': 'drums.png', 'Vocals': 'vocals.png'
}

class ConfigManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.defaults = {
            'font_size': '16',
            'opacity': '1.0',
            'bg_visible': 'False',
            'language': 'tr',
            'x': '50',
            'y': '50'
        }
        self.load()

    def load(self):
        if os.path.exists(CONFIG_FILE):
            self.config.read(CONFIG_FILE)
        else:
            self.config['SETTINGS'] = self.defaults
            self.save()

    def get(self, key, type_func=str):
        try: return type_func(self.config['SETTINGS'].get(key, self.defaults[key]))
        except: return type_func(self.defaults[key])

    def set(self, key, value):
        if 'SETTINGS' not in self.config: self.config['SETTINGS'] = {}
        self.config['SETTINGS'][key] = str(value)
        self.save()

    def save(self):
        with open(CONFIG_FILE, 'w') as f: self.config.write(f)

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent, config, update_callback, lang_dict):
        super().__init__(parent)
        self.config = config
        self.update_callback = update_callback
        self.lang = lang_dict
        self.title(self.lang['settings'])
        self.geometry("300x300")
        self.resizable(False, False)
        
        # Dil Seçimi
        tk.Label(self, text=self.lang['language']).pack(pady=(10, 0))
        self.lang_var = tk.StringVar(value=self.config.get('language'))
        lang_frame = tk.Frame(self)
        lang_frame.pack()
        tk.Radiobutton(lang_frame, text="Türkçe", variable=self.lang_var, value="tr", command=self.on_change).pack(side='left')
        tk.Radiobutton(lang_frame, text="English", variable=self.lang_var, value="en", command=self.on_change).pack(side='left')

        # Font Boyutu
        tk.Label(self, text=self.lang['font_size']).pack(pady=(10, 0))
        self.font_scale = tk.Scale(self, from_=10, to=40, orient=tk.HORIZONTAL, command=self.on_change)
        self.font_scale.set(self.config.get('font_size', int))
        self.font_scale.pack(fill='x', padx=20)

        # Şeffaflık
        tk.Label(self, text=self.lang['opacity']).pack(pady=(10, 0))
        self.opacity_scale = tk.Scale(self, from_=20, to=100, orient=tk.HORIZONTAL, command=self.on_change)
        self.opacity_scale.set(int(self.config.get('opacity', float) * 100))
        self.opacity_scale.pack(fill='x', padx=20)

        # Arkaplan
        self.bg_var = tk.BooleanVar(value=self.config.get('bg_visible', lambda x: x == 'True'))
        tk.Checkbutton(self, text=self.lang['bg_visible'], variable=self.bg_var, command=self.on_change).pack(pady=15)

    def on_change(self, *args):
        font_size = self.font_scale.get()
        opacity = self.opacity_scale.get() / 100.0
        bg_visible = self.bg_var.get()
        language = self.lang_var.get()

        self.config.set('font_size', font_size)
        self.config.set('opacity', opacity)
        self.config.set('bg_visible', bg_visible)
        self.config.set('language', language)

        self.update_callback()

class FestivalPathOverlay:
    def __init__(self, root):
        self.root = root
        self.cfg = ConfigManager()
        
        self.current_lang = self.cfg.get('language')
        self.L = LANGUAGES[self.current_lang]

        self.root.title(self.L['app_title'])
        x = self.cfg.get('x', int)
        y = self.cfg.get('y', int)
        self.root.geometry(f"400x150+{x}+{y}")

        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.configure_background(self.cfg.get('bg_visible', lambda x: x == 'True'))
        self.root.attributes('-alpha', self.cfg.get('opacity', float))

        self.js_data = ""
        self.current_song_id = None
        self.current_instrument = "Guitar"
        self.is_running = True
        self.icon_image = None
        self.settings_window = None

        # --- ARAYÜZ ---
        self.song_title_label = tk.Label(self.root, text=self.L['system_starting'], 
                                         font=("Segoe UI", 12), 
                                         fg="#cccccc", bg=self.root['bg'], wraplength=380, justify="left")
        self.song_title_label.pack(fill='x', padx=10, pady=(5, 0))

        self.header_frame = tk.Frame(self.root, bg=self.root['bg'])
        self.header_frame.pack(fill='x', padx=10, pady=0)

        self.icon_label = tk.Label(self.header_frame, bg=self.root['bg'])
        self.icon_label.pack(side='left')

        self.inst_label = tk.Label(self.header_frame, text="", 
                                   font=("Segoe UI", self.cfg.get('font_size', int), "bold", "underline"), 
                                   fg="white", bg=self.root['bg'])
        self.inst_label.pack(side='left', padx=5)

        self.score_label = tk.Label(self.header_frame, text="", 
                                    font=("Segoe UI", self.cfg.get('font_size', int), "bold"), 
                                    fg="white", bg="#6a0dad", padx=5)
        self.score_label.pack(side='right')

        self.path_text = tk.Text(self.root, 
                                 font=("Consolas", self.cfg.get('font_size', int), "bold"), 
                                 bg=self.root['bg'], fg="white", 
                                 borderwidth=0, highlightthickness=0)
        self.path_text.pack(fill="both", expand=True, padx=10, pady=5)

        self.setup_tags()

        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<ButtonRelease-1>", self.stop_move)
        self.root.bind("<B1-Motion>", self.do_move)

        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label=self.L['settings'], command=self.open_settings)
        self.menu.add_separator()
        self.menu.add_command(label=self.L['close'], command=self.close_app)
        self.root.bind("<Button-3>", self.show_menu)

        threading.Thread(target=self.fetch_js_data, daemon=True).start()
        threading.Thread(target=self.monitor_log, daemon=True).start()

    def configure_background(self, visible):
        self.bg_color = "#111111" if visible else "black"
        self.root.configure(bg=self.bg_color)
        self.root.attributes('-transparentcolor', 'black')
        try:
            self.header_frame.config(bg=self.bg_color)
            self.icon_label.config(bg=self.bg_color)
            self.inst_label.config(bg=self.bg_color)
            self.path_text.config(bg=self.bg_color)
            self.song_title_label.config(bg=self.bg_color)
        except: pass

    def setup_tags(self):
        self.path_text.tag_config("R", foreground="#FF4444")
        self.path_text.tag_config("G", foreground="#44FF44")
        self.path_text.tag_config("Y", foreground="#FFFF44")
        self.path_text.tag_config("B", foreground="#4444FF")
        self.path_text.tag_config("O", foreground="#FFA500")
        self.path_text.tag_config("W", foreground="white")

    def open_settings(self):
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.lift()
        else:
            self.settings_window = SettingsWindow(self.root, self.cfg, self.apply_settings, self.L)

    def apply_settings(self):
        new_lang = self.cfg.get('language')
        if new_lang != self.current_lang:
            self.current_lang = new_lang
            self.L = LANGUAGES[new_lang]
            self.root.title(self.L['app_title'])
            
            # Menüyü güncelle
            self.menu.entryconfigure(0, label=self.L['settings'])
            self.menu.entryconfigure(2, label=self.L['close'])
            
            if self.settings_window:
                self.settings_window.destroy()
                self.open_settings()

        font_size = self.cfg.get('font_size', int)
        opacity = self.cfg.get('opacity', float)
        bg_visible = self.cfg.get('bg_visible', lambda x: x == 'True')

        new_font = ("Consolas", font_size, "bold")
        title_font = ("Segoe UI", font_size, "bold", "underline")
        self.path_text.configure(font=new_font)
        self.inst_label.configure(font=title_font)
        self.score_label.configure(font=("Segoe UI", font_size, "bold"))
        self.song_title_label.configure(font=("Segoe UI", int(font_size * 0.75)))

        self.root.attributes('-alpha', opacity)
        self.configure_background(bg_visible)
        self.auto_resize_window()

    def auto_resize_window(self):
        self.root.update_idletasks()
        header_h = self.song_title_label.winfo_reqheight() + self.header_frame.winfo_reqheight()
        num_lines = int(self.path_text.index('end-1c').split('.')[0])
        text_font = font.Font(font=self.path_text['font'])
        line_height = text_font.metrics('linespace')
        text_h = (num_lines * line_height) + 20
        min_h = 100
        total_h = max(min_h, header_h + text_h + 20)
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        self.root.geometry(f"400x{total_h}+{x}+{y}")

    def start_move(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def stop_move(self, event):
        self.offset_x = None
        self.offset_y = None
        self.cfg.set('x', self.root.winfo_x())
        self.cfg.set('y', self.root.winfo_y())

    def do_move(self, event):
        x = self.root.winfo_x() + (event.x - self.offset_x)
        y = self.root.winfo_y() + (event.y - self.offset_y)
        self.root.geometry(f"+{x}+{y}")

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def close_app(self):
        self.is_running = False
        self.root.destroy()
        sys.exit()

    def load_icon(self, display_name):
        filename = ICON_FILES.get(display_name)
        if filename:
            path = os.path.join(IMG_DIR, filename)
            if os.path.exists(path):
                try:
                    img = tk.PhotoImage(file=path)
                    if img.width() > 64: img = img.subsample(2, 2)
                    self.icon_image = img
                    self.icon_label.config(image=img)
                    return
                except: pass
        self.icon_label.config(image='')
        self.icon_image = None

    def fetch_js_data(self):
        try:
            resp = requests.get(DATA_URL, timeout=10)
            if resp.status_code == 200:
                self.js_data = resp.text
                self.root.after(0, lambda: self.song_title_label.config(text=self.L['waiting']))
            else:
                self.root.after(0, lambda: self.song_title_label.config(text=self.L['server_error']))
        except:
            self.root.after(0, lambda: self.song_title_label.config(text=self.L['internet_error']))

    def clean_id(self, raw):
        return str(raw).lower().replace("sparks_song_", "").replace("sparkssong:", "").replace(" ", "").strip()

    def parse_full_info(self, song_id, instrument_raw):
        if not self.js_data: return self.L['no_data'], self.L['no_data'], "0"

        display_name = DISPLAY_NAME_MAP.get(instrument_raw, instrument_raw)
        inst_code = INSTRUMENT_MAP.get(instrument_raw, 'l') 
        target_short = self.clean_id(song_id)
        
        pattern = re.compile(r'shortname\s*:\s*["\']' + re.escape(target_short) + r'["\']', re.IGNORECASE)
        match = pattern.search(self.js_data)

        if not match: return target_short, self.L['path_not_found'], "0"

        curr_pos = match.start()
        
        search_window_back = self.js_data[max(0, curr_pos-600):curr_pos]
        value_match = re.search(r'value\s*:\s*["\'](.*?)["\']', search_window_back, re.S)
        full_name = value_match.group(1) if value_match else target_short.upper()

        search_window_fwd = self.js_data[curr_pos:curr_pos+3000]
        path_regex = re.compile(rf'{inst_code}path\s*:\s*["\'](.*?)["\']')
        score_regex = re.compile(rf'{inst_code}score\s*:\s*["\'](.*?)["\']')

        p_match = path_regex.search(search_window_fwd)
        s_match = score_regex.search(search_window_fwd)

        path_val = p_match.group(1) if p_match else ""
        score_val = s_match.group(1) if s_match else "0"

        return full_name, path_val, score_val

    def update_gui(self, inst_raw, full_name, path, score):
        display_name = DISPLAY_NAME_MAP.get(inst_raw, inst_raw)
        
        self.load_icon(display_name)
        self.inst_label.config(text=display_name)
        self.song_title_label.config(text=full_name)
        
        try: fmt_score = f"{int(score):,}"
        except: fmt_score = score
        self.score_label.config(text=fmt_score)
        
        self.path_text.config(state=tk.NORMAL)
        self.path_text.delete("1.0", tk.END)
        
        if path:
            formatted_path = path.replace(", ", "\n").replace(",", "\n")
            lines = formatted_path.split('\n')
            for line in lines:
                parts = re.split(r'([RGBYO])', line)
                for part in parts:
                    if part in ["R", "G", "Y", "B", "O"]:
                        self.path_text.insert(tk.END, part, part)
                    else:
                        self.path_text.insert(tk.END, part, "W")
                self.path_text.insert(tk.END, "\n")
        else:
            self.path_text.insert(tk.END, self.L['path_not_found'], "W")
        
        self.path_text.config(state=tk.DISABLED)
        self.auto_resize_window()

    def monitor_log(self):
        while not os.path.exists(LOG_PATH) and self.is_running:
            time.sleep(1)
        
        with open(LOG_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            f.seek(0, 2)
            while self.is_running:
                line = f.readline()
                if not line:
                    time.sleep(0.1)
                    continue

                if 'received song to play:' in line:
                    try:
                        raw = line.split('received song to play: ')[1]
                        self.current_song_id = raw.split(' - ')[0].strip()
                        self.trigger()
                    except: pass
                
                elif 'SparksSong:' in line:
                    try:
                        self.current_song_id = line.split('SparksSong:')[1].strip()
                        self.trigger()
                    except: pass

                # Enstrümanı agresif yakala: "TrackType::Track..." (Örn: ::TrackGuitar)
                match = re.search(r"TrackType::Track(\w+)", line)
                if match:
                    raw_inst = match.group(1)
                    # "Type" hatasını önlemek için kontrol
                    if raw_inst != "Type" and raw_inst != self.current_instrument:
                        self.current_instrument = raw_inst
                        self.trigger()

    def trigger(self):
        if self.current_song_id:
            inst = self.current_instrument if self.current_instrument else "Guitar"
            full_name, path, score = self.parse_full_info(self.current_song_id, inst)
            self.root.after(0, lambda: self.update_gui(inst, full_name, path, score))

if __name__ == "__main__":
    root = tk.Tk()
    app = FestivalPathOverlay(root)
    root.mainloop()