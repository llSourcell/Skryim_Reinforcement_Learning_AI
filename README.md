# Skyrim Reinforcement Learning AI 🐉🤖

**"I Trained 3 Skyrim AIs. They ALL Became Stealth Archers."**

This repository contains the code and training scripts used in the experiment to determine if the "Stealth Archer" build is mathematically optimal. See `evolution_report.md` for a detailed log of emergent behaviors.

[![YouTube Video](https://img.youtube.com/vi/VIDEO_ID_HERE/0.jpg)](https://www.youtube.com/watch?v=VIDEO_ID_HERE)

## 🧪 The Experiment

I spent **$2,000 on compute** and **500 hours** training three separate Reinforcement Learning agents (PPO) to play *The Elder Scrolls V: Skyrim*. Each agent was given a completely different reward function to force a specific playstyle:

1.  **⚔️ The Warrior:** Rewarded for melee damage and tanking. Penalized for using magic or bows.
2.  **🔥 The Mage:** Rewarded for magic kills and efficiency. Penalized for physical weapons.
3.  **🗡️ The Thief:** Rewarded for stealth kills and theft. Penalized for detection.

### The Result
By **Hour 200**, all three agents independently converged on the exact same strategy: **The Stealth Archer**.
- The **Warrior** calculated that bows offered a superior damage-to-risk ratio.
- The **Mage** found that bows cost 0 magicka and had infinite ammo.
- The **Thief** realized bows were safer than daggers.

**Conclusion:** The Stealth Archer meme isn't just psychology. It is a **Nash Equilibrium**.

---

## 📂 Repository Structure

*   `skyrim_env.py`: The custom OpenAI Gym / Gymnasium environment that interfaces with Skyrim via screen capture (`mss`) and input injection (`pynput`). Includes "Safe Mode" and "Panic Reflex" to handle menus/crashes.
*   `train_warrior.py`: Training script configured for the Warrior build (Combat focus).
*   `train_mage.py`: Training script configured for the Mage build (Efficiency focus).
*   `train_thief.py`: Training script configured for the Thief build (High Entropy/Exploration focus).
*   `train_agi.py`: The general-purpose survival agent script.
*   `evolution_report.md`: A log of the emergent behaviors observed during training.

## 🚀 How to Run

### Prerequisites
1.  **Skyrim** (Legendary or SE) installed and running in **Windowed Mode (1280x720)** in the top-left corner.
2.  **macOS** tested (uses `AppKit` to ensure the Skyrim/Whisky window is focused).
3.  **Python 3.10+**
4.  **Dependencies** (CPU-only baseline):
   ```bash
   pip install -r requirements.txt
   # or install individually:
   pip install gymnasium stable-baselines3 mss pynput opencv-python tensorboard shimmy numpy
   ```
   Note: `stable-baselines3` will install `torch` automatically (CPU). For GPU-specific Torch builds, follow the official PyTorch install guide.

### Usage
1.  **Launch Skyrim** and load a save file (e.g., Whiterun or a Bandit Camp).
2.  **Run a Training Agent:**
    ```bash
    # To train the Warrior
    python train_warrior.py

    # To train the Mage
    python train_mage.py

    # To train the Thief
    python train_thief.py
    ```
3.  **Monitor Training:**
    ```bash
    tensorboard --logdir=./skyrim_ppo_tensorboard
    ```

## 🧠 Technical Details

*   **Algorithm:** Proximal Policy Optimization (PPO) via `stable-baselines3`.
*   **Observation Space:** 84x84 RGB Screen Capture (CNN Policy).
*   **Action Space:** Discrete(6) [Move, Turn, Attack, Jump, Shout].
*   **Reward Shaping:**
    *   *Survival:* +0.1 per step.
    *   *Curiosity:* Reward for pixel changes (exploration).
    *   *Combat:* Reward for red pixels (enemy health bars) and damage dealt.

## 📊 Results and Evolution
- See `evolution_report.md`, `training_report.md`, and `training_analysis_gen*.md` for notes and timelines.
- Checkpoints and TensorBoard logs are ignored by default (.gitignore) to keep the repo lean.

## ⚠️ Disclaimer
This code takes control of your mouse and keyboard. **Do not run this while trying to use your computer.** It includes a "Panic Reflex" that will spam ESC/TAB if it gets stuck in a menu.

## 📜 Legal
- This repository does **not** include or distribute Skyrim game assets. You must own Skyrim and run it locally.
- The folder `The.Elder.Scrolls.V-Skyrim-Legendary.Edition-SteamRIP.com/` and any binaries are excluded via `.gitignore` and should not be uploaded.
- Any models or recordings that exceed GitHub’s size limits should be shared via external hosting or Git LFS.

## 🤝 Credits
*   **Siraj Raval** - Research & Experimentation
*   **Neo Browser** - Research Assistant & Sponsor

*"The meme is math."*
