import tkinter as tk
from tkinter import ttk, font, messagebox
import threading
import time
import os
import re
import requests
import sys
import configparser
import json
import keyboard  # pip install keyboard
import webbrowser
import base64

# --- SABİTLER VE VERSİYON ---
APP_VERSION = "v1.5"
REPO_OWNER = "FNFest-TR"
REPO_NAME = "FestiPath"
DEVELOPER_NAME = "ekicionur" 

# Linkler
LINK_GITHUB = f"https://github.com/{REPO_OWNER}/{REPO_NAME}"
LINK_TWITCH = "https://www.twitch.tv/ekicionur"
LINK_KICK = "https://kick.com/ekicionur"
LINK_HUB = "http://ekicionur.com.tr/"

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_PATH = os.path.expandvars(r'%localappdata%\FortniteGame\Saved\Logs\FortniteGame.log')
DATA_URL = "https://fnfpaths.github.io/fnfp.js"
MAPPING_URL = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/song_id.json"
UPDATE_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/latest"
IMG_BASE_URL = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/img/" 

CONFIG_FILE = os.path.join(BASE_DIR, 'config.ini')

# --- DİL VERİTABANI ---
LANGUAGES = {
    'tr': {
        'app_title': f'FestiPath {APP_VERSION}',
        'waiting': 'Şarkı Bekleniyor...',
        'ready': 'Hazır',
        'settings': 'Ayarlar',
        'font_size': 'Font Boyutu',
        'opacity': 'Şeffaflık',
        'bg_visible': 'Arka Plan',
        'language': 'Dil / Language',
        'close': 'Kapat',
        'no_data': 'Veri Yok',
        'path_not_found': 'Yol verisi bulunamadı.',
        'internet_error': 'Bağlantı Hatası',
        'server_error': 'Sunucu Hatası',
        'log_reading': 'Log Okunuyor...',
        'system_starting': 'Sistem Başlatılıyor...',
        'update_available': 'GÜNCELLEME VAR!',
        'hotkey_hide': 'Gizle/Göster Tuşu:',
        'hotkey_lock': 'Kilit (Sürükleme) Tuşu:',
        'locked': 'KİLİTLİ',
        'unlocked': 'AÇIK',
        'hotkey_waiting': 'Tuşa Basın...'
    },
    'en': {
        'app_title': f'FestiPath {APP_VERSION}',
        'waiting': 'Waiting for song...',
        'ready': 'Ready',
        'settings': 'Settings',
        'font_size': 'Font Size',
        'opacity': 'Opacity',
        'bg_visible': 'Background',
        'language': 'Language',
        'close': 'Close',
        'no_data': 'No Data',
        'path_not_found': 'Path data not found.',
        'internet_error': 'Connection Error',
        'server_error': 'Server Error',
        'log_reading': 'Reading Log...',
        'system_starting': 'System Starting...',
        'update_available': 'UPDATE AVAILABLE!',
        'hotkey_hide': 'Hide/Show Hotkey:',
        'hotkey_lock': 'Drag Lock Hotkey:',
        'locked': 'LOCKED',
        'unlocked': 'UNLOCKED',
        'hotkey_waiting': 'Press a key...'
    }
}

INSTRUMENT_MAP = {
    'Drums': 'd', 'Drum': 'd', 'Bass': 'b', 'Vocals': 'v', 'Vocal': 'v',
    'Guitar': 'l', 'Lead': 'l', 'PlasticGuitar': 'g', 'ProGuitar': 'g', 
    'PlasticBass': 'm', 'ProBass': 'm'      
}

DISPLAY_NAME_MAP = {
    'Guitar': 'Lead', 'Lead': 'Lead',
    'PlasticGuitar': 'Pro Guitar', 'ProGuitar': 'Pro Guitar',
    'PlasticBass': 'Pro Bass', 'ProBass': 'Pro Bass',
    'Bass': 'Bass', 'Drums': 'Drums', 'Drum': 'Drums', 
    'Vocals': 'Vocals', 'Vocal': 'Vocals'
}

ICON_FILES = {
    'Lead': 'lead.png', 'Pro Guitar': 'proguitar.png',
    'Pro Bass': 'probass.png', 'Bass': 'bass.png',
    'Drums': 'drums.png', 'Vocals': 'vocals.png'
}

class ConfigManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.defaults = {
            'font_size': '16', 'opacity': '0.9', 'bg_visible': 'True',
            'language': 'tr', 'x': '50', 'y': '50',
            'hotkey_hide': 'F8', 'hotkey_lock': 'F9'
        }
        self.load()

    def load(self):
        if os.path.exists(CONFIG_FILE):
            try:
                self.config.read(CONFIG_FILE)
                if 'SETTINGS' not in self.config:
                    self.config['SETTINGS'] = self.defaults
                    self.save()
            except: self.config['SETTINGS'] = self.defaults
        else:
            self.config['SETTINGS'] = self.defaults
            self.save()

    def get(self, key, type_func=str):
        try: return type_func(self.config['SETTINGS'].get(key, self.defaults.get(key, '')))
        except: return type_func(self.defaults.get(key, ''))

    def set(self, key, value):
        if 'SETTINGS' not in self.config: self.config['SETTINGS'] = {}
        self.config['SETTINGS'][key] = str(value)
        self.save()

    def save(self):
        try:
            with open(CONFIG_FILE, 'w') as f: self.config.write(f)
        except: pass

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent, config, update_callback, lang_dict):
        super().__init__(parent)
        self.config = config
        self.update_callback = update_callback
        self.lang = lang_dict
        self.title(self.lang['settings'])
        self.geometry("350x450")
        self.resizable(False, False)
        self.configure(bg="#2b2b2b")
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#2b2b2b", foreground="white", font=("Segoe UI", 10))
        
        ttk.Label(self, text=self.lang['language']).pack(pady=(10, 5))
        self.lang_var = tk.StringVar(value=self.config.get('language'))
        lang_frame = tk.Frame(self, bg="#2b2b2b")
        lang_frame.pack()
        tk.Radiobutton(lang_frame, text="Türkçe", variable=self.lang_var, value="tr", command=self.on_change, bg="#2b2b2b", fg="white", selectcolor="#444").pack(side='left', padx=10)
        tk.Radiobutton(lang_frame, text="English", variable=self.lang_var, value="en", command=self.on_change, bg="#2b2b2b", fg="white", selectcolor="#444").pack(side='left', padx=10)

        ttk.Label(self, text=self.lang['hotkey_hide']).pack(pady=(10, 5))
        self.hk_hide_btn = tk.Button(self, text=self.config.get('hotkey_hide').upper(), command=lambda: self.listen_hotkey('hotkey_hide', self.hk_hide_btn), bg="#444", fg="white", width=20, relief="flat")
        self.hk_hide_btn.pack()

        ttk.Label(self, text=self.lang['hotkey_lock']).pack(pady=(10, 5))
        self.hk_lock_btn = tk.Button(self, text=self.config.get('hotkey_lock').upper(), command=lambda: self.listen_hotkey('hotkey_lock', self.hk_lock_btn), bg="#444", fg="white", width=20, relief="flat")
        self.hk_lock_btn.pack()

        ttk.Label(self, text=self.lang['font_size']).pack(pady=(10, 5))
        self.font_scale = tk.Scale(self, from_=10, to=30, orient=tk.HORIZONTAL, command=self.on_change, bg="#2b2b2b", fg="white", highlightthickness=0)
        self.font_scale.set(self.config.get('font_size', int))
        self.font_scale.pack(fill='x', padx=40)

        ttk.Label(self, text=self.lang['opacity']).pack(pady=(10, 5))
        self.opacity_scale = tk.Scale(self, from_=20, to=100, orient=tk.HORIZONTAL, command=self.on_change, bg="#2b2b2b", fg="white", highlightthickness=0)
        self.opacity_scale.set(int(self.config.get('opacity', float) * 100))
        self.opacity_scale.pack(fill='x', padx=40)

        self.bg_var = tk.BooleanVar(value=self.config.get('bg_visible', lambda x: x == 'True'))
        tk.Checkbutton(self, text=self.lang['bg_visible'], variable=self.bg_var, command=self.on_change, bg="#2b2b2b", fg="white", selectcolor="#444", activebackground="#2b2b2b").pack(pady=15)

    def listen_hotkey(self, key_name, btn_widget):
        btn_widget.config(text=self.lang['hotkey_waiting'], bg="#d63031")
        self.update()
        key = keyboard.read_key()
        time.sleep(0.2)
        btn_widget.config(text=key.upper(), bg="#444")
        self.config.set(key_name, key)
        self.update_callback()

    def on_change(self, *args):
        self.config.set('font_size', self.font_scale.get())
        self.config.set('opacity', self.opacity_scale.get() / 100.0)
        self.config.set('bg_visible', self.bg_var.get())
        self.config.set('language', self.lang_var.get())
        self.update_callback()

