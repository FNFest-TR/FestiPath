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
import asyncio
import edge_tts
import warnings
import shutil

def resource_path(relative_path):
    """ EXE içine gömülen dosyalara erişmek için geçici yolu bulur """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Klasör yolunu bu fonksiyonla tanımla
CACHE_DIR = resource_path('tts_cache')



# --- SİSTEM AYARLARI ---
warnings.filterwarnings("ignore")
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# --- SABİTLER ---
APP_VERSION = "v2.0"
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

LOG_PATH = os.path.expandvars(r'%localappdata%\FortniteGame\Saved\Logs\FortniteGame.log')
DATA_URL = "https://fnfpaths.github.io/fnfp.js"
MAPPING_URL = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/song_id.json"
IMG_BASE_URL = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main/img/"
CACHE_DIR = os.path.join(BASE_DIR, 'tts_cache')
CONFIG_FILE = os.path.join(BASE_DIR, 'config.ini')

# --- SIRA SAYILARI (Genişletilmiş - 31'e kadar) ---
ORDINALS_TR = {
    '1st': 'Birinci', '1nd': 'Birinci', '1rd': 'Birinci', '1th': 'Birinci',
    '2nd': 'İkinci', '2st': 'İkinci', '2rd': 'İkinci', '2th': 'İkinci',
    '3rd': 'Üçüncü', '3st': 'Üçüncü', '3nd': 'Üçüncü', '3th': 'Üçüncü',
    '4th': 'Dördüncü', '5th': 'Beşinci', '6th': 'Altıncı', '7th': 'Yedinci', 
    '8th': 'Sekizinci', '9th': 'Dokuzuncu', '10th': 'Onuncu',
    '11th': 'On birinci', '12th': 'On ikinci', '13th': 'On üçüncü',
    '14th': 'On dördüncü', '15th': 'On beşinci', '16th': 'On altıncı',
    '17th': 'On yedinci', '18th': 'On sekizinci', '19th': 'On dokuzuncu', '20th': 'Yirminci',
    '21st': 'Yirmi birinci', '22nd': 'Yirmi ikinci', '23rd': 'Yirmi üçüncü', '24th': 'Yirmi dördüncü',
    '25th': 'Yirmi beşinci', '26th': 'Yirmi altıncı', '27th': 'Yirmi yedinci', '28th': 'Yirmi sekizinci',
    '29th': 'Yirmi dokuzuncu', '30th': 'Otuzuncu', '31st': 'Otuz birinci'
}

ORDINALS_EN = {
    '1st': 'First', '1nd': 'First', '1rd': 'First', '1th': 'First',
    '2nd': 'Second', '2st': 'Second', '2rd': 'Second', '2th': 'Second',
    '3rd': 'Third', '3st': 'Third', '3nd': 'Third', '3th': 'Third',
    '4th': 'Fourth', '5th': 'Fifth', '6th': 'Sixth', '7th': 'Seventh',
    '8th': 'Eighth', '9th': 'Ninth', '10th': 'Tenth',
    '11th': 'Eleventh', '11st': 'Eleventh',
    '12th': 'Twelfth', '12nd': 'Twelfth',
    '13th': 'Thirteenth', '13rd': 'Thirteenth',
    '14th': 'Fourteenth', '15th': 'Fifteenth', '16th': 'Sixteenth',
    '17th': 'Seventeenth', '18th': 'Eighteenth', '19th': 'Nineteenth', '20th': 'Twentieth',
    '21st': 'Twenty-first', '22nd': 'Twenty-second', '23rd': 'Twenty-third', '24th': 'Twenty-fourth',
    '25th': 'Twenty-fifth', '26th': 'Twenty-sixth', '27th': 'Twenty-seventh', '28th': 'Twenty-eighth',
    '29th': 'Twenty-ninth', '30th': 'Thirtieth', '31st': 'Thirty-first'
}

