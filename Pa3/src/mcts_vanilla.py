from mcts_node import MCTSNode
from random import choice
from math import sqrt, logc

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
    pass
    # Hint: return leaf_node


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

    return node
    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    pass
    #return who one the simulation


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
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

        if len(node.untried_actions) == 0: #termination condition
        # check state and winner
        #here we select the node we want to move to, based on the all the propagation
        maxWins = 0
        selection = None
        for child in node.child_node.values():
            if child.wins > maxWins:
                maxWins = child.wins
                selection = child
        else:
            #expand, simulate, propagate
            new_node = expand_leaf(node, board, sampled_game)
            new_state = board.next_state(sampled_game)
            end = rollout(board, new_state)
            backpropagate(new_node,end)


        # Do MCTS - This is all you!

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return selection
