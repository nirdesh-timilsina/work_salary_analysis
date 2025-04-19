import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
merged_df = pd.read_csv('./data/megaMergedData.csv')
merged_df.head()
mainScalar = StandardScaler()
stander_columns   = ['total_ear_2018', 'male_ear_2018', 'female_ear_2018', 'total_pop_2018', 'male_pop_2018', 'female_pop_2018', 'total_wor_2018', 'male_wor_2018', 'female_wor_2018']
stander_columns_2 = ['total_ear_2008', 'male_ear_2008', 'female_ear_2008', 'total_pop_2008', 'male_pop_2008', 'female_pop_2008', 'total_wor_2008', 'male_wor_2008', 'female_wor_2008']
stander_columns_3 = ['total_ear_1998', 'male_ear_1998', 'female_ear_1998', 'total_pop_1998', 'male_pop_1998', 'female_pop_1998', 'total_wor_1998', 'male_wor_1998', 'female_wor_1998']

mainScalar = mainScalar.fit(merged_df[stander_columns])
# Standardize stander_columns (2018)
normalized_2018 = pd.DataFrame(
    mainScalar.fit_transform(merged_df[stander_columns]),
    columns=stander_columns
)

# Standardize stander_columns_2 (2008)
normalized_2008 = pd.DataFrame(
    mainScalar.fit_transform(merged_df[stander_columns_2]), 
    columns=stander_columns_2
)

# Standardize stander_columns_3 (1998)
normalized_1998 = pd.DataFrame(
    mainScalar.fit_transform(merged_df[stander_columns_3]), 
    columns=stander_columns_3
)

# Merge back to the original DataFrame
merged_df_scaled = merged_df.copy()
merged_df_scaled[stander_columns] = normalized_2018
merged_df_scaled[stander_columns_2] = normalized_2008
merged_df_scaled[stander_columns_3] = normalized_1998

Occupation = 0  # Row number
years = [ 1998,2008,2018]  # years have flexibility to be choosed any among 3
colors = ["#FF5733", "green", "#3357FF"]  # Different colors for each year
labels = ["Salary", "Population", "Working Hours", "Female Population", "Male Population",
          "Male Salary", "Female Salary", "Female Working Hours", "Male Working Hours"]


# Convert to radians for radar plot
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()

# Create a figure with two subplots (1 row, 2 columns)
fig, axs = plt.subplots(1, 2, figsize=(12, 6), gridspec_kw={'width_ratios': [1, 1]})


ax = fig.add_subplot(121, polar=True)  # Ensure correct polar plot
ax.set_facecolor("#F8F9FA")
for i, year in enumerate(years):
    values = [
        merged_df_scaled[f'total_ear_{year}'][Occupation],
        merged_df_scaled[f'total_pop_{year}'][Occupation],
        merged_df_scaled[f'total_wor_{year}'][Occupation],
        merged_df_scaled[f'female_pop_{year}'][Occupation],
        merged_df_scaled[f'male_pop_{year}'][Occupation],
        merged_df_scaled[f'male_ear_{year}'][Occupation],
        merged_df_scaled[f'female_ear_{year}'][Occupation],
        merged_df_scaled[f'female_wor_{year}'][Occupation],
        merged_df_scaled[f'male_wor_{year}'][Occupation]
    ]

    values += values[:1]  # Close shape
    angle_list = angles + angles[:1]

    ax.plot(angle_list, values, color=colors[i], linewidth=2, label=f'Year {year}')
    ax.fill(angle_list, values, color=colors[i], alpha=0.15)

ax.set_xticks(angles)
ax.set_xticklabels(labels)
ax.set_ylim(-2.5, 2.5)
ax.set_title(f"Occupation: {merged_df_scaled['Occupation'][Occupation]}")
ax.legend(loc="upper right")
ax.set_aspect('equal')  # Ensure circular radar plot

#  Data Table (Right Side)
ax2 = axs[1]
ax2.axis("off")  # Remove axes for a clean table look

# Prepare table data
table_data = []
for i, label in enumerate(labels):
    row = [label] + [
                     merged_df[f'female_pop_{year}'][Occupation] if "Female Population" in label else#this order seriously matters lol
                     merged_df[f'male_pop_{year}'][Occupation] if "Male Population" in label else
                     merged_df[f'male_ear_{year}'][Occupation] if "Male Salary" in label else
                     merged_df[f'female_ear_{year}'][Occupation] if "Female Salary" in label else
                     merged_df[f'female_wor_{year}'][Occupation] if "Female Working Hours" in label else
                     merged_df[f'male_wor_{year}'][Occupation] if "Male Working Hours" in label else 
                     merged_df[f'total_ear_{year}'][Occupation] if "Salary" in label else
                     merged_df[f'total_pop_{year}'][Occupation] if "Population" in label else
                     merged_df[f'total_wor_{year}'][Occupation] if "Working Hours" in label else 0
                     for year in years]
    table_data.append(row)

# Column headers
columns = ["Year"] + [str(year) for year in years]

# Create the table
table = ax2.table(cellText=table_data, colLabels=columns, cellLoc='center', loc='center')

table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width([0, 1, 2, 3])  # Adjust column width

ax2.set_title(f"Data Values for Occupation: {merged_df['Occupation'][Occupation]}", fontsize=12)

#  Adjust Layout and Show Plot
plt.tight_layout()
plt.show()