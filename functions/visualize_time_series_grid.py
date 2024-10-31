import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def visualize_time_series_grid(file_path, column_names):
    """
    Visualize specified columns over time from a CSV file in separate subplots with a maximum of 2 charts per row.

    Parameters:
    file_path (str): Path to the CSV file containing 'date' and specified columns.
    column_names (list of str): List of column names to visualize against the date.
    """
    # Load the data from the CSV file
    df = pd.read_csv(file_path)

    # Ensure the date column is in datetime format
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Sort the DataFrame by date
    df.sort_values('date', inplace=True)

    # Check if all specified columns exist in the DataFrame
    for column_name in column_names:
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found in the CSV file.")

    # Number of subplots needed
    n = len(column_names)
    cols = 2  # Fixed number of columns in the grid
    rows = (n + cols - 1) // cols  # Calculate number of rows needed

    # Create subplots
    fig, axes = plt.subplots(rows, cols, figsize=(12, 4 * rows))
    axes = axes.flatten()  # Flatten to easily index the axes

    # Plot each column in its own subplot
    for i, column_name in enumerate(column_names):
        axes[i].plot(df['date'], df[column_name], linestyle='-', color='b')
        axes[i].set_title(column_name)
        axes[i].set_xlabel('Date')
        axes[i].set_ylabel('Values')
        axes[i].grid()
        axes[i].tick_params(axis='x', rotation=45)  # Rotate x-axis labels

        # Set y-ticks to be integers only
        axes[i].yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Hide unused subplots
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    plt.tight_layout()
    plt.show()
