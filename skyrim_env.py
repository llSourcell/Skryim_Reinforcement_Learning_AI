import gymnasium as gym
from gymnasium import spaces
import numpy as np
import cv2
import time
from mss import mss
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController, Button
from AppKit import NSWorkspace

class SkyrimEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render_modes': ['human']}

    def __init__(self, combat_mode=False):
        super(SkyrimEnv, self).__init__()
        
        self.combat_mode = combat_mode
        
        # Define action and observation space
        # Actions: 
        # 0: Move Forward
        # 1: Turn Left
        # 2: Turn Right
        # 3: Attack (Left Click)
        # 4: Jump (Space)
        # 5: Shout (Z)
        # REMOVED: Block (Right Click) to force aggression
        self.action_space = spaces.Discrete(6)
        
        # Observation: Screen capture, resized to 84x84, RGB
        self.observation_space = spaces.Box(low=0, high=255,
                                            shape=(84, 84, 3), dtype=np.uint8)

        # Controllers
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        self.sct = mss()
        
        # Monitor config (from successful test)
        self.monitor = {"top": 50, "left": 0, "width": 1280, "height": 720}
        
    def step(self, action):
        # Execute action
        self._take_action(action)
        
        # Get observation
        observation = self._get_observation()
        
        # Calculate Reward
        reward = 0.0
        
        # 1. Survival Reward: It's alive!
        reward += 0.1
        
        if self.combat_mode:
            # --- COMBAT MODE REWARDS ---
            # 1. Violence: Reward Attacking (Action 3)
            if action == 3:
                reward += 0.1 # Lower base reward, we want to reward HITTING
            
            # 2. Aggression: Reward Moving Forward (Action 0)
            if action == 0:
                reward += 0.05 # Lower forward reward to stop "Charging Blindly"
                
            # 3. BLOOD/COMBAT REWARD (Red Pixel Detection)
            # Detect bright red pixels (Enemy Health Bar / Blood)
            # R > 100 and R > G*1.5 and R > B*1.5
            r_channel = observation[:, :, 0]
            g_channel = observation[:, :, 1]
            b_channel = observation[:, :, 2]
            
            # Create mask for red pixels
            red_mask = (r_channel > 100) & (r_channel > g_channel * 1.5) & (r_channel > b_channel * 1.5)
            red_count = np.count_nonzero(red_mask)
            
            # If we see red (combat), give HUGE reward
            if red_count > 50: # Threshold for "Seeing an enemy health bar or blood"
                reward += 2.0 * (red_count / 1000.0) # Scale reward with amount of red
                # print(f"🩸 BLOOD DETECTED! Reward: {reward}")
                
            # 4. CURIOSITY (Re-enabled to find targets)
            if hasattr(self, 'last_frame'):
                diff = cv2.absdiff(observation, self.last_frame)
                non_zero_count = np.count_nonzero(diff)
                change_pct = non_zero_count / 21168.0
                # Reward significant changes (moving, turning), penalize static (stuck/wall)
                # Increased threshold to 5% to avoid getting fooled by low-health pulsing or menu animations
                if change_pct > 0.05: 
                    reward += 0.5 * change_pct # Up to +0.5 extra
                    self.stuck_steps = 0
                else:
                    reward -= 0.1 # Penalty for being stuck/static
                    self.stuck_steps += 1
                
                # PANIC REFLEX: If stuck for ~30 steps (approx 3-5s), smash buttons
                if self.stuck_steps > 30:
                    print("⚠️ PANIC: Stuck detected! Smashing TAB/ESC/ENTER!")
                    # Try to close menus (Potion screen usually needs TAB, Tutorials need ENTER)
                    # Press TAB twice with longer hold
                    self.keyboard.press(Key.tab)
                    time.sleep(0.2)
                    self.keyboard.release(Key.tab)
                    time.sleep(0.1)
                    self.keyboard.press(Key.tab)
                    time.sleep(0.2)
                    self.keyboard.release(Key.tab)
                    
                    time.sleep(0.2)
                    self.keyboard.press(Key.esc)
                    time.sleep(0.2)
                    self.keyboard.release(Key.esc)
                    
                    time.sleep(0.2)
                    self.keyboard.press(Key.enter)
                    time.sleep(0.2)
                    self.keyboard.release(Key.enter)
                    
                    reward -= 5.0 # Big penalty to learn "Menus = Bad"
                    self.stuck_steps = 0
                
        self.last_frame = observation
        
        # Check if done
        # For now, we don't have a good death detector, so we'll just run for fixed steps in training
        # We will rely on the 'truncated' flag from the training loop if needed
        terminated = False 
        truncated = False
        
        info = {}
        
        return observation, reward, terminated, truncated, info

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        print("Resetting environment...")
        # Focus window
        self.mouse.position = (100, 100)
        self.mouse.click(Button.left, 1)
        time.sleep(0.5)
        
        # Quickload (F9)
        print("Pressing F9 to Quickload...")
        self.keyboard.press(Key.f9)
        time.sleep(0.1)
        self.keyboard.release(Key.f9)
        
        # Wait for load (adjust based on machine speed)
        print("Waiting 5s for load...")
        time.sleep(5) 
        
        # Initialize last_frame
        self.last_frame = self._get_observation()
        self.stuck_steps = 0
        
        return self.last_frame, {}

    def render(self):
        pass # We are capturing screen anyway

    def close(self):
        pass

    def _take_action(self, action):
        # Safety Check: Only press keys if Whisky is the active window
        active_app = NSWorkspace.sharedWorkspace().frontmostApplication().localizedName()
        allowed_apps = ["Whisky", "wine64-preloader", "Skyrim", "TESV", "SkyrimLauncher"]
        if active_app not in allowed_apps:
            # print(f"Paused: Active app is '{active_app}', not in allowed list")
            return

        # 0: Move Forward, 1: Turn Left, 2: Turn Right, 3: Attack, 4: Jump, 5: Shout
        if action == 0:
            self.keyboard.press('w')
            time.sleep(0.2)
            self.keyboard.release('w')
        elif action == 1:
            self.keyboard.press('a')
            time.sleep(0.1)
            self.keyboard.release('a')
        elif action == 2:
            self.keyboard.press('d')
            time.sleep(0.1)
            self.keyboard.release('d')
        elif action == 3: # Attack (Left Click)
            # Use press/release to ensure it registers for heavy weapons
            self.mouse.press(Button.left)
            time.sleep(0.2) 
            self.mouse.release(Button.left)
        elif action == 4: # Jump
            self.keyboard.press(Key.space)
            time.sleep(0.1)
            self.keyboard.release(Key.space)
        elif action == 5: # Shout
            self.keyboard.press('z')
            time.sleep(0.1)
            self.keyboard.release('z')
            
    def _get_observation(self):
        # Capture screen
        sct_img = self.sct.grab(self.monitor)
        frame = np.array(sct_img)
        
        # Convert to RGB (MSS returns BGRA)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2RGB)
        
        # Resize to 84x84 for CNN
        frame = cv2.resize(frame, (84, 84), interpolation=cv2.INTER_AREA)
        
        return frame
