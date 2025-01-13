from utils.ssl.Navigation import Navigation
from utils.ssl.base_agent import BaseAgent
from utils.Point import Point

class ExampleAgent(BaseAgent):
    def __init__(self, id=0, yellow=False):
        super().__init__(id, yellow)

    def decision(self):
        if len(self.targets) == 0:
            return

        target_velocity, target_angle_velocity = Navigation.goToPoint(self.robot, self.targets[0], self.opponents.values())
        
        # Potencial Field
        
        obstacle_radius = 10
        avoidance_weight = 40

        # Attraction force
        direction_to_target = self.targets[0] - self.pos
        distance_to_target = self.pos.dist_to(self.targets[0])
        attraction_force = Point(0, 0)
        if distance_to_target > 0:
            attraction_force = direction_to_target.normalize() * distance_to_target
        
        # Repulsion force
        repulsion_force = Point(0, 0)
        for obstacle in self.opponents.values():
            direction_to_obstacle = self.pos - obstacle
            distance_to_obstacle = self.pos.dist_to(obstacle)
            if distance_to_obstacle < obstacle_radius and distance_to_obstacle > 0:
                repulsion_force += direction_to_obstacle.normalize() * (obstacle_radius - distance_to_obstacle) / distance_to_obstacle

        # Combining forces
        total_force = attraction_force + repulsion_force * avoidance_weight
        if total_force.length() > 0:
            target_velocity = total_force.normalize() * target_velocity.length()        
        
        """
        # Avoidance behavior
        avoidance_vector = Point(0, 0)
        for obstacle in self.opponents.values():
            distance_to_obstacle = self.pos.dist_to(obstacle)
            if distance_to_obstacle < 1:
                avoidance_vector += (self.pos - obstacle) / distance_to_obstacle

        if avoidance_vector.x != 0 or avoidance_vector.y != 0:
            avoidance_vector = avoidance_vector.normalize() * 1
            target_velocity = (target_velocity * 0.7 + avoidance_vector * 0.3).normalize()
            if target_velocity.length() != 0:
                target_velocity = target_velocity.normalize()
        """
        
        # Gradual deceleration as the robot approaches the target
        """
        This is already happening in the Navigation.goToPoint function
        distance_to_target = self.pos.dist_to(self.targets[0])
        if distance_to_target < 0.5:
            target_velocity *= distance_to_target / 0.5
        """

        self.set_vel(target_velocity)
        self.set_angle_vel(target_angle_velocity)

        return

    def post_decision(self):
        pass
 