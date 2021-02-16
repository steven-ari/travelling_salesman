# Python3 program to implement traveling salesman
# problem using naive approach.
import sys
import logging
import numpy as np
from itertools import permutations

# default graph from assignment
graph_matrix = np.array([[0., 10., 15., 20.],
                         [10., 0., 35., 25.],
                         [15., 35., 0., 30.],
                         [20., 25., 30., 0.]])


# check ig graph is legitimate
def graph_check(graph):
    """
    Check if graph is proper
    :param Graph: 2-D numpy array with floating point
    :return: True for legitimate
    """

    # check if all >=0
    pos_flag = (graph >= 0).all()
    # check if graph matrix symmetrical
    sym_flag = np.allclose(graph, graph.T, rtol=1e-05, atol=1e-05)
    # check if sum of diagonal is zero
    diag_flag = np.isclose(0, np.diag(graph).sum(), rtol=1e-05, atol=1e-08, equal_nan=False)

    return pos_flag and sym_flag and diag_flag


# implementation of traveling Salesman Problem
def ts_problem():
    """
    Calculate minimal energy for current graph
    :param None
    :return:
    """

    global graph_matrix

    # check if graph is legit, symmetrical
    try:
        if not graph_check(graph_matrix):
            raise ValueError
    except ValueError:
        print(graph_matrix)
        logging.error("Graph not legitimate, matrix should be positive, symetrical and zeros on the diagonal!")
        return

    # create possible paths with permutation
    path_perm = permutations(range(graph_matrix.shape[0]))
    min_energy = sys.maxsize
    min_path = tuple(range(graph_matrix.shape[0]))

    # try every possible path
    for path in path_perm:
        current_pathenergy = 0
        current_node = path[0]
        # walkthrough
        for node in path:
            current_pathenergy += graph_matrix[current_node][node]
            current_node = node
        # back to start
        current_pathenergy += graph_matrix[current_node][path[0]]

        # update min energy
        if min_energy > current_pathenergy:
            min_energy = current_pathenergy
            min_path = path

    # convert path for user friendliness
    min_path = tuple(x+1 for x in min_path)

    # log results
    print("Current graph: ")
    print(str(graph_matrix))
    print('min energy: ' + str(min_energy))
    print('most efficient path: ' + str(min_path) + '\n')

    return


def add_node(energy_vector):
    """
    Accept only list as energy vector
    :param energy_vector: Energy vector value only contain energy path to every other nodes
    :return:
    """

    # prepare variables
    global graph_matrix
    energy_vector = np.array(energy_vector)

    # assert vec length
    try:
        if not energy_vector.__len__() == graph_matrix.shape[0]:
            raise ValueError
    except ValueError:
        print("Energy vector: " + str(energy_vector))
        logging.error("New energy vector not legitimate, check length of input vector")
        return

    # assert if zero energy error exist
    try:
        if 0 in energy_vector:
            raise ValueError
    except ValueError:
        print("Energy vector: " + energy_vector)
        logging.error("New energy vector not legitimate, check value of input vector")
        return

    # log action
    print("Adding " + str(energy_vector) + " as " + str(energy_vector.__len__() + 1) + "-th  node")

    # append zero energy to define as new node
    energy_vector = np.append(energy_vector, 0)

    # add to graph
    graph_matrix = np.row_stack((graph_matrix, energy_vector[0:-1]))
    graph_matrix = np.column_stack((graph_matrix, energy_vector))

    # show result
    ts_problem()

    return


def delete_node(node_nr):
    """
    # delete selected node
    :param node_nr: i-th node to be deleted. This refer to standard index and not python index
    :return: node
    """

    global graph_matrix
    node_nr = node_nr - 1

    # assert if zero energy correct
    try:
        if not (0 <= node_nr < graph_matrix.shape[0] and isinstance(node_nr, int)):
            raise ValueError
    except ValueError:
        print('Node Number: ' + str(node_nr + 1))
        logging.error("New node not legitimate, check node value")
        return

    # log action
    print("Delete " + str(node_nr+1) + "-th node")

    # just delete
    graph_matrix = np.delete(graph_matrix, node_nr, axis=0)
    graph_matrix = np.delete(graph_matrix, node_nr, axis=1)

    # show result
    ts_problem()

    return


def main():
    """
    User interface in CLI implemented here. User input assertion as well
    """

    global graph_matrix

    # matrix representation of graph
    task = input("Insert Action ('calc', 'add', 'del', 'exit'): ")

    # start CLI
    while task != 'exit':
        print('You wrote: ' + task)

        # calculate optimal solution
        if task == 'calc':
            ts_problem()

        # add new node, calculate optimal solution
        elif task == 'add':
            # show current condition
            print('Current graph condition:')
            print(graph_matrix)
            energy_list = []
            # iterate through existing graphs
            for i_node in range(graph_matrix.shape[1]):
                while not (energy_list.__len__() > i_node):
                    # only store energy is value legitimate
                    try:
                        arg = input("Insert energy vector to " + str(i_node+1) + "-th nodes: ")
                        energy_list.append(float(arg))
                    # keep requesting value
                    except ValueError:
                        continue
            # Finally add node to graph
            add_node(energy_list)

        # delete a node, calculate optimal solution
        elif task == 'del':
            # show current condition
            print('Current graph condition:')
            print(graph_matrix)

            # request node to be deleted
            node_arg = -1
            while node_arg == -1:
                # only store node value if integer
                try:
                    arg = input("Insert n-th vector to be deleted, integer equal less than "
                                + str(graph_matrix.shape[1]) + " please: ")
                    # check if integer
                    node_arg = int(arg)
                # keep requesting value
                except ValueError:
                    continue

                # check if node value too large
                try:
                    # check if node value too large
                    if node_arg > graph_matrix.shape[1]:
                        raise ValueError
                # keep requesting value
                except ValueError:
                    node_arg = -1
                    continue

            # apply node deletion
            delete_node(node_arg)

        else:
            print("Wrong command. Please retype command between 'calc', 'add', 'del', 'end': ")

        task = input("Insert Command ('calc', 'add', 'del', 'exit'): ")


if __name__ == "__main__":
    main()
