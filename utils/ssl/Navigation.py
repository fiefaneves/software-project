
import math
import numpy as np
from rsoccer_gym.Entities import Robot
from utils.Point import Point
from utils.Geometry import Geometry


PROP_VELOCITY_MIN_FACTOR: float = 0.1
MAX_VELOCITY: float = 1.5
ANGLE_EPSILON: float = 0.1
ANGLE_KP: float = 5
MIN_DIST_TO_PROP_VELOCITY: float = 720

ADJUST_ANGLE_MIN_DIST: float = 50
M_TO_MM: float = 1000.0

OBSTACLE_RADIUS: float = 10
AVOIDANCE_WEIGHT: float = 40


class Navigation:

  @staticmethod
  def degrees_to_radians(degrees):
    return degrees * (math.pi / 180.0)
  
  @staticmethod
  def radians_to_degrees(radians):
    return radians * (180.0 / math.pi)
  
  @staticmethod
  def global_to_local_velocity(vx, vy, theta):
    vx_local = vx * math.cos(theta) + vy * math.sin(theta)
    vy_local = -vx * math.sin(theta) + vy * math.cos(theta)
    return Point(vx_local, vy_local)

  @staticmethod
  def map_value(value, lLower, lHigher, rLower, rHigher):
    if (lHigher - lLower) == 0:
      return
    
    return ((value - lLower) * (rHigher - rLower) / (lHigher - lLower) + rLower)

  @staticmethod
  def goToPoint(robot: Robot, target: Point, obstacles: list[Point]):
    target = Point(target.x * M_TO_MM, target.y * M_TO_MM)
    robot_position = Point(robot.x * M_TO_MM, robot.y * M_TO_MM)
    robot_angle = Navigation.degrees_to_radians(Geometry.normalize_angle(robot.theta, 0, 180))

    max_velocity = MAX_VELOCITY
    distance_to_target = robot_position.dist_to(target)
    kp = ANGLE_KP

    # Use proportional speed to decelerate when getting close to desired target
    proportional_velocity_factor = PROP_VELOCITY_MIN_FACTOR
    min_proportional_distance = MIN_DIST_TO_PROP_VELOCITY

    if distance_to_target <= min_proportional_distance:
      max_velocity = max_velocity * Navigation.map_value(distance_to_target, 0.0, min_proportional_distance, proportional_velocity_factor, 1.0)

    target_angle = (target - robot_position).angle()
    d_theta = Geometry.smallest_angle_diff(target_angle, robot_angle)

    """
    # Calculate repulsion force from obstacles
    repulsion_force = Point(0, 0)
    for obstacle in obstacles:
        direction_to_obstacle = robot_position - obstacle
        distance_to_obstacle = robot_position.dist_to(obstacle)
        if distance_to_obstacle < OBSTACLE_RADIUS and distance_to_obstacle > 0:
            repulsion_force += direction_to_obstacle.normalize() * (OBSTACLE_RADIUS - distance_to_obstacle) / distance_to_obstacle

    # Combine attraction and repulsion forces
    total_force = (target - robot_position).normalize() * distance_to_target + repulsion_force * AVOIDANCE_WEIGHT
    if total_force.length() > 0:
        target_velocity = total_force.normalize() * max_velocity
    """

    if distance_to_target > ADJUST_ANGLE_MIN_DIST:
      v_angle = Geometry.abs_smallest_angle_diff(math.pi - ANGLE_EPSILON, d_theta)
      v_proportional = v_angle * (max_velocity / (math.pi - ANGLE_EPSILON))
      global_final_velocity = Geometry.from_polar(v_proportional, target_angle)
      target_velocity = Navigation.global_to_local_velocity(global_final_velocity.x, global_final_velocity.y, robot_angle)

      return target_velocity, -kp * d_theta
    else:
      return Point(0.0, 0.0), -kp * d_theta