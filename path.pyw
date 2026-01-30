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
from math import ceil
from urllib.parse import quote

# --- HARİCİ KÜTÜPHANELER ---
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
APP_VERSION = "v2.3"
REPO_OWNER = "YOUR_REPO_OWNER"
REPO_NAME = "YOUR_REPO_NAME"
DEVELOPER_NAME = "YOUR_NAME"

LINK_GITHUB = f"https://github.com/{REPO_OWNER}/{REPO_NAME}"
LINK_TWITCH = "https://www.twitch.tv/..."
LINK_KICK = "https://kick.com/..."
LINK_HUB = "http://your-website.com/"
UPDATE_JSON_URL = "https://raw.githubusercontent.com/YOUR_REPO_OWNER/YOUR_REPO_NAME/main/update.json"

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
AUTH_JSON_URL = "https://raw.githubusercontent.com/YOUR_REPO_OWNER/YOUR_REPO_NAME/main/auth.json"
CONFIG_FILE = os.path.join(BASE_DIR, 'config.ini')
SECRET_KEY = "YOUR_SECRET_KEY"

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
        'gt_lang': 'tr', 
        'color_blind': 'Renk Körü Modu',
        'Normal': 'Normal', 'Deuteranope': 'Dötenarop (Yeşil)', 'Protanope': 'Protanop (Kırmızı)', 'Tritanope': 'Tritanope',
        'R': 'Kırmızı', 'G': 'Yeşil', 'Y': 'Sarı', 'B': 'Mavi', 'O': 'Turuncu', 'NN': 'Sonraki Nota',
        'ls_title': 'CANLI SKOR',
        'ls_no_data': 'Veri Yok',
        'ls_season_title': 'SEZON',
        'ls_alltime_title': 'GENEL (ALL-TIME)',
        'ls_show': 'Canlı Skor Penceresini Göster',
        'ls_lock_pos': 'Pencere Pozisyonunu Kilitle',
        'ls_season_no': 'Geçerli Sezon No:',
        'ls_font': 'Skor Font Boyutu:',
        'ls_opacity': 'Pencere Opaklığı:'
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
        'gt_lang': 'en',
        'color_blind': 'Color Blind Mode',
        'Normal': 'Normal', 'Deuteranope': 'Deuteranope', 'Protanope': 'Protanope', 'Tritanope': 'Tritanope',
        'R': 'Red', 'G': 'Green', 'Y': 'Yellow', 'B': 'Blue', 'O': 'Orange', 'NN': 'Next Note',
        'ls_title': 'LIVE SCORE',
        'ls_no_data': 'No Data',
        'ls_season_title': 'SEASON',
        'ls_alltime_title': 'ALL-TIME',
        'ls_show': 'Show Live Score Popup',
        'ls_lock_pos': 'Lock Position',
        'ls_season_no': 'Current Season No:',
        'ls_font': 'Score Font Size:',
        'ls_opacity': 'Window Opacity:'
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
            'color_blind_mode': 'Normal',
            # --- AUTH & SKOR AYARLARI ---
            'season': '12',
            'score_popup_enabled': 'True',
            'score_popup_x': '300', 'score_popup_y': '300',
            'score_popup_locked': 'False',
            'score_popup_opacity': '0.9', 
            'score_popup_font_size': '14'
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

    def get(self, key, type_func=str, default=None):
        try: 
            val = self.config['SETTINGS'].get(key, self.defaults.get(key, ''))
            if not val and default is not None:
                return default
            return type_func(val)
        except: 
            if default is not None: return default
            # Fallback to defaults dict if possible
            def_val = self.defaults.get(key, '')
            try: return type_func(def_val)
            except: return type_func() # Last resort: empty int/str/float

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
    """Google Translate tabanlı TTS - DÜZELTİLMİŞ VERSİYON"""
    def __init__(self, language_code):
        if not pygame.get_init(): pygame.init()
        try: pygame.mixer.init()
        except: pass
        self.lang_code = language_code
        self.gt_lang = LANGUAGES[language_code].get('gt_lang', 'en')
        self.vocab = LANGUAGES[language_code]

    def play_live(self, text_line):
        threading.Thread(target=self._stream_audio, args=(text_line,), daemon=True).start()

    def _stream_audio(self, text):
        if not text.strip(): return
        
        # 1. Temel Temizlik
        clean_text = re.sub(r'[()\/]', ' ', text)
        
        # --- DÜZELTME: 6th -> 6. (Sadece Türkçe ise) ---
        if self.lang_code == 'tr':
            clean_text = re.sub(r'(\d+)(st|nd|rd|th)', r'\1.', clean_text)
        
        # 2. Renk Kodlarını Değiştir
        target_keys = ['R', 'G', 'Y', 'B', 'O', 'NN']
        for key in target_keys:
            if key in self.vocab:
                replacement = f" {self.vocab[key]} " 
                clean_text = clean_text.replace(key, replacement)

        try:
            tts = gTTS(text=clean_text, lang=self.gt_lang, slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            pygame.mixer.music.load(fp)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"TTS Stream Error: {e}")

