from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from skyrim_env import SkyrimEnv
import time

# 🗡️ AI BUILD 3: THE THIEF 🗡️
# Goal: Assassin / Stealth.
# Reward Function:
# - Positive: Stealth Kills, Gold Stolen, Undetected Time.
# - Negative: Being Detected, Direct Combat.
# Result after 200 hours: Became a Stealth Archer.

# Initialize Environment (Standard Mode)
# We rely on high entropy to discover the "Crouch" mechanic and stealth paths
env = SkyrimEnv(combat_mode=False)

model = PPO("CnnPolicy", env, 
            verbose=1, 
            tensorboard_log="./skyrim_ppo_tensorboard/THIEF_BUILD",
            learning_rate=0.0003,
            ent_coef=0.05, # High entropy to discover complex stealth mechanics
            n_steps=512)

print("🗡️ STARTING THIEF TRAINING 🗡️")
print("Constraint: LIGHT ARMOR + DAGGERS ONLY.")
print("Penalty for Detection: -30 pts.")

checkpoint_callback = CheckpointCallback(
    save_freq=20000,
    save_path="./skyrim_checkpoints_thief/",
    name_prefix="thief_model"
)

print("Starting in 5 seconds...")
time.sleep(5)

try:
    model.learn(total_timesteps=1000000, callback=checkpoint_callback)
    model.save("skyrim_thief_final")
except KeyboardInterrupt:
    model.save("skyrim_thief_interrupted")
    print("Training paused.")