# --- DİL ---
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
        'grp_bar': 'Görsel Bar',
        'grp_lang': 'Dil / Language',
        'grp_tts': 'Sesli Okuma (TTS)',
        'font_size': 'Font Boyutu',
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
        'tts_enable': 'Sesli Okumayı Aktif Et',
        'auto_read': 'Şarkı Başlayınca Oku',
        'visual_bar_enable': 'Görsel Barı Göster',
        'visual_bar_popup': 'Popup Modu (Ayrı Pencere)',
        'hotkey_waiting': 'Tuşa Basın...',
        'voice_model': 'tr-TR-AhmetNeural',
        'R': 'Kırmızı', 'G': 'Yeşil', 'Y': 'Sarı', 'B': 'Mavi', 'O': 'Turuncu', 
        'NN': 'Sonraki Nota', 'beats': 'Vuruş', 'after': 'Sonra',
        **{str(i): str(i) for i in range(1, 32)}, 
        **ORDINALS_TR
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
        'grp_bar': 'Visual Bar',
        'grp_lang': 'Language',
        'grp_tts': 'Text-to-Speech',
        'font_size': 'Font Size',
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
        'tts_enable': 'Enable TTS',
        'auto_read': 'Auto Read on Start',
        'visual_bar_enable': 'Show Visual Bar',
        'visual_bar_popup': 'Popup Mode (Detached)',
        'hotkey_waiting': 'Press Key...',
        'voice_model': 'en-US-ChristopherNeural',
        'R': 'Red', 'G': 'Green', 'Y': 'Yellow', 'B': 'Blue', 'O': 'Orange', 
        'NN': 'Next Note', 'beats': 'Beats', 'after': 'After',
        **{str(i): str(i) for i in range(1, 32)},
        **ORDINALS_EN
    }
}

COLOR_HEX_MAP = {'G': '#00ff00', 'R': '#ff0000', 'Y': '#ffff00', 'B': '#5656ff', 'O': '#ffa500'}
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
            'font_size': '16', 'opacity': '0.9', 'bg_visible': 'True',
            'language': 'en', 'x': '50', 'y': '50', 'bar_x': '100', 'bar_y': '100',
            'hotkey_hide': 'F8', 'hotkey_lock': 'F9', 
            'hotkey_reset': 'F7',
            'hotkey_tts': 'space', 
            'gamepad_tts_btn': 'NONE',
            'tts_enabled': 'True', 'visual_bar_enabled': 'True', 'visual_bar_popup': 'False',
            'auto_read_first': 'False',
            'ignored_version': '0.0'
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
        self.DEADZONE = 0.9 
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
        # AXIS İPTAL EDİLDİ
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

