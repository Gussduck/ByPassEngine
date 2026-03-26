import sys
import os
import traceback

# ==========================================
# BULLETPROOF IMPORT CATCHER
# ==========================================
# If any module is missing, it will pop up an error box instead of silently crashing.
try:
    import tkinter as tk
    from tkinter import messagebox
    import customtkinter as ctk
    from PIL import Image  # ADDED: Pillow for image processing
    import threading
    import uuid
    import requests
    from bs4 import BeautifulSoup
    import json
    import pyautogui
    import keyboard
    import time
    import random
    import string
    import webbrowser
except ImportError as e:
    import tkinter as tk
    from tkinter import messagebox
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Missing Dependency", f"A required library is missing:\n\n{str(e)}\n\nPlease run:\npip install customtkinter requests beautifulsoup4 pyautogui keyboard Pillow")
    sys.exit(1)

# ==========================================
# PYINSTALLER RESOURCE PATH HELPER
# ==========================================
def resource_path(relative_path):
    """Get absolute path to resource — works for dev and PyInstaller .exe"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# ==========================================
# CUSTOMTKINTER INITIALIZATION
# ==========================================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ==========================================
# GLOBAL CONFIGURATION & PREMIUM THEME
# ==========================================
APP_NAME = "ByPassEngine"
# Upgraded Deep Navy / Dark Blue Palette
BG_COLOR = "#0B101E"          
SIDEBAR_COLOR = "#151C2C"     
PANEL_COLOR = "#1A233A"       
TEXT_BG = "#111827"           
TEXT_FG = "#F3F4F6"           
ACCENT = "#3B82F6"            
ACCENT_HOVER = "#60A5FA"      
DANGER = "#EF4444"            
SUCCESS = "#10B981"           

# Fonts
FONT_MAIN = ("Segoe UI", 12)
FONT_BOLD = ("Segoe UI", 12, "bold")
FONT_TITLE = ("Segoe UI", 20, "bold")

# ==========================================
# TOOL 1: AI HUMANIZER LOGIC (API)
# ==========================================
class CleverHumanizerAPI:
    def __init__(self):
        self.base_url = "https://cleverhumanizer.ai"
        self.visitor_id = uuid.uuid4().hex 
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
            "X-Visitor-ID": self.visitor_id,
            "Accept": "application/json, text/plain, */*"
        })

    def process_chunk(self, text: str, style: str = "casual"):
        try:
            response = self.session.get(self.base_url, timeout=15)
            soup = BeautifulSoup(response.text, "html.parser")
            csrf_tag = soup.select_one('meta[name="csrf-token"]')
            if csrf_tag:
                self.session.headers.update({"X-CSRF-TOKEN": csrf_tag.get("content")})

            self.session.post(f"{self.base_url}/fingerprint-init", json={"visitorId": self.visitor_id}, timeout=15)
            payload = {"html": text, "text": text, "style": style, "type_generation": "humanize"}
            rewrite_resp = self.session.post(f"{self.base_url}/rewrite", json=payload, timeout=30)
            data = rewrite_resp.json()
            return data["data"]["text"] if "data" in data and "text" in data["data"] else "Error: Unexpected response format."
        except Exception as e:
            return f"Error: {str(e)}"

# ==========================================
# MODULE: AI HUMANIZER FRAME
# ==========================================
class HumanizerFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=BG_COLOR, corner_radius=0)
        self.setup_ui()

    def setup_ui(self):
        lbl_input = ctk.CTkLabel(self, text="Input Text (AI Content):", font=FONT_BOLD, text_color=ACCENT)
        lbl_input.pack(anchor="w", padx=25, pady=(20, 5))
        
        self.input_text = ctk.CTkTextbox(self, height=150, font=("Consolas", 13), 
                                         fg_color=TEXT_BG, text_color=TEXT_FG, 
                                         corner_radius=10, border_width=1, border_color=PANEL_COLOR)
        self.input_text.pack(fill="both", expand=True, padx=25, pady=5)

        ctrl_frame = ctk.CTkFrame(self, fg_color="transparent")
        ctrl_frame.pack(fill="x", padx=25, pady=15)
        
        ctk.CTkLabel(ctrl_frame, text="Writing Style:", text_color=TEXT_FG, font=FONT_MAIN).pack(side="left")
        self.style_var = tk.StringVar(value="casual")
        style_combo = ctk.CTkComboBox(ctrl_frame, variable=self.style_var, 
                                      values=["casual", "academic", "formal"], width=150, 
                                      state="readonly", fg_color=TEXT_BG, border_color=PANEL_COLOR, 
                                      button_color=PANEL_COLOR, button_hover_color=ACCENT)
        style_combo.pack(side="left", padx=15)

        self.btn_run = ctk.CTkButton(ctrl_frame, text="🚀 Start Humanizing", fg_color=ACCENT, hover_color=ACCENT_HOVER, 
                                     text_color="white", font=FONT_BOLD, corner_radius=8, 
                                     command=self.start_batch, cursor="hand2")
        self.btn_run.pack(side="right", ipady=3, ipadx=10)

        self.progress = ctk.CTkProgressBar(self, orientation="horizontal", progress_color=ACCENT, fg_color=TEXT_BG, height=8)
        self.progress.pack(fill="x", padx=25, pady=5)
        self.progress.set(0) 

        out_header = ctk.CTkFrame(self, fg_color="transparent")
        out_header.pack(fill="x", padx=25, pady=(15, 5))
        
        lbl_output = ctk.CTkLabel(out_header, text="Humanized Result:", font=FONT_BOLD, text_color=SUCCESS)
        lbl_output.pack(side="left")
        
        btn_copy = ctk.CTkButton(out_header, text="📋 Copy Result", fg_color=PANEL_COLOR, hover_color=SIDEBAR_COLOR, 
                                 text_color=TEXT_FG, font=FONT_MAIN, corner_radius=8, 
                                 command=self.copy_result, cursor="hand2")
        btn_copy.pack(side="right")
        
        self.output_text = ctk.CTkTextbox(self, height=150, font=("Consolas", 13), 
                                          fg_color=TEXT_BG, text_color=TEXT_FG, 
                                          corner_radius=10, border_width=1, border_color=PANEL_COLOR)
        self.output_text.pack(fill="both", expand=True, padx=25, pady=(5, 25))

    def copy_result(self):
        text_to_copy = self.output_text.get("1.0", "end-1c").strip()
        if text_to_copy:
            self.clipboard_clear()
            self.clipboard_append(text_to_copy)
            messagebox.showinfo(APP_NAME, "Text successfully copied to clipboard!")
        else:
            messagebox.showwarning(APP_NAME, "There is no text to copy yet.")

    def split_into_chunks(self, text, max_words=1200):
        paragraphs = text.split('\n')
        chunks, current_chunk, current_word_count = [], [], 0
        for p in paragraphs:
            word_count = len(p.split())
            if current_word_count + word_count > max_words:
                chunks.append("\n".join(current_chunk))
                current_chunk, current_word_count = [p], word_count
            else:
                current_chunk.append(p); current_word_count += word_count
        if current_chunk: chunks.append("\n".join(current_chunk))
        return chunks

    def start_batch(self):
        raw_text = self.input_text.get("1.0", "end-1c").strip()
        if not raw_text: return
        self.output_text.delete("1.0", "end")
        self.btn_run.configure(state="disabled", text="Processing...")
        threading.Thread(target=self.process_thread, args=(raw_text,), daemon=True).start()

    def process_thread(self, text):
        chunks = self.split_into_chunks(text)
        total = len(chunks)
        api = CleverHumanizerAPI()
        for i, chunk in enumerate(chunks):
            res = api.process_chunk(chunk, self.style_var.get())
            self.after(0, lambda r=res: self.output_text.insert("end", r + "\n\n"))
            self.after(0, lambda v=i: self.progress.set((v+1)/total)) 
        
        self.after(0, lambda: self.btn_run.configure(state="normal", text="🚀 Start Humanizing"))
        self.after(0, lambda: messagebox.showinfo(APP_NAME, "All chunks processed successfully!"))

# ==========================================
# MODULE: GHOSTWRITER FRAME
# ==========================================
class GhostWriterFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=BG_COLOR, corner_radius=0)
        self.is_running = False
        self.setup_ui()
        self.setup_hotkeys()

    def setup_ui(self):
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        left_p = ctk.CTkFrame(main_container, fg_color="transparent")
        left_p.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        ctk.CTkLabel(left_p, text="Source Text for Emulation:", font=FONT_BOLD, text_color=ACCENT).pack(anchor="w", pady=(0, 10))
        self.text_area = ctk.CTkTextbox(left_p, font=("Consolas", 14), fg_color=TEXT_BG, text_color=TEXT_FG, 
                                        corner_radius=10, border_width=1, border_color=PANEL_COLOR)
        self.text_area.pack(fill="both", expand=True)

        right_p = ctk.CTkFrame(main_container, fg_color=PANEL_COLOR, width=320, corner_radius=15)
        right_p.pack(side="right", fill="y")
        right_p.pack_propagate(False)

        inner_right = ctk.CTkFrame(right_p, fg_color="transparent")
        inner_right.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(inner_right, text="EMULATION CONFIG", font=FONT_BOLD, text_color=TEXT_FG).pack(pady=(0, 20))

        ctk.CTkLabel(inner_right, text="Typing Speed (Delay):", text_color=TEXT_FG, font=FONT_MAIN).pack(anchor="w")
        self.speed_var = tk.DoubleVar(value=75)
        ctk.CTkSlider(inner_right, from_=20, to=250, variable=self.speed_var, 
                      progress_color=ACCENT, button_color=ACCENT, button_hover_color=ACCENT_HOVER).pack(fill="x", pady=(5, 15))

        self.enable_mistakes = tk.BooleanVar(value=True)
        ctk.CTkCheckBox(inner_right, text="Simulate Random Mistakes", variable=self.enable_mistakes, 
                        fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color=TEXT_FG, font=FONT_MAIN).pack(anchor="w", pady=5)
        
        self.enable_pause = tk.BooleanVar(value=True)
        ctk.CTkCheckBox(inner_right, text="Natural Thought Pauses", variable=self.enable_pause, 
                        fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color=TEXT_FG, font=FONT_MAIN).pack(anchor="w", pady=5)

        ctk.CTkFrame(inner_right, height=1, fg_color="#444").pack(fill="x", pady=20)
        hk_frame = ctk.CTkFrame(inner_right, fg_color="transparent")
        hk_frame.pack(fill="x")
        
        self.start_hk = tk.StringVar(value="f9")
        ctk.CTkLabel(hk_frame, text="Start HK:", text_color=TEXT_FG).grid(row=0, column=0, sticky="w", pady=5)
        ctk.CTkEntry(hk_frame, textvariable=self.start_hk, width=100, fg_color=TEXT_BG, 
                     text_color=TEXT_FG, border_width=1, border_color=PANEL_COLOR).grid(row=0, column=1, padx=10)

        self.stop_hk = tk.StringVar(value="f10")
        ctk.CTkLabel(hk_frame, text="Stop HK:", text_color=TEXT_FG).grid(row=1, column=0, sticky="w", pady=5)
        ctk.CTkEntry(hk_frame, textvariable=self.stop_hk, width=100, fg_color=TEXT_BG, 
                     text_color=TEXT_FG, border_width=1, border_color=PANEL_COLOR).grid(row=1, column=1, padx=10)

        self.btn_start = ctk.CTkButton(inner_right, text="EXECUTE TYPING", fg_color=ACCENT, hover_color=ACCENT_HOVER, 
                                       text_color="white", font=FONT_BOLD, corner_radius=8, 
                                       command=lambda: self.start_sim(5))
        self.btn_start.pack(fill="x", pady=(25, 10), ipady=5)
        
        self.btn_stop = ctk.CTkButton(inner_right, text="ABORT", fg_color=DANGER, hover_color="#B91C1C", 
                                      text_color="white", font=FONT_BOLD, corner_radius=8, 
                                      command=self.stop_sim)
        self.btn_stop.pack(fill="x", ipady=2)

        self.status_lbl = ctk.CTkLabel(inner_right, text="STATUS: READY", text_color=SUCCESS, font=FONT_BOLD)
        self.status_lbl.pack(side="bottom", pady=10)

    def setup_hotkeys(self):
        try:
            keyboard.unhook_all()
            keyboard.add_hotkey(self.start_hk.get(), lambda: self.after(0, lambda: self.start_sim(0.5)))
            keyboard.add_hotkey(self.stop_hk.get(), lambda: self.after(0, self.stop_sim))
        except: pass

    def start_sim(self, delay):
        if self.is_running: return
        txt = self.text_area.get("1.0", "end").strip()
        if not txt: return
        self.is_running = True
        self.status_lbl.configure(text=f"INITIATING ({delay}s)", text_color="#FBBF24")
        threading.Thread(target=self.typing_loop, args=(txt, delay), daemon=True).start()

    def stop_sim(self):
        self.is_running = False
        self.status_lbl.configure(text="STATUS: STOPPED", text_color=DANGER)

    def typing_loop(self, text, delay):
        time.sleep(delay)
        self.after(0, lambda: self.status_lbl.configure(text="STATUS: TYPING", text_color=SUCCESS))
        base = self.speed_var.get() / 1000.0
        for char in text:
            if not self.is_running: break
            if self.enable_mistakes.get() and char.isalpha() and random.random() < 0.015:
                pyautogui.write(random.choice(string.ascii_lowercase))
                time.sleep(0.1); pyautogui.press('backspace')
            pyautogui.write(char)
            time.sleep(random.uniform(base*0.6, base*1.4))
        self.after(0, self.stop_sim)

# ==========================================
# MODULE: DETECTOR LIST FRAME
# ==========================================
class DetectorFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=BG_COLOR, corner_radius=0)
        self.setup_ui()

    def setup_ui(self):
        container = ctk.CTkFrame(self, width=550, fg_color=PANEL_COLOR, corner_radius=15)
        container.place(relx=0.5, rely=0.5, anchor="center")

        inner = ctk.CTkFrame(container, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=40, pady=40)

        ctk.CTkLabel(inner, text="Verified Detection Portals", font=FONT_TITLE, text_color=ACCENT).pack(pady=(0, 30))

        sites = [
            ("ZeroGPT", "https://www.zerogpt.com/"),
            ("Turnitin", "https://turnitin.app/"),
            ("Quillbot", "https://quillbot.com/ai-content-detector"),
            ("DeCopy AI", "https://decopy.ai/ai-detector/")
        ]

        for name, url in sites:
            row = ctk.CTkFrame(inner, fg_color="transparent")
            row.pack(fill="x", pady=8)
            
            ctk.CTkLabel(row, text=f"• {name}", font=FONT_BOLD, text_color=TEXT_FG).pack(side="left")
            
            btn = ctk.CTkButton(row, text="Launch Portal", fg_color=SUCCESS, hover_color="#059669", 
                                text_color="white", corner_radius=8, font=("Segoe UI", 12, "bold"),
                                command=lambda u=url: webbrowser.open(u), cursor="hand2")
            btn.pack(side="right")
            
            ctk.CTkFrame(inner, height=1, fg_color="#444").pack(fill="x", pady=5)

# ==========================================
# MODULE: CUSTOM UI CARD WIDGET
# ==========================================
class MenuCard(ctk.CTkFrame):
    def __init__(self, parent, title, subtitle, icon_text, command, **kwargs):
        super().__init__(parent, width=280, height=360, fg_color=PANEL_COLOR, corner_radius=15, **kwargs)
        self.pack_propagate(False) 
        self.command = command
        
        self.configure(cursor="hand2")
        
        self.card_color = PANEL_COLOR
        self.card_hover_color = "#1D273D" 
        
        self.icon_lbl = ctk.CTkLabel(self, text=icon_text, font=("Segoe UI", 56), text_color=ACCENT)
        self.icon_lbl.pack(pady=(60, 20))
        
        self.title_lbl = ctk.CTkLabel(self, text=title, font=("Segoe UI", 18, "bold"), text_color=TEXT_FG)
        self.title_lbl.pack(pady=(10, 5))
        
        self.sub_lbl = ctk.CTkLabel(self, text=subtitle, font=("Segoe UI", 12), text_color="#8B949E", justify="center")
        self.sub_lbl.pack(pady=(5, 20))
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", lambda e: self.command())
        
        for child in self.winfo_children():
            child.bind("<Enter>", self.on_enter)
            child.bind("<Leave>", self.on_leave)
            child.bind("<Button-1>", lambda e: self.command())
            
    def on_enter(self, event):
        self.configure(fg_color=self.card_hover_color)
            
    def on_leave(self, event):
        self.configure(fg_color=self.card_color)

# ==========================================
# MODULE: MAIN HOME MENU FRAME
# ==========================================
class HomeFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG_COLOR, corner_radius=0)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        # --- LOAD LOGO ---
        home_logo = self.controller.load_logo_image((100, 100))
        
        if home_logo:
            # Display real image
            logo_lbl = ctk.CTkLabel(self, text="", image=home_logo)
            logo_lbl.place(x=40, y=40)
        else:
            # Fallback text circle if image is missing
            logo_frame = ctk.CTkFrame(self, width=80, height=80, corner_radius=40, fg_color=ACCENT)
            logo_frame.place(x=40, y=40)
            logo_frame.pack_propagate(False)
            ctk.CTkLabel(logo_frame, text="BE", font=("Segoe UI", 26, "bold"), text_color="#FFFFFF").place(relx=0.5, rely=0.5, anchor="center")

        center_container = ctk.CTkFrame(self, fg_color="transparent")
        center_container.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(center_container, text="WELCOME to ByPassEngine", font=("Segoe UI", 42, "bold"), text_color=TEXT_FG).pack(pady=(0, 10))
        ctk.CTkLabel(center_container, text="Select a module to continue optimizing your workflow.", font=("Segoe UI", 14), text_color="#8B949E").pack(pady=(0, 50))

        cards_frame = ctk.CTkFrame(center_container, fg_color="transparent")
        cards_frame.pack()

        MenuCard(cards_frame, "Ai Humanizer", "Transform AI generated text\ninto natural human writing.", "🤖", 
                 self.controller.show_humanizer).pack(side="left", padx=25)
                 
        MenuCard(cards_frame, "Ai Detector", "Verify your written text\nagainst detection portals.", "🔍", 
                 self.controller.show_detectors).pack(side="left", padx=25)
                 
        MenuCard(cards_frame, "GhostWriter", "Emulate real human typing\nbehavior in real-time.", "💻", 
                 self.controller.show_ghostwriter).pack(side="left", padx=25)

# ==========================================
# MAIN APPLICATION (BYPASSENGINE)
# ==========================================
class ByPassEngine:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("1150x780")
        self.root.configure(fg_color=BG_COLOR)
        
        # --- SET WINDOW ICON ---
        try:
            icon_img = tk.PhotoImage(file=resource_path("logo.png"))
            self.root.iconphoto(False, icon_img)
        except Exception:
            pass # Fails gracefully if file is missing

        self.top_nav = ctk.CTkFrame(self.root, fg_color=SIDEBAR_COLOR, height=60, corner_radius=0)
        self.top_nav.pack_propagate(False)
        
        btn_back = ctk.CTkButton(self.top_nav, text="⬅ Back to Home", font=FONT_BOLD, fg_color="transparent", 
                                 text_color=ACCENT, hover_color=PANEL_COLOR, cursor="hand2", 
                                 command=self.show_home, width=120)
        btn_back.pack(side="left", padx=20)
        
        nav_menu = ctk.CTkFrame(self.top_nav, fg_color="transparent")
        nav_menu.pack(side="left", padx=30)
        
        ctk.CTkButton(nav_menu, text="Ai Humanizer", font=FONT_BOLD, fg_color="transparent", text_color=TEXT_FG, 
                      hover_color=PANEL_COLOR, cursor="hand2", command=self.show_humanizer, width=100).pack(side="left", padx=10)
        
        ctk.CTkButton(nav_menu, text="Ai Detector", font=FONT_BOLD, fg_color="transparent", text_color=TEXT_FG, 
                      hover_color=PANEL_COLOR, cursor="hand2", command=self.show_detectors, width=100).pack(side="left", padx=10)
        
        ctk.CTkButton(nav_menu, text="GhostWriter", font=FONT_BOLD, fg_color="transparent", text_color=TEXT_FG, 
                      hover_color=PANEL_COLOR, cursor="hand2", command=self.show_ghostwriter, width=100).pack(side="left", padx=10)

        # --- SET TOP NAV LOGO ---
        nav_logo = self.load_logo_image((30, 30))
        if nav_logo:
            ctk.CTkLabel(self.top_nav, text=f" {APP_NAME}", image=nav_logo, compound="left", font=("Segoe UI", 16, "bold"), text_color=TEXT_FG).pack(side="right", padx=20)
        else:
            ctk.CTkLabel(self.top_nav, text=APP_NAME, font=("Segoe UI", 16, "bold"), text_color=TEXT_FG).pack(side="right", padx=20)

        self.viewport = ctk.CTkFrame(self.root, fg_color=BG_COLOR, corner_radius=0)
        self.viewport.pack(side="bottom", fill="both", expand=True)

        self.frames = {
            "home": HomeFrame(self.viewport, self),
            "humanizer": HumanizerFrame(self.viewport),
            "ghostwriter": GhostWriterFrame(self.viewport),
            "detectors": DetectorFrame(self.viewport)
        }

        self.show_home()
        self.root.after(2500, self.donation_popup)

    # --- IMAGE LOADER HELPER ---
    def load_logo_image(self, size):
        try:
            logo_file = resource_path("logo.png")
            if os.path.exists(logo_file):
                img = Image.open(logo_file)
                return ctk.CTkImage(light_image=img, dark_image=img, size=size)
        except Exception:
            pass
        return None

    def show_frame(self, name):
        if name == "home":
            self.top_nav.pack_forget()
        else:
            self.top_nav.pack(side="top", fill="x", before=self.viewport)
            
        for f in self.frames.values(): 
            f.pack_forget()
        self.frames[name].pack(fill="both", expand=True)

    def show_home(self): self.show_frame("home")
    def show_humanizer(self): self.show_frame("humanizer")
    def show_ghostwriter(self): self.show_frame("ghostwriter")
    def show_detectors(self): self.show_frame("detectors")

    def donation_popup(self):
        win = ctk.CTkToplevel(self.root)
        win.title("Support ByPassEngine")
        win.geometry("420x220")
        win.configure(fg_color=PANEL_COLOR)
        win.attributes('-topmost', True)
        win.resizable(False, False)

        ctk.CTkLabel(win, text=f"Support {APP_NAME} Development", font=FONT_TITLE, text_color=ACCENT).pack(pady=(20, 10))
        ctk.CTkLabel(win, text="If this tool saved you time, consider buying us a coffee!", 
                     text_color=TEXT_FG, wraplength=350).pack()
        
        btn = ctk.CTkButton(win, text="☕ Buy me a coffee", fg_color=ACCENT, hover_color=ACCENT_HOVER, 
                            text_color="white", font=FONT_BOLD, corner_radius=8,
                            command=lambda: webbrowser.open("https://www.buymeacoffee.com/melstemirlan"), cursor="hand2")
        btn.pack(pady=20, ipadx=15, ipady=5)


if __name__ == "__main__":
    try:
        pyautogui.FAILSAFE = True
        root = ctk.CTk()
        app = ByPassEngine(root)
        root.mainloop()
    except Exception as e:
        import tkinter as tk
        from tkinter import messagebox
        import traceback
        
        err_root = tk.Tk()
        err_root.withdraw()
        
        error_info = traceback.format_exc()
        with open("error_log.txt", "w") as f:
            f.write(error_info)
            
        messagebox.showerror(
            "Fatal Application Error", 
            f"The application failed to start because of an error.\n\n"
            f"Error details have been saved to 'error_log.txt'.\n\n"
            f"Message: {str(e)}"
        )