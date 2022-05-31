import numpy as np
from rlgym.utils import TerminalCondition
from rlgym.utils.gamestates import GameState
from rlgym.utils.terminal_conditions.common_conditions import NoTouchTimeoutCondition, GoalScoredCondition, \
    TimeoutCondition


def NectoHumanTerminalCondition(tick_skip=8):
    return (
        TimeoutCondition(round(30 * 120 / tick_skip)),
        GoalScoredCondition()
    )


class NectoTerminalCondition(TerminalCondition):
    def __init__(self, tick_skip=8):
        super().__init__()
        self.no_touch = NoTouchTimeoutCondition(round(30 * 120 / tick_skip))
        self.goal_scored = GoalScoredCondition()

    def reset(self, initial_state: GameState):
        self.no_touch.reset(initial_state)
        self.goal_scored.reset(initial_state)

    def is_terminal(self, current_state: GameState) -> bool:
        if self.no_touch.is_terminal(current_state):
            return True
        if self.goal_scored.is_terminal(current_state):
            return True
        blue, orange, ticks_left = current_state.inverted_ball.angular_velocity
        if ticks_left < 0 and np.isinf(ticks_left):
            return True
        return False
