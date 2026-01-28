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
import keyboard
import webbrowser
import base64
import warnings
import io

# --- HARİCİ KÜTÜPHANELER ---
# Bu sürüm Google Translate altyapısı için gTTS kullanır.
try:
    from gtts import gTTS
except ImportError:
    messagebox.showerror("Eksik Kütüphane", "Lütfen 'gTTS' kütüphanesini yükleyin.\nKomut: pip install gTTS")
    sys.exit()

# --- SİSTEM AYARLARI ---
warnings.filterwarnings("ignore")
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# --- SABİTLER ---
APP_VERSION = "v2.2"
REPO_OWNER = "FNFest-TR"
REPO_NAME = "FestiPath"
DEVELOPER_NAME = "ekicionur"

LINK_GITHUB = f"https://github.com/{REPO_OWNER}/{REPO_NAME}"
LINK_TWITCH = "https://www.twitch.tv/ekicionur"
LINK_KICK = "https://kick.com/ekicionur"
LINK_HUB = "http://ekicionur.com.tr/"
UPDATE_JSON_URL = "https://raw.githubusercontent.com/FNFest-TR/FestiPath/refs/heads/main/update.json"

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

LOG_PATH = os.path.expandvars(r'%localappdata%\FortniteGame\Saved\Logs\FortniteGame.log')
DATA_URL = "https://fnfpaths.github.io/fnfp.js"
MAPPING_URL = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/song_id.json"
IMG_BASE_URL = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/img/"
CONFIG_FILE = os.path.join(BASE_DIR, 'config.ini')

# --- RENK PALETLERİ ---
COLOR_PALETTES = {
    'Normal':       {'G': '#00ff00', 'R': '#ff0000', 'Y': '#ffff00', 'B': '#5656ff', 'O': '#ffa500'},
    'Deuteranope':  {'G': '#ffd700', 'R': '#005ac2', 'Y': '#f0e442', 'B': '#0072b2', 'O': '#e69f00'},
    'Protanope':    {'G': '#f0e442', 'R': '#0072b2', 'Y': '#e69f00', 'B': '#56b4e9', 'O': '#d55e00'},
    'Tritanope':    {'G': '#009e73', 'R': '#d55e00', 'Y': '#f0e442', 'B': '#cc79a7', 'O': '#e69f00'}
}

# Dil Ayarları
LANGUAGES = {
    'tr': {
        'app_title': f'FestiPath {APP_VERSION}',
        'waiting': 'Şarkı Bekleniyor...',
        'ready': 'Hazır',
        'settings': 'Ayarlar',
        'tab_visual': 'Görünüm',
        'tab_hotkeys': 'Kısayollar',
        'tab_system': 'Genel',
        'grp_window': 'Pencere & Font',
        'grp_bar': 'Görsel Bar & Popup',
        'grp_lang': 'Dil / Language',
        'grp_tts': 'Sesli Okuma (Google Translate)',
        'font_size': 'Ana Font Boyutu',
        'popup_font_size': 'Popup Font Boyutu',
        'opacity': 'Şeffaflık',
        'bg_visible': 'Arka Planı Göster',
        'language': 'Dil / Language',
        'close': 'Kapat',
        'no_data': 'Veri Yok',
        'path_not_found': 'Yol verisi bulunamadı.',
        'internet_error': 'Bağlantı Hatası',
        'server_error': 'Sunucu Hatası',
        'log_reading': 'Log Okunuyor...',
        'system_starting': 'Sistem Başlatılıyor...',
        'update_available': 'GÜNCELLEME MEVCUT!',
        'update_desc': 'Yeni özellikler ve düzeltmeler:',
        'dont_show_again': 'Bu sürüm için tekrar gösterme',
        'hotkey_hide': 'Gizle/Göster:',
        'hotkey_lock': 'Kilit (Sürükleme):',
        'hotkey_reset': 'Pencereyi Ortala:',
        'hotkey_tts': 'Sonraki Satır:',
        'hotkey_sett': 'Ayarlar Menüsü:',
        'tts_enable': 'Sesli Okumayı Aktif Et',
        'auto_read': 'Şarkı Başlayınca Oku',
        'visual_bar_enable': 'Renk Barını Göster (Mevcut)',
        'visual_bar_popup': 'Renk Barı (Ayrı Pencere)',
        'current_line_popup_enable': 'Satır Okuma Popup\'ı Göster (Renkli)',
        'hotkey_waiting': 'Tuşa Basın...',
        'gt_lang': 'tr', # Google Translate Kodu
        'color_blind': 'Renk Körü Modu',
        'Normal': 'Normal', 'Deuteranope': 'Dötenarop (Yeşil)', 'Protanope': 'Protanop (Kırmızı)', 'Tritanope': 'Tritanop (Mavi)',
        # OKUNUŞLAR (Google Translate'e gönderilecek kelimeler)
        'R': 'Kırmızı', 'G': 'Yeşil', 'Y': 'Sarı', 'B': 'Mavi', 'O': 'Turuncu', 'NN': 'Sonraki Nota'
    },
    'en': {
        'app_title': f'FestiPath {APP_VERSION}',
        'waiting': 'Waiting for song...',
        'ready': 'Ready',
        'settings': 'Settings',
        'tab_visual': 'Visuals',
        'tab_hotkeys': 'Hotkeys',
        'tab_system': 'General',
        'grp_window': 'Window & Font',
        'grp_bar': 'Visual Bar & Popup',
        'grp_lang': 'Language',
        'grp_tts': 'Text-to-Speech (Google Translate)',
        'font_size': 'Main Font Size',
        'popup_font_size': 'Popup Font Size',
        'opacity': 'Opacity',
        'bg_visible': 'Show Background',
        'language': 'Language',
        'close': 'Close',
        'no_data': 'No Data',
        'path_not_found': 'Path data not found.',
        'internet_error': 'Connection Error',
        'server_error': 'Server Error',
        'log_reading': 'Reading Log...',
        'system_starting': 'System Starting...',
        'update_available': 'UPDATE AVAILABLE!',
        'update_desc': 'New features and fixes:',
        'dont_show_again': 'Don\'t show again for this version',
        'hotkey_hide': 'Hide/Show:',
        'hotkey_lock': 'Drag Lock:',
        'hotkey_reset': 'Reset Position:',
        'hotkey_tts': 'Next Line:',
        'hotkey_sett': 'Settings Menu:',
        'tts_enable': 'Enable TTS',
        'auto_read': 'Auto Read on Start',
        'visual_bar_enable': 'Show Color Bar (Current)',
        'visual_bar_popup': 'Color Bar Popup (Detached)',
        'current_line_popup_enable': 'Show Line Reader Popup (Colored)',
        'hotkey_waiting': 'Press Key...',
        'gt_lang': 'en', # Google Translate Code
        'color_blind': 'Color Blind Mode',
        'Normal': 'Normal', 'Deuteranope': 'Deuteranope', 'Protanope': 'Protanope', 'Tritanope': 'Tritanope',
        # PRONUNCIATIONS (Words to send to Google Translate)
        'R': 'Red', 'G': 'Green', 'Y': 'Yellow', 'B': 'Blue', 'O': 'Orange', 'NN': 'Next Note'
    }
}

