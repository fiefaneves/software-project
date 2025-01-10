import numpy as np
from gymnasium.spaces import Box
from rsoccer_gym.Entities import Ball, Frame, Robot
from rsoccer_gym.ssl.ssl_gym_base import SSLBaseEnv
from rsoccer_gym.Utils import KDTree
from utils.Point import Point
from utils.FixedQueue import FixedQueue
from utils.ssl.small_field import SSLHRenderField
from agent import ExampleAgent
from random_agent import RandomAgent
import random
import pygame
from utils.CLI import Difficulty

class SSLExampleEnv(SSLBaseEnv):
    def __init__(self, render_mode="human", difficulty=Difficulty.EASY):
        field = 2   # 1: SSL Div B    2: SSL Software challenge
        super().__init__(
            field_type=field, 
            n_robots_blue=11,
            n_robots_yellow=11, 
            time_step=0.025,
            render_mode=render_mode)
        
        self.DYNAMIC_OBSTACLES, self.max_targets, self.max_rounds = Difficulty.parse(difficulty)

        n_obs = 4 # Ball x,y and Robot x, y
        self.action_space = Box(low=-1, high=1, shape=(2, ))
        self.observation_space = Box(low=-self.field.length/2,\
            high=self.field.length/2,shape=(n_obs, ))
        
        self.targets = []
        self.min_dist = 0.18
        self.all_points = FixedQueue(max(4, self.max_targets))
        self.robots_paths = [FixedQueue(40) for i in range(11)]

        self.rounds = self.max_rounds  ## because of the first round
        self.targets_per_round = 1

        self.my_agents = {0: ExampleAgent(0, False)}
        self.blue_agents = {i: RandomAgent(i, False) for i in range(1, 11)}
        self.yellow_agents = {i: RandomAgent(i, True) for i in range(0, 11)}

        self.gen_target_prob = 0.003

        if field == 2:
            self.field_renderer = SSLHRenderField()
            self.window_size = self.field_renderer.window_size

    # converts the current frame's ball and robot positions into an observation array    
    def _frame_to_observations(self):
        ball, robot = self.frame.ball, self.frame.robots_blue[0]
        return np.array([ball.x, ball.y, robot.x, robot.y])

    def _get_commands(self, actions):
        # Keep only the last M target points
        for target in self.targets:
            if target not in self.all_points:
                self.all_points.push(target)
                
        # Visible path drawing control
        """Quando existir mais de um agente, apenas mandar o agente para o target mais próximo"""
        for i in self.my_agents:
            self.robots_paths[i].push(Point(self.frame.robots_blue[i].x, self.frame.robots_blue[i].y))

        # Check if the robot is close to the target
        for j in range(len(self.targets) - 1, -1, -1):
            for i in self.my_agents:
                if Point(self.frame.robots_blue[i].x, self.frame.robots_blue[i].y).dist_to(self.targets[j]) < self.min_dist:
                    self.targets.pop(j)
                    break
        
        # Check if there are no more targets
        if len(self.targets) == 0:
            self.rounds -= 1

        # Finish the phase and increase the number of targets for the next phase
        if self.rounds == 0:
            self.rounds = self.max_rounds
            if self.targets_per_round < self.max_targets:
                self.targets_per_round += 1
                self.blue_agents.pop(len(self.my_agents))
                self.my_agents[len(self.my_agents)] = ExampleAgent(len(self.my_agents), False)

        # Generate new targets
        if len(self.targets) == 0:
            for i in range(self.targets_per_round):
                self.targets.append(Point(self.x(), self.y()))
        
        obstacles = {id: robot for id, robot in self.frame.robots_blue.items()}
        for i in range(0, self.n_robots_yellow):
            obstacles[i + self.n_robots_blue] = self.frame.robots_yellow[i]
        teammates = {id: self.frame.robots_blue[id] for id in self.my_agents.keys()}

        remove_self = lambda robots, selfId: {id: robot for id, robot in robots.items() if id != selfId}

        myActions = []
        for i in self.my_agents.keys():
            action = self.my_agents[i].step(self.frame.robots_blue[i], remove_self(obstacles, i), teammates, self.targets)
            myActions.append(action)

        others_actions = []
        if self.DYNAMIC_OBSTACLES:
            for i in self.blue_agents.keys():
                random_target = []
                if random.uniform(0.0, 1.0) < self.gen_target_prob:
                    random_target.append(Point(x=self.x(), y=self.y()))
                    
                others_actions.append(self.blue_agents[i].step(self.frame.robots_blue[i], obstacles, dict(), random_target, True))

            for i in self.yellow_agents.keys():
                random_target = []
                if random.uniform(0.0, 1.0) < self.gen_target_prob:
                    random_target.append(Point(x=self.x(), y=self.y()))

                others_actions.append(self.yellow_agents[i].step(self.frame.robots_yellow[i], obstacles, dict(), random_target, True))

        return myActions + others_actions

    def _calculate_reward_and_done(self):
        return 0, False
    
    def x(self):
        return random.uniform(-self.field.length/2 + self.min_dist, self.field.length/2 - self.min_dist)

    def y(self):
        return random.uniform(-self.field.width/2 + self.min_dist, self.field.width/2 - self.min_dist)
    
    def _get_initial_positions_frame(self):

        def theta():
            return random.uniform(0, 360)
    
        pos_frame: Frame = Frame()

        pos_frame.ball = Ball(x=self.x(), y=self.y())

        pos_frame.robots_blue[0] = Robot(x=self.x(), y=self.y(), theta=theta())

        self.targets = [Point(x=self.x(), y=self.y())]

        places = KDTree()
        places.insert((pos_frame.ball.x, pos_frame.ball.y))

        for i in range(self.n_robots_blue):
            pos = (self.x(), self.y())
            while places.get_nearest(pos)[1] < self.min_dist:
                pos = (self.x(), self.y())

            places.insert(pos)
            pos_frame.robots_blue[i] = Robot(x=pos[0], y=pos[1], theta=theta())
        

        for i in range(0, self.n_robots_yellow):
            pos = (self.x(), self.y())
            while places.get_nearest(pos)[1] < self.min_dist:
                pos = (self.x(), self.y())

            places.insert(pos)
            pos_frame.robots_yellow[i] = Robot(x=pos[0], y=pos[1], theta=theta())

        return pos_frame
    

    def _render(self):
        def pos_transform(pos_x, pos_y):
            return (
                int(pos_x * self.field_renderer.scale + self.field_renderer.center_x),
                int(pos_y * self.field_renderer.scale + self.field_renderer.center_y),
            )

        super()._render()
        
        for target in self.targets:
            self.draw_target(
                self.window_surface,
                pos_transform,
                target,
                (255, 0, 255),
            )

        if len(self.all_points) > 0:
            my_path = [pos_transform(*p) for p in self.all_points]
            for point in my_path:
                pygame.draw.circle(self.window_surface, (255, 0, 0), point, 3)
        
        for i in range(len(self.robots_paths)):
            if len(self.robots_paths[i]) > 1:
                my_path = [pos_transform(*p) for p in self.robots_paths[i]]
                pygame.draw.lines(self.window_surface, (255, 0, 0), False, my_path, 1)

    def draw_target(self, screen, transformer, point, color):
        x, y = transformer(point.x, point.y)
        size = 0.09 * self.field_renderer.scale
        pygame.draw.circle(screen, color, (x, y), size, 2)