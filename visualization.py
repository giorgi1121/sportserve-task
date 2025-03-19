import matplotlib.pyplot as plt


def visualize_groups(strong_groups, weak_groups):
    """
    Visualize the number and size of strong vs. weak groups.

    Parameters:
        strong_groups (list): List of strong groups (each a list of user IDs).
        weak_groups (list): List of weak groups (each a list of user IDs).
    """
    # Compare total number of strong groups vs. weak groups
    num_strong_groups = len(strong_groups)
    num_weak_groups = len(weak_groups)

    plt.figure(figsize=(8, 6))
    plt.bar(
        ["Strong Groups", "Weak Groups"],
        [num_strong_groups, num_weak_groups],
        color=["lightcoral", "lightblue"],
    )
    plt.xlabel("Group Type")
    plt.ylabel("Number of Groups")
    plt.title("Count of Strong vs. Weak Groups")
    plt.savefig("group_count.png")
    plt.close()

    # Show distribution of group sizes for strong and weak groups
    strong_sizes = [len(grp) for grp in strong_groups]
    weak_sizes = [len(grp) for grp in weak_groups]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Bar chart for Strong group sizes
    axes[0].bar(range(1, len(strong_sizes) + 1), strong_sizes, color="lightcoral")
    axes[0].set_title("Strong Group Sizes")
    axes[0].set_xlabel("Group Number")
    axes[0].set_ylabel("Number of Users")

    # Bar chart for Weak group sizes
    axes[1].bar(range(1, len(weak_sizes) + 1), weak_sizes, color="lightblue")
    axes[1].set_title("Weak Group Sizes")
    axes[1].set_xlabel("Group Number")
    axes[1].set_ylabel("Number of Users")

    plt.tight_layout()
    plt.savefig("group_sizes.png")
    plt.close()


def visualize_common_properties(common_props):
    """
    Visualizes the most common property values with their counts.

    Parameters:
        common_props (dict): A dictionary where each key is a property name and
                             the value is a tuple (most_common_value, count).
    """
    properties = list(common_props.keys())
    counts = [item[1] for item in common_props.values()]
    # Prepare labels showing the most common value for each property
    labels = [str(item[0]) for item in common_props.values()]

    plt.figure(figsize=(12, 7))
    bars = plt.bar(properties, counts, color="skyblue")
    plt.xlabel("Property")
    plt.ylabel("Count")
    plt.title("Most Common Values per Property")

    # Annotate each bar with the most common value
    for bar, label in zip(bars, labels):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.5,
            label,
            ha="center",
            va="bottom",
            fontsize=8,
        )

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("most_common_properties.png")
    plt.close()
