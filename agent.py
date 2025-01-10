from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent
from utils.Point import Point

class ExampleAgent(BaseAgent):
    def __init__(self, id=0, yellow=False):
        super().__init__(id, yellow)

    def decision(self):
        if len(self.targets) == 0:
            return

        target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, self.targets[0])
        
        # Avoidance behavior
        avoidance_vector = Point(0, 0)
        for obstacle in self.opponents.values():
            distance_to_obstacle = self.pos.dist_to(obstacle)
            if distance_to_obstacle < 1:
                avoidance_vector += (self.pos - obstacle) / distance_to_obstacle

        if avoidance_vector.x != 0 or avoidance_vector.y != 0:
            avoidance_vector = avoidance_vector.normalize() * 1
            target_velocity = (target_velocity * 0.7 + avoidance_vector * 0.3).normalize() * target_velocity.length()
            if target_velocity.length() != 0:
                target_velocity = target_velocity.normalize() * target_velocity.length()

        # Gradual deceleration as the robot approaches the target
        distance_to_target = self.pos.dist_to(self.targets[0])
        if distance_to_target < 0.5:
            target_velocity *= distance_to_target / 0.5

        # Minimum velocity
        if target_velocity.length() < 0.1:
            target_velocity = target_velocity.normalize() * 0.1

        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)

        return

    def post_decision(self):
        pass
 