class FestivalPathOverlay:
    def __init__(self, root):
        self.root = root
        self.cfg = ConfigManager()
        self.current_lang = self.cfg.get('language')
        self.L = LANGUAGES[self.current_lang]

        self.root.title(self.L['app_title'])
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', self.cfg.get('opacity', float))
        
        self.colors = {
            'bg': '#1e1e1e', 'panel': '#252526', 'accent': '#0984e3',
            'text': '#dfe6e9', 'warning': '#fdcb6e', 'danger': '#d63031', 'success': '#00b894',
            'link': '#74b9ff', 'link_hover': '#a29bfe',
            'score_bg': '#e67e22', # Turuncu Arkaplan
            'version': '#00d2d3'   # Turkuaz Versiyon Rengi
        }
        self.root.configure(bg=self.colors['bg'])
        self.root.attributes('-transparentcolor', '#000001')

        self.drag_locked = False
        self.is_visible = True
        self.js_data = ""
        self.song_mapping = {}
        self.current_song_id = None
        self.current_instrument = "Guitar"
        self.is_running = True
        self.icon_image = None
        self.settings_window = None
        self.img_cache = {}

        # --- ARAYÜZ YAPISI ---
        self.main_container = tk.Frame(self.root, bg=self.colors['panel'])
        self.main_container.pack(fill='both', expand=True, padx=2, pady=2)
        
        self.status_bar = tk.Frame(self.main_container, bg=self.colors['warning'], width=8)
        self.status_bar.pack(side='left', fill='y')

        self.content_frame = tk.Frame(self.main_container, bg=self.colors['panel'])
        self.content_frame.pack(side='left', fill='both', expand=True, padx=8, pady=5)

        # ÜST KISIM (Şarkı Adı)
        self.top_frame = tk.Frame(self.content_frame, bg=self.colors['panel'])
        self.top_frame.pack(fill='x')
        self.song_title_label = tk.Label(self.top_frame, text=self.L['system_starting'], font=("Segoe UI", 11, "bold"), fg=self.colors['text'], bg=self.colors['panel'], anchor='w')
        self.song_title_label.pack(side='left', fill='x', expand=True)

        # ORTA KISIM (Enstrüman, Skor)
        self.mid_frame = tk.Frame(self.content_frame, bg=self.colors['panel'])
        self.mid_frame.pack(fill='x', pady=2)
        
        self.icon_label = tk.Label(self.mid_frame, bg=self.colors['panel'])
        self.icon_label.pack(side='left')
        
        self.inst_label = tk.Label(self.mid_frame, text="", font=("Segoe UI", self.cfg.get('font_size', int), "bold"), fg=self.colors['accent'], bg=self.colors['panel'])
        self.inst_label.pack(side='left', padx=5)
        
        # SKOR LABEL (Turuncu Arkaplan, Beyaz Kalın Yazı)
        self.score_label = tk.Label(self.mid_frame, text="", font=("Consolas", 20, "bold"), fg="white", bg=self.colors['score_bg'], padx=5)
        self.score_label.pack(side='right')

        # PATH KISMI
        self.path_text = tk.Text(self.content_frame, height=1, font=("Consolas", self.cfg.get('font_size', int), "bold"), bg=self.colors['panel'], fg="white", borderwidth=0, highlightthickness=0)
        self.path_text.pack(fill="both", expand=True, pady=(5,0))

        # ALT KISIM (Footer: Linkler, Versiyon, Update)
        self.footer_frame = tk.Frame(self.content_frame, bg=self.colors['panel'])
        self.footer_frame.pack(side='bottom', fill='x', pady=(10, 0))

        # Update Uyarısı
        self.update_label = tk.Label(self.footer_frame, text=self.L['update_available'], font=("Segoe UI", 7, "bold"), fg="white", bg=self.colors['danger'], cursor="hand2")

        # Versiyon (Renkli)
        tk.Label(self.footer_frame, text=APP_VERSION, font=("Segoe UI", 8, "bold"), fg=self.colors['version'], bg=self.colors['panel']).pack(side='left')
        tk.Label(self.footer_frame, text=" | ", font=("Segoe UI", 8), fg="#636e72", bg=self.colors['panel']).pack(side='left')
        
        # Developer Name
        tk.Label(self.footer_frame, text=DEVELOPER_NAME, font=("Segoe UI", 8), fg="#b2bec3", bg=self.colors['panel']).pack(side='left')
        tk.Label(self.footer_frame, text=" | ", font=("Segoe UI", 8), fg="#636e72", bg=self.colors['panel']).pack(side='left')

        # Linkler
        self.create_link_label("Github", LINK_GITHUB).pack(side='left', padx=2)
        tk.Label(self.footer_frame, text="|", font=("Segoe UI", 8), fg="#636e72", bg=self.colors['panel']).pack(side='left', padx=2)
        self.create_link_label("Festival Hub", LINK_HUB).pack(side='left', padx=2)
        tk.Label(self.footer_frame, text="|", font=("Segoe UI", 8), fg="#636e72", bg=self.colors['panel']).pack(side='left', padx=2)
        self.create_link_label("Twitch", LINK_TWITCH).pack(side='left', padx=2)
        tk.Label(self.footer_frame, text="|", font=("Segoe UI", 8), fg="#636e72", bg=self.colors['panel']).pack(side='left', padx=2)
        self.create_link_label("Kick", LINK_KICK).pack(side='left', padx=2)

        self.setup_tags()
        self.apply_settings()
        self.bind_drag_events(self.root)
        
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label=self.L['settings'], command=self.open_settings)
        self.menu.add_separator()
        self.menu.add_command(label=self.L['close'], command=self.close_app)
        self.root.bind("<Button-3>", self.show_menu)

        threading.Thread(target=self.fetch_initial_data, daemon=True).start()
        threading.Thread(target=self.monitor_log, daemon=True).start()
        threading.Thread(target=self.check_updates, daemon=True).start()
        self.register_hotkeys()

        x = self.cfg.get('x', int)
        y = self.cfg.get('y', int)
        self.root.geometry(f"+{x}+{y}")
        self.auto_resize_window()

    def create_link_label(self, text, url):
        lbl = tk.Label(self.footer_frame, text=text, font=("Segoe UI", 8, "bold"), fg=self.colors['link'], bg=self.colors['panel'], cursor="hand2")
        lbl.bind("<Button-1>", lambda e: webbrowser.open(url))
        lbl.bind("<Enter>", lambda e: lbl.config(fg=self.colors['link_hover']))
        lbl.bind("<Leave>", lambda e: lbl.config(fg=self.colors['link']))
        return lbl

    def bind_drag_events(self, widget):
        if isinstance(widget, tk.Label) and widget.cget("cursor") == "hand2":
            return
        widget.bind("<ButtonPress-1>", self.start_move)
        widget.bind("<ButtonRelease-1>", self.stop_move)
        widget.bind("<B1-Motion>", self.do_move)
        for child in widget.winfo_children():
            self.bind_drag_events(child)

    def register_hotkeys(self):
        try:
            keyboard.unhook_all()
            hk_hide = self.cfg.get('hotkey_hide')
            hk_lock = self.cfg.get('hotkey_lock')
            if hk_hide: keyboard.add_hotkey(hk_hide, self.toggle_visibility)
            if hk_lock: keyboard.add_hotkey(hk_lock, self.toggle_lock)
        except: pass

    def toggle_visibility(self):
        if self.is_visible:
            self.root.withdraw()
            self.is_visible = False
        else:
            self.root.deiconify()
            self.is_visible = True

    def toggle_lock(self):
        self.drag_locked = not self.drag_locked
        if self.drag_locked:
            self.status_bar.config(bg="#d63031")
        else:
            self.status_bar.config(bg=self.colors['warning'] if self.song_title_label.cget('text') != self.L['ready'] else self.colors['success'])

    def auto_resize_window(self):
        self.root.update_idletasks()
        content = self.path_text.get("1.0", "end-1c")
        num_lines = content.count('\n') + 1 if content else 1
        text_font = font.Font(font=self.path_text['font'])
        line_height = text_font.metrics('linespace')
        req_text_height = (num_lines * line_height) + 10
        
        header_height = self.top_frame.winfo_reqheight() + self.mid_frame.winfo_reqheight()
        footer_height = self.footer_frame.winfo_reqheight()
        
        total_h = header_height + req_text_height + footer_height + 40
        current_w = 480 # Linkler arttığı için genişliği biraz artırdım
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        self.root.geometry(f"{current_w}x{total_h}+{x}+{y}")

    def configure_background(self, visible):
        bg = self.colors['panel'] if visible else '#000001'
        self.main_container.config(bg=bg)
        self.colors['panel'] = '#252526' if visible else '#000001'

        for widget in [self.content_frame, self.top_frame, self.mid_frame, 
                       self.song_title_label, self.icon_label, self.inst_label, 
                       self.path_text, self.footer_frame]:
            try: widget.config(bg=bg)
            except: pass
            
        # Skor label rengini koru
        try: self.score_label.config(bg=self.colors['score_bg'])
        except: pass
        
        # Linklerin ve textlerin arkaplanını da güncelle (ama yazı rengini bozma)
        for child in self.footer_frame.winfo_children():
            try: 
                if child != self.update_label:
                    child.config(bg=bg)
            except: pass

    def setup_tags(self):
        self.path_text.tag_config("R", foreground="#ff4757")
        self.path_text.tag_config("G", foreground="#2ed573")
        self.path_text.tag_config("Y", foreground="#ffa502")
        self.path_text.tag_config("B", foreground="#1e90ff")
        self.path_text.tag_config("O", foreground="#e67e22")
        self.path_text.tag_config("W", foreground="#f1f2f6")

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
            self.song_title_label.config(text=self.L['ready'])
            self.menu.entryconfigure(0, label=self.L['settings'])
            self.menu.entryconfigure(2, label=self.L['close'])
            self.update_label.config(text=self.L['update_available'])

        font_size = self.cfg.get('font_size', int)
        opacity = self.cfg.get('opacity', float)
        bg_visible = self.cfg.get('bg_visible', lambda x: x == 'True')

        self.path_text.configure(font=("Consolas", font_size, "bold"))
        self.inst_label.configure(font=("Segoe UI", font_size, "bold"))
        
        self.root.attributes('-alpha', opacity)
        self.configure_background(bg_visible)
        self.register_hotkeys()
        self.root.after(100, self.auto_resize_window)

    def start_move(self, event):
        if not self.drag_locked:
            self.offset_x = event.x
            self.offset_y = event.y

    def stop_move(self, event):
        if not self.drag_locked:
            self.offset_x = None
            self.offset_y = None
            self.cfg.set('x', self.root.winfo_x())
            self.cfg.set('y', self.root.winfo_y())

    def do_move(self, event):
        if not self.drag_locked and self.offset_x is not None:
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
        if not filename:
            self.icon_label.config(image='')
            return
        if display_name in self.img_cache:
            self.icon_image = self.img_cache[display_name]
            self.icon_label.config(image=self.icon_image)
            return

        url = IMG_BASE_URL + filename
        def fetch_image():
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = base64.encodebytes(response.content)
                    img = tk.PhotoImage(data=data)
                    if img.width() > 48: img = img.subsample(2, 2)
                    self.img_cache[display_name] = img
                    self.root.after(0, lambda: self._set_icon(img))
            except: pass
        threading.Thread(target=fetch_image, daemon=True).start()

    def _set_icon(self, img):
        self.icon_image = img
        self.icon_label.config(image=img)

    def fetch_initial_data(self):
        try:
            m_resp = requests.get(MAPPING_URL, timeout=5)
            if m_resp.status_code == 200: self.song_mapping = json.loads(m_resp.text)
        except: pass

        try:
            resp = requests.get(DATA_URL, timeout=10)
            if resp.status_code == 200:
                self.js_data = resp.text
                self.set_status('ready')
            else: self.set_status('server_error')
        except: self.set_status('internet_error')

    def check_updates(self):
        try:
            resp = requests.get(UPDATE_API_URL, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('tag_name', '') != APP_VERSION:
                    self.root.after(0, lambda: self.show_update_notification(data.get('html_url')))
        except: pass

    def show_update_notification(self, url):
        self.update_label.pack(side='right', padx=5)
        self.update_label.bind("<Button-1>", lambda e: webbrowser.open(url))
        self.auto_resize_window()

    def set_status(self, status_key, extra_text=""):
        text = self.L.get(status_key, status_key) + extra_text
        color = self.colors['warning']
        if status_key == 'ready': color = self.colors['success']
        elif 'error' in status_key: color = self.colors['danger']
        self.root.after(0, lambda: self._update_ui_status(text, color))

    def _update_ui_status(self, text, color):
        self.song_title_label.config(text=text)
        if not self.drag_locked: self.status_bar.config(bg=color)

    def clean_id(self, raw):
        cleaned = str(raw).lower().replace("sparks_song_", "").replace("sparkssong:", "").replace(" ", "").strip()
        return self.song_mapping.get(cleaned, cleaned)

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

        return full_name, p_match.group(1) if p_match else "", s_match.group(1) if s_match else "0"

    def update_gui(self, inst_raw, full_name, path, score):
        display_name = DISPLAY_NAME_MAP.get(inst_raw, inst_raw)
        self.load_icon(display_name)
        self.inst_label.config(text=display_name)
        self.song_title_label.config(text=full_name)
        
        if not self.drag_locked: self.status_bar.config(bg=self.colors['accent'])
        try: self.score_label.config(text=f"{int(score):,}")
        except: self.score_label.config(text=score)
        
        self.path_text.config(state=tk.NORMAL)
        self.path_text.delete("1.0", tk.END)
        
        if path:
            formatted_path = path.replace(", ", "\n").replace(",", "\n")
            lines = formatted_path.split('\n')
            for line in lines:
                parts = re.split(r'([RGBYO])', line)
                for part in parts:
                    if part in ["R", "G", "Y", "B", "O"]: self.path_text.insert(tk.END, part, part)
                    else: self.path_text.insert(tk.END, part, "W")
                self.path_text.insert(tk.END, "\n")
        else:
            self.path_text.insert(tk.END, self.L['path_not_found'], "W")
        
        self.path_text.config(state=tk.DISABLED)
        self.auto_resize_window()

    def monitor_log(self):
        while not os.path.exists(LOG_PATH) and self.is_running:
            time.sleep(1)
            self.set_status('waiting', " (Log Aranıyor)")
        self.set_status('ready')

        try:
            with open(LOG_PATH, 'r', encoding='utf-8', errors='ignore') as f:
                f.seek(0, 2)
                while self.is_running:
                    line = f.readline()
                    if not line:
                        time.sleep(0.1)
                        continue
                    if 'received song to play:' in line:
                        try:
                            self.current_song_id = line.split('received song to play: ')[1].split(' - ')[0].strip()
                            self.trigger()
                        except: pass
                    elif 'SparksSong:' in line:
                        try:
                            self.current_song_id = line.split('SparksSong:')[1].strip()
                            self.trigger()
                        except: pass
                    match = re.search(r"TrackType::Track(\w+)", line)
                    if match:
                        raw_inst = match.group(1)
                        if raw_inst != "Type" and raw_inst != self.current_instrument:
                            self.current_instrument = raw_inst 
                            self.trigger()
        except: pass

    def trigger(self):
        if self.current_song_id:
            inst = self.current_instrument if self.current_instrument else "Guitar"
            full_name, path, score = self.parse_full_info(self.current_song_id, inst)
            self.root.after(0, lambda: self.update_gui(inst, full_name, path, score))

if __name__ == "__main__":
    root = tk.Tk()
    app = FestivalPathOverlay(root)
    root.mainloop()
