from all_imports import *


def Plot_heatmap_participant_data(participant_data_local, start_date, end_date, column='ws_survey_count', operation='count'):
    """
    Generates a heatmap of participant data based on specified criteria.

    Parameters:
    - participant_data_local: dict
    A dictionary where keys are participant IDs and values are pandas DataFrames containing participant data.

    - start_date: str
    The start date for filtering the data. It should be in the format 'YYYY-MM-DD'.

    - end_date: str
    The end date for filtering the data. It should be in the format 'YYYY-MM-DD'.

    - column: str, optional (default='ws_survey_count')
    The column in the DataFrame to be used for the heatmap. Defaults to 'ws_survey_count'.

    - operation: str, optional (default='count')
    The operation to be performed on the data. It can be one of 'count', 'sum', or 'mean'. Defaults to 'count'. (Mean doenst work yet somehow)

    Returns:
    - A heatmap displaying the specified operation of the data in the given date range, grouped by participant IDs.
    """

    filtered_data = []

    for participant_id, df in participant_data_local.items():
        df['timestamp_lambda'] = pd.to_datetime(df['timestamp_lambda']).dt.tz_localize(None)  # Convert to timezone naive
        
        if operation == 'count':
            df_resampled = df.resample('D', on='timestamp_lambda').count()
        elif operation == 'sum':
            df_resampled = df.resample('D', on='timestamp_lambda').sum()
        elif operation == 'mean':
            df_resampled = df.resample('D', on='timestamp_lambda').mean()
        else:
            raise ValueError("Invalid operation. Choose from 'count', 'sum', or 'mean'.")

        filtered_count = df_resampled.loc[start_date:end_date, column]

        for timestamp, count in filtered_count.items():
            filtered_data.append({'participant_id': participant_id, 'timestamp_lambda': timestamp, column: count})

    df_filtered = pd.DataFrame(filtered_data)
    df_filtered['timestamp_lambda'] = df_filtered['timestamp_lambda'].dt.strftime('%d.%m')
    df_pivoted = df_filtered.pivot(index='participant_id', columns='timestamp_lambda', values=column)

    plt.figure(figsize=(12, 6))
    heatmap = sns.heatmap(df_pivoted, annot=True, cmap='YlGnBu', fmt=".1f", linewidths=5, linecolor='white', 
                        cbar_kws={"shrink": 0.5, "anchor": (1.0, 0.0)}, annot_kws={"size": 8})
    plt.title(f'{operation.capitalize()} of {column}')

    heatmap.set_yticklabels(heatmap.get_yticklabels(), rotation=0)
    heatmap.set_xticklabels(heatmap.get_xticklabels(), rotation=0)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


def Plot_linechart_participant_data(participant_data_local, start_date, end_date, data='ws_survey_count', operation='max'):
    combined_data = pd.DataFrame()

    for key, value in participant_data_local.items():
        # Assuming each value is a DataFrame with 'timestamp_lambda' and 'ws_survey_count' columns
        df = value[['timestamp_lambda', data]].dropna()
        df['timestamp_lambda'] = pd.to_datetime(df['timestamp_lambda'])
        df = df.set_index('timestamp_lambda')


        if operation =='count':
            df = df.resample('D').count()
        elif operation =='max':
            df = df.resample('D').max()
        else:
            raise ValueError("Invalid operation. Choose from 'count', 'max'.")
        # Slice the DataFrame based on the date range
        df = df.loc[start_date:end_date]
        
        # Rename the column to include participant_id and previous column name
        column_name = f"{key}_{data}"  # Modified the column name
        df.rename(columns={data: column_name}, inplace=True)
        
        # Concatenate data to combined_data DataFrame
        combined_data = pd.concat([combined_data, df], axis=1)

    # Plot using plotly express
    fig = px.line(combined_data, x=combined_data.index, y=combined_data.columns,
                title='Combined Data')
    fig.show()





def Plot_plotly_heatmap_participant_data(participant_data_local, start_date, end_date, column='ws_survey_count', operation='count'):
    """
    Generates a heatmap of participant data based on specified criteria.

    Parameters:
    - participant_data_local: dict
    A dictionary where keys are participant IDs and values are pandas DataFrames containing participant data.

    - start_date: str
    The start date for filtering the data. It should be in the format 'YYYY-MM-DD'.

    - end_date: str
    The end date for filtering the data. It should be in the format 'YYYY-MM-DD'.

    - column: str, optional (default='ws_survey_count')
    The column in the DataFrame to be used for the heatmap. Defaults to 'ws_survey_co unt'.

    - operation: str, optional (default='count')
    The operation to be performed on the data. It can be one of 'count', 'sum', or 'mean'. Defaults to 'count'.

    Returns:
    - A Plotly heatmap displaying the specified operation of the data in the given date range, grouped by participant IDs.
    """

    filtered_data = []

    for participant_id, df in participant_data_local.items():
        df['timestamp_lambda'] = pd.to_datetime(df['timestamp_lambda']).dt.tz_localize(None)  # Convert to timezone naive
        
        if operation == 'count':
            df_resampled = df.resample('D', on='timestamp_lambda').count()
        elif operation == 'sum':
            df_resampled = df.resample('D', on='timestamp_lambda').sum()
        elif operation == 'mean':
            df_resampled = df.resample('D', on='timestamp_lambda').mean()
        else:
            raise ValueError("Invalid operation. Choose from 'count', 'sum', or 'mean'.")

        filtered_count = df_resampled.loc[start_date:end_date, column]

        for timestamp, count in filtered_count.items():
            filtered_data.append({'participant_id': participant_id, 'timestamp_lambda': timestamp, column: count})

    df_filtered = pd.DataFrame(filtered_data)
    df_filtered['timestamp_lambda'] = df_filtered['timestamp_lambda'].dt.strftime('%d.%m')
    df_pivoted = df_filtered.pivot(index='participant_id', columns='timestamp_lambda', values=column)

    fig = go.Figure(data=go.Heatmap(
        z=df_pivoted,
        x=df_pivoted.columns,
        y=df_pivoted.index,
        colorscale='YlGnBu',
        hoverongaps = False,
        text=df_pivoted.values,
        hoverinfo='text'))
    
    fig.update_layout(
        title=f'{operation.capitalize()} of {column}',
        xaxis_title='Date',
        yaxis_title='Participant ID',
        yaxis={'autorange': 'reversed'})  # Reverse the y-axis to display participant IDs from top to bottom

    fig.show()