INSTRUMENT_MAP = {'Drums': 'd', 'Drum': 'd', 'Bass': 'b', 'Vocals': 'v', 'Vocal': 'v', 'Guitar': 'l', 'Lead': 'l', 'PlasticGuitar': 'g', 'ProGuitar': 'g', 'PlasticBass': 'm', 'ProBass': 'm'}
DISPLAY_NAME_MAP = {'Guitar': 'Lead', 'Lead': 'Lead', 'PlasticGuitar': 'Pro Guitar', 'ProGuitar': 'Pro Guitar', 'PlasticBass': 'Pro Bass', 'ProBass': 'Pro Bass', 'Bass': 'Bass', 'Drums': 'Drums', 'Drum': 'Drums', 'Vocals': 'Vocals', 'Vocal': 'Vocals'}
ICON_FILES = {'Lead': 'lead.png', 'Pro Guitar': 'proguitar.png', 'Pro Bass': 'probass.png', 'Bass': 'bass.png', 'Drums': 'drums.png', 'Vocals': 'vocals.png'}

GP_ICONS = {
    '0': 'Ⓐ', '1': 'Ⓑ', '2': 'ⓧ', '3': 'ⓨ', 
    '4': 'LB', '5': 'RB', '6': '⧉', '7': '☰', 
    '8': 'LS', '9': 'RS', '10': '🏠',
    'UP': '⬆', 'DOWN': '⬇', 'LEFT': '⬅', 'RIGHT': '➡'
}

def format_gamepad_text(code):
    if not code or code == 'NONE': return 'NONE'
    parts = code.split(':')
    if parts[0] == 'BTN':
        idx = parts[1]
        sym = GP_ICONS.get(idx, f"({idx})")
        return f"{sym}"
    elif parts[0] == 'HAT':
        direction = parts[2]
        sym = GP_ICONS.get(direction, direction)
        return f"DPAD {sym}"
    return code

class ConfigManager:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.defaults = {
            'font_size': '16', 'popup_font_size': '20', 
            'opacity': '0.9', 'bg_visible': 'True',
            'language': 'en', 'x': '50', 'y': '50', 'bar_x': '100', 'bar_y': '100',
            'popup_x': '200', 'popup_y': '200',
            'hotkey_hide': 'F8', 'hotkey_lock': 'F9', 
            'hotkey_reset': 'F7',
            'hotkey_settings': 'F10',
            'hotkey_tts': 'space', 
            'gamepad_tts_btn': 'NONE',
            'tts_enabled': 'True', 
            'visual_bar_enabled': 'True', 'visual_bar_popup': 'False',
            'current_line_popup_enabled': 'False',
            'auto_read_first': 'False',
            'ignored_version': '0.0',
            'color_blind_mode': 'Normal'
        }
        self.load()

    def load(self):
        try:
            if os.path.exists(CONFIG_FILE):
                self.config.read(CONFIG_FILE)
            if 'SETTINGS' not in self.config:
                self.config['SETTINGS'] = self.defaults
                self.save()
        except:
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

class GamepadManager:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joystick = None
        self.connect_joystick()

    def connect_joystick(self):
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            return True
        return False

    def get_any_input(self):
        if not self.joystick:
            if not self.connect_joystick(): return None

        pygame.event.pump()
        for i in range(self.joystick.get_numbuttons()):
            if self.joystick.get_button(i):
                return f"BTN:{i}"
        for i in range(self.joystick.get_numhats()):
            hat = self.joystick.get_hat(i)
            if hat[1] == 1: return f"HAT:{i}:UP"
            if hat[1] == -1: return f"HAT:{i}:DOWN"
            if hat[0] == 1: return f"HAT:{i}:RIGHT"
            if hat[0] == -1: return f"HAT:{i}:LEFT"
        return None

    def check_specific_input(self, input_code):
        if not self.joystick or not input_code or input_code == 'NONE': return False
        pygame.event.pump()
        parts = input_code.split(':')
        type = parts[0]
        try:
            if type == "BTN":
                return self.joystick.get_button(int(parts[1]))
            elif type == "HAT":
                idx = int(parts[1])
                direction = parts[2]
                hat = self.joystick.get_hat(idx)
                if direction == "UP" and hat[1] == 1: return True
                if direction == "DOWN" and hat[1] == -1: return True
                if direction == "RIGHT" and hat[0] == 1: return True
                if direction == "LEFT" and hat[0] == -1: return True
        except: pass
        return False

