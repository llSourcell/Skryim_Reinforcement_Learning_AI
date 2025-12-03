from manim import *
import numpy as np
from visual_style import GlowingAgent, NeonGrid, CyberObstacle, EtherealGoal, NEON_BLUE, NEON_PURPLE, DEEP_SPACE_BLUE, CYBER_GREEN, WARNING_RED, GOLD_GLOW

class RLWorldClass(ThreeDScene):
    def construct(self):
        # --- CONFIGURATION ---
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        
        # --- SCENE 1: THE CYBER-ARENA ---
        # Grid
        grid = NeonGrid(size=12, step=1)
        
        # Agent
        agent = GlowingAgent()
        agent.move_to(np.array([0, 0.3, 0]))
        
        # Obstacles
        obstacles_coords = [(2, 0), (2, 1), (2, -1), (-1, 2), (-2, 2), (0, -2)]
        obstacles = VGroup()
        for x, z in obstacles_coords:
            obs = CyberObstacle()
            obs.move_to(np.array([x, 0.5, z]))
            obstacles.add(obs)
            
        # Goal
        goal = EtherealGoal()
        goal.move_to(np.array([3, 1, 3]))
        
        # Intro
        title = Text("Reinforcement Learning", font_size=60, font="Orbitron", color=NEON_BLUE)
        subtitle = Text("The Agent's Journey", font_size=30, font="Orbitron", color=WHITE).next_to(title, DOWN)
        intro_group = VGroup(title, subtitle).to_edge(UP)
        
        self.add_fixed_in_frame_mobjects(intro_group)
        self.play(Write(title), FadeIn(subtitle))
        self.wait(1)
        
        self.play(
            Create(grid),
            LaggedStart(*[Create(o) for o in obstacles], lag_ratio=0.1),
            run_time=2
        )
        self.play(FadeIn(agent), FadeIn(goal))
        self.play(agent.pulse(), goal.idle_animation())
        self.wait(1)
        
        self.play(FadeOut(intro_group))

        # --- SCENE 2: THE BRAIN (Q-TABLE HUD) ---
        # Create a Q-Table visualization (2D HUD)
        # Rows: States (simplified), Cols: Actions (Up, Down, Left, Right)
        
        q_table_bg = Rectangle(width=4, height=3, color=NEON_PURPLE, fill_opacity=0.8, fill_color=BLACK)
        q_table_bg.to_corner(UL)
        
        q_title = Text("Q-Table (Brain)", font_size=24, color=NEON_PURPLE).next_to(q_table_bg, UP, buff=0.1)
        q_title.align_to(q_table_bg, LEFT)
        
        # Simplified Grid for HUD
        rows = 4
        cols = 4
        cells = VGroup()
        for i in range(rows):
            for j in range(cols):
                cell = Rectangle(width=0.8, height=0.5, stroke_color=WHITE, stroke_width=1)
                cell.move_to(q_table_bg.get_corner(UL) + np.array([0.5 + j*0.9, -0.5 - i*0.6, 0]))
                val = Text("0.0", font="Courier New", font_size=20, color=WHITE)
                val.move_to(cell)
                cells.add(VGroup(cell, val))
        
        hud_group = VGroup(q_table_bg, cells)
        
        self.add_fixed_in_frame_mobjects(q_title, hud_group)
        self.play(FadeIn(q_title), Create(hud_group))
        self.wait(1)

        # --- SCENE 3: THE BELLMAN EQUATION ---
        # Q(s,a) <- Q(s,a) + alpha * [R + gamma * max(Q(s',a')) - Q(s,a)]
        
        # Using Text instead of MathTex to avoid LaTeX dependency issues in this environment
        eq_font = "Courier New"
        equation = VGroup(
            Text("Q(s,a) ← ", font=eq_font, font_size=30),
            Text("Q(s,a) ", font=eq_font, font_size=30),
            Text("+ α [", font=eq_font, font_size=30),
            Text("R", font=eq_font, font_size=30, color=WARNING_RED),
            Text(" + γ max Q(s',a') ", font=eq_font, font_size=30, color=CYBER_GREEN),
            Text("- Q(s,a)]", font=eq_font, font_size=30)
        ).arrange(RIGHT, buff=0.1)
        
        equation.to_edge(DOWN)
        
        self.add_fixed_in_frame_mobjects(equation)
        self.play(Write(equation))
        self.wait(1)

        # --- SCENE 4: THE LOOP & EXPLORATION ---
        
        # Camera move
        self.move_camera(phi=60 * DEGREES, theta=45 * DEGREES, zoom=0.7, run_time=2)
        
        # Episode Loop
        for step in range(3):
            # 1. State
            state_text = Text(f"State: {step}", font_size=24, color=NEON_BLUE).next_to(q_table_bg, DOWN)
            self.add_fixed_in_frame_mobjects(state_text)
            
            # 2. Action Selection (Exploration)
            die = Square(side_length=1, color=WHITE).to_corner(UR)
            die_txt = Text("?", font_size=40).move_to(die)
            die_group = VGroup(die, die_txt)
            self.add_fixed_in_frame_mobjects(die_group)
            
            self.play(Rotate(die_group, angle=360*DEGREES), run_time=0.5)
            
            # Arrows appear
            arrows = VGroup()
            moves = [RIGHT, LEFT, UP, DOWN] # 3D relative
            # Map to 3D: Right (+x), Left (-x), Up (+z), Down (-z)
            moves_3d = [np.array([1,0,0]), np.array([-1,0,0]), np.array([0,0,1]), np.array([0,0,-1])]
            
            for m in moves_3d:
                arr = Arrow3D(start=agent.get_center(), end=agent.get_center() + m, color=WHITE)
                arrows.add(arr)
            
            self.play(Create(arrows), run_time=0.5)
            
            # Pick one (randomly for demo)
            chosen_idx = step % 4 # predictable for demo
            chosen_arrow = arrows[chosen_idx]
            
            self.play(
                chosen_arrow.animate.set_color(CYBER_GREEN).scale(1.2),
                FadeOut(arrows[:chosen_idx]), FadeOut(arrows[chosen_idx+1:])
            )
            
            # Move
            move_vec = moves_3d[chosen_idx]
            self.play(agent.animate.shift(move_vec), FadeOut(chosen_arrow), run_time=0.5)
            
            # 3. Reward & Update
            # Highlight R in equation (Index 3 is R)
            self.play(equation[3].animate.scale(1.5).set_color(GOLD_GLOW), run_time=0.3)
            self.play(equation[3].animate.scale(1/1.5).set_color(WARNING_RED), run_time=0.3)
            
            # Update Q-Table cell
            target_cell_group = cells[step * 4 + chosen_idx]
            old_val = target_cell_group[1]
            new_val = Text(f"{0.5 * (step+1):.1f}", font="Courier New", font_size=20, color=CYBER_GREEN).move_to(old_val)
            
            self.play(
                ReplacementTransform(old_val, new_val),
                Indicate(target_cell_group[0], color=CYBER_GREEN)
            )
            # Update the group reference for future (though we don't use it again in this loop structure)
            target_cell_group.remove(old_val)
            target_cell_group.add(new_val)
            
            self.remove(state_text)
            self.remove(die_group)
            self.wait(0.5)

        # --- SCENE 5: DEEP RL TRANSITION ---
        
        # "Too many states?"
        transition_text = Text("Too many states?", font_size=48, color=WARNING_RED).to_edge(UP)
        self.add_fixed_in_frame_mobjects(transition_text)
        self.play(Write(transition_text))
        self.wait(1)
        
        # Morph Q-Table to Neural Net
        # Create NN nodes
        layers = [3, 4, 4, 2]
        nn_group = VGroup()
        
        # Position NN where Q-Table was
        start_x = -6
        start_y = 2
        
        for i, layer_size in enumerate(layers):
            layer_group = VGroup()
            for j in range(layer_size):
                node = Circle(radius=0.15, color=NEON_BLUE, fill_opacity=0.5)
                node.move_to(np.array([start_x + i*1.5, start_y - j*0.5, 0]))
                layer_group.add(node)
            nn_group.add(layer_group)
            
        # Edges
        edges = VGroup()
        for i in range(len(layers)-1):
            for n1 in nn_group[i]:
                for n2 in nn_group[i+1]:
                    edge = Line(n1.get_center(), n2.get_center(), stroke_width=1, stroke_opacity=0.3, color=WHITE)
                    edges.add(edge)
        
        full_nn = VGroup(edges, nn_group)
        # We need to put this in fixed frame to replace HUD
        # But VGroup of 3D objects? No, Circle/Line are 2D Mobjects, can be fixed.
        
        self.play(
            FadeOut(hud_group), FadeOut(q_title),
            FadeIn(full_nn),
            FadeOut(transition_text)
        )
        
        nn_label = Text("Deep Q-Network", font_size=30, color=NEON_BLUE).next_to(full_nn, UP)
        self.add_fixed_in_frame_mobjects(nn_label)
        self.play(Write(nn_label))
        
        # Pulse the network
        self.play(
            full_nn.animate.set_color(CYBER_GREEN),
            rate_func=there_and_back,
            run_time=1
        )
        
        # Final Agent Rush
        path_points = [
            agent.get_center(),
            agent.get_center() + np.array([1,0,0]),
            agent.get_center() + np.array([1,0,1]),
            agent.get_center() + np.array([2,0,1]),
            goal.get_center()
        ]
        path = VMobject().set_points_as_corners(path_points).set_color(CYBER_GREEN)
        
        self.play(MoveAlongPath(agent, path), run_time=1.5)
        self.play(Flash(goal, color=GOLD_GLOW, line_length=1, num_lines=8))
        
        final_text = Text("AGI Achieved?", font_size=60, color=GOLD_GLOW)
        self.add_fixed_in_frame_mobjects(final_text)
        self.play(Write(final_text))
        self.wait(2)
        
        # Cleanup
        self.play(FadeOut(Group(*self.mobjects)))
