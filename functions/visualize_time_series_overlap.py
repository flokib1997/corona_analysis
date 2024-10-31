import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def visualize_time_series_overlap(file_path, column_names):
    """
    Visualize specified columns over time from a CSV file in a grouped chart.

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

    # Plotting
    plt.figure(figsize=(12, 6))

    # Plot each column in the list
    for column_name in column_names:
        plt.plot(df['date'], df[column_name], linestyle='-', label=column_name)

    # Add title and labels
    plt.title('Time Series Visualization of Selected Columns')
    plt.xlabel('Date')
    plt.ylabel('Values')
    plt.xticks(rotation=45)

    # Set y-ticks to be integers only
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    # Add grid and legend
    plt.grid()
    plt.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()