class GoogleTTSManager:
    """Google Translate tabanlı, dosya kaydetmeyen (In-Memory) TTS Yöneticisi"""
    def __init__(self, language_code):
        if not pygame.get_init(): pygame.init()
        try: pygame.mixer.init()
        except: pass
        self.lang_code = language_code
        self.gt_lang = LANGUAGES[language_code].get('gt_lang', 'en')
        # Kelime değişim sözlüğünü al (R -> Red, G -> Green vb.)
        self.vocab = LANGUAGES[language_code]

    def play_live(self, text_line):
        """Metni alır, Google'a gönderir, gelen sesi RAM'den çalar."""
        threading.Thread(target=self._stream_audio, args=(text_line,), daemon=True).start()

    def _stream_audio(self, text):
        if not text.strip(): return
        
        # 1. Sembol Temizliği (Parantez, Slash)
        clean_text = re.sub(r'[()\/]', ' ', text)
        
        # 2. Renk Kodlarını ve Kısaltmaları Tam Kelimeye Çevir
        # Örnek: "3 R G" -> "3 Red Green"
        # Sadece tanımlı anahtarları (R, G, B, Y, O, NN) değiştir.
        target_keys = ['R', 'G', 'Y', 'B', 'O', 'NN']
        
        for key in target_keys:
            if key in self.vocab:
                # Boşluk ekleyerek değiştiriyoruz ki kelimeler birbirine yapışmasın
                # Örn: R -> " Red "
                replacement = f" {self.vocab[key]} " 
                clean_text = clean_text.replace(key, replacement)

        try:
            # gTTS nesnesi oluştur
            tts = gTTS(text=clean_text, lang=self.gt_lang, slow=False)
            
            # RAM üzerinde dosya (BytesIO) oluştur
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0) # Başa sar
            
            # Pygame ile RAM'den yükle ve çal
            pygame.mixer.music.load(fp)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"TTS Stream Error: {e}")

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent, config, update_callback, lang_dict, gamepad_mgr):
        super().__init__(parent)
        self.config = config
        self.update_callback = update_callback
        self.lang = lang_dict
        self.gamepad_mgr = gamepad_mgr
        
        self.title(self.lang['settings'])
        self.geometry("580x550") 
        self.resizable(False, False)
        self.configure(bg="#2b2b2b")
        self.attributes('-topmost', True)
        
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('TNotebook', background='#2b2b2b', borderwidth=0)
        self.style.configure('TNotebook.Tab', background='#444', foreground='white', padding=[10, 5], font=('Segoe UI', 9))
        self.style.map('TNotebook.Tab', background=[('selected', '#00b894')], foreground=[('selected', 'white')])
        self.style.configure('TLabelframe', background='#2b2b2b', foreground='white')
        self.style.configure('TLabelframe.Label', background='#2b2b2b', foreground='#00cec9', font=('Segoe UI', 9, 'bold'))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.tab_visual = tk.Frame(self.notebook, bg="#2b2b2b")
        self.tab_hotkeys = tk.Frame(self.notebook, bg="#2b2b2b")
        self.tab_system = tk.Frame(self.notebook, bg="#2b2b2b")

        self.notebook.add(self.tab_visual, text=self.lang['tab_visual'])
        self.notebook.add(self.tab_hotkeys, text=self.lang['tab_hotkeys'])
        self.notebook.add(self.tab_system, text=self.lang['tab_system'])

        self.setup_visual_tab()
        self.setup_hotkeys_tab()
        self.setup_system_tab()

    def setup_visual_tab(self):
        grp_win = ttk.LabelFrame(self.tab_visual, text=self.lang['grp_window'])
        grp_win.pack(fill='x', padx=10, pady=10)

        # Ana Font
        f1 = tk.Frame(grp_win, bg="#2b2b2b"); f1.pack(fill='x', padx=5, pady=5)
        tk.Label(f1, text=self.lang['font_size'], bg="#2b2b2b", fg="white", width=20, anchor='w').pack(side='left')
        self.fs = tk.Scale(f1, from_=10, to=40, orient=tk.HORIZONTAL, command=self.on_change, bg="#2b2b2b", fg="white", highlightthickness=0, length=200)
        self.fs.set(self.config.get('font_size', int)); self.fs.pack(side='left')

        # Opaklık
        f2 = tk.Frame(grp_win, bg="#2b2b2b"); f2.pack(fill='x', padx=5, pady=5)
        tk.Label(f2, text=self.lang['opacity'], bg="#2b2b2b", fg="white", width=20, anchor='w').pack(side='left')
        self.op = tk.Scale(f2, from_=20, to=100, orient=tk.HORIZONTAL, command=self.on_change, bg="#2b2b2b", fg="white", highlightthickness=0, length=200)
        self.op.set(int(self.config.get('opacity', float)*100)); self.op.pack(side='left')

        self.bgv = tk.BooleanVar(value=self.config.get('bg_visible')=='True')
        tk.Checkbutton(grp_win, text=self.lang['bg_visible'], variable=self.bgv, command=self.on_change, 
                       bg="#2b2b2b", fg="white", selectcolor="#444", activebackground="#2b2b2b").pack(anchor='w', padx=5, pady=5)

        # Renk Körü
        f3 = tk.Frame(grp_win, bg="#2b2b2b"); f3.pack(fill='x', padx=5, pady=5)
        tk.Label(f3, text=self.lang['color_blind'], bg="#2b2b2b", fg="white", width=20, anchor='w').pack(side='left')
        self.cb_mode = ttk.Combobox(f3, values=["Normal", "Deuteranope", "Protanope", "Tritanope"], state="readonly", width=20)
        self.cb_mode.set(self.config.get('color_blind_mode'))
        self.cb_mode.pack(side='left', padx=5)
        self.cb_mode.bind("<<ComboboxSelected>>", self.on_change)

        grp_bar = ttk.LabelFrame(self.tab_visual, text=self.lang['grp_bar'])
        grp_bar.pack(fill='x', padx=10, pady=5)

        self.barv = tk.BooleanVar(value=self.config.get('visual_bar_enabled')=='True')
        tk.Checkbutton(grp_bar, text=self.lang['visual_bar_enable'], variable=self.barv, command=self.on_change, 
                       bg="#2b2b2b", fg="white", selectcolor="#444", activebackground="#2b2b2b").pack(anchor='w', padx=5, pady=2)
        
        self.popv = tk.BooleanVar(value=self.config.get('visual_bar_popup')=='True')
        tk.Checkbutton(grp_bar, text=self.lang['visual_bar_popup'], variable=self.popv, command=self.on_change, 
                       bg="#2b2b2b", fg="white", selectcolor="#444", activebackground="#2b2b2b").pack(anchor='w', padx=5, pady=2)

        # Popup Checkbox
        self.nextv = tk.BooleanVar(value=self.config.get('current_line_popup_enabled')=='True')
        tk.Checkbutton(grp_bar, text=self.lang['current_line_popup_enable'], variable=self.nextv, command=self.on_change,
                       bg="#2b2b2b", fg="#fab1a0", selectcolor="#444", activebackground="#2b2b2b").pack(anchor='w', padx=5, pady=2)

        # YENİ: Popup Font Ayarı
        f_pop = tk.Frame(grp_bar, bg="#2b2b2b"); f_pop.pack(fill='x', padx=5, pady=5)
        tk.Label(f_pop, text=self.lang['popup_font_size'], bg="#2b2b2b", fg="#fab1a0", width=20, anchor='w').pack(side='left')
        self.fs_pop = tk.Scale(f_pop, from_=10, to=60, orient=tk.HORIZONTAL, command=self.on_change, bg="#2b2b2b", fg="white", highlightthickness=0, length=200)
        self.fs_pop.set(self.config.get('popup_font_size', int)); self.fs_pop.pack(side='left')

    def setup_hotkeys_tab(self):
        frame = tk.Frame(self.tab_hotkeys, bg="#2b2b2b")
        frame.pack(expand=True, padx=20, pady=20)
        
        self.create_hk_row(frame, 0, self.lang['hotkey_hide'], 'hotkey_hide')
        self.create_hk_row(frame, 1, self.lang['hotkey_lock'], 'hotkey_lock')
        self.create_hk_row(frame, 2, self.lang['hotkey_reset'], 'hotkey_reset')
        self.create_hk_row(frame, 3, self.lang['hotkey_sett'], 'hotkey_settings')
        self.create_hk_row(frame, 4, self.lang['hotkey_tts'], 'hotkey_tts', is_gamepad_capable=True)

    def create_hk_row(self, parent, row, txt, k, is_gamepad_capable=False):
        tk.Label(parent, text=txt, bg="#2b2b2b", fg="white", font=("Segoe UI", 10), anchor='e').grid(row=row, column=0, padx=10, pady=10, sticky='e')
        
        current_val = self.config.get(k).upper()
        if is_gamepad_capable:
            gp_btn = self.config.get('gamepad_tts_btn')
            if gp_btn != 'NONE': 
                icon_text = format_gamepad_text(gp_btn)
                current_val += f" / {icon_text}"
        
        b = tk.Button(parent, text=current_val, bg="#444", fg="white", width=20, relief="flat", font=("Segoe UI Symbol", 9))
        b.config(command=lambda: self.start_listening(k, b, is_gamepad_capable))
        b.grid(row=row, column=1, padx=10, pady=10, sticky='w')

    def setup_system_tab(self):
        col1 = tk.Frame(self.tab_system, bg="#2b2b2b")
        col1.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        grp_lang = ttk.LabelFrame(col1, text=self.lang['grp_lang'])
        grp_lang.pack(fill='x', pady=5)
        
        self.lang_var = tk.StringVar(value=self.config.get('language'))
        tk.Radiobutton(grp_lang, text="Türkçe", variable=self.lang_var, value="tr", command=self.on_change, 
                       bg="#2b2b2b", fg="white", selectcolor="#444", activebackground="#2b2b2b").pack(anchor='w', padx=10, pady=5)
        tk.Radiobutton(grp_lang, text="English", variable=self.lang_var, value="en", command=self.on_change, 
                       bg="#2b2b2b", fg="white", selectcolor="#444", activebackground="#2b2b2b").pack(anchor='w', padx=10, pady=5)

        col2 = tk.Frame(self.tab_system, bg="#2b2b2b")
        col2.pack(side='right', fill='both', expand=True, padx=10, pady=10)

        grp_tts = ttk.LabelFrame(col2, text=self.lang['grp_tts'])
        grp_tts.pack(fill='x', pady=5)

        self.ttsv = tk.BooleanVar(value=self.config.get('tts_enabled')=='True')
        tk.Checkbutton(grp_tts, text=self.lang['tts_enable'], variable=self.ttsv, command=self.on_change, 
                       bg="#2b2b2b", fg="white", selectcolor="#444", activebackground="#2b2b2b").pack(anchor='w', padx=10, pady=5)
        
        self.autoread_v = tk.BooleanVar(value=self.config.get('auto_read_first')=='True')
        tk.Checkbutton(grp_tts, text=self.lang['auto_read'], variable=self.autoread_v, command=self.on_change, 
                       bg="#2b2b2b", fg="white", selectcolor="#444", activebackground="#2b2b2b").pack(anchor='w', padx=10, pady=5)

    def start_listening(self, k, b, is_gamepad_capable):
        b.config(text=self.lang['hotkey_waiting'], bg="#d63031")
        self.update()
        threading.Thread(target=self.listen_thread, args=(k, b, is_gamepad_capable), daemon=True).start()

    def listen_thread(self, k, b, is_gamepad_capable):
        start_time = time.time()
        detected_text = None
        new_key = None
        new_btn = None
        
        self.key_pressed = None
        def on_key(e): self.key_pressed = e.name
        hook = keyboard.on_press(on_key)
        
        while time.time() - start_time < 5:
            if self.key_pressed:
                new_key = self.key_pressed
                detected_text = new_key.upper()
                break
            if is_gamepad_capable:
                btn_code = self.gamepad_mgr.get_any_input()
                if btn_code:
                    new_btn = btn_code
                    detected_text = format_gamepad_text(btn_code)
                    break
            time.sleep(0.05)
        
        keyboard.unhook(hook)
        
        if detected_text:
            if new_key:
                self.config.set(k, new_key)
                if is_gamepad_capable: self.config.set('gamepad_tts_btn', 'NONE')
            if new_btn is not None:
                self.config.set('gamepad_tts_btn', new_btn)
                self.config.set(k, 'NONE')
            try: b.config(text=detected_text, bg="#444")
            except: pass
            self.update_callback()
        else:
            try:
                curr = self.config.get(k).upper()
                if is_gamepad_capable:
                    gp = self.config.get('gamepad_tts_btn')
                    if gp != 'NONE':
                        curr += f" / {format_gamepad_text(gp)}"
                b.config(text=curr, bg="#444")
            except: pass

    def on_change(self, *a):
        try:
            self.config.set('font_size', self.fs.get())
            self.config.set('popup_font_size', self.fs_pop.get())
            self.config.set('opacity', self.op.get()/100)
            self.config.set('bg_visible', self.bgv.get())
            self.config.set('tts_enabled', self.ttsv.get())
            self.config.set('auto_read_first', self.autoread_v.get())
            self.config.set('visual_bar_enabled', self.barv.get())
            self.config.set('visual_bar_popup', self.popv.get())
            self.config.set('current_line_popup_enabled', self.nextv.get())
            self.config.set('language', self.lang_var.get())
            self.config.set('color_blind_mode', self.cb_mode.get())
            self.update_callback()
        except: pass

