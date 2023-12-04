import pandas as pd
import matplotlib.pyplot as plt

file_path = "./result.csv"

# Read the CSV file
df = pd.read_csv(file_path)

# Group by 'eval' and 'agent', then get lists of scores
grouped = df.groupby(["eval", "agent"])["score"].apply(list)

# Calculate the mean score for each 'eval' group and sort
mean_scores = df.groupby("eval")["score"].mean().sort_values()
sorted_evals = mean_scores.index.tolist()

# List of agents
agents = df["agent"].unique()

# Define a color map for the agents
color_map = {agent: plt.cm.tab10(i) for i, agent in enumerate(agents)}

# Recalculate positions for sorted evals
positions_sorted = {}
pos = 1
for eval in sorted_evals:
    positions_sorted[eval] = [pos + i for i in range(len(agents))]
    pos += len(agents) + 1

# Create subplots for each 'eval' in the sorted order
plt.figure(figsize=(12, 8))
for eval_name in sorted_evals:
    for i, agent in enumerate(agents):
        if (eval_name, agent) in grouped:
            scores = grouped[(eval_name, agent)]
            box = plt.boxplot(
                scores,
                positions=[positions_sorted[eval_name][i]],
                widths=0.6,
                patch_artist=True,
                boxprops=dict(facecolor=color_map[agent]),
            )

            for median in box["medians"]:
                median.set_color("red")

# Set plot labels and titles with sorted evals
plt.xticks([sum(pos) / len(pos) for pos in positions_sorted.values()], sorted_evals)
plt.title("Box Plot of Scores by Sorted Evaluation Heuristic and Agent")
plt.xlabel("Evaluation Heuristic (Sorted by Mean Score)")
plt.ylabel("Score")
plt.grid(True)

# Adding legend for agents
patch_list = [
    plt.Line2D([0], [0], color=color_map[agent], label=agent, marker="o", linestyle="")
    for agent in agents
]
plt.legend(handles=patch_list, title="Agents")

plt.show()
