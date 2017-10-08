"""The Trained Bot"""
from public.hlt import format_moves
from public.models.agent.Agent import start_agent
from public.models.bot.Bot import Bot
from public.state.state import get_game_state


class TrainedBot(Bot):
    """The trained bot"""

    def __init__(self, agent_class, state):
        self.sess, self.agent = start_agent(agent_class, state)

    def compute_moves(self, game_map):
        """Compute the moves given a game_map"""
        game_state = get_game_state(game_map, self.my_id)
        moves1, moves2 = self.agent.choose_actions(self.sess, game_state, train=False)
        return format_moves(game_map, -(moves1*moves2))

    def get_policies(self, game_state):
        """Compute the policies given a game_state"""
        return self.agent.get_policies(self.sess, game_state)

    def close(self):
        """Close the tensorflow session"""
        self.sess.close()