class VisualBar:
    def __init__(self, root, config):
        self.root = root; self.cfg = config; self.popup = None; self.canvas = None; self.docked = None; self.cols = []; self.ox = 0; self.oy = 0
    def setup(self, parent=None):
        self.destroy()
        if self.cfg.get('visual_bar_enabled') != 'True': return
        if self.cfg.get('visual_bar_popup') == 'True':
            self.popup = tk.Toplevel(self.root); self.popup.overrideredirect(True); self.popup.attributes('-topmost', True); self.popup.config(bg='black')
            x = self.cfg.get('bar_x', int); y = self.cfg.get('bar_y', int)
            self.popup.geometry(f"300x40+{x}+{y}")
            self.canvas = tk.Canvas(self.popup, bg="black", highlightthickness=0); self.canvas.pack(fill='both', expand=True)
            self.canvas.bind("<ButtonPress-1>", self.sm); self.canvas.bind("<ButtonRelease-1>", self.em); self.canvas.bind("<B1-Motion>", self.mm)
        else:
            if parent:
                self.docked = tk.Frame(parent, bg="black", height=30); self.docked.pack(side='top', fill='x', pady=(0, 5)); self.docked.pack_propagate(False)
                self.canvas = tk.Canvas(self.docked, bg="black", highlightthickness=0); self.canvas.pack(fill='both', expand=True)
        self.draw(self.cols)

    def update(self, txt, color_map):
        self.cols = [color_map[c] for c in txt if c in color_map]
        self.draw(self.cols)

    def draw(self, cols):
        if not self.canvas: return
        self.canvas.delete("all")
        if not cols: return
        self.canvas.update_idletasks()
        w = self.canvas.winfo_width(); h = self.canvas.winfo_height()
        if w <= 1: w = 300 
        if h <= 1: h = 40
        bw = w/len(cols)
        for i, c in enumerate(cols): 
            self.canvas.create_rectangle(i*bw, 0, (i+1)*bw + 1, h, fill=c, outline="")
    def destroy(self):
        if self.popup: self.popup.destroy(); self.popup = None
        if self.docked: self.docked.destroy(); self.docked = None
    def sm(self, e): self.ox, self.oy = e.x, e.y
    def em(self, e): 
        if self.popup: self.cfg.set('bar_x', self.popup.winfo_x()); self.cfg.set('bar_y', self.popup.winfo_y())
    def mm(self, e): 
        if self.popup: self.popup.geometry(f"+{self.popup.winfo_x()+e.x-self.ox}+{self.popup.winfo_y()+e.y-self.oy}")
    def set_visibility(self, v): 
        if self.popup: self.popup.deiconify() if v else self.popup.withdraw()

