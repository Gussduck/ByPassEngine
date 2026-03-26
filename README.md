# ByPassEngine

<p align="center">
  <img src="logo.png" alt="ByPassEngine Logo" width="100"/>
</p>

<p align="center">
  <b>Transform AI-generated text into undetectable human writing.</b><br/>
  A desktop toolkit for humanizing content, detecting AI, and emulating real typing behavior.
</p>

---

## What is ByPassEngine?

ByPassEngine is a Windows desktop application that gives you three powerful tools in one clean interface:

- **AI Humanizer** — Rewrites AI-generated text to sound natural and human, bypassing detection tools
- **AI Detector** — Quickly launches the best AI detection portals so you can verify your content
- **GhostWriter** — Types your text automatically while simulating real human typing patterns, mistakes, and pauses

---

## Download & Install

1. Go to the [Releases](../../releases) page
2. Download the latest `ByPassEngine_Setup.exe`
3. Run the installer and follow the steps
4. Launch **ByPassEngine** from your Desktop or Start Menu

> ⚠️ **Windows SmartScreen Warning** — You may see a popup saying *"Windows protected your PC."*
> This is normal for independent apps. Click **"More info"** → **"Run anyway"** to proceed.
> The app contains no malware or tracking of any kind.

---

## System Requirements

| | |
|---|---|
| **OS** | Windows 10 or Windows 11 (64-bit) |
| **RAM** | 200 MB minimum |
| **Storage** | ~50 MB |
| **Internet** | Required for AI Humanizer and AI Detector modules |

---

## How to Use

### 🤖 AI Humanizer
1. Paste your AI-generated text into the **Input Text** box
2. Select a **Writing Style** — `Casual`, `Academic`, or `Formal`
3. Click **🚀 Start Humanizing**
4. Wait for the result, then click **📋 Copy Result**

> Long texts are automatically split into chunks and processed one by one. The progress bar shows you how far along it is.

---

### 🔍 AI Detector
1. Click **AI Detector** from the home screen or top navigation
2. Choose a detection portal from the list:
   - [ZeroGPT](https://www.zerogpt.com/)
   - [Turnitin](https://turnitin.app/)
   - [Quillbot AI Detector](https://quillbot.com/ai-content-detector)
   - [DeCopy AI](https://decopy.ai/ai-detector/)
3. The portal opens in your browser — paste your text and check the result

---

### 💻 GhostWriter
1. Paste the text you want to type automatically into the text area
2. Configure your settings:
   - **Typing Speed** — adjust the delay between keystrokes (lower = faster)
   - **Simulate Random Mistakes** — adds realistic typos and backspaces
   - **Natural Thought Pauses** — adds occasional pauses to mimic a real person
3. Click **EXECUTE TYPING** (or press your Start hotkey, default: `F9`)
4. Quickly switch focus to the target window — typing begins after a 5-second countdown
5. Press **ABORT** (or `F10`) to stop at any time

> 💡 **Tip:** You can customize the Start/Stop hotkeys directly in the GhostWriter panel.

---

## Troubleshooting

**The app won't open / crashes immediately**
- An `error_log.txt` file will be created in the same folder as the `.exe`. Open it to see the exact error.

**AI Humanizer returns an error**
- Check your internet connection. The humanizer requires access to `cleverhumanizer.ai`.

**GhostWriter isn't typing in my target window**
- Make sure you click into the target text field before the countdown finishes.
- Run ByPassEngine as **Administrator** if the target app is elevated (e.g., a browser with admin rights).

**Antivirus is blocking the app**
- This is a false positive common with PyInstaller apps. Add the `.exe` to your antivirus exclusion list.

---

## Privacy

ByPassEngine does **not** collect, store, or transmit any personal data. The AI Humanizer sends your text to the `cleverhumanizer.ai` API to process — no data is stored on our end. All other features work entirely offline.

---

## Support the Project

If ByPassEngine saved you time, consider buying a coffee ☕

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-support-yellow?style=for-the-badge&logo=buy-me-a-coffee)](https://www.buymeacoffee.com/melstemirlan)

---

## License

This project is for personal use only. Redistribution or resale is not permitted without explicit permission from the author.
