import pyperclip   # pip install pyperclip
import time
import os
import sys
from pyfiglet import Figlet # pip install pyfiglet
from colorama import init, Fore, Style # pip install colorama

init(autoreset=True)

# ─────────────── Reading arrow keys (cross-platform) ───────────────
if os.name == "nt":                       # Windows
    import msvcrt

    def get_key():
        ch = msvcrt.getwch()
        if ch in ("\x00", "\xe0"):        # special key prefix
            ch2 = msvcrt.getwch()
            return {"H": "up", "P": "down", "K": "left", "M": "right"}.get(ch2, "")
        if ch == "\r":
            return "enter"
        if ch == "\x1b":
            return "esc"
        if ch == "\x03":
            raise KeyboardInterrupt
        if ch == "\x08":
            return "backspace"
        return ch

else:                                     # Linux / macOS
    import termios, tty, select

    def get_key():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                r, _, _ = select.select([sys.stdin], [], [], 0.05)
                if r:
                    ch2 = sys.stdin.read(1)
                    if ch2 == "[":
                        ch3 = sys.stdin.read(1)
                        return {"A": "up", "B": "down", "C": "right", "D": "left"}.get(ch3, "")
                return "esc"
            if ch in ("\r", "\n"):
                return "enter"
            if ch == "\x03":
                raise KeyboardInterrupt
            if ch == "\x7f":
                return "backspace"
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

# ─────────────── Color and font palettes ───────────────
COLORS = [
    ("GREEN",           Fore.GREEN),
    ("CYAN",            Fore.CYAN),
    ("YELLOW",          Fore.YELLOW),
    ("MAGENTA",         Fore.MAGENTA),
    ("BLUE",            Fore.BLUE),
    ("RED",             Fore.RED),
    ("WHITE",           Fore.WHITE),
    ("LIGHTGREEN_EX",   Fore.LIGHTGREEN_EX),
    ("LIGHTCYAN_EX",    Fore.LIGHTCYAN_EX),
    ("LIGHTYELLOW_EX",  Fore.LIGHTYELLOW_EX),
    ("LIGHTMAGENTA_EX", Fore.LIGHTMAGENTA_EX),
    ("LIGHTBLUE_EX",    Fore.LIGHTBLUE_EX),
    ("LIGHTRED_EX",     Fore.LIGHTRED_EX),
]

FONTS = [
    "slant", "big", "small", "standard", "banner", "block",
    "bubble", "digital", "doom", "ghost", "graffiti", "isometric1",
    "ivrit", "lean", "mini", "script", "shadow", "smscript", "starwars",
]

def clear():
    print("\x1b[2J\x1b[H", end="", flush=True)

def copy_to_clipboard(art):
    try:
        pyperclip.copy(art)
        return True
    except Exception:
        import subprocess
        try:
            if os.name == "nt":
                subprocess.run("clip", input=art.encode("utf-16"), check=True, shell=True)
            elif sys.platform == "darwin":
                subprocess.run("pbcopy", input=art.encode("utf-8"), check=True)
            else:
                subprocess.run(["xclip", "-selection", "clipboard"],
                               input=art.encode("utf-8"), check=True)
            return True
        except Exception:
            return False

def main():
    text     = ""
    color_i  = 0
    font_i   = 0
    max_show = 30          # crop very long texts

    while True:
        color_name, color_code = COLORS[color_i]
        font_name = FONTS[font_i]

        clear()

        # ── Header ──
        print(f"{Fore.WHITE}╔══════════════════════════════════════════════════╗")
        print(f"{Fore.WHITE}║  {Fore.LIGHTCYAN_EX}✦  A S C I I   A R T   S T U D I O  ✦{Fore.WHITE}          ║")
        print(f"{Fore.WHITE}╚══════════════════════════════════════════════════╝")

        # ── Active settings ──
        print(f"  {color_code}● Color: {color_name:<16}{Fore.WHITE}"
              f"{Fore.LIGHTYELLOW_EX}✎ Font: {font_name:<12}{Fore.WHITE}")

        # ── Shortcuts ──
        print(f"  {Fore.LIGHTBLACK_EX}← →  color    ↑ ↓  font    "
              f"Backspace  delete    Esc  exit{Fore.WHITE}")
        print(f"  {Fore.WHITE}{'─' * 50}")

        # ── Live preview ──
        if text:
            try:
                art = Figlet(font=font_name).renderText(text).rstrip("\n")
            except Exception as e:
                art = f"{Fore.RED}Font error: {e}"
            print(color_code + art + Style.RESET_ALL)
        else:
            print(f"{Fore.LIGHTBLACK_EX}  (type something...){Fore.WHITE}")

        # ── Input line ──
        print()
        shown = text if len(text) <= max_show else "…" + text[-max_show:]
        print(f"{Fore.WHITE}Text> {Fore.LIGHTWHITE_EX}{shown}{Fore.LIGHTGREEN_EX}█")

        # ── Read key ──
        key = get_key()

        if key == "esc":
            clear()
            print(f"{Fore.WHITE}{'═' * 50}")
            print(f"  {color_code}● {color_name}   {Fore.LIGHTYELLOW_EX}✎ {font_name}{Fore.WHITE}")
            print(f"{Fore.WHITE}{'═' * 50}\n")
            if text:
                try:
                    print(color_code + Figlet(font=font_name).renderText(text) + Style.RESET_ALL)
                except Exception:
                    pass
            print(f"{Fore.LIGHTBLACK_EX}See you! 👋{Fore.WHITE}")
            break

        elif key == "left":
            color_i = (color_i - 1) % len(COLORS)
        elif key == "right":
            color_i = (color_i + 1) % len(COLORS)
        elif key == "up":
            font_i = (font_i - 1) % len(FONTS)
        elif key == "down":
            font_i = (font_i + 1) % len(FONTS)
        elif key == "backspace":
            text = text[:-1]
        elif key == "enter":
            if text:
                try:
                    art_to_copy = Figlet(font=font_name).renderText(text).rstrip("\n")
                    ok = copy_to_clipboard(art_to_copy)
                except Exception:
                    ok = False
                clear()
                if ok:
                    print(f"{Fore.LIGHTGREEN_EX}✓  {len(art_to_copy)} characters copied to clipboard!")
                else:
                    print(f"{Fore.LIGHTRED_EX}✗  Could not copy (is pyperclip / xclip installed?)")
                time.sleep(0.7)
        elif len(key) == 1 and key.isprintable():
            text += key

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print("Exited.")
