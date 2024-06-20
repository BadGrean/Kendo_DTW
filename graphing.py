import matplotlib.pyplot as plt
import numpy as np
import os

def plot_three_graphs(list1, list2, indexes_list1, indexes_list2, title, filepath):
    """
    Plot three graphs in one figure and save to a file.

    Parameters:
    - list1: List of size n of lists of size 3 containing float type values (first dataset)
    - list2: List of size m of lists of size 3 containing float type values (second dataset)
    - indexes_list1: List of size n containing indices corresponding to list1
    - indexes_list2: List of size m containing indices corresponding to list2
    - title: Title for the plots
    - filepath: Path to save the plot file
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    try:
        indexes_list1 = extract_keys_as_ints(indexes_list1)
        indexes_list2 = extract_keys_as_ints(indexes_list2)
        Frames = True
    except:
        Frames = False

    n = len(list1[0])  # Assuming inner lists in list1 have the same length
    m = len(list2[0])  # Assuming inner lists in list2 have the same length

    # Create a figure with three subplots (3 rows, 1 column)
    fig, axes = plt.subplots(3, 1, figsize=(10, 15))  # Adjust figsize as needed

    # Plot the first graph
    axes[0].plot(indexes_list1, [list1[j][0] for j in range(len(list1))], marker='o', label='Master line')
    axes[0].plot(indexes_list2, [list2[j][0] for j in range(len(list2))], marker='o', label='Newbie line')
    axes[0].set_title('X-axis trajectory')
    if Frames:
        axes[0].set_xlabel('Frame')
    else:
        axes[0].set_xlabel('Time[s]')
    axes[0].set_ylabel('X-axis Value')
    axes[0].legend()

    # Plot the second graph
    axes[1].plot(indexes_list1, [list1[j][1] for j in range(len(list1))], marker='o', label='Master line')
    axes[1].plot(indexes_list2, [list2[j][1] for j in range(len(list2))], marker='o', label='Newbie line')
    axes[1].set_title('Y-axis trajectory')
    if Frames:
        axes[1].set_xlabel('Frame')
    else:
        axes[1].set_xlabel('Time[s]')
    axes[1].set_ylabel('Y-axis Value')
    axes[1].legend()

    # Plot the third graph
    axes[2].plot(indexes_list1, [list1[j][2] for j in range(len(list1))], marker='o', label='Master line')
    axes[2].plot(indexes_list2, [list2[j][2] for j in range(len(list2))], marker='o', label='Newbie line')
    axes[2].set_title('Z-axis trajectory')
    if Frames:
        axes[2].set_xlabel('Frame')
    else:
        axes[2].set_xlabel('Time[s]')
    axes[2].set_ylabel('Z-axis Value')
    axes[2].legend()

    fig.suptitle(title)

    # Adjust layout and save plot
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust rect to make room for suptitle
    plt.savefig(filepath)
    plt.close()

def extract_keys_as_ints(d):
    int_keys = []
    for key in d.keys():
        int_key = int(key)  # Convert key from string to int
        int_keys.append(int_key)
    return int_keys

def plot_alignment_graphs(name_coordinates_dict_master, name_coordinates_dict, path_x, path_y, path_z, Title, filepath):
    """
    Plot alignment graphs for X, Y, and Z-axis values and save to a file.

    Parameters:
    - name_coordinates_dict_master: Dictionary containing master coordinates
    - name_coordinates_dict: Dictionary containing newbie coordinates
    - path_x: Optimal path for X-axis from dynamic programming
    - path_y: Optimal path for Y-axis from dynamic programming
    - path_z: Optimal path for Z-axis from dynamic programming
    - Title: Title for the plots
    - filepath: Path to save the plot file
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    fig, axes = plt.subplots(3, 1, figsize=(10, 15))  # Create a figure with three subplots (3 rows, 1 column)

    # Plot the alignment graph for X-axis values
    for x_i, y_j in path_x:
        axes[0].plot([x_i, y_j],
                     [name_coordinates_dict_master[Title][x_i][0] + 1.5, name_coordinates_dict[Title][y_j][0] - 1.5],
                     c="C7")
    axes[0].plot(np.arange(name_coordinates_dict_master[Title].shape[0]),
                 name_coordinates_dict_master[Title][:, 0] + 1.5, "-o", c="C3")
    axes[0].plot(np.arange(name_coordinates_dict[Title].shape[0]), name_coordinates_dict[Title][:, 0] - 1.5, "-o",
                 c="C0")
    axes[0].set_title('Alignment - X-axis')
    axes[0].axis("off")

    # Plot the alignment graph for Y-axis values
    for x_i, y_j in path_y:
        axes[1].plot([x_i, y_j],
                     [name_coordinates_dict_master[Title][x_i][1] + 1.5, name_coordinates_dict[Title][y_j][1] - 1.5],
                     c="C7")
    axes[1].plot(np.arange(name_coordinates_dict_master[Title].shape[0]),
                 name_coordinates_dict_master[Title][:, 1] + 1.5, "-o", c="C3")
    axes[1].plot(np.arange(name_coordinates_dict[Title].shape[0]), name_coordinates_dict[Title][:, 1] - 1.5, "-o",
                 c="C0")
    axes[1].set_title('Alignment - Y-axis')
    axes[1].axis("off")

    # Plot the alignment graph for Z-axis values
    for x_i, y_j in path_z:
        axes[2].plot([x_i, y_j],
                     [name_coordinates_dict_master[Title][x_i][2] + 1.5, name_coordinates_dict[Title][y_j][2] - 1.5],
                     c="C7")
    axes[2].plot(np.arange(name_coordinates_dict_master[Title].shape[0]),
                 name_coordinates_dict_master[Title][:, 2] + 1.5, "-o", c="C3")
    axes[2].plot(np.arange(name_coordinates_dict[Title].shape[0]), name_coordinates_dict[Title][:, 2] - 1.5, "-o",
                 c="C0")
    axes[2].set_title('Alignment - Z-axis')
    axes[2].axis("off")

    fig.suptitle(f'Alignment Graphs for {Title}')
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust rect to make room for suptitle
    plt.savefig(filepath)
    plt.close()