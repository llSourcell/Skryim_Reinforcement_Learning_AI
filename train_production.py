import argparse
from stable_baselines3 import PPO
from skyrim_env import SkyrimEnv
import time
import numpy as np

# Argument Parser for "Behaviors"
parser = argparse.ArgumentParser(description='Train Skyrim AI with specific behaviors.')
parser.add_argument('--behavior', type=str, default='explore', 
                    choices=['explore', 'combat', 'chaos'],
                    help='Choose behavior: explore (walking), combat (attacking), chaos (random)')
args = parser.parse_args()

print(f"⚔️ STARTING SKYRIM AI: {args.behavior.upper()} MODE ⚔️")

# Custom Reward Wrapper could go here, but for simplicity we'll hack it in the Env or just rely on PPO exploring.
# For "Chaos" mode, we don't even need PPO, just random actions.

if args.behavior == 'chaos':
    print("🤪 CHAOS MODE ACTIVATED: Perfect for 'Failures' and 'Glitches' footage.")
    print("The agent will act randomly.")
    env = SkyrimEnv()
    env.reset()
    try:
        while True:
            action = env.action_space.sample()
            obs, reward, term, trunc, info = env.step(action)
            # Randomly hold keys longer for glitch potential
            if np.random.rand() > 0.9:
                time.sleep(0.5)
    except KeyboardInterrupt:
        print("Chaos managed.")

else:
    # Training Modes
    env = SkyrimEnv()
    
    # Load existing model if possible, else create new
    try:
        model = PPO.load("skyrim_ppo_model")
        print("Loaded existing brain! 🧠")
        model.set_env(env)
    except:
        print("Creating NEW brain! 👶")
        model = PPO("CnnPolicy", env, verbose=1, tensorboard_log=f"./skyrim_ppo_tensorboard/{args.behavior}")

    # Customize learning based on behavior (conceptual - PPO will optimize whatever reward is in Env)
    # To truly specialize, we'd need to change the Env's reward function dynamically.
    # For now, we'll just train and let the user guide it by where they save/load.
    
    print("Starting training in 5 seconds...")
    print("Ensure Skyrim is ready (F5 saved).")
    time.sleep(5)

    try:
        # Train for a long time to get "Smart" behavior
        steps = 100000 if args.behavior == 'combat' else 20000
        model.learn(total_timesteps=steps)
        model.save(f"skyrim_ppo_{args.behavior}")
        print(f"Saved {args.behavior} model.")
    except KeyboardInterrupt:
        model.save(f"skyrim_ppo_{args.behavior}_interrupted")
        print("Saved interrupted model.")