class EpicScraper:
    """Kullanıcı tarafından sağlanan Epic Games API Scraper - ENTREGRE EDİLDİ"""
    def __init__(self, config_manager):
        self.cfg = config_manager
        self.access_token = None
        self.my_account_id = None
        self.session = requests.Session()
        self.session.verify = False 
        
        self.REFRESH_TOKEN = None
        self.BASIC_AUTH = None

    def fetch_remote_auth(self):
        self.log("[AUTH] Uzak sunucudan bilgiler alınıyor...")
        try:
            resp = requests.get(AUTH_JSON_URL, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                enc_refresh = data.get('epic_refresh_token')
                enc_basic = data.get('epic_basic_auth')
                
                if enc_refresh and enc_basic:
                    self.REFRESH_TOKEN = self.deobfuscate(enc_refresh, mode='HEX')
                    self.BASIC_AUTH = self.deobfuscate(enc_basic, mode='ALPHANUM')
                    
                    if self.REFRESH_TOKEN and self.BASIC_AUTH:
                        self.log("[AUTH] Uzak bilgiler alındı ve çözüldü.")
                        return True
            
            self.log("[AUTH WARN] Uzak sunucuya erişilemedi.")
        except Exception as e:
            self.log(f"[AUTH ERROR] Fetch Error: {e}")
            
        return False

    def log(self, message):
        hidden_tags = ["[SEARCH]", "[SCAN]", "[SUCCESS]", "[FAIL]", "[INFO]", "[DEBUG]", "[SONG]"]
        if any(tag in message for tag in hidden_tags):
            return
        print(message)

    def login(self):
        self.log("[AUTH] Token alınıyor...")
        try:
            if not self.REFRESH_TOKEN:
                if not self.fetch_remote_auth():
                    self.log("[AUTH FAIL] Kimlik bilgileri bulunamadı!")
                    return False

            if not self.REFRESH_TOKEN or not self.BASIC_AUTH:
                 self.log("[AUTH FAIL] Tokenlar eksik.")
                 return False
            
            resp = self.session.post(
                'https://account-public-service-prod.ol.epicgames.com/account/api/oauth/token',
                headers={'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': f'Basic {self.BASIC_AUTH}'},
                data={'grant_type': 'refresh_token', 'refresh_token': self.REFRESH_TOKEN, 'token_type': 'eg1'},
                timeout=20
            )
            resp.raise_for_status()
            data = resp.json()
            self.access_token = data['access_token']
            self.my_account_id = data['account_id']
            self.log(f"[AUTH] Giriş başarılı. Bot ID: {self.my_account_id}")
            return True
        except Exception as e:
            self.log(f"[ERROR] Login Hatası: {str(e)}")
            return False

    def get_account_id_from_log(self, log_path):
        if not os.path.exists(log_path): return None
        try:
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                head_content = f.read(10 * 1024 * 1024) 
                matches = re.finditer(r'-caldera=([A-Za-z0-9_\-\.]+)', head_content)
                for match in matches:
                    decoded = self._decode_jwt(match.group(1))
                    if decoded: return decoded
        except Exception as e:
            self.log(f"[HATA] Log okuma: {e}")
        return None

    def _decode_jwt(self, token):
        try:
            parts = token.split('.')
            if len(parts) != 3: return None
            payload = parts[1]
            padding = 4 - (len(payload) % 4)
            if padding != 4: payload += '=' * padding
            decoded = base64.urlsafe_b64decode(payload)
            return json.loads(decoded).get('account_id')
        except: return None

    def get_song_event_id(self, song_id_input):
        self.log(f"[SONG] '{song_id_input}' verisi çekiliyor...")
        try:
            url = 'https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game/spark-tracks'
            resp = self.session.get(url, timeout=20)
            data = resp.json()
            if song_id_input in data:
                val = data[song_id_input]
                if isinstance(val, dict) and 'track' in val:
                    return val['track'].get('su')
            song_id_lower = song_id_input.lower().replace("sparks_song_","").strip()
            for key, val in data.items():
                if not isinstance(val, dict): continue
                track = val.get('track')
                if not track: continue
                key_lower = key.lower()
                sn_lower = track.get('sn', '').lower()
                tt_lower = track.get('tt', '').lower()
                if (key_lower == song_id_lower) or (sn_lower == song_id_lower) or (tt_lower == song_id_lower):
                    su_id = track.get('su')
                    self.log(f"[SONG] Döngüde bulundu! Event ID: {su_id}")
                    return su_id
            self.log("[ERROR] Şarkı bulunamadı.")
            return None
        except Exception as e:
            self.log(f"[ERROR] Song API Hatası: {str(e)}")
            return None

    def search_score(self, target_acc_id, event_id, instrument, season, page_limit=20):
        if not self.access_token: return None
        inst_map = {
            'Lead': 'Solo_Guitar', 'Guitar': 'Solo_Guitar',
            'Pro Guitar': 'Solo_PeripheralGuitar', 'PlasticGuitar': 'Solo_PeripheralGuitar',
            'Bass': 'Solo_Bass',
            'Pro Bass': 'Solo_PeripheralBass', 'PlasticBass': 'Solo_PeripheralBass',
            'Drums': 'Solo_Drums', 'Drum': 'Solo_Drums',
            'Vocals': 'Solo_Vocals', 'Vocal': 'Solo_Vocals'
        }
        api_inst = inst_map.get(instrument, instrument) 
        self.log(f"[SEARCH] Parametreler: {event_id} | {api_inst} | {season}")
        headers = {'Authorization': f'Bearer {self.access_token}'}
        if str(season) == "alltime":
            final_event_id = f"alltime_{event_id}_{api_inst}"
            final_window_id = "alltime"
        else:
            s_num = int(season)
            final_event_id = f"season{s_num:03d}_{event_id}"
            final_window_id = f"{event_id}_{api_inst}"
        
        try:
            self.log("[SEARCH] Yöntem 1: Hedef Kullanıcı ID'si ile deneniyor...")
            url = f"https://events-public-service-live.ol.epicgames.com/api/v1/leaderboards/FNFestival/{final_event_id}/{final_window_id}/{target_acc_id}?page=0&rank=0&appId=Fortnite"
            resp = self.session.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                entries = resp.json().get('entries', [])
                if entries:
                    if entries[0].get('rank') == 1 and entries[0].get('teamId') != target_acc_id:
                        pass
                    else:
                        for entry in entries:
                            if entry.get('teamId') == target_acc_id:
                                self.log(f"[SUCCESS] 🔥 BULUNDU! Rank: {entry.get('rank')}")
                                return self.parse_entry(entry)
        except: pass

        self.log(f"[SEARCH] Yöntem 2: İlk {page_limit*100} kişi taranıyor...")
        base_url = f"https://events-public-service-live.ol.epicgames.com/api/v1/leaderboards/FNFestival/{final_event_id}/{final_window_id}/{self.my_account_id}"
        for page in range(page_limit): 
            try:
                url = f"{base_url}?page={page}&rank=0&appId=Fortnite"
                resp = self.session.get(url, headers=headers, timeout=5)
                if resp.status_code != 200: break
                entries = resp.json().get('entries', [])
                if not entries: break
                for entry in entries:
                    if entry.get('teamId') == target_acc_id:
                        self.log(f"[SUCCESS] 🔥 BULUNDU! (Sayfa: {page}, Rank: {entry.get('rank')})")
                        return self.parse_entry(entry)
                time.sleep(0.1)
            except: break
        return None

    def parse_entry(self, entry):
        best_score = 0
        best_stats = {}
        for sess in entry.get('sessionHistory', []):
            stats = sess.get('trackedStats', {})
            if stats.get('SCORE', 0) > best_score:
                best_score = stats.get('SCORE', 0)
                best_stats = stats
        return {
            "score": best_score,
            "rank": entry.get('rank'),
            "full_combo": (best_stats.get('FULL_COMBO') == 1),
            "accuracy": int(best_stats.get('ACCURACY', 0) / 10000) if best_stats.get('ACCURACY') else 0,
            "stars": best_stats.get('STARS_EARNED'),
            "difficulty": best_stats.get('DIFFICULTY')
        }

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
        self.tab_livescore = tk.Frame(self.notebook, bg="#2b2b2b")
        self.notebook.add(self.tab_livescore, text="Live Score")
        self.notebook.add(self.tab_hotkeys, text=self.lang['tab_hotkeys'])
        self.notebook.add(self.tab_system, text=self.lang['tab_system'])
        self.setup_visual_tab()
        self.setup_livescore_tab()
        self.setup_hotkeys_tab()
        self.setup_system_tab()

    def setup_visual_tab(self):
        grp_win = ttk.LabelFrame(self.tab_visual, text=self.lang['grp_window'])
        grp_win.pack(fill='x', padx=10, pady=10)
        f1 = tk.Frame(grp_win, bg="#2b2b2b"); f1.pack(fill='x', padx=5, pady=5)
        tk.Label(f1, text=self.lang['font_size'], bg="#2b2b2b", fg="white", width=20, anchor='w').pack(side='left')
        self.fs = tk.Scale(f1, from_=10, to=40, orient=tk.HORIZONTAL, command=self.on_change, bg="#2b2b2b", fg="white", highlightthickness=0, length=200)
        self.fs.set(self.config.get('font_size', int)); self.fs.pack(side='left')
        f2 = tk.Frame(grp_win, bg="#2b2b2b"); f2.pack(fill='x', padx=5, pady=5)
        tk.Label(f2, text=self.lang['opacity'], bg="#2b2b2b", fg="white", width=20, anchor='w').pack(side='left')
        self.op = tk.Scale(f2, from_=20, to=100, orient=tk.HORIZONTAL, command=self.on_change, bg="#2b2b2b", fg="white", highlightthickness=0, length=200)
        self.op.set(int(self.config.get('opacity', float)*100)); self.op.pack(side='left')
        self.bgv = tk.BooleanVar(value=self.config.get('bg_visible')=='True')
        tk.Checkbutton(grp_win, text=self.lang['bg_visible'], variable=self.bgv, command=self.on_change, bg="#2b2b2b", fg="white", selectcolor="#444", activebackground="#2b2b2b").pack(anchor='w', padx=5, pady=5)
        f3 = tk.Frame(grp_win, bg="#2b2b2b"); f3.pack(fill='x', padx=5, pady=5)
        tk.Label(f3, text=self.lang['color_blind'], bg="#2b2b2b", fg="white", width=20, anchor='w').pack(side='left')
        self.cb_mode = ttk.Combobox(f3, values=["Normal", "Deuteranope", "Protanope", "Tritanope"], state="readonly", width=20)
        self.cb_mode.set(self.config.get('color_blind_mode'))
        self.cb_mode.pack(side='left', padx=5)
        self.cb_mode.bind("<<ComboboxSelected>>", self.on_change)
        grp_bar = ttk.LabelFrame(self.tab_visual, text=self.lang['grp_bar'])
        grp_bar.pack(fill='x', padx=10, pady=5)
        self.barv = tk.BooleanVar(value=self.config.get('visual_bar_enabled')=='True')
        tk.Checkbutton(grp_bar, text=self.lang['visual_bar_enable'], variable=self.barv, command=self.on_change, bg="#2b2b2b", fg="white", selectcolor="#444", activebackground="#2b2b2b").pack(anchor='w', padx=5, pady=2)
        self.popv = tk.BooleanVar(value=self.config.get('visual_bar_popup')=='True')
        tk.Checkbutton(grp_bar, text=self.lang['visual_bar_popup'], variable=self.popv, command=self.on_change, bg="#2b2b2b", fg="white", selectcolor="#444", activebackground="#2b2b2b").pack(anchor='w', padx=5, pady=2)
        self.nextv = tk.BooleanVar(value=self.config.get('current_line_popup_enabled')=='True')
        tk.Checkbutton(grp_bar, text=self.lang['current_line_popup_enable'], variable=self.nextv, command=self.on_change, bg="#2b2b2b", fg="#fab1a0", selectcolor="#444", activebackground="#2b2b2b").pack(anchor='w', padx=5, pady=2)
        f_pop = tk.Frame(grp_bar, bg="#2b2b2b"); f_pop.pack(fill='x', padx=5, pady=5)
        tk.Label(f_pop, text=self.lang['popup_font_size'], bg="#2b2b2b", fg="#fab1a0", width=20, anchor='w').pack(side='left')
        self.fs_pop = tk.Scale(f_pop, from_=10, to=60, orient=tk.HORIZONTAL, command=self.on_change, bg="#2b2b2b", fg="white", highlightthickness=0, length=200)
        self.fs_pop.set(self.config.get('popup_font_size', int)); self.fs_pop.pack(side='left')

    def setup_livescore_tab(self):
        frame = tk.Frame(self.tab_livescore, bg="#2b2b2b")
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        self.scorepopv = tk.BooleanVar(value=self.config.get('score_popup_enabled')=='True')
        cb_show = tk.Checkbutton(frame, text=self.lang.get('ls_show', "Show Live Score Popup"), variable=self.scorepopv, command=self.on_change, bg="#2b2b2b", fg="#74b9ff", font=("Segoe UI", 10, "bold"), selectcolor="#444", activebackground="#2b2b2b")
        cb_show.pack(anchor='w', pady=5)
        self.scorelockv = tk.BooleanVar(value=self.config.get('score_popup_locked')=='True')
        cb_lock = tk.Checkbutton(frame, text=self.lang.get('ls_lock_pos', "Lock Position"), variable=self.scorelockv, command=self.on_change, bg="#2b2b2b", fg="#fab1a0", font=("Segoe UI", 9), selectcolor="#444", activebackground="#2b2b2b")
        cb_lock.pack(anchor='w', pady=5, padx=20)
        tk.Label(frame, text="-"*50, bg="#2b2b2b", fg="#636e72").pack(anchor='w', pady=5)
        row_season = tk.Frame(frame, bg="#2b2b2b")
        row_season.pack(fill='x', pady=5)
        tk.Label(row_season, text=self.lang.get('ls_season_no', "Season No:"), bg="#2b2b2b", fg="white", width=20, anchor='w').pack(side='left')
        self.ent_season = tk.Entry(row_season, bg="#444", fg="white", width=10)
        self.ent_season.insert(0, str(self.config.get('season')))
        self.ent_season.bind("<Return>", self.on_change)
        self.ent_season.bind("<FocusOut>", self.on_change)
        self.ent_season.pack(side='left')
        row_font = tk.Frame(frame, bg="#2b2b2b")
        row_font.pack(fill='x', pady=5)
        tk.Label(row_font, text=self.lang.get('ls_font', "Font Size:"), bg="#2b2b2b", fg="white", width=20, anchor='w').pack(side='left')
        self.fs_score = tk.Scale(row_font, from_=8, to=24, orient=tk.HORIZONTAL, command=self.on_change, bg="#2b2b2b", fg="white", highlightthickness=0, length=200)
        self.fs_score.set(self.config.get('score_popup_font_size', int, default=14))
        self.fs_score.pack(side='left')
        row_op = tk.Frame(frame, bg="#2b2b2b")
        row_op.pack(fill='x', pady=5)
        tk.Label(row_op, text=self.lang.get('ls_opacity', "Opacity:"), bg="#2b2b2b", fg="white", width=20, anchor='w').pack(side='left')
        self.op_score = tk.Scale(row_op, from_=20, to=100, orient=tk.HORIZONTAL, command=self.on_change, bg="#2b2b2b", fg="white", highlightthickness=0, length=200)
        self.op_score.set(int(float(self.config.get('score_popup_opacity', default=0.9))*100))
        self.op_score.pack(side='left')

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
            if gp_btn != 'NONE': current_val += f" / {format_gamepad_text(gp_btn)}"
        b = tk.Button(parent, text=current_val, bg="#444", fg="white", width=20, relief="flat", font=("Segoe UI Symbol", 9))
        b.config(command=lambda: self.start_listening(k, b, is_gamepad_capable))
        b.grid(row=row, column=1, padx=10, pady=10, sticky='w')

    def setup_system_tab(self):
        col1 = tk.Frame(self.tab_system, bg="#2b2b2b"); col1.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        grp_lang = ttk.LabelFrame(col1, text=self.lang['grp_lang']); grp_lang.pack(fill='x', pady=5)
        self.lang_var = tk.StringVar(value=self.config.get('language'))
        tk.Radiobutton(grp_lang, text="Türkçe", variable=self.lang_var, value="tr", command=self.on_change, bg="#2b2b2b", fg="white", selectcolor="#444").pack(anchor='w', padx=10, pady=5)
        tk.Radiobutton(grp_lang, text="English", variable=self.lang_var, value="en", command=self.on_change, bg="#2b2b2b", fg="white", selectcolor="#444").pack(anchor='w', padx=10, pady=5)
        col2 = tk.Frame(self.tab_system, bg="#2b2b2b"); col2.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        grp_tts = ttk.LabelFrame(col2, text=self.lang['grp_tts']); grp_tts.pack(fill='x', pady=5)
        self.ttsv = tk.BooleanVar(value=self.config.get('tts_enabled')=='True')
        tk.Checkbutton(grp_tts, text=self.lang['tts_enable'], variable=self.ttsv, command=self.on_change, bg="#2b2b2b", fg="white", selectcolor="#444").pack(anchor='w', padx=10, pady=5)
        self.autoread_v = tk.BooleanVar(value=self.config.get('auto_read_first')=='True')
        tk.Checkbutton(grp_tts, text=self.lang['auto_read'], variable=self.autoread_v, command=self.on_change, bg="#2b2b2b", fg="white", selectcolor="#444").pack(anchor='w', padx=10, pady=5)

    def start_listening(self, k, b, is_gamepad_capable):
        b.config(text=self.lang['hotkey_waiting'], bg="#d63031")
        self.update()
        threading.Thread(target=self.listen_thread, args=(k, b, is_gamepad_capable), daemon=True).start()

    def listen_thread(self, k, b, is_gamepad_capable):
        start_time = time.time(); self.key_pressed = None
        def on_key(e): self.key_pressed = e.name
        hook = keyboard.on_press(on_key)
        while time.time() - start_time < 5:
            if self.key_pressed:
                self.config.set(k, self.key_pressed)
                if is_gamepad_capable: self.config.set('gamepad_tts_btn', 'NONE')
                break
            if is_gamepad_capable:
                btn = self.gamepad_mgr.get_any_input()
                if btn:
                    self.config.set('gamepad_tts_btn', btn); self.config.set(k, 'NONE')
                    break
            time.sleep(0.05)
        keyboard.unhook(hook); self.update_callback()

    def on_change(self, *a):
        try:
            for k, v in [('font_size', self.fs.get()), ('popup_font_size', self.fs_pop.get()), ('opacity', self.op.get()/100), ('bg_visible', self.bgv.get()), ('tts_enabled', self.ttsv.get()), ('auto_read_first', self.autoread_v.get()), ('visual_bar_enabled', self.barv.get()), ('visual_bar_popup', self.popv.get()), ('current_line_popup_enabled', self.nextv.get()), ('score_popup_enabled', self.scorepopv.get()), ('score_popup_locked', self.scorelockv.get()), ('season', self.ent_season.get()), ('score_popup_font_size', self.fs_score.get()), ('score_popup_opacity', self.op_score.get()/100), ('language', self.lang_var.get()), ('color_blind_mode', self.cb_mode.get())]: self.config.set(k, v)
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
    def update(self, txt, color_map): self.cols = [color_map[c] for c in txt if c in color_map]; self.draw(self.cols)
    def draw(self, cols):
        if not self.canvas: return
        try:
            self.canvas.delete("all")
            if not cols: return
            w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
            if w <= 1: w = 300
            bw = w/len(cols)
            for i, c in enumerate(cols): self.canvas.create_rectangle(i*bw, 0, (i+1)*bw + 1, h, fill=c, outline="")
        except: pass
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

class LineReaderPopup:
    def __init__(self, root, config):
        self.root = root; self.cfg = config; self.popup = None; self.txt_widget = None; self.ox, self.oy = 0, 0
    def setup(self):
        self.destroy()
        if self.cfg.get('current_line_popup_enabled') != 'True': return
        self.popup = tk.Toplevel(self.root); self.popup.overrideredirect(True); self.popup.attributes('-topmost', True, '-alpha', 0.8); self.popup.config(bg='black')
        x, y = self.cfg.get('popup_x', int), self.cfg.get('popup_y', int)
        self.popup.geometry(f"400x60+{x}+{y}")
        self.txt_widget = tk.Text(self.popup, font=("Consolas", self.cfg.get('popup_font_size', int), "bold"), bg="black", fg="white", bd=0, height=1)
        self.txt_widget.pack(fill='both', expand=True)
        self.txt_widget.bind("<ButtonPress-1>", self.sm); self.txt_widget.bind("<ButtonRelease-1>", self.em); self.txt_widget.bind("<B1-Motion>", self.mm)
        self.txt_widget.config(state='disabled', cursor='arrow')
    def update_text(self, text, color_map):
        if not (self.popup and self.txt_widget): return
        self.txt_widget.config(state='normal'); self.txt_widget.delete("1.0", "end")
        for c, h in color_map.items(): self.txt_widget.tag_config(c, foreground=h)
        self.txt_widget.tag_config('W', foreground='#f1f2f6')
        if text:
            for p in re.split(r'([RGBYO])', text): self.txt_widget.insert('end', p, p if p in "RGBYO" else "W")
        else: self.txt_widget.insert('end', "...", "W")
        self.txt_widget.tag_configure("center", justify='center'); self.txt_widget.tag_add("center", "1.0", "end"); self.txt_widget.config(state='disabled')
    def destroy(self):
        if self.popup: self.popup.destroy(); self.popup = None
    def sm(self, e): self.ox, self.oy = e.x, e.y
    def em(self, e): 
        if self.popup: self.cfg.set('popup_x', self.popup.winfo_x()); self.cfg.set('popup_y', self.popup.winfo_y())
    def mm(self, e): 
        if self.popup: self.popup.geometry(f"+{self.popup.winfo_x()+e.x-self.ox}+{self.popup.winfo_y()+e.y-self.oy}")
    def set_visibility(self, v): 
        if self.popup: self.popup.deiconify() if (v and self.cfg.get('current_line_popup_enabled') == 'True') else self.popup.withdraw()

class UpdatePopup(tk.Toplevel):
    def __init__(self, parent, version_data, config, lang_dict):
        super().__init__(parent); self.config = config; self.lang = lang_dict
        self.version_tag = version_data.get('version', 'v0.0')
        self.download_url = version_data.get('url', LINK_GITHUB)
        self.title(self.lang['update_available']); self.geometry("520x480"); self.configure(bg="#202020"); self.attributes('-topmost', True); self.resizable(False, False)
        header = tk.Frame(self, bg="#202020"); header.pack(side='top', fill='x', pady=20)
        tk.Label(header, text=self.lang['update_available'], font=("Segoe UI", 16, "bold"), fg="#00b894", bg="#202020").pack()
        tk.Label(header, text=f"Version: {self.version_tag}", font=("Consolas", 10), fg="#b2bec3", bg="#202020").pack()
        bot = tk.Frame(self, bg="#202020"); bot.pack(side='bottom', fill='x', pady=15)
        self.dont_show = tk.BooleanVar()
        tk.Checkbutton(bot, text=self.lang['dont_show_again'], variable=self.dont_show, bg="#202020", fg="#dfe6e9", selectcolor="#202020", activebackground="#202020").pack(pady=5)
        btns = tk.Frame(bot, bg="#202020"); btns.pack()
        tk.Button(btns, text="Download", bg="#00b894", fg="white", command=self.go_url, width=15).pack(side='left', padx=10)
        tk.Button(btns, text="Close", bg="#d63031", fg="white", command=self.close_win, width=15).pack(side='left', padx=10)
        nb = ttk.Notebook(self); nb.pack(fill='both', expand=True, padx=20)
        f_tr = tk.Frame(nb, bg="#2d3436"); self.cv(f_tr, version_data.get('notes_tr', [])); nb.add(f_tr, text="TR")
        f_en = tk.Frame(nb, bg="#2d3436"); self.cv(f_en, version_data.get('notes_en', [])); nb.add(f_en, text="EN")
        if self.config.get('language') == 'en': nb.select(1)
    def cv(self, p, l):
        t = tk.Text(p, bg="#2d3436", fg="#dfe6e9", font=("Segoe UI", 10), bd=0, padx=10, pady=10); t.pack(fill='both', expand=True)
        if isinstance(l, list):
            for item in l: t.insert('end', f"• {item}\n\n")
        t.config(state='disabled')
    def go_url(self): webbrowser.open(self.download_url); self.close_win()
    def close_win(self):
        if self.dont_show.get(): self.config.set('ignored_version', self.version_tag)
        self.destroy()

class LiveScorePopup(tk.Toplevel):
    def __init__(self, root, config, lang_dict):
        super().__init__(root); self.cfg = config; self.lang = lang_dict; self.ox, self.oy = 0, 0; self.is_locked = False
        self.overrideredirect(True); self.attributes('-topmost', True); self.config(bg="#2b2b2b")
        self.main_frame = tk.Frame(self, bg="#2b2b2b", highlightthickness=2, highlightbackground="#00b894")
        self.main_frame.pack(fill='both', expand=True)
        self.title_bar = tk.Frame(self.main_frame, bg="#1a1a1a", height=30); self.title_bar.pack(side='top', fill='x'); self.title_bar.pack_propagate(False)
        self.title_label = tk.Label(self.title_bar, text=f"🏆 {self.lang.get('ls_title', 'LIVE SCORE')}", bg="#1a1a1a", fg="#00cec9", font=("Segoe UI", 9, "bold"), cursor="fleur")
        self.title_label.pack(side='left', padx=8)
        for w in [self.title_bar, self.title_label]:
            w.bind("<ButtonPress-1>", self.start_move); w.bind("<ButtonRelease-1>", self.stop_move); w.bind("<B1-Motion>", self.do_move)
        self.lock_btn = tk.Label(self.title_bar, text="🔓", bg="#1a1a1a", fg="#fdcb6e", font=("Segoe UI", 12), cursor="hand2", padx=5)
        self.lock_btn.pack(side='right', padx=2); self.lock_btn.bind("<Button-1>", self.toggle_lock)
        close_btn = tk.Label(self.title_bar, text="✕", bg="#1a1a1a", fg="#ff7675", font=("Segoe UI", 12, "bold"), cursor="hand2", padx=5)
        close_btn.pack(side='right', padx=2); close_btn.bind("<Button-1>", lambda e: self.hide_popup())
        self.content_frame = tk.Frame(self.main_frame, bg="#2b2b2b"); self.content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        at_f = tk.Frame(self.content_frame, bg="#252526", highlightthickness=1, highlightbackground="#74b9ff"); at_f.pack(fill='x', pady=(0, 5))
        tk.Label(at_f, text=self.lang.get('ls_alltime_title', 'ALL-TIME'), bg="#252526", fg="#74b9ff", font=("Segoe UI", 8, "bold")).pack(anchor='w', padx=5, pady=(3, 0))
        self.lbl_alltime = tk.Label(at_f, text="---", bg="#252526", fg="white", font=("Consolas", 14, "bold"), wraplength=280); self.lbl_alltime.pack(anchor='w', padx=5, pady=(0, 3), fill='x')
        ss_f = tk.Frame(self.content_frame, bg="#252526", highlightthickness=1, highlightbackground="#fdcb6e"); ss_f.pack(fill='x')
        self.lbl_season_title = tk.Label(ss_f, text=self.lang.get('ls_season_title', 'SEASON'), bg="#252526", fg="#fdcb6e", font=("Segoe UI", 8, "bold")); self.lbl_season_title.pack(anchor='w', padx=5, pady=(3, 0))
        self.lbl_season = tk.Label(ss_f, text="---", bg="#252526", fg="white", font=("Consolas", 14, "bold"), wraplength=280); self.lbl_season.pack(anchor='w', padx=5, pady=(0, 3), fill='x')
        self.refresh_state()

    def toggle_lock(self, event=None):
        self.is_locked = not self.is_locked; self.cfg.set('score_popup_locked', str(self.is_locked))
        if self.is_locked: self.lock_btn.config(text="🔒", fg="#e74c3c"); self.title_bar.config(bg="#3d1a1a")
        else: self.lock_btn.config(text="🔓", fg="#fdcb6e"); self.title_bar.config(bg="#1a1a1a")
    def hide_popup(self): self.cfg.set('score_popup_enabled', 'False'); self.withdraw()
    def refresh_state(self):
        if self.cfg.get('score_popup_enabled') != 'True': self.withdraw(); return
        else: self.deiconify()
        self.attributes('-alpha', self.cfg.get('score_popup_opacity', float, default=0.9))
        fs = int(self.cfg.get('score_popup_font_size', default=14))
        self.lbl_alltime.config(font=("Consolas", fs, "bold")); self.lbl_season.config(font=("Consolas", fs, "bold"))
        x, y = self.cfg.get('score_popup_x', int), self.cfg.get('score_popup_y', int)
        self.geometry(f"300x180+{x}+{y}")
    def update_data(self, alltime, seasonal):
        if self.cfg.get('score_popup_enabled') != 'True': return
        self.deiconify()
        if alltime: self.lbl_alltime.config(text=f"{alltime.get('score', 0):,} #{alltime.get('rank', '-')} {'⭐'*alltime.get('stars',0)}")
        else: self.lbl_alltime.config(text=self.lang.get('ls_no_data', 'No Data'))
        if seasonal: self.lbl_season.config(text=f"{seasonal.get('score', 0):,} #{seasonal.get('rank', '-')} {'⭐'*seasonal.get('stars',0)}")
        else: self.lbl_season.config(text=self.lang.get('ls_no_data', 'No Data'))
        self.lbl_season_title.config(text=f"{self.lang.get('ls_season_title', 'SEASON')} {self.cfg.get('season')}")
    def start_move(self, event):
        if not self.is_locked: self.ox, self.oy = event.x, event.y
    def stop_move(self, event):
        if not self.is_locked: self.cfg.set('score_popup_x', self.winfo_x()); self.cfg.set('score_popup_y', self.winfo_y())
    def do_move(self, event):
        if not self.is_locked: self.geometry(f"+{self.winfo_x() + event.x - self.ox}+{self.winfo_y() + event.y - self.oy}")

class FestivalPathOverlay:
    def __init__(self, root):
        self.root = root; self.cfg = ConfigManager(); self.last_trigger_time = 0; self.auto_read_timer = None
        self.lang = self.cfg.get('language'); self.L = LANGUAGES[self.lang]; self.current_colors = COLOR_PALETTES['Normal']; self.current_line_text = ""
        self.root.title(self.L['app_title']); self.root.overrideredirect(True); self.root.attributes('-topmost', True); self.root.attributes('-alpha', self.cfg.get('opacity', float))
        self.cols = {'bg': '#1e1e1e', 'panel': '#252526', 'warn': '#fdcb6e', 'dang': '#d63031', 'succ': '#00b894', 'link': '#74b9ff'}
        self.root.configure(bg=self.cols['bg']); self.gamepad = GamepadManager(); self.tts = GoogleTTSManager(self.lang); self.vis = VisualBar(self.root, self.cfg); self.curr_popup = LineReaderPopup(self.root, self.cfg)
        self.scraper = EpicScraper(self.cfg); self.account_id = self.scraper.get_account_id_from_log(LOG_PATH)
        if self.account_id: self.scraper.my_account_id = self.account_id; threading.Thread(target=self.scraper.login, daemon=True).start()
        self.score_popup = LiveScorePopup(self.root, self.cfg, self.L); self.score_query_timer = None
        self.run, self.lock, self.vis_on, self.js, self.map, self.sid, self.inst, self.cache, self.lines, self.lidx = True, False, True, "", {}, None, "Guitar", {}, [], 0
        self.cont = tk.Frame(root, bg=self.cols['panel']); self.cont.pack(fill='both', expand=True, padx=2, pady=2)
        self.bar = tk.Frame(self.cont, bg=self.cols['warn'], width=8); self.bar.pack(side='left', fill='y')
        self.main = tk.Frame(self.cont, bg=self.cols['panel']); self.main.pack(side='left', fill='both', expand=True, padx=8, pady=5)
        self.vis.setup(self.main); self.curr_popup.setup(); self.h_fr = tk.Frame(self.main, bg=self.cols['panel']); self.h_fr.pack(fill='x')
        self.lbl_ti = tk.Label(self.h_fr, text=self.L['waiting'], font=("Segoe UI", 11, "bold"), fg="#dfe6e9", bg=self.cols['panel']); self.lbl_ti.pack(side='left', fill='x', expand=True)
        self.m_fr = tk.Frame(self.main, bg=self.cols['panel']); self.m_fr.pack(fill='x', pady=2)
        self.lbl_ic = tk.Label(self.m_fr, bg=self.cols['panel']); self.lbl_ic.pack(side='left')
        self.lbl_in = tk.Label(self.m_fr, font=("Segoe UI", 16, "bold"), fg="#0984e3", bg=self.cols['panel']); self.lbl_in.pack(side='left', padx=5)
        self.lbl_sc = tk.Label(self.m_fr, font=("Consolas", 12, "bold"), fg="white", bg="#e67e22", padx=5); self.lbl_sc.pack(side='right')
        self.txt = tk.Text(self.main, height=1, font=("Consolas", 16, "bold"), bg=self.cols['panel'], fg="white", bd=0); self.txt.pack(fill="both", expand=True, pady=5)
        self.ft_fr = tk.Frame(self.main, bg=self.cols['panel']); self.ft_fr.pack(side='bottom', fill='x', pady=10)
        self.menu = tk.Menu(self.root, tearoff=0); self.menu.add_command(label=self.L['settings'], command=self.sett); self.menu.add_separator(); self.menu.add_command(label=self.L['close'], command=self.close)
        self.root.bind("<Button-3>", lambda e: self.menu.post(e.x_root, e.y_root)); self.apply(); self.binds(self.root); self.hk()
        for t in [self.fetch, self.log, self.upd_chk]: threading.Thread(target=t, daemon=True).start()
        self.poll_gamepad(); self.resize()

    def binds(self, w): 
        if isinstance(w, tk.Toplevel): return
        if not (isinstance(w, tk.Label) and w.cget("cursor")=="hand2"): w.bind("<ButtonPress-1>", self.ds); w.bind("<ButtonRelease-1>", self.de); w.bind("<B1-Motion>", self.dm)
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
    def reset_pos(self): self.root.geometry(f"+50+50"); self.cfg.set('x', 50); self.cfg.set('y', 50)
    def poll_gamepad(self):
        if self.gamepad.joystick:
            pygame.event.pump(); target = self.cfg.get('gamepad_tts_btn')
            if target != 'NONE' and self.gamepad.check_specific_input(target):
                if time.time() - self.last_trigger_time > 0.3: self.nxt(); self.last_trigger_time = time.time()
        self.root.after(50, self.poll_gamepad)
    def nxt(self):
        if self.vis_on and self.sid and self.lidx < len(self.lines):
            l = self.lines[self.lidx]; self.current_line_text = l
            if self.cfg.get('tts_enabled')=='True': self.tts.play_live(l)
            self.vis.update(l, self.current_colors); self.curr_popup.update_text(l, self.current_colors); self.lidx+=1
    def tog(self): 
        self.vis_on = not self.vis_on
        if self.vis_on: self.root.deiconify(); self.vis.set_visibility(True); self.curr_popup.set_visibility(True)
        else: self.root.withdraw(); self.vis.set_visibility(False); self.curr_popup.set_visibility(False)
    def lck(self): self.lock = not self.lock; self.bar.config(bg=self.cols['dang'] if self.lock else self.cols['warn'])
    def resize(self): self.root.update_idletasks(); self.root.geometry(f"480x300")
    def apply(self):
        l = self.cfg.get('language')
        if l != self.lang: self.lang=l; self.L=LANGUAGES[l]; self.tts=GoogleTTSManager(l)
        self.current_colors = COLOR_PALETTES.get(self.cfg.get('color_blind_mode'), COLOR_PALETTES['Normal'])
        self.txt.config(font=("Consolas", self.cfg.get('font_size', int), "bold")); self.vis.setup(self.main); self.curr_popup.setup()
        self.root.attributes('-alpha', self.cfg.get('opacity', float)); self.hk(); self.resize()
    def sett(self): SettingsWindow(self.root, self.cfg, self.apply, self.L, self.gamepad)
    def fetch(self):
        try: self.map = json.loads(requests.get(MAPPING_URL).text); r = requests.get(DATA_URL); self.js = r.text if r.status_code==200 else ""
        except: pass
    def upd_chk(self):
        try:
            d = requests.get(UPDATE_JSON_URL).json()
            if d.get('version')!=APP_VERSION and d.get('version')!=self.cfg.get('ignored_version'):
                self.root.after(0, lambda: UpdatePopup(self.root, d, self.cfg, self.L))
        except: pass
    def log(self):
        while not os.path.exists(LOG_PATH): time.sleep(1)
        try:
            with open(LOG_PATH, 'r', encoding='utf-8', errors='ignore') as f:
                f.seek(0, 2)
                while self.run:
                    l = f.readline()
                    if not l: time.sleep(0.1); continue
                    self.par(l)
        except: pass
    def par(self, l):
        if 'received song to play:' in l: self.sid = l.split('received song to play: ')[1].split(' - ')[0].strip(); self.trig()
        elif 'TrackType::Track' in l: 
            m = re.search(r"TrackType::Track(\w+)", l)
            if m and m.group(1) not in ["Type", "Events", "Section"]: self.inst = m.group(1); self.trig()
    def trig(self):
        if not self.sid: return
        tid = self.sid.lower().replace("sparks_song_","").replace(" ","").strip(); tid=self.map.get(tid, tid)
        i = self.inst if self.inst else "Guitar"; dn = DISPLAY_NAME_MAP.get(i, i)
        if dn not in self.cache: threading.Thread(target=self.dl_ic, args=(dn,), daemon=True).start()
        else: self.lbl_ic.config(image=self.cache[dn])
        self.lbl_in.config(text=dn); m = re.search(r'shortname\s*:\s*["\']'+re.escape(tid)+r'["\']', self.js, re.I)
        if not m: return
        idx = m.start(); ic = INSTRUMENT_MAP.get(i, 'l'); chk = self.js[idx:idx+3000]
        pth = re.search(rf'{ic}path\s*:\s*["\'](.*?)["\']', chk); scr = re.search(rf'{ic}score\s*:\s*["\'](.*?)["\']', chk)
        self.lbl_sc.config(text=f"{int(scr.group(1)):,}" if scr else "0")
        if self.score_query_timer: self.root.after_cancel(self.score_query_timer)
        self.score_query_timer = self.root.after(25000, lambda: self.query_and_show_score(self.sid, i))
        self.txt.config(state='normal'); self.txt.delete("1.0",'end'); self.lines=[]; self.lidx=0
        if pth:
            for l in pth.group(1).replace(", ", "\n").replace(",", "\n").split('\n'):
                for p in re.split(r'([RGBYO])', l): self.txt.insert('end', p, p if p in "RGBYO" else "W")
                self.txt.insert('end', '\n')
                if re.search(r'[RGBYO]|NN', l): self.lines.append(l.strip())
        self.txt.config(state='disabled'); self.resize()
    def query_and_show_score(self, song_id, instrument):
        def worker():
            evt = self.scraper.get_song_event_id(song_id)
            if evt: self.score_popup.update_data(self.scraper.search_score(self.account_id, evt, instrument, "alltime"), self.scraper.search_score(self.account_id, evt, instrument, self.cfg.get('season')))
        threading.Thread(target=worker, daemon=True).start()
    def dl_ic(self, n):
        f = ICON_FILES.get(n)
        try:
            d = base64.encodebytes(requests.get(IMG_BASE_URL+f).content); i = tk.PhotoImage(data=d)
            self.cache[n]=i; self.root.after(0, lambda: self.lbl_ic.config(image=i))
        except: pass
    def close(self): self.run=False; self.root.destroy(); sys.exit()

if __name__ == "__main__":
    r = tk.Tk(); app = FestivalPathOverlay(r); r.mainloop()


