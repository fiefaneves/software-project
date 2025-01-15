from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent
from utils.Point import Point
import numpy as np


# Parameters for potential field
K_ATTRACT: float = 3.5  # Attractive potential gain
K_REPULSE: float = 3.0  # Repulsive potential gain
REPULSE_RADIUS: float = 0.5  # Radius of influence for obstacles
MAX_FORCE: float = 0.7  # Maximum force that can be applied to the robot 


class ExampleAgent(BaseAgent):
    def __init__(self, id=0, yellow=False):
        super().__init__(id, yellow)
        self.prev_velocity = Point(0, 0)
        self.alpha = 0.5 # Smoothing factor (0 < alpha <= 1)

    def decision(self):
        if len(self.targets) == 0:
            return
        
        obstacles = list(self.opponents.values())
        target = self.targets[0]
        
        # Calculate distance to target
        dist_to_target = self.pos.dist_to(target)
        
        # Dynamic scaling of attractive and repulsive forces
        dynamic_k_attract = K_ATTRACT * (1.0 + dist_to_target)
        dynamic_k_repulse = K_REPULSE * (1.0 / (1.0 + dist_to_target))

        # Attractive potential
        """force_x = K_ATTRACT * (target.x - self.robot.x)
        force_y = K_ATTRACT * (target.y - self.robot.y)"""
        force_x = dynamic_k_attract * (target.x - self.robot.x)
        force_y = dynamic_k_attract * (target.y - self.robot.y)

        # Repulsive potential
        for obstacle in obstacles:
            dist = self.pos.dist_to(obstacle)
            if dist < REPULSE_RADIUS:
                factor = dynamic_k_repulse * (1.0 / dist - 1.0 / REPULSE_RADIUS) * (1.0 / dist**2)
                # factor = K_REPULSE * (1.0 / dist - 1.0 / REPULSE_RADIUS) * (1.0 / dist**2)
                repulse_x = factor * (1.0 / dist**2) * (self.robot.x - obstacle.x)
                repulse_y = factor * (self.robot.y - obstacle.y)

                # Tangential component to avoid obstacles
                tangential_x = -repulse_y
                tangential_y = repulse_x

                force_x += repulse_x + tangential_x
                force_y += repulse_y + tangential_y
                """force_x += repulse_x
                force_y += repulse_y"""

        # Normalize forces to avoid excessively large values
        force_magnitude = np.hypot(force_x, force_y)
        if force_magnitude > MAX_FORCE:
            force_x = (force_x / force_magnitude) * MAX_FORCE
            force_y = (force_y / force_magnitude) * MAX_FORCE

        # Calculate target velocity and angle velocity
        target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, Point(self.robot.x + force_x, self.robot.y + force_y))

        # Apply low-pass filter for smoothness
        smoothed_velocity = Point(
            self.alpha * target_velocity.x + (1 - self.alpha) * self.prev_velocity.x,
            self.alpha * target_velocity.y + (1 - self.alpha) * self.prev_velocity.y
        )
        self.prev_velocity = smoothed_velocity

        self.set_vel(smoothed_velocity)
        # self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)

        return

    def post_decision(self):
        pass
 