# ⭐ SmartPaste
A tiny workflow booster I built to make copying and pasting text almost effortless. If you work with text all day (coding, writing, researching), this tool quietly saves a ton of clicks.

---

## 🚀 What It Does

### **✔ Auto‑Copy**
Select any text and simply **release** the left mouse button — SmartPaste sends a `Ctrl+C` automatically.
- Clipboard only updates *if* something actually changed (no accidental overwrites!).

### **✔ Auto‑Paste**
Double‑click the left mouse button anywhere and SmartPaste instantly pastes (`Ctrl+V`).

### **✔ Quick Exit**
- Press **Ctrl + Shift + S** from anywhere to stop it.
- Or just press `Ctrl+C` in the terminal.

It’s small, simple, and after using it a while, it feels like a built‑in OS feature.

---

## 📦 Requirements
- Python **3.8+**
- Packages:
  - `pynput`
  - `pyperclip`

Install them:
```bash
pip install pynput pyperclip
```
Linux users may also need:
```bash
sudo apt install xclip   # or xsel
```

---

## 📁 File
- **Smart_Paste.py** — the script

---

## ⚙ Configuration
Tweak these at the top of the script if needed:
```py
DOUBLE_CLICK_MAX_INTERVAL = 0.35   # seconds
DOUBLE_CLICK_MAX_DISTANCE = 6      # pixels
SHORT_SLEEP_AFTER_COPY = 0.06      # seconds
```
If double‑clicks trigger too easily or rarely, adjust those values.

---

## 🧰 How to Use
1. Install requirements.
2. Run:
```bash
python Smart_Paste.py
```
3. Use normally:
   - Select → release → **Auto‑Copy**
   - Double‑click → **Auto‑Paste**
   - Ctrl+Shift+S → **Stop**

That’s literally all you need.

---

## 💡 Tips & Notes
- The auto‑copy runs in the background so clicks never feel delayed.
- Clipboard content is only replaced when a real change happens.
- macOS: may need Accessibility permissions.
- Linux: behavior may vary a bit depending on the desktop environment.

---

## 🛠 Troubleshooting
- **Pasting on accidental double‑clicks?** Lower `DOUBLE_CLICK_MAX_INTERVAL`.
- **Not copying reliably?** Increase `SHORT_SLEEP_AFTER_COPY` slightly.
- **Clipboard errors on Linux?** Install `xclip` or `xsel`.

---

## 🙌 Why I’m Sharing This
I built SmartPaste for myself and ended up relying on it every day. It’s a simple hack, but it removes enough friction that I figured others might appreciate it too.

If you have ideas, improvements, or want new features — PRs and suggestions are welcome.

---

## 📄 License
MIT — use it however you like.

