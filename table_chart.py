import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Function to create a color gradient from green to red
def get_color_gradient(values, reverse=False):
    # Normalize the values to range between 0 and 1
    normalized = (values - np.min(values)) / (np.max(values) - np.min(values))
    if reverse:
        normalized = (
            1 - normalized
        )  # Reverse the gradient for the average evaluation time

    print(normalized)
    # Generate colors (green to red)
    colors = [[0, 1, 0, n] for n in normalized]
    return colors


# Load the data from the provided CSV file
file_path = "./pre_result.csv"
df = pd.read_csv(file_path)

# Calculate the required statistics
stats_df = (
    df.groupby("eval")
    .agg({"score": ["mean", "min", "max"], "ave_time_per_step": "mean"})
    .reset_index()
)

# Convert average evaluation time to milliseconds and round to two decimal places
stats_df["ave_time_per_step"] = (stats_df["ave_time_per_step"] * 1000).round(2)

# Rename columns for clarity
stats_df.columns = [
    "Heuristic",
    "Mean Score",
    "Min Score",
    "Max Score",
    "Average Evaluation Time (ms)",
]

# Sort the DataFrame by 'Mean Score'
stats_df.sort_values(by="Mean Score", ascending=False, inplace=True)

# Create a figure and a subplot
fig, ax = plt.subplots(figsize=(12, 6))

# Hide axes
ax.axis("tight")
ax.axis("off")

# Create cell text array
cell_text = stats_df[
    [
        "Heuristic",
        "Mean Score",
        "Min Score",
        "Max Score",
        "Average Evaluation Time (ms)",
    ]
].values

# Initialize cell color array with white color
cell_colors = [
    ["w" for _ in range(cell_text.shape[1])] for _ in range(cell_text.shape[0])
]

# Apply color gradients to each column
for col_index, col_name in enumerate(["Mean Score", "Min Score", "Max Score"]):
    values = stats_df[col_name]
    colors = get_color_gradient(values)
    for row_index, color in enumerate(colors):
        cell_colors[row_index][
            col_index + 1
        ] = color  # +1 to skip the first column ('Heuristic')

# Apply reversed color gradient for 'Average Evaluation Time (ms)'
values = stats_df["Average Evaluation Time (ms)"]
colors = get_color_gradient(values, reverse=True)
for row_index, color in enumerate(colors):
    cell_colors[row_index][4] = color  # Column index for 'Average Evaluation Time (ms)'

# Create the table with colored cells
table = ax.table(
    cellText=cell_text,
    cellColours=cell_colors,
    colLabels=stats_df.columns[:5],
    loc="center",
)

# Adjust layout to make room for table
plt.subplots_adjust(left=0.2, top=0.8)

# Display the table
plt.show()
