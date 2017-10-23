from mcts_node import MCTSNode
from random import choice
from math import sqrt, log
import random

num_nodes = 1000
explore_faction = 2.


def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    min_node = node
    while(len(node.untried_actions) < 0):
        minVisits = float('Inf');
        for child in node.child_nodes.values():
            if child.visits <= minVisits:
                minVisits = child.visits
                min_node = child
            if child.visits != 0:
                if child.wins / child.visits >= .5:
                    return child

    return min_node

    pass


def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    for actions in node.untried_actions:
        if actions not in node.child_nodes:
            new_state = board.next_state(state, actions)
            new_node = MCTSNode(node, actions, action_list=board.legal_actions(new_state))
            node.child_nodes[actions] = new_node
            node.untried_actions.remove(actions)
            return new_node
    pass
    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    me = board.current_player(state)

    rollout_state = state

    while True:
        # if state is the very last
        if board.is_ended(rollout_state):
            break
        rollout_move = random.choice(board.legal_actions(rollout_state))
        rollout_state = board.next_state(rollout_state, rollout_move)

    # total_score += outcome(board.owned_boxes(rollout_state),
    #                       board.points_values(rollout_state))
    final_score = board.points_values(rollout_state)

    # Return value 1: win for bot/me, value 0: loss
    if final_score[me] == 1:
        return 1
    else:
        return 0


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    prev_node = node

    while prev_node.parent != None:
        if won == 1:
            prev_node.visits += 1
            prev_node.wins += 1
        else:
            prev_node.visits += 1
        # Set node to the parent
        prev_node = prev_node.parent

    pass


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        node = traverse_nodes(node, board, sampled_game, identity_of_bot)

        if len(node.untried_actions) == 0:  # termination condition
            # check state and winner
            # here we select the node we want to move to, based on the all the propagation
            maxWins = 0
            selection = None
            for childKeys in node.child_nodes.keys():
                child = node.child_nodes.get(childKeys)
                if child.wins >= maxWins:
                    maxWins = child.wins
                    selection = childKeys

        else:
            # expand, simulate, propagate
            new_node = expand_leaf(node, board, sampled_game)
            new_state = board.next_state(sampled_game, new_node.parent_action)
            end = rollout(board, new_state)
            backpropagate(new_node, end)


            # Do MCTS - This is all you!

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return selection
