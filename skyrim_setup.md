# Skyrim Setup & Troubleshooting

## Status
- **Registry Fix**: Applied (Fixed "Failed to read install path")
- **INI Files**: Created (Fixed "Unable to find INI file")
- **Dependencies**: Installed `vcredist_x86.exe` and `oalinst.exe`.

## How to Launch
1. Open **Whisky**.
2. Select **Skyrim** bottle.
3. Click **Run**.
4. Select **`TESV.exe`** (Recommended) or `SkyrimLauncher.exe`.
   - Path: `/Users/sirajraval/Desktop/gemini_craazy/The.Elder.Scrolls.V-Skyrim-Legendary.Edition-SteamRIP.com/The Elder Scrolls V - Skyrim - Legendary Edition/TESV.exe`

## If it still crashes or doesn't open:
1. **Install DirectX**:
   - In Whisky, run: `/Users/sirajraval/Desktop/gemini_craazy/The.Elder.Scrolls.V-Skyrim-Legendary.Edition-SteamRIP.com/_CommonRedist/dxwebsetup.exe`
   - Follow the prompts.

2. **Verify Registry**:
   - If you still get "Install Path" error, run `regedit` in Whisky and import the `fix_skyrim.reg` file located on your Desktop (`/Users/sirajraval/Desktop/gemini_craazy/fix_skyrim.reg`).

3. **Graphics Settings**:
   - If `SkyrimLauncher.exe` works now, use it to set graphics to "Medium" or "Low" to test.
   - Ensure "Windowed Mode" is unchecked for best performance, or checked if fullscreen crashes.
