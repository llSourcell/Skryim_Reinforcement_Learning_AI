from manim import *
import numpy as np

# --- THEME COLORS ---
NEON_BLUE = "#00F3FF"
NEON_PURPLE = "#BC13FE"
DEEP_SPACE_BLUE = "#020024"
CYBER_GREEN = "#0AFF99"
WARNING_RED = "#FF073A"
GOLD_GLOW = "#FFD700"

class GlowingAgent(VGroup):
    """
    A futuristic drone/agent representation.
    Consists of a solid core and a pulsing outer shell.
    """
    def __init__(self, radius=0.3, color=NEON_BLUE, **kwargs):
        super().__init__(**kwargs)
        self.core = Sphere(radius=radius, resolution=(24, 24))
        self.core.set_color(color)
        self.core.set_sheen(0.8, direction=UP)
        
        self.glow = Sphere(radius=radius * 1.4, resolution=(24, 24))
        self.glow.set_color(color)
        self.glow.set_opacity(0.2)
        
        # Add a ring/orbit for extra detail
        self.ring = Circle(radius=radius * 1.8, color=WHITE, stroke_width=2)
        self.ring.rotate(90 * DEGREES, axis=RIGHT)
        self.ring.set_opacity(0.5)
        
        self.add(self.core, self.glow, self.ring)
        
    def pulse(self):
        """Returns an animation of the glow pulsing."""
        return AnimationGroup(
            self.glow.animate.scale(1.1).set_opacity(0.1),
            self.ring.animate.rotate(180 * DEGREES, axis=UP),
            run_time=1,
            rate_func=there_and_back
        )

class CyberObstacle(Cube):
    """
    A wireframe-heavy cube that looks like a digital barrier.
    """
    def __init__(self, side_length=1, color=WARNING_RED, **kwargs):
        super().__init__(side_length=side_length, **kwargs)
        self.set_fill(color, opacity=0.1)
        self.set_stroke(color, width=3, opacity=0.8)
        
        # Add an inner wireframe for complexity
        inner = Cube(side_length=side_length * 0.7)
        inner.set_stroke(color, width=1, opacity=0.5)
        inner.set_fill(opacity=0)
        self.add(inner)

class NeonGrid(VGroup):
    """
    A glowing grid floor with a 'Tron' aesthetic.
    """
    def __init__(self, size=10, step=1, color=NEON_PURPLE, **kwargs):
        super().__init__(**kwargs)
        plane = NumberPlane(
            x_range=(-size/2, size/2, step),
            y_range=(-size/2, size/2, step),
            background_line_style={
                "stroke_color": color,
                "stroke_width": 2,
                "stroke_opacity": 0.6
            },
            axis_config={"stroke_opacity": 0} # Hide axes
        )
        plane.rotate(90 * DEGREES, axis=RIGHT)
        self.add(plane)

class EtherealGoal(VGroup):
    """
    A floating, spinning artifact representing the goal.
    """
    def __init__(self, color=GOLD_GLOW, **kwargs):
        super().__init__(**kwargs)
        self.shape = Octahedron(edge_length=1)
        self.shape.set_color(color)
        self.shape.set_opacity(0.8)
        self.shape.set_sheen(1.0, direction=UP + RIGHT)
        
        self.beams = VGroup()
        for _ in range(3):
            beam = Circle(radius=0.8, color=color, stroke_width=2)
            beam.rotate(np.random.random() * 90 * DEGREES, axis=np.random.random(3))
            self.beams.add(beam)
            
        self.add(self.shape, self.beams)
        
    def idle_animation(self):
        """Returns a continuous rotation animation."""
        return AnimationGroup(
            Rotate(self.shape, angle=360 * DEGREES, axis=UP, run_time=4, rate_func=linear),
            Rotate(self.beams, angle=-360 * DEGREES, axis=UP, run_time=6, rate_func=linear)
        )