class EdgeTTSManager:
    def __init__(self, language_code):
        if not pygame.get_init(): pygame.init()
        try: pygame.mixer.init()
        except: pass

        self.lang = language_code
        self.sounds = {}
        self.voice = LANGUAGES[self.lang]['voice_model']
        if not os.path.exists(CACHE_DIR): os.makedirs(CACHE_DIR)
        threading.Thread(target=self.check_and_download_sounds, daemon=True).start()

    def check_and_download_sounds(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        needed_words = ['R', 'G', 'Y', 'B', 'O', 'NN', 'beats', 'after']
        # 31 Dahil olacak şekilde
        needed_words.extend([str(i) for i in range(1, 32)]) 
        ords = ORDINALS_TR if self.lang == 'tr' else ORDINALS_EN
        needed_words.extend(list(ords.keys()))

        download_queue = []
        for code in needed_words:
            word_text = LANGUAGES[self.lang].get(code, code)
            file_name = f"{self.lang}_{code}.mp3"
            file_path = os.path.join(CACHE_DIR, file_name)
            if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                download_queue.append((word_text, file_path))
        
        if download_queue:
            try: loop.run_until_complete(self.download_files(download_queue))
            except Exception as e: print(f"TTS Error: {e}")
        loop.close()
        self.load_sounds_to_memory(needed_words)

    async def download_files(self, queue):
        for text, path in queue:
            try:
                await asyncio.sleep(0.5)
                communicate = edge_tts.Communicate(text, self.voice)
                await communicate.save(path)
            except: 
                if os.path.exists(path): os.remove(path)

    def load_sounds_to_memory(self, codes):
        time.sleep(1)
        for code in codes:
            file_name = f"{self.lang}_{code}.mp3"
            file_path = os.path.join(CACHE_DIR, file_name)
            if os.path.exists(file_path) and os.path.getsize(file_path) > 100:
                try: self.sounds[code] = pygame.mixer.Sound(file_path)
                except: pass

    def play_sequence(self, text_line):
        threading.Thread(target=self._play_thread, args=(text_line,), daemon=True).start()

    def _play_thread(self, text_line):
        clean_text = text_line.replace("/", " ")
        words = clean_text.split()
        tokens = []
        for w in words:
            w = w.strip()
            if not w: continue
            if any(x in w for x in ['st', 'nd', 'rd', 'th']):
                if w in LANGUAGES[self.lang]: tokens.append(w); continue
            if w.isdigit():
                if 1 <= int(w) <= 31: tokens.append(w)
                continue
            w_lower = w.lower()
            if w_lower in ['beats', 'after']: tokens.append(w_lower); continue
            if "NN" in w: tokens.append("NN"); continue
            for char in w:
                if char in ['R', 'G', 'Y', 'B', 'O']: tokens.append(char)

        for token in tokens:
            if token in self.sounds:
                self.sounds[token].play()
                if any(x in token for x in ['st', 'nd', 'rd', 'th']) or token == "NN" or token in ['beats', 'after']:
                    time.sleep(0.6)
                else:
                    time.sleep(0.4)

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent, config, update_callback, lang_dict, gamepad_mgr):
        super().__init__(parent)
        self.config = config
        self.update_callback = update_callback
        self.lang = lang_dict
        self.gamepad_mgr = gamepad_mgr
        
        self.title(self.lang['settings'])
        self.geometry("580x420") 
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

        f1 = tk.Frame(grp_win, bg="#2b2b2b"); f1.pack(fill='x', padx=5, pady=5)
        tk.Label(f1, text=self.lang['font_size'], bg="#2b2b2b", fg="white", width=15, anchor='w').pack(side='left')
        self.fs = tk.Scale(f1, from_=10, to=30, orient=tk.HORIZONTAL, command=self.on_change, bg="#2b2b2b", fg="white", highlightthickness=0, length=200)
        self.fs.set(self.config.get('font_size', int)); self.fs.pack(side='left')

        f2 = tk.Frame(grp_win, bg="#2b2b2b"); f2.pack(fill='x', padx=5, pady=5)
        tk.Label(f2, text=self.lang['opacity'], bg="#2b2b2b", fg="white", width=15, anchor='w').pack(side='left')
        self.op = tk.Scale(f2, from_=20, to=100, orient=tk.HORIZONTAL, command=self.on_change, bg="#2b2b2b", fg="white", highlightthickness=0, length=200)
        self.op.set(int(self.config.get('opacity', float)*100)); self.op.pack(side='left')

        self.bgv = tk.BooleanVar(value=self.config.get('bg_visible')=='True')
        tk.Checkbutton(grp_win, text=self.lang['bg_visible'], variable=self.bgv, command=self.on_change, 
                      bg="#2b2b2b", fg="white", selectcolor="#444", activebackground="#2b2b2b").pack(anchor='w', padx=5, pady=5)

        grp_bar = ttk.LabelFrame(self.tab_visual, text=self.lang['grp_bar'])
        grp_bar.pack(fill='x', padx=10, pady=5)

        self.barv = tk.BooleanVar(value=self.config.get('visual_bar_enabled')=='True')
        tk.Checkbutton(grp_bar, text=self.lang['visual_bar_enable'], variable=self.barv, command=self.on_change, 
                      bg="#2b2b2b", fg="white", selectcolor="#444", activebackground="#2b2b2b").pack(anchor='w', padx=5, pady=2)
        
        self.popv = tk.BooleanVar(value=self.config.get('visual_bar_popup')=='True')
        tk.Checkbutton(grp_bar, text=self.lang['visual_bar_popup'], variable=self.popv, command=self.on_change, 
                      bg="#2b2b2b", fg="white", selectcolor="#444", activebackground="#2b2b2b").pack(anchor='w', padx=5, pady=2)

    def setup_hotkeys_tab(self):
        frame = tk.Frame(self.tab_hotkeys, bg="#2b2b2b")
        frame.pack(expand=True, padx=20, pady=20)
        
        self.create_hk_row(frame, 0, self.lang['hotkey_hide'], 'hotkey_hide')
        self.create_hk_row(frame, 1, self.lang['hotkey_lock'], 'hotkey_lock')
        self.create_hk_row(frame, 2, self.lang['hotkey_reset'], 'hotkey_reset')
        self.create_hk_row(frame, 3, self.lang['hotkey_tts'], 'hotkey_tts', is_gamepad_capable=True)

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
            self.config.set('opacity', self.op.get()/100)
            self.config.set('bg_visible', self.bgv.get())
            self.config.set('tts_enabled', self.ttsv.get())
            self.config.set('auto_read_first', self.autoread_v.get())
            self.config.set('visual_bar_enabled', self.barv.get())
            self.config.set('visual_bar_popup', self.popv.get())
            self.config.set('language', self.lang_var.get())
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
    def update(self, txt):
        self.cols = [COLOR_HEX_MAP[c] for c in txt if c in COLOR_HEX_MAP]; self.draw(self.cols)
    def draw(self, cols):
        if not self.canvas: return
        self.canvas.delete("all")
        if not cols: return
        self.canvas.update_idletasks()
        w = self.canvas.winfo_width(); h = self.canvas.winfo_height()
        if w <= 1: w = 300 
        if h <= 1: h = 40
        bw = w/len(cols)
        for i, c in enumerate(cols): self.canvas.create_rectangle(i*bw, 0, (i+1)*bw, h, fill=c, outline="")
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

