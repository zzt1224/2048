import pandas as pd
import matplotlib.pyplot as plt

file_path = "./result.csv"

# Read the CSV file
df = pd.read_csv(file_path)

# Get unique values for 'depth', 'eval', and 'agent'
depths = sorted(df["depth"].unique())
agents = df["agent"].unique()

# Define a color map for agents
color_map = {agent: plt.cm.tab10(i) for i, agent in enumerate(agents)}

# Create a figure with subplots (facets) arranged vertically
fig, axes = plt.subplots(
    len(depths), 1, figsize=(10, 6 * len(depths)), constrained_layout=True
)

# If only one depth, we still want a list of axes to iterate over
if len(depths) == 1:
    axes = [axes]

# Create box plots for each depth
for ax, depth in zip(axes, depths):
    # For each depth, sort evals by mean score
    sorted_evals = (
        df[df["depth"] == depth].groupby("eval")["score"].mean().sort_values().index
    )

    # Prepare the data for plotting by agent
    positions = []
    data = []
    labels = []
    for i, eval_name in enumerate(sorted_evals):
        for j, agent in enumerate(agents):
            # Extract scores for the current eval and agent
            scores = df[
                (df["depth"] == depth)
                & (df["eval"] == eval_name)
                & (df["agent"] == agent)
            ]["score"].tolist()
            if scores:  # Only add if there are scores for this agent and eval
                data.append(scores)
                positions.append(
                    i * (len(agents) + 1) + j
                )  # Offset positions for each agent
                labels.append(f"{eval_name}\n{agent}")

    # Create the boxplot
    box = ax.boxplot(data, positions=positions, widths=0.6, patch_artist=True)

    # Color each box by agent
    for patch, agent in zip(
        box["boxes"], [agent for eval in sorted_evals for agent in agents]
    ):
        patch.set_facecolor(color_map[agent])

    # Set the axis titles and labels
    ax.set_title(f"Depth {depth}")
    ax.set_xticks(
        [
            pos
            for i, _ in enumerate(sorted_evals)
            for pos in [i * (len(agents) + 1) + (len(agents) - 1) / 2]
        ]
    )
    ax.set_xticklabels(sorted_evals)
    ax.grid(True)

# Add a legend for the agents
legend_patches = [
    plt.Line2D([0], [0], color=color_map[agent], label=agent, marker="s", linestyle="")
    for agent in agents
]
fig.legend(handles=legend_patches, loc="upper right", title="Agents")

# Set common labels and titles
fig.suptitle(
    "Box Plot of Scores by Evaluation Heuristic, Agent, and Depth", fontsize=16
)
axes[0].set_ylabel("Score")

plt.show()
