from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent
from utils.Point import Point
import numpy as np


# Parameters for potential field
K_ATTRACT = 5.0  # Attractive potential gain
K_REPULSE = 3.0  # Repulsive potential gain
REPULSE_RADIUS = 0.5  # Radius of influence for obstacles


class ExampleAgent(BaseAgent):
    def __init__(self, id=0, yellow=False):
        super().__init__(id, yellow)

    def decision(self):
        if len(self.targets) == 0:
            return
        
        obstacles = list(self.opponents.values())
        target = self.targets[0]
        
        # Attractive potential
        force_x = K_ATTRACT * (target.x - self.robot.x)
        force_y = K_ATTRACT * (target.y - self.robot.y)

        # Repulsive potential
        for obstacle in obstacles:
            dist = np.hypot(obstacle.x - self.robot.x, obstacle.y - self.robot.y)
            if dist < REPULSE_RADIUS:
                repulse_x = K_REPULSE * (1.0 / dist - 1.0 / REPULSE_RADIUS) * (1.0 / dist**2) * (self.robot.x - obstacle.x)
                repulse_y = K_REPULSE * (1.0 / dist - 1.0 / REPULSE_RADIUS) * (1.0 / dist**2) * (self.robot.y - obstacle.y)
                force_x += repulse_x
                force_y += repulse_y

        # Calculate target velocity and angle velocity
        target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, Point(self.robot.x + force_x, self.robot.y + force_y))
        
        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)

        return

    def post_decision(self):
        pass
 