class CurrentLinePopup:
    """O anki satırı renkli gösteren popup"""
    def __init__(self, root, config):
        self.root = root
        self.cfg = config
        self.popup = None
        self.txt_widget = None
        self.ox = 0
        self.oy = 0
        self.visible = False

    def setup(self):
        self.destroy()
        if self.cfg.get('current_line_popup_enabled') != 'True': 
            self.visible = False
            return
        
        self.visible = True
        self.popup = tk.Toplevel(self.root)
        self.popup.overrideredirect(True)
        self.popup.attributes('-topmost', True)
        self.popup.attributes('-alpha', 0.8)
        self.popup.config(bg='black')
        
        x = self.cfg.get('popup_x', int)
        y = self.cfg.get('popup_y', int)
        self.popup.geometry(f"400x60+{x}+{y}")
        
        # Text Widget kullanımı (Renkli yazı için)
        font_size = self.cfg.get('popup_font_size', int)
        self.txt_widget = tk.Text(self.popup, font=("Consolas", font_size, "bold"), bg="black", fg="white", bd=0, height=1)
        self.txt_widget.pack(fill='both', expand=True)
        
        # Event binding (Sürükleme için text widget'a bağla)
        self.txt_widget.bind("<ButtonPress-1>", self.sm)
        self.txt_widget.bind("<ButtonRelease-1>", self.em)
        self.txt_widget.bind("<B1-Motion>", self.mm)
        
        self.txt_widget.config(state='disabled', cursor='arrow')

    def update_text(self, text, color_map):
        if self.popup and self.txt_widget:
            self.txt_widget.config(state='normal')
            self.txt_widget.delete("1.0", "end")
            
            # Tag konfigürasyonu
            for char_code, hex_color in color_map.items():
                self.txt_widget.tag_config(char_code, foreground=hex_color)
            self.txt_widget.tag_config('W', foreground='#f1f2f6')
            
            # Renkli yazdırma mantığı
            if text:
                for p in re.split(r'([RGBYO])', text):
                    tag = p if p in "RGBYO" else "W"
                    self.txt_widget.insert('end', p, tag)
            else:
                self.txt_widget.insert('end', "...", "W")
            
            # Ortala ve kapat
            self.txt_widget.tag_configure("center", justify='center')
            self.txt_widget.tag_add("center", "1.0", "end")
            self.txt_widget.config(state='disabled')

    def destroy(self):
        if self.popup:
            self.popup.destroy()
            self.popup = None
            self.txt_widget = None

    def sm(self, e): self.ox, self.oy = e.x, e.y
    def em(self, e): 
        if self.popup: 
            self.cfg.set('popup_x', self.popup.winfo_x())
            self.cfg.set('popup_y', self.popup.winfo_y())
    def mm(self, e): 
        if self.popup: 
            self.popup.geometry(f"+{self.popup.winfo_x()+e.x-self.ox}+{self.popup.winfo_y()+e.y-self.oy}")
    def set_visibility(self, v):
        if self.popup:
            if v and self.cfg.get('current_line_popup_enabled') == 'True': self.popup.deiconify()
            else: self.popup.withdraw()

