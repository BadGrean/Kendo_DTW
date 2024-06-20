import numpy as np
import os
import csv
import graphing
import matplotlib.pyplot as plt

def dp(dist_mat):

    N, M = dist_mat.shape

    # Initialize the cost matrix
    cost_mat = np.zeros((N + 1, M + 1))
    for i in range(1, N + 1):
        cost_mat[i, 0] = np.inf
    for i in range(1, M + 1):
        cost_mat[0, i] = np.inf

    # Fill the cost matrix while keeping traceback information
    traceback_mat = np.zeros((N, M))
    for i in range(N):
        for j in range(M):
            penalty = [
                cost_mat[i, j],  # match (0)
                cost_mat[i, j + 1],  # insertion (1)
                cost_mat[i + 1, j]]  # deletion (2)
            i_penalty = np.argmin(penalty)
            cost_mat[i + 1, j + 1] = dist_mat[i, j] + penalty[i_penalty]
            traceback_mat[i, j] = i_penalty

    # Traceback from bottom right
    i = N - 1
    j = M - 1
    path = [(i, j)]
    while i > 0 or j > 0:
        tb_type = traceback_mat[i, j]
        if tb_type == 0:
            # Match
            i = i - 1
            j = j - 1
        elif tb_type == 1:
            # Insertion
            i = i - 1
        elif tb_type == 2:
            # Deletion
            j = j - 1
        path.append((i, j))

    # Strip infinity edges from cost_mat before returning
    cost_mat = cost_mat[1:, 1:]
    return (path[::-1], cost_mat)


def prepare_csvs():
    # Hard-coded folder path
    folder_path = '/path/to/your/folder'

    # List to store results of operations on files
    results = []

    # Check if the specified path exists
    if not os.path.exists(folder_path):
        print(f"The folder path {folder_path} does not exist.")
        return results

    # Walk through all files in the specified folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)


            results.append(file_path)

    return results


