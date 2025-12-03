from stable_baselines3 import PPO
from skyrim_env import SkyrimEnv
import time
import os

# Create environment
env = SkyrimEnv()

# Instantiate the agent
# CnnPolicy is used because our observation is an image
model = PPO("CnnPolicy", env, verbose=1, tensorboard_log="./skyrim_ppo_tensorboard/")

print("Starting training in 5 seconds...")
print("Please ensure Skyrim is running and you have a QUICK SAVE ready (F5 to save).")
print("The script will press F9 to load it.")
time.sleep(5)

try:
    # Train the agent
    # 10000 steps is a short run to verify it works
    model.learn(total_timesteps=10000)

    # Save the agent
    model.save("skyrim_ppo_model")
    print("Training complete. Model saved.")

except KeyboardInterrupt:
    print("Training interrupted. Saving model...")
    model.save("skyrim_ppo_model_interrupted")
    print("Model saved.")