class UpdatePopup(tk.Toplevel):
    def __init__(self, parent, version_data, config, lang_dict):
        super().__init__(parent)
        self.config = config
        self.lang = lang_dict
        self.version_tag = version_data.get('version', 'v0.0')
        self.download_url = version_data.get('url', LINK_GITHUB)
        
        self.notes_tr = version_data.get('notes_tr', [])
        self.notes_en = version_data.get('notes_en', [])

        self.title(self.lang['update_available'])
        self.geometry("520x480") 
        self.configure(bg="#202020")
        self.attributes('-topmost', True)
        self.resizable(False, False)

        header_frame = tk.Frame(self, bg="#202020")
        header_frame.pack(side='top', fill='x', pady=(20, 10))
        
        tk.Label(header_frame, text=self.lang['update_available'], font=("Segoe UI", 16, "bold"), fg="#00b894", bg="#202020").pack()
        tk.Label(header_frame, text=f"Version: {self.version_tag}", font=("Consolas", 10), fg="#b2bec3", bg="#202020").pack()

        bottom_frame = tk.Frame(self, bg="#202020")
        bottom_frame.pack(side='bottom', fill='x', pady=15)

        self.dont_show = tk.BooleanVar()
        cb = tk.Checkbutton(bottom_frame, text=self.lang['dont_show_again'], variable=self.dont_show, 
                            bg="#202020", fg="#dfe6e9", selectcolor="#202020", activebackground="#202020", font=("Segoe UI", 9))
        cb.pack(side='top', pady=(0, 10))

        btn_container = tk.Frame(bottom_frame, bg="#202020")
        btn_container.pack(side='top')

        tk.Button(btn_container, text="İndir / Download", bg="#00b894", fg="white", font=("Segoe UI", 10, "bold"), 
                 command=self.go_url, width=18, relief="flat", pady=5, cursor="hand2").pack(side='left', padx=10)
        
        tk.Button(btn_container, text="Kapat / Close", bg="#d63031", fg="white", font=("Segoe UI", 10, "bold"), 
                 command=self.close_win, width=18, relief="flat", pady=5, cursor="hand2").pack(side='left', padx=10)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#202020', borderwidth=0)
        style.configure('TNotebook.Tab', background='#2d3436', foreground='white', padding=[15, 5], font=('Segoe UI', 9))
        style.map('TNotebook.Tab', background=[('selected', '#0984e3')], foreground=[('selected', 'white')])

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(side='top', fill='both', expand=True, padx=20, pady=5)

        self.frame_tr = tk.Frame(self.notebook, bg="#2d3436")
        self.create_notes_view(self.frame_tr, self.notes_tr)
        self.notebook.add(self.frame_tr, text="🇹🇷 Türkçe")

        self.frame_en = tk.Frame(self.notebook, bg="#2d3436")
        self.create_notes_view(self.frame_en, self.notes_en)
        self.notebook.add(self.frame_en, text="🇺🇸 English")
        
        if self.config.get('language') == 'en':
            self.notebook.select(1)

    def create_notes_view(self, parent, notes_list):
        txt_frame = tk.Frame(parent, bg="#2d3436")
        txt_frame.pack(fill='both', expand=True)

        scrollbar = tk.Scrollbar(txt_frame)
        scrollbar.pack(side='right', fill='y')

        text_widget = tk.Text(txt_frame, bg="#2d3436", fg="#dfe6e9", font=("Segoe UI", 10), 
                              bd=0, highlightthickness=0, wrap='word', padx=10, pady=10,
                              yscrollcommand=scrollbar.set)
        text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=text_widget.yview)

        text_widget.tag_configure("bold", font=("Segoe UI", 10, "bold"), foreground="white")
        text_widget.tag_configure("bullet", lmargin1=10, lmargin2=25)

        if isinstance(notes_list, list):
            for note in notes_list:
                self.insert_formatted_note(text_widget, note)
        else:
            text_widget.insert('end', str(notes_list))

        text_widget.config(state='disabled')

    def insert_formatted_note(self, widget, text):
        widget.insert('end', "• ", "bullet")
        parts = re.split(r'(\*\*.*?\*\*)', text)
        for part in parts:
            if part.startswith('**') and part.endswith('**'):
                clean_text = part[2:-2]
                widget.insert('end', clean_text, ("bold", "bullet"))
            else:
                widget.insert('end', part, "bullet")
        widget.insert('end', "\n\n")

    def go_url(self): 
        webbrowser.open(self.download_url)
        self.close_win()
    
    def close_win(self):
        if self.dont_show.get(): 
            self.config.set('ignored_version', self.version_tag)
        self.destroy()

