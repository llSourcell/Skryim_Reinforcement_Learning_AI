from stable_baselines3 import PPO
from skyrim_env import SkyrimEnv
import time

# 🧠 THE AGI SURVIVAL AGENT 🧠
# Goal: Survive as long as possible, explore new areas, and defend itself.
# It uses the updated "Curiosity Reward" in SkyrimEnv.

import os
import glob

env = SkyrimEnv()

# Check for existing checkpoints to resume
# checkpoints = glob.glob("./skyrim_checkpoints/*.zip")
# FORCE FRESH START
checkpoints = [] 

if checkpoints:
    latest_checkpoint = max(checkpoints, key=os.path.getctime)
    print(f"🧠 RESUMING from checkpoint: {latest_checkpoint}")
    model = PPO.load(latest_checkpoint, env=env)
    model.set_env(env)
else:
    print("🧠 Creating NEW brain (Fresh Start requested)")
    # We use a larger learning rate and entropy coefficient to encourage exploration
    # n_steps=512 means it updates/logs every 512 steps (faster feedback than default 2048)
    model = PPO("CnnPolicy", env, 
                verbose=1, 
                tensorboard_log="./skyrim_ppo_tensorboard/AGI_FRESH",
                learning_rate=0.0003,
                ent_coef=0.01,
                n_steps=512) # Update every ~5-10 minutes instead of 30+

print("🤖 STARTING AGI SURVIVAL TRAINING (FRESH) 🤖")
print("This agent is rewarded for:")
print("1. STAYING ALIVE (+0.1/step)")
print("2. SEEING NEW THINGS (Pixel Change Reward)")
print("3. NOT GETTING STUCK (Static Penalty)")

from stable_baselines3.common.callbacks import CheckpointCallback

# Save a checkpoint every 20,000 steps (approx 1 hour)
checkpoint_callback = CheckpointCallback(
    save_freq=20000,
    save_path="./skyrim_checkpoints_fresh/",
    name_prefix="agi_fresh_model"
)

print("Starting in 5 seconds... (Ensure F5 Save is ready)")
time.sleep(5)

try:
    # Train for a long time (100k steps)
    # This allows it to evolve from "random chaos" to "purposeful survival"
    model.learn(total_timesteps=100000, callback=checkpoint_callback)
    model.save("skyrim_agi_model")
    print("AGI Model Saved.")
except KeyboardInterrupt:
    model.save("skyrim_agi_model_interrupted")
    print("Training paused. Model saved.")
