from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from skyrim_env import SkyrimEnv
import time

# ⚔️ GEN 6: THE WARLORD ⚔️
# Goal: Hunt, Kill, Conquer.
# Rewards: +Attack, +Forward, -Curiosity (No spinning)

# Enable COMBAT MODE
env = SkyrimEnv(combat_mode=True)

# Fresh Brain for the Pub Brawl
model = PPO("CnnPolicy", env, 
            verbose=1, 
            tensorboard_log="./skyrim_ppo_tensorboard/AGI_PUB_BRAWL",
            learning_rate=0.0003,
            ent_coef=0.05, # HIGH ENTROPY to force exploration (stop charging blindly)
            n_steps=512)

print("🍺 STARTING GEN 7: PUB BRAWL TRAINING 🍺")
print("Rewards:")
print("1. BLOODLUST (Red Pixels = Enemy Health/Blood)")
print("2. CURIOSITY (Look around to find targets)")
print("3. VIOLENCE (Small reward for swinging)")
print("4. HIGH ENTROPY (Randomness forced)")

# Save frequently
checkpoint_callback = CheckpointCallback(
    save_freq=20000,
    save_path="./skyrim_checkpoints_combat/",
    name_prefix="warlord_model"
)

print("Starting in 5 seconds... (Ensure F5 Save is NEAR ENEMIES!)")
time.sleep(5)

try:
    model.learn(total_timesteps=100000, callback=checkpoint_callback)
    model.save("skyrim_warlord_model")
    print("Warlord Model Saved.")
except KeyboardInterrupt:
    model.save("skyrim_warlord_model_interrupted")
    print("Training paused. Model saved.")