class FestivalPathOverlay:
    def __init__(self, root):
        self.root = root
        
        try:
            icon_path = resource_path('app_icon.ico')
            self.root.iconbitmap(icon_path)
        except:
            pass

        # --- DEĞİŞKENLER ---
        self.cfg = ConfigManager()
        self.last_trigger_time = 0
        self.auto_read_timer = None 
        
        self.lang = self.cfg.get('language')
        self.L = LANGUAGES[self.lang]
        
        # Seçili Renk Paleti (Varsayılan Normal)
        self.current_colors = COLOR_PALETTES['Normal']

        # Son okunan satırı tutmak için
        self.current_line_text = "" 

        # --- PENCERE AYARLARI ---
        self.root.title(self.L['app_title'])
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', self.cfg.get('opacity', float))
        self.cols = {'bg': '#1e1e1e', 'panel': '#252526', 'warn': '#fdcb6e', 'dang': '#d63031', 'succ': '#00b894', 'link': '#74b9ff', 'score_bg': '#e67e22', 'version': '#00d2d3'}
        self.root.configure(bg=self.cols['bg'])
        self.root.attributes('-transparentcolor', '#000001')
        
        self.gamepad = GamepadManager()
        self.tts = GoogleTTSManager(self.lang)
        self.vis = VisualBar(self.root, self.cfg)
        self.curr_popup = CurrentLinePopup(self.root, self.cfg) # Yeni Popup Sınıfı
        
        self.run = True; self.lock = False; self.vis_on = True; self.js=""; self.map={}; self.sid=None; self.inst="Guitar"; self.cache={}; self.lines=[]; self.lidx=0
        self.settings_window = None; self.last_btn_press = 0

        self.cont = tk.Frame(root, bg=self.cols['panel']); self.cont.pack(fill='both', expand=True, padx=2, pady=2)
        self.bar = tk.Frame(self.cont, bg=self.cols['warn'], width=8); self.bar.pack(side='left', fill='y')
        self.main = tk.Frame(self.cont, bg=self.cols['panel']); self.main.pack(side='left', fill='both', expand=True, padx=8, pady=5)
        self.vis.setup(self.main)
        self.curr_popup.setup()
        
        self.h_fr = tk.Frame(self.main, bg=self.cols['panel']); self.h_fr.pack(fill='x')
        self.lbl_ti = tk.Label(self.h_fr, text=self.L['system_starting'], font=("Segoe UI", 11, "bold"), fg="#dfe6e9", bg=self.cols['panel'], anchor='w'); self.lbl_ti.pack(side='left', fill='x', expand=True)
        self.m_fr = tk.Frame(self.main, bg=self.cols['panel']); self.m_fr.pack(fill='x', pady=2)
        self.lbl_ic = tk.Label(self.m_fr, bg=self.cols['panel']); self.lbl_ic.pack(side='left')
        self.lbl_in = tk.Label(self.m_fr, font=("Segoe UI", 16, "bold"), fg="#0984e3", bg=self.cols['panel']); self.lbl_in.pack(side='left', padx=5)
        self.lbl_sc = tk.Label(self.m_fr, font=("Consolas", 12, "bold"), fg="white", bg="#e67e22", padx=5); self.lbl_sc.pack(side='right')

        self.txt = tk.Text(self.main, height=1, font=("Consolas", 16, "bold"), bg=self.cols['panel'], fg="white", bd=0); self.txt.pack(fill="both", expand=True, pady=5)
        
        self.ft_fr = tk.Frame(self.main, bg=self.cols['panel']); self.ft_fr.pack(side='bottom', fill='x', pady=10)
        self.lbl_up = tk.Label(self.ft_fr, text=self.L['update_available'], font=("Segoe UI", 8, "bold"), fg="white", bg=self.cols['dang'], cursor="hand2")
        self.add_ft(APP_VERSION, "#00d2d3", True); self.add_ft(DEVELOPER_NAME, "#b2bec3")
        self.add_lnk("Github", LINK_GITHUB); self.add_lnk("Hub", LINK_HUB); self.add_lnk("Twitch", LINK_TWITCH); self.add_lnk("Kick", LINK_KICK)

        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label=self.L['settings'], command=self.sett)
        self.menu.add_separator(); self.menu.add_command(label=self.L['close'], command=self.close)
        self.root.bind("<Button-3>", lambda e: self.menu.post(e.x_root, e.y_root))

        self.apply(); self.binds(self.root); self.hk()
        for t in [self.fetch, self.log, self.upd_chk]: threading.Thread(target=t, daemon=True).start()
        
        self.poll_gamepad()
        self.resize()

    def add_ft(self, t, c, f=False): 
        if not f: tk.Label(self.ft_fr, text="|", fg="#636e72", bg=self.cols['panel']).pack(side='left', padx=2)
        tk.Label(self.ft_fr, text=t, font=("Segoe UI", 8, "bold"), fg=c, bg=self.cols['panel']).pack(side='left')
    def add_lnk(self, t, u):
        tk.Label(self.ft_fr, text="|", fg="#636e72", bg=self.cols['panel']).pack(side='left', padx=2)
        l = tk.Label(self.ft_fr, text=t, font=("Segoe UI", 8, "bold"), fg=self.cols['link'], bg=self.cols['panel'], cursor="hand2")
        l.bind("<Button-1>", lambda e: webbrowser.open(u)); l.pack(side='left')
    def binds(self, w):
        if not (isinstance(w, tk.Label) and w.cget("cursor")=="hand2"):
            w.bind("<ButtonPress-1>", self.ds); w.bind("<ButtonRelease-1>", self.de); w.bind("<B1-Motion>", self.dm)
        for c in w.winfo_children(): self.binds(c)
    def ds(self, e): self.dx, self.dy = e.x, e.y
    def de(self, e): self.cfg.set('x', self.root.winfo_x()); self.cfg.set('y', self.root.winfo_y())
    def dm(self, e): 
        if not self.lock: self.root.geometry(f"+{self.root.winfo_x()+e.x-self.dx}+{self.root.winfo_y()+e.y-self.dy}")

    def hk(self):
        try:
            keyboard.unhook_all()
            for k, f in [('hotkey_hide', self.tog), ('hotkey_lock', self.lck), ('hotkey_reset', self.reset_pos), ('hotkey_tts', self.nxt), ('hotkey_settings', self.sett)]:
                v = self.cfg.get(k); 
                if v and v != 'NONE': keyboard.add_hotkey(v, f)
        except: pass

    def reset_pos(self):
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.root.geometry(f"+{w//2-240}+{h//2-200}")
        self.cfg.set('x', w//2-240)
        self.cfg.set('y', h//2-200)

    def poll_gamepad(self):
        if self.gamepad.joystick:
            pygame.event.pump()
            target = self.cfg.get('gamepad_tts_btn')
            if target != 'NONE':
                if self.gamepad.check_specific_input(target):
                    current_time = time.time()
                    if current_time - self.last_btn_press > 0.3:
                        self.nxt(); self.last_btn_press = current_time
        self.root.after(50, self.poll_gamepad)

    def nxt(self):
        if self.vis_on and self.sid and self.lidx < len(self.lines):
            l = self.lines[self.lidx]
            self.current_line_text = l 
            
            # Google Translate TTS Çal
            if self.cfg.get('tts_enabled')=='True': self.tts.play_live(l)
            
            # Görsel Barı Güncelle
            self.vis.update(l, self.current_colors)
            
            # --- YENİ: MEVCUT Satır Popup Güncelle ---
            # Artık "Next Step" değil, "Current Step" gösteriyoruz.
            self.curr_popup.update_text(l, self.current_colors)
            
            self.lidx+=1
    def tog(self): 
        self.vis_on = not self.vis_on
        if self.vis_on: 
            self.root.deiconify(); self.vis.set_visibility(True)
            self.curr_popup.set_visibility(True)
        else: 
            self.root.withdraw(); self.vis.set_visibility(False)
            self.curr_popup.set_visibility(False)
    def lck(self): 
        self.lock = not self.lock
        self.bar.config(bg=self.cols['dang'] if self.lock else (self.cols['succ'] if self.lbl_ti.cget('text')==self.L['ready'] else self.cols['warn']))

    def resize(self):
        self.root.update_idletasks(); c = self.txt.get("1.0", "end-1c"); nl = c.count('\n')+1 if c else 1
        th = (nl * font.Font(font=self.txt['font']).metrics('linespace')) + 10
        bh = 35 if (self.cfg.get('visual_bar_enabled')=='True' and self.cfg.get('visual_bar_popup')!='True') else 0
        h = self.h_fr.winfo_reqheight() + self.m_fr.winfo_reqheight() + self.ft_fr.winfo_reqheight() + th + bh + 40
        self.root.geometry(f"480x{h}+{self.root.winfo_x()}+{self.root.winfo_y()}")

    def apply(self):
        # Dil Ayarı
        l = self.cfg.get('language')
        if l != self.lang: self.lang=l; self.L=LANGUAGES[l]; self.lbl_ti.config(text=self.L['ready']); self.tts=GoogleTTSManager(l)
        
        # Renk Körü Modu Ayarı
        mode = self.cfg.get('color_blind_mode')
        self.current_colors = COLOR_PALETTES.get(mode, COLOR_PALETTES['Normal'])

        # Font ve Pencere
        self.txt.config(font=("Consolas", self.cfg.get('font_size', int), "bold"))
        self.vis.setup(self.main); self.curr_popup.setup()
        self.root.attributes('-alpha', self.cfg.get('opacity', float))
        bg = self.cols['panel'] if self.cfg.get('bg_visible')=='True' else '#000001'
        self.cont.config(bg=bg); self.main.config(bg=bg)
        for w in self.main.winfo_children():
            try: w.config(bg=bg)
            except: pass
            for c in w.winfo_children(): 
                try: 
                    if c!=self.lbl_sc and c!=self.lbl_up: c.config(bg=bg)
                except: pass
        self.hk(); self.root.after(100, self.resize)
        
        # Tagleri Güncelle
        self.setup_tags()
        
        # Visual Bar'ı mevcut satır ve yeni renklerle güncelle (FIX)
        if self.current_line_text:
            self.vis.update(self.current_line_text, self.current_colors)
            self.curr_popup.update_text(self.current_line_text, self.current_colors)

    def sett(self): 
        # Toggle Mantığı: Açıksa kapat, kapalıysa aç
        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.destroy()
            self.settings_window = None
        else:
            self.settings_window = SettingsWindow(self.root, self.cfg, self.apply, self.L, self.gamepad)

    def setup_tags(self):
        # Mevcut renk paletine göre tag renklerini güncelle
        for char_code, hex_color in self.current_colors.items():
            self.txt.tag_config(char_code, foreground=hex_color)
        self.txt.tag_config('W', foreground='#f1f2f6') # Beyaz (White) sabittir

    def fetch(self):
        try: self.map = json.loads(requests.get(MAPPING_URL).text)
        except: pass
        try: 
            r = requests.get(DATA_URL); self.js = r.text if r.status_code==200 else ""; self.st('ready')
        except: self.st('internet_error')
    def upd_chk(self):
        try:
            d = requests.get(UPDATE_JSON_URL).json()
            if d.get('version')!=APP_VERSION and d.get('version')!=self.cfg.get('ignored_version'):
                self.root.after(0, lambda: UpdatePopup(self.root, d, self.cfg, self.L))
        except: pass

    def log(self):
        while not os.path.exists(LOG_PATH): time.sleep(1); self.st('waiting')
        self.st('ready')
        try:
            with open(LOG_PATH, 'r', encoding='utf-8', errors='ignore') as f:
                f.seek(0, 2); f.seek(max(0, f.tell()-20000), 0)
                for l in f.readlines(): self.par(l)
        except: pass
        try:
            with open(LOG_PATH, 'r', encoding='utf-8', errors='ignore') as f:
                f.seek(0, 2)
                while self.run:
                    l = f.readline()
                    if not l: time.sleep(0.1); continue
                    self.par(l)
        except: pass

    def par(self, l):
        if 'received song to play:' in l:
            try: self.sid = l.split('received song to play: ')[1].split(' - ')[0].strip(); self.trig()
            except: pass
        elif 'SparksSong:' in l:
            try: self.sid = l.split('SparksSong:')[1].strip(); self.trig()
            except: pass
        
        m = re.search(r"TrackType::Track(\w+)", l)
        if m:
            found_inst = m.group(1)
            # Eğer bulunan enstrüman "Events", "Type", "Section" ise yoksay
            if found_inst not in ["Type", "Events", "Section"] and found_inst != self.inst:
                self.inst = found_inst
                self.trig()

    def trig(self):
        if not self.sid: return
        tid = self.sid.lower().replace("sparks_song_","").replace(" ","").strip(); tid=self.map.get(tid, tid)
        i = self.inst if self.inst else "Guitar"
        dn = DISPLAY_NAME_MAP.get(i, i)
        
        if dn not in self.cache: threading.Thread(target=self.dl_ic, args=(dn,), daemon=True).start()
        else: self.lbl_ic.config(image=self.cache[dn])
        self.lbl_in.config(text=dn)

        m = re.search(r'shortname\s*:\s*["\']'+re.escape(tid)+r'["\']', self.js, re.I)
        if not m:
            self.lbl_ti.config(text=tid); self.txt.config(state='normal'); self.txt.delete("1.0",'end'); self.txt.insert('end', self.L['path_not_found']); self.txt.config(state='disabled'); return
        
        idx = m.start()
        try: self.lbl_ti.config(text=re.search(r'value\s*:\s*["\'](.*?)["\']', self.js[max(0,idx-600):idx], re.S).group(1))
        except: self.lbl_ti.config(text=tid.upper())

        ic = INSTRUMENT_MAP.get(i, 'l'); chk = self.js[idx:idx+3000]
        pth = re.search(rf'{ic}path\s*:\s*["\'](.*?)["\']', chk); scr = re.search(rf'{ic}score\s*:\s*["\'](.*?)["\']', chk)
        
        self.lbl_sc.config(text=f"{int(scr.group(1)):,}" if scr else "0")
        
        self.txt.config(state='normal'); self.txt.delete("1.0",'end'); self.lines=[]; self.lidx=0; 
        self.current_line_text = "" # Reset
        self.vis.update("", self.current_colors)
        self.curr_popup.update_text("", self.current_colors)
        
        if pth:
            raw = pth.group(1).replace(", ", "\n").replace(",", "\n")
            for l in raw.split('\n'):
                for p in re.split(r'([RGBYO])', l): self.txt.insert('end', p, p if p in "RGBYO" else "W")
                self.txt.insert('end', '\n')
                if re.search(r'[RGBYO]|NN', l): self.lines.append(l.strip())
            
            if self.cfg.get('auto_read_first') == 'True':
                if self.auto_read_timer:
                    self.root.after_cancel(self.auto_read_timer)
                    self.auto_read_timer = None
                self.auto_read_timer = self.root.after(2500, self.nxt) 
        else: self.txt.insert('end', self.L['path_not_found'], "W")
        self.txt.config(state='disabled'); self.root.after(100, self.resize)

    def dl_ic(self, n):
        f = ICON_FILES.get(n)
        if not f: return
        try:
            d = base64.encodebytes(requests.get(IMG_BASE_URL+f).content)
            i = tk.PhotoImage(data=d); 
            if i.width()>48: i=i.subsample(2,2)
            self.cache[n]=i; self.root.after(0, lambda: self.lbl_ic.config(image=i))
        except: pass
        
    def st(self, k, e=""): self.lbl_ti.config(text=self.L.get(k, k)+e); self.bar.config(bg=self.cols['succ'] if k=='ready' else self.cols['warn'])
    def close(self): self.run=False; self.vis.destroy(); self.curr_popup.destroy(); self.root.destroy(); sys.exit()

if __name__ == "__main__":
    r = tk.Tk(); app = FestivalPathOverlay(r); r.mainloop()