def csv_parser(file_path):
    # Check if the file exists
    frame_time_dict = {}
    name_coordinates_dict = {}

    if not os.path.isfile(file_path):
        print(f"The file {file_path} does not exist.")
        return

    # Open the CSV file and read its contents
    with open(file_path, mode='r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = list(csv_reader)  # Read all rows into memory

    # Check if the CSV file has at least 7 rows
    if len(rows) < 7:
        print(f"The file {file_path} does not contain enough rows.")
        return

    # Identify columns to keep based on the sixth row (index 5)
    columns_to_keep = [0, 1]  # Keep first two columns initially
    for i, value in enumerate(rows[5]):
        if value.strip() == "Position":
            columns_to_keep.append(i)

    # Remove first two columns and any column not marked "Position"
    filtered_rows = []
    counter = 0
    for row in rows:
        if counter < 2:
            counter += 1
            continue
        filtered_row = []
        for i in columns_to_keep:
            filtered_row.append(row[i])
        #filtered_row = [row[i] for i in columns_to_keep if i < len(row)]
        filtered_rows.append(filtered_row)

    # Process the filtered data for frame_time_dict
    for row in filtered_rows[5:]:  # Skip first 7 rows
        #if len(row) < 2:
        #    continue  # Skip rows that do not have at least 2 columns
        frame = int(row[0])  # First column is the frame (key)
        time = float(row[1])  # Second column is the time (value)
        frame_time_dict[frame] = time

    for row in filtered_rows[1:2]:
        for i in range(2, len(row)):
            if row[i] not in name_coordinates_dict:
                 name_coordinates_dict[row[i].rsplit(":", 1)[len(row[i].rsplit(":", 1))-1]] = []

    for row in filtered_rows[5:]:
        triplet = []
        for i in range(2, len(row)):
            if i % 3 == 2:
                triplet.append(float(row[i]))# append x
            if i % 3 == 0:
                triplet.append(float(row[i]))# append y
            if i % 3 == 1:
                triplet.append(float(row[i]))# append z
                name_coordinates_dict[filtered_rows[1][i].rsplit(":", 1)[len(filtered_rows[1][i].rsplit(":", 1))-1]].append(triplet)
                triplet = []


    return frame_time_dict, name_coordinates_dict
# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    for k in range(4):
        for l in range(4):
            # if k >= l:
            #     continue

            frame_time_dict, name_coordinates_dict = csv_parser(
                f"..Wojtek_NORMALIZACJA/NORMALIZACJA_Wojtek_Tsuki/Wojtek_Tsuki2_00{l}_NORMALIZACJA.csv")
            frame_time_dict_master, name_coordinates_dict_master = csv_parser(
                f"..Master_NORMALIZACJA/NORMALIZACJA_Master_Tsuki/Master_Tsuki_00{k}_NORMALIZACJA.csv")

    #frame_time_dict, name_coordinates_dict = csv_parser("Wojtek_NORMALIZACJA/NORMALIZACJA_Wojtek_Tsuki/Wojtek_Tsuki2_003_NORMALIZACJA.csv")
    errors_dict = {}

    for k in range(4):
        for l in range(4):
            # if k >= l:
            #     continue

            frame_time_dict, name_coordinates_dict = csv_parser(
                f"..Wojtek_NORMALIZACJA/NORMALIZACJA_Wojtek_Tsuki/Wojtek_Tsuki2_00{l}_NORMALIZACJA.csv")
            frame_time_dict_master, name_coordinates_dict_master = csv_parser(
                f"..Master_NORMALIZACJA/NORMALIZACJA_Master_Tsuki/Master_Tsuki_00{k}_NORMALIZACJA.csv")

            move_error_dict = {}

            for Title in name_coordinates_dict_master.keys():


                # Convert the lists to numpy arrays
                name_coordinates_dict_master[Title] = np.array(name_coordinates_dict_master[Title])
                name_coordinates_dict[Title] = np.array(name_coordinates_dict[Title])

                N = name_coordinates_dict_master[Title].shape[0]
                M = name_coordinates_dict[Title].shape[0]
                dist_mat_x = np.zeros((N, M))
                dist_mat_y = np.zeros((N, M))
                dist_mat_z = np.zeros((N, M))

                for i in range(N):
                    for j in range(M):
                        dist_mat_x[i, j] = abs(
                            name_coordinates_dict_master[Title][i][0] - name_coordinates_dict[Title][j][0])
                        dist_mat_y[i, j] = abs(
                            name_coordinates_dict_master[Title][i][1] - name_coordinates_dict[Title][j][1])
                        dist_mat_z[i, j] = abs(
                            name_coordinates_dict_master[Title][i][2] - name_coordinates_dict[Title][j][2])

                path_x, cost_mat_x = dp(dist_mat_x)
                path_y, cost_mat_y = dp(dist_mat_y)
                path_z, cost_mat_z = dp(dist_mat_z)

                # if Title == "Marker2":
                #     plt.figure(figsize=(6, 4))
                #     plt.imshow(cost_mat_x, cmap=plt.cm.binary, interpolation="nearest", origin="lower")
                #     x_path, y_path = zip(*path_x)
                #     plt.plot(y_path, x_path)
                #     plt.xlabel("$j$")
                #     plt.ylabel("$i$");

                graphing.plot_alignment_graphs(name_coordinates_dict_master, name_coordinates_dict, path_x, path_y,
                                               path_z, Title, f"Graphs/Tsuki/Master_Wojtek/Alignment_graphs/Master{k}-Wojtek{l}/_Align_{Title}")

                # Plot the three graphs with the provided function
                graphing.plot_three_graphs(name_coordinates_dict_master[Title], name_coordinates_dict[Title],
                                           frame_time_dict_master.values(), frame_time_dict.values(), Title,f"Graphs/Tsuki/Master_Wojtek/Marker_data_graphs/Master{k}-Wojtek{l}/_Marker_{Title}")

                single_marker_error = ((cost_mat_x[N - 1, M - 1] / (N + M)) + (cost_mat_y[N - 1, M - 1] / (N + M)) + (
                            cost_mat_z[N - 1, M - 1] / (N + M))) / 3

                move_error_dict[Title] = single_marker_error

                print(f"Processing {Title} for Master file {k} and Newbie file {l}")
                print("Alignment cost_x: {:.4f}".format(cost_mat_x[N - 1, M - 1]))
                print("Normalized alignment cost_x: {:.4f}".format(cost_mat_x[N - 1, M - 1] / (N + M)))
                print("Alignment cost_y: {:.4f}".format(cost_mat_y[N - 1, M - 1]))
                print("Normalized alignment cost_y: {:.4f}".format(cost_mat_y[N - 1, M - 1] / (N + M)))
                print("Alignment cost_z: {:.4f}".format(cost_mat_z[N - 1, M - 1]))
                print("Normalized alignment cost_z: {:.4f}".format(cost_mat_z[N - 1, M - 1] / (N + M)))

            # Store the move_error_dict in the errors_dict with the key as M{k}-N{l}
            errors_dict[f"M{k}-N{l}"] = move_error_dict

    marker_errors = {}
    for key, move_error_dict in errors_dict.items():
        for marker, error in move_error_dict.items():
            if marker not in marker_errors:
                marker_errors[marker] = []
            marker_errors[marker].append(error)

    # Calculate standard deviation for each marker
    # marker_std_devs = {}
    # for key in marker_errors.keys():
    #     marker_std_devs[key] = np.std(marker_errors[key])




    # with open("Graphs/DoUchi/Master_Master/marker_std_devs.csv", 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(['Marker', 'Standard Deviation'])
    #     for marker, std_dev in marker_std_devs.items():
    #         writer.writerow([marker, std_dev])

    with open("Graphs/Tsuki/Master_Wojtek/marker_mean_error.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Marker', 'MeanError'])
        for marker, errors in marker_errors.items():
            writer.writerow([marker, np.mean(errors)])
    # Use the function from graphing.py to plot the graphs
    #graphing.plot_alignment_graphs(name_coordinates_dict_master, name_coordinates_dict, path_x, path_y, path_z, Title)

    # Plot the three graphs with the provided function
    #graphing.plot_three_graphs(name_coordinates_dict_master[Title], name_coordinates_dict[Title],
    #                           frame_time_dict_master.values(), frame_time_dict.values(), Title,)
    # graphing.plot_three_graphs(name_coordinates_dict_master[Title], name_coordinates_dict[Title],
    #                            frame_time_dict_master, frame_time_dict, Title)
    print("0")



