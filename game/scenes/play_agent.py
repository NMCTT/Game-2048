import pygame
import torch
import time
import numpy as np
from game.core.env_2048 import Game2048Env
from game.rl.dqn_model import QNet

from game.settings import SCREEN, CLOCK
import game.logic as logic

# ===== Mapping hành động của env → hành động logic.py =====
ACTION_MAP = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT",
}

class AgentPlayer:
    def __init__(self, model_path="dqn_2048.pth", device="cpu"):
        self.device = device

        # ---- Load model đúng chuẩn ----
        self.model = QNet().to(device)
        self.model.load_state_dict(torch.load(model_path, map_location=device))
        self.model.eval()

        # ---- Env không UI ----
        self.env = Game2048Env()

        # ---- Reset và sync UI ----
        obs = self.env.reset()
        logic.g_board = self.env.board.copy()
        logic.g_score = self.env.score

        self.done = False
        self.speed = 0.5

    def get_valid_actions(self):
        valid = []
        board = self.env.board

        for a in range(4):
            temp = board.copy()

            if a == 0:  # UP
                t = temp.T.copy()
                logic.move_board_left(t)
                temp2 = t.T.copy()

            elif a == 1:  # DOWN
                t = temp.T.copy()
                logic.move_board_right(t)
                temp2 = t.T.copy()

            elif a == 2:  # LEFT
                temp2 = temp.copy()
                logic.move_board_left(temp2)

            elif a == 3:  # RIGHT
                temp2 = temp.copy()
                logic.move_board_right(temp2)

            if not np.array_equal(board, temp2):
                valid.append(a)

        return valid

    # -------- chọn action từ QNet --------
    def choose_action(self, state):
        state = torch.tensor(state, dtype=torch.float32, device=self.device)
        with torch.no_grad():
            q_values = self.model(state)

        valid = self.get_valid_actions()

        q_np = q_values.cpu().numpy()

        # chọn action hợp lệ có Q-value cao nhất
        best = max(valid, key=lambda a: q_np[a])
        return best
        if not valid:
            return None


    # -------- agent chạy 1 bước --------
    def step_agent(self):
        if self.done:
            return "GAME OVER"

        # state dạng [16]
        state = self.env.board.flatten().astype("float32")
        action_id = self.choose_action(state)

        if action_id is None:
            self.done = True
            logic.g_is_game_over = True
            return "GAME OVER"

        # env.step chuẩn
        next_state, reward, terminated, truncated = self.env.step(action_id)
        self.done = terminated or truncated

        # update UI sync
        logic.g_board = self.env.board.copy()
        logic.g_score = self.env.score

        if self.done:
            logic.g_is_game_over = True
            return "GAME OVER"

        return None


class PlayAgentScene:
    def __init__(self):
        from game.scenes.board import GameScene
        self.board_scene = GameScene()
        self.agent = AgentPlayer()
        self.last_step_time = 0
        self.step_delay = 300  # ms


    def Update(self):
        if self.agent.done:
            return "EXIT DIALOG"

        now = pygame.time.get_ticks()
        if now - self.last_step_time < self.step_delay:
            return None

        self.last_step_time = now

        result = self.agent.step_agent()
        if result == "GAME OVER":
            return "EXIT DIALOG"

        return None


    def Handle_Event(self, event):
        # Only back with B
        if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            return "BACK TO MENU"

    def Draw(self):
        self.board_scene.Draw()
