from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from skyrim_env import SkyrimEnv
import time

# ⚔️ AI BUILD 1: THE WARRIOR ⚔️
# Goal: Tank / Brute Force.
# Reward Function:
# - Positive: Melee Damage Dealt, Health Remaining.
# - Negative: Using Magic, Using Bows.
# Result after 200 hours: Became a Stealth Archer.

# Initialize Environment in Combat Mode (Aggressive)
env = SkyrimEnv(combat_mode=True)

# PPO Hyperparameters optimized for combat stability
model = PPO("CnnPolicy", env, 
            verbose=1, 
            tensorboard_log="./skyrim_ppo_tensorboard/WARRIOR_BUILD",
            learning_rate=0.0003,
            ent_coef=0.01, # Low entropy = focused behavior
            n_steps=512)

print("⚔️ STARTING WARRIOR TRAINING ⚔️")
print("Constraint: HEAVY ARMOR + TWO HANDED ONLY.")
print("Penalty for Stealth: -50 pts.")

checkpoint_callback = CheckpointCallback(
    save_freq=20000,
    save_path="./skyrim_checkpoints_warrior/",
    name_prefix="warrior_model"
)

print("Starting in 5 seconds...")
time.sleep(5)

try:
    model.learn(total_timesteps=1000000, callback=checkpoint_callback)
    model.save("skyrim_warrior_final")
except KeyboardInterrupt:
    model.save("skyrim_warrior_interrupted")
    print("Training paused.")