class UpdatePopup(tk.Toplevel):
    def __init__(self, parent, version_data, config, lang_dict):
        super().__init__(parent)
        self.config = config
        self.lang = lang_dict
        self.version_tag = version_data.get('version', 'v0.0')
        self.download_url = version_data.get('url', LINK_GITHUB)
        
        # JSON'dan gelen notlar
        self.notes_tr = version_data.get('notes_tr', [])
        self.notes_en = version_data.get('notes_en', [])

        # Pencere Başlığı (Dinamik)
        self.title(self.lang['update_available'])
        self.geometry("520x480") # Pencere biraz daha büyütüldü
        self.configure(bg="#202020")
        self.attributes('-topmost', True)
        self.resizable(False, False)

        # --- 1. BAŞLIK (EN ÜST) ---
        header_frame = tk.Frame(self, bg="#202020")
        header_frame.pack(side='top', fill='x', pady=(20, 10))
        
        # Başlık metni artık dilden geliyor (LANGUAGES içinden)
        tk.Label(header_frame, text=self.lang['update_available'], font=("Segoe UI", 16, "bold"), fg="#00b894", bg="#202020").pack()
        tk.Label(header_frame, text=f"Version: {self.version_tag}", font=("Consolas", 10), fg="#b2bec3", bg="#202020").pack()

        # --- 2. ALT BUTONLAR (EN ALT - Sabitlensin diye önce bunu paketliyoruz) ---
        bottom_frame = tk.Frame(self, bg="#202020")
        bottom_frame.pack(side='bottom', fill='x', pady=15)

        # "Tekrar Gösterme" Kutucuğu
        self.dont_show = tk.BooleanVar()
        cb = tk.Checkbutton(bottom_frame, text=self.lang['dont_show_again'], variable=self.dont_show, 
                           bg="#202020", fg="#dfe6e9", selectcolor="#202020", activebackground="#202020", font=("Segoe UI", 9))
        cb.pack(side='top', pady=(0, 10))

        # Butonlar
        btn_container = tk.Frame(bottom_frame, bg="#202020")
        btn_container.pack(side='top')

        tk.Button(btn_container, text="İndir / Download", bg="#00b894", fg="white", font=("Segoe UI", 10, "bold"), 
                 command=self.go_url, width=18, relief="flat", pady=5, cursor="hand2").pack(side='left', padx=10)
        
        tk.Button(btn_container, text="Kapat / Close", bg="#d63031", fg="white", font=("Segoe UI", 10, "bold"), 
                 command=self.close_win, width=18, relief="flat", pady=5, cursor="hand2").pack(side='left', padx=10)

        # --- 3. SEKMELER (ORTA - Kalan alanı kaplasın) ---
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#202020', borderwidth=0)
        style.configure('TNotebook.Tab', background='#2d3436', foreground='white', padding=[15, 5], font=('Segoe UI', 9))
        style.map('TNotebook.Tab', background=[('selected', '#0984e3')], foreground=[('selected', 'white')])

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(side='top', fill='both', expand=True, padx=20, pady=5)

        # Türkçe Sekmesi
        self.frame_tr = tk.Frame(self.notebook, bg="#2d3436")
        self.create_notes_view(self.frame_tr, self.notes_tr)
        self.notebook.add(self.frame_tr, text="🇹🇷 Türkçe")

        # İngilizce Sekmesi
        self.frame_en = tk.Frame(self.notebook, bg="#2d3436")
        self.create_notes_view(self.frame_en, self.notes_en)
        self.notebook.add(self.frame_en, text="🇺🇸 English")
        
        # Eğer program dili İngilizce ise, İngilizce sekmesini aç
        if self.config.get('language') == 'en':
            self.notebook.select(1)

    def create_notes_view(self, parent, notes_list):
        # Scrollbar eklendi (Metin uzunsa butonları itmesin diye)
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
        # Markdown benzeri **bold** parsing
        parts = re.split(r'(\*\*.*?\*\*)', text)
        for part in parts:
            if part.startswith('**') and part.endswith('**'):
                clean_text = part[2:-2] # Yıldızları temizle
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
        
        # --- İKON VE PENCERE AYARI (Buraya eklendi) ---
        try:
            # EXE içine gömülen ikonu bulur ve pencereye basar
            icon_path = resource_path('app_icon.ico')
            self.root.iconbitmap(icon_path)
        except:
            pass # İkon dosyası klasörde yoksa hata vermez, varsayılanla devam eder

        # --- DEĞİŞKENLER ---
        self.cfg = ConfigManager()
        self.last_trigger_time = 0  # Çift ses okumasını engelleyen kilit (Buraya eklendi)
        self.lang = self.cfg.get('language')
        self.L = LANGUAGES[self.lang]
        
        # --- PENCERE AYARLARI ---
        self.root.title(self.L['app_title'])
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', self.cfg.get('opacity', float))
        self.cols = {'bg': '#1e1e1e', 'panel': '#252526', 'warn': '#fdcb6e', 'dang': '#d63031', 'succ': '#00b894', 'link': '#74b9ff', 'score_bg': '#e67e22', 'version': '#00d2d3'}
        self.root.configure(bg=self.cols['bg'])
        self.root.attributes('-transparentcolor', '#000001')
        
        self.gamepad = GamepadManager()
        self.tts = EdgeTTSManager(self.lang)
        self.vis = VisualBar(self.root, self.cfg)
        self.run = True; self.lock = False; self.vis_on = True; self.js=""; self.map={}; self.sid=None; self.inst="Guitar"; self.cache={}; self.lines=[]; self.lidx=0
        self.settings_window = None; self.last_btn_press = 0

        self.cont = tk.Frame(root, bg=self.cols['panel']); self.cont.pack(fill='both', expand=True, padx=2, pady=2)
        self.bar = tk.Frame(self.cont, bg=self.cols['warn'], width=8); self.bar.pack(side='left', fill='y')
        self.main = tk.Frame(self.cont, bg=self.cols['panel']); self.main.pack(side='left', fill='both', expand=True, padx=8, pady=5)
        self.vis.setup(self.main)
        
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

        self.setup_tags(); self.apply(); self.binds(self.root); self.hk()
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
            for k, f in [('hotkey_hide', self.tog), ('hotkey_lock', self.lck), ('hotkey_reset', self.reset_pos), ('hotkey_tts', self.nxt)]:
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
            if self.cfg.get('tts_enabled')=='True': self.tts.play_sequence(l)
            self.vis.update(l); self.lidx+=1
    def tog(self): 
        self.vis_on = not self.vis_on
        if self.vis_on: self.root.deiconify(); self.vis.set_visibility(True)
        else: self.root.withdraw(); self.vis.set_visibility(False)
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
        l = self.cfg.get('language')
        if l != self.lang: self.lang=l; self.L=LANGUAGES[l]; self.lbl_ti.config(text=self.L['ready']); self.tts=EdgeTTSManager(l)
        self.txt.config(font=("Consolas", self.cfg.get('font_size', int), "bold"))
        self.vis.setup(self.main); self.root.attributes('-alpha', self.cfg.get('opacity', float))
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

    def sett(self): 
        if self.settings_window and self.settings_window.winfo_exists(): self.settings_window.lift()
        else: self.settings_window = SettingsWindow(self.root, self.cfg, self.apply, self.L, self.gamepad)
    def setup_tags(self):
        for c, h in {'R':'#ff4757','G':'#2ed573','Y':'#ffa502','B':'#1e90ff','O':'#e67e22','W':'#f1f2f6'}.items():
            self.txt.tag_config(c, foreground=h)

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
        if m and m.group(1)!="Type" and m.group(1)!=self.inst: self.inst=m.group(1); self.trig()

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
        
        self.txt.config(state='normal'); self.txt.delete("1.0",'end'); self.lines=[]; self.lidx=0; self.vis.update("")
        if pth:
            raw = pth.group(1).replace(", ", "\n").replace(",", "\n")
            for l in raw.split('\n'):
                for p in re.split(r'([RGBYO])', l): self.txt.insert('end', p, p if p in "RGBYO" else "W")
                self.txt.insert('end', '\n')
                if re.search(r'[RGBYO]|NN', l): self.lines.append(l.strip())
            
            if self.cfg.get('auto_read_first') == 'True':
                self.root.after(500, self.nxt) 
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
    def close(self): self.run=False; self.vis.destroy(); self.root.destroy(); sys.exit()

if __name__ == "__main__":
    r = tk.Tk(); app = FestivalPathOverlay(r); r.mainloop()
