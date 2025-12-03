# Phase 2: Skyrim PPO Agent Implementation Plan

## Goal
Create a fully functional Reinforcement Learning environment for Skyrim and train a PPO agent to control the character.

## Components

### 1. `skyrim_env.py` (The Environment)
- **Inherits**: `gymnasium.Env`
- **Observation Space**: Screen capture (resized to 84x84 or similar for speed).
- **Action Space**: Discrete actions (Move Forward, Turn Left, Turn Right, Attack, etc.).
- **Reward Function**: 
    - +1 for every step alive.
    - +0.1 for moving forward (optical flow check?).
    - -100 for dying.
- **Reset Logic**: 
    - Press `F9` (Quickload) to reset state.
    - Wait for loading screen.
- **Death Detection**: 
    - Simple template matching or color check for the "You Died" text/screen.

### 2. `train_ppo.py` (The Trainer)
- **Algorithm**: PPO (Proximal Policy Optimization) from `stable-baselines3`.
- **Policy**: CnnPolicy (Convolutional Neural Network) to process game frames.
- **Training Loop**: Run for N timesteps, save model periodically.

## Steps
1. [x] Install dependencies (`stable-baselines3`, `gymnasium`, `torch`).
2. [ ] Create `skyrim_env.py`.
3. [ ] Create `train_ppo.py`.
4. [ ] Run training and verify.

## Verification
- Agent should be able to launch, control the character, and restart upon death/timeout.
- Tensorboard logs should show reward progression.
