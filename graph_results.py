import pandas as pd
import matplotlib.pyplot as plt


def calculate_z_values(master_errors, newbie_errors, standard_deviations):
    z_values = (newbie_errors - master_errors) / standard_deviations
    return z_values


def save_z_values_plot(z_values, title, file_path):
    plt.figure(figsize=(10, 6))
    z_values.plot(kind='bar', color='blue')
    plt.xlabel('Markers')
    plt.ylabel('Z-values')
    plt.title(title)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()


def save_top_z_values_plot(z_values, top_n, title, file_path):
    top_z_values = z_values.nlargest(top_n)
    plt.figure(figsize=(10, 6))
    top_z_values.plot(kind='bar', color='red')
    plt.xlabel('Markers')
    plt.ylabel('Z-values')
    plt.title(f'Worst {top_n} {title}')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()


def process_files(master_error_file, newbie_error_file, std_dev_file, all_z_values_file_path, top_z_values_file_path,
                  title):
    # Read the CSV files
    master_errors = pd.read_csv(master_error_file, index_col='Marker')
    newbie_errors = pd.read_csv(newbie_error_file, index_col='Marker')
    standard_deviations = pd.read_csv(std_dev_file, index_col='Marker')

    # Calculate Z-values
    z_values = calculate_z_values(master_errors['MeanError'], newbie_errors['MeanError'],
                                  standard_deviations['Standard Deviation'])

    # Save the Z-values plot
    save_z_values_plot(z_values, title, all_z_values_file_path)

    # Save the top 10 Z-values plot
    save_top_z_values_plot(z_values, 10, title, top_z_values_file_path)


# Example usage
master_error_file_path = 'Graphs/Tsuki/Master_Master/marker_mean_error.csv'
newbie_error_file_path = 'Graphs/Tsuki/Master_Wojtek/marker_mean_error.csv'
std_dev_file_path = 'Graphs/Tsuki/Master_Master/marker_std_devs.csv'
title = 'Tsuki Z-values for Wojtek vs Master'
all_z_values_file_path = 'Graphs/Tsuki/Master_Wojtek/Woj-tsuki-all_z_values_plot.png'
top_z_values_file_path = 'Graphs/Tsuki/Master_Wojtek/Woj-tsuki-worst_10_z_values_plot.png'

process_files(master_error_file_path, newbie_error_file_path, std_dev_file_path, all_z_values_file_path, top_z_values_file_path, title)