from manim import *
from visual_style import GlowingAgent, NeonGrid, CyberObstacle, EtherealGoal

class AssetShowcase(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES)
        
        # 1. The Grid
        grid = NeonGrid()
        self.add(grid)
        
        # 2. The Agent
        agent = GlowingAgent()
        agent.move_to(np.array([0, 0.5, 0]))
        self.add(agent)
        self.play(agent.pulse())
        
        # 3. Obstacles
        obs = CyberObstacle()
        obs.move_to(np.array([2, 0.5, 2]))
        self.play(Create(obs))
        
        # 4. Goal
        goal = EtherealGoal()
        goal.move_to(np.array([-2, 1, -2]))
        self.add(goal)
        self.play(goal.idle_animation())
        
        self.wait(2)
