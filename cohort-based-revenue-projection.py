import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_ltv_revenue_projection(cumulative_revenue_curve, acquisition_days, users_per_day, cpi):
    """
    Calculates the LTV expected revenue model and projects revenue based on the provided article.

    Args:
        cumulative_revenue_curve (dict): A dictionary representing the cumulative revenue curve.
                                         Keys are days (integers), values are cumulative revenue per user (floats).
                                         e.g., {20: 0.67, 90: 1.00, 180: 1.15}
        acquisition_days (int): Number of days of user acquisition.
        users_per_day (int): Number of users acquired per day.
        cpi (float): Cost per install/user acquisition.

    Returns:
        pandas.DataFrame: DataFrame containing daily revenue, cost, profit/loss, and cumulative values.
    """

    # 1. Create a Pandas Series for the cumulative revenue curve, indexed by day
    cumulative_revenue_series = pd.Series(cumulative_revenue_curve)
    max_day_curve = cumulative_revenue_series.index.max()

    # 2. Calculate Daily Revenue Contribution (incremental revenue per day)
    daily_revenue_contribution = cumulative_revenue_series.diff().fillna(cumulative_revenue_series.iloc[0])
    daily_revenue_contribution.name = 'daily_revenue_per_user'

    # 3. Create a DataFrame to represent cohorts
    cohort_days = range(acquisition_days)
    cohort_data = []
    for day in cohort_days:
        cohort_data.append({'cohort_day': day, 'users': users_per_day})
    cohort_df = pd.DataFrame(cohort_data)
    cohort_df['acquisition_cost'] = cohort_df['users'] * cpi

    # 4. Initialize revenue columns efficiently
    max_projection_days = max_day_curve # Project revenue up to the maximum day in the curve
    revenue_columns = [f'day_{d}' for d in range(max_projection_days + 1)]
    revenue_df = pd.DataFrame(0.0, index=cohort_df.index, columns=revenue_columns) # Create DataFrame with all revenue columns initialized to 0
    cohort_df = pd.concat([cohort_df, revenue_df], axis=1) # Concatenate to cohort_df

    # 5. Project Daily Revenue for each cohort over the LTV curve duration
    for index, cohort in cohort_df.iterrows():
        for day in range(max_projection_days + 1):
            cohort_age = day # Cohort age is the same as the day number in this daily projection
            if cohort_age in daily_revenue_contribution.index:
                cohort_df.loc[index, f'day_{day}'] = daily_revenue_contribution.get(cohort_age, 0) * cohort['users']

    # 6. Calculate Total Daily Revenue by summing revenue from all cohorts for each day
    daily_revenue_df = pd.DataFrame(index=range(max_projection_days + 1))
    for day in range(max_projection_days + 1):
        day_column_name = f'day_{day}'
        daily_revenue_df.loc[day, 'daily_revenue'] = cohort_df[day_column_name].sum()

    # 7. Calculate Daily Cost
    daily_revenue_df['daily_cost'] = 0.0
    daily_revenue_df.loc[cohort_days, 'daily_cost'] = users_per_day * cpi # Cost incurred only during acquisition days

    # 8. Calculate Daily Profit/Loss
    daily_revenue_df['daily_profit'] = daily_revenue_df['daily_revenue'] - daily_revenue_df['daily_cost']

    # 9. Calculate Cumulative Revenue, Cost, and Profit/Loss
    daily_revenue_df['cumulative_revenue'] = daily_revenue_df['daily_revenue'].cumsum()
    daily_revenue_df['cumulative_cost'] = daily_revenue_df['daily_cost'].cumsum()
    daily_revenue_df['cumulative_profit'] = daily_revenue_df['cumulative_profit'] = daily_revenue_df['cumulative_revenue'] - daily_revenue_df['cumulative_cost']

    # 10. Calculate Cumulative Users
    daily_revenue_df['daily_users_acquired'] = 0
    daily_revenue_df.loc[cohort_days, 'daily_users_acquired'] = users_per_day
    daily_revenue_df['cumulative_users'] = daily_revenue_df['daily_users_acquired'].cumsum()

    return daily_revenue_df

# Example Usage based on the article:
cumulative_revenue_curve_90day = {
    1: 0.05,
    2: 0.15,
    3: 0.25,
    4: 0.33,
    5: 0.40,
    6: 0.46,
    7: 0.51,
    8: 0.55,
    9: 0.58,
    10: 0.60,
    20: 0.67,
    30: 0.75,
    40: 0.81,
    50: 0.86,
    60: 0.90,
    70: 0.94,
    80: 0.97,
    90: 1.00
}

# Extend the curve to 180 days as mentioned in the article
cumulative_revenue_curve_180day = cumulative_revenue_curve_90day.copy()
cumulative_revenue_curve_180day[180] = 1.15

acquisition_days = 20
users_per_day = 1000
cpi = 1.0

# Calculate for 180-day LTV
revenue_projection_180day = calculate_ltv_revenue_projection(
    cumulative_revenue_curve=cumulative_revenue_curve_180day,
    acquisition_days=acquisition_days,
    users_per_day=users_per_day,
    cpi=cpi
)

# --- Plotting the graph with secondary axis ---
plt.figure(figsize=(12, 6))
ax1 = plt.gca() # Get current axes
ax2 = ax1.twinx() # Create a twin Axes sharing the x-axis

days = revenue_projection_180day.index

# Plot financial data on the primary axis (ax1)
line1, = ax1.plot(days, revenue_projection_180day['cumulative_cost'], label='Cumulative Spend', color='red')
line2, = ax1.plot(days, revenue_projection_180day['cumulative_revenue'], label='Cumulative Revenue', color='blue')
line3, = ax1.plot(days, revenue_projection_180day['cumulative_profit'], label='Cumulative Profit', color='green')

# Plot user data on the secondary axis (ax2)
line4, = ax2.plot(days, revenue_projection_180day['cumulative_users'], label='Cumulative Users', color='purple', linestyle='--')

ax1.set_xlabel('Days')
ax1.set_ylabel('Value ($)', color='black') # Label for primary axis (financial values)
ax2.set_ylabel('Users', color='purple') # Label for secondary axis (users)
plt.title('LTV Revenue Projection & User Growth (Secondary Axis for Users)')

# Create a combined legend for both axes
lines = [line1, line2, line3, line4]
labels = [l.get_label() for l in lines]
plt.legend(lines, labels, loc='upper left') # Adjust location if needed

ax1.grid(True)
plt.tight_layout()
plt.show()