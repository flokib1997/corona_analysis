import pandas as pd
import plotly.express as px


def visualize_gantt_chart(csv_path, columns):
    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Assuming there is a 'date' column in the CSV for the date range
    df['Date'] = pd.to_datetime(df['date'])  # Convert to datetime if not already

    # Prepare the data for Gantt chart
    gantt_data = []

    for column in columns:
        # Filter out rows where the value is 0
        filtered_df = df[df[column] > 0]

        # Calculate Start and End dates based on the 'Date' column
        for index, row in filtered_df.iterrows():
            start_date = row['Date']  # Start date is the date column
            end_date = start_date + pd.Timedelta(days=1)  # End date is one day later

            gantt_data.append({
                'Restriction': column,
                'Start': start_date,
                'End': end_date,
                'Value': row[column]
            })

    # Create a DataFrame for the Gantt chart
    gantt_df = pd.DataFrame(gantt_data)

    # Merge adjacent entries with the same value
    merged_entries = []
    for column in columns:
        temp_df = gantt_df[gantt_df['Restriction'] == column].copy()
        temp_df = temp_df.sort_values('Start')  # Sort by Start date

        # Create a new DataFrame for merged entries
        last_start = None
        last_value = None

        for _, row in temp_df.iterrows():
            if last_value is None:
                last_start = row['Start']
                last_value = row['Value']
                last_end = row['End']
            elif row['Value'] == last_value:
                # Extend the end date for the last entry
                last_end = row['End']
            else:
                # Append new entry
                merged_entries.append({
                    'Restriction': column,
                    'Start': last_start,
                    'End': last_end,
                    'Value': last_value
                })
                last_start = row['Start']
                last_value = row['Value']
                last_end = row['End']

        # Add the last entry if valid
        if last_value is not None:
            merged_entries.append({
                'Restriction': column,
                'Start': last_start,
                'End': last_end,
                'Value': last_value
            })

    # Create a DataFrame for the merged entries
    merged_df = pd.DataFrame(merged_entries)

    # Plotting the Gantt chart with color intensity based on the value
    fig = px.timeline(
        merged_df,
        x_start='Start',
        x_end='End',
        y='Restriction',
        title='Gantt Chart',
        color='Value',  # Color by the 'Value' column
        color_continuous_scale='Blues',  # Choose a color scale
        labels={'Value': 'Measurement Value'}
    )

    # Update layout for transparency, grid, and x-axis tick frequency
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Set plot background to transparent
        paper_bgcolor='rgba(0,0,0,0)',  # Set paper background to transparent
        title_font=dict(size=20),  # Adjust title font size
        xaxis_title='Dates',  # Set x-axis title
        xaxis=dict(
            showgrid=True,
            gridcolor='LightGray',
            dtick='M1',  # Set x-axis ticks to every month
            tickformat='%b %Y'  # Format for the ticks (e.g., 'Jan 2024')
        ),
    )

    # Remove border from entries
    fig.update_traces(marker=dict(line=dict(width=0)))  # Set line width to 0

    fig.show()
