from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from skyrim_env import SkyrimEnv
import time

# 🔥 AI BUILD 2: THE MAGE 🔥
# Goal: Glass Cannon / Pure Magic.
# Reward Function:
# - Positive: Magic Kills, Magicka Efficiency.
# - Negative: Using Physical Weapons, Taking Damage.
# Result after 200 hours: Became a Stealth Archer.

# Initialize Environment (Standard Mode with Curiosity for finding targets)
env = SkyrimEnv(combat_mode=False) 

model = PPO("CnnPolicy", env, 
            verbose=1, 
            tensorboard_log="./skyrim_ppo_tensorboard/MAGE_BUILD",
            learning_rate=0.0003,
            ent_coef=0.03, # Medium entropy for kiting/spacing
            n_steps=512)

print("🔥 STARTING MAGE TRAINING 🔥")
print("Constraint: NO ARMOR + DESTRUCTION MAGIC ONLY.")
print("Penalty for Weapons: -50 pts.")

checkpoint_callback = CheckpointCallback(
    save_freq=20000,
    save_path="./skyrim_checkpoints_mage/",
    name_prefix="mage_model"
)

print("Starting in 5 seconds...")
time.sleep(5)

try:
    model.learn(total_timesteps=1000000, callback=checkpoint_callback)
    model.save("skyrim_mage_final")
except KeyboardInterrupt:
    model.save("skyrim_mage_interrupted")
    print("Training paused.")
