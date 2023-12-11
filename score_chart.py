import pandas as pd
import matplotlib.pyplot as plt

file_path = "./pre_result.csv"

df = pd.read_csv(file_path)

# Calculate medians and sort the categories based on these medians
sorted_categories = df.groupby("eval")["score"].median().sort_values().index

# Create a boxplot with categories sorted by median
plt.figure(figsize=(10, 6))
plt.boxplot(
    [df[df["eval"] == category]["score"] for category in sorted_categories],
    labels=sorted_categories,
)
plt.xlabel("Evaluation Method")
plt.ylabel("Score")
plt.title("Boxplot of Scores by Evaluation Method (Sorted by Median)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
