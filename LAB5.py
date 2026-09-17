import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Play Tennis Dataset
data = [
    ['Sunny', 'Hot', 'High', 'Weak', 'No'],
    ['Sunny', 'Hot', 'High', 'Strong', 'No'],
    ['Overcast', 'Hot', 'High', 'Weak', 'Yes'],
    ['Rain', 'Mild', 'High', 'Weak', 'Yes'],
    ['Rain', 'Cool', 'Normal', 'Weak', 'Yes'],
    ['Rain', 'Cool', 'Normal', 'Strong', 'No'],
    ['Overcast', 'Cool', 'Normal', 'Strong', 'Yes'],
    ['Sunny', 'Mild', 'High', 'Weak', 'No'],
    ['Sunny', 'Cool', 'Normal', 'Weak', 'Yes'],
    ['Rain', 'Mild', 'Normal', 'Weak', 'Yes'],
    ['Sunny', 'Mild', 'Normal', 'Strong', 'Yes'],
    ['Overcast', 'Mild', 'High', 'Strong', 'Yes'],
    ['Overcast', 'Hot', 'Normal', 'Weak', 'Yes'],
    ['Rain', 'Mild', 'High', 'Strong', 'No']
]

attributes = ['Outlook', 'Temperature', 'Humidity', 'Wind']


# Entropy
def entropy(rows):
    yes = sum(row[4] == 'Yes' for row in rows)
    no = sum(row[4] == 'No' for row in rows)
    total = len(rows)

    result = 0

    if yes > 0:
        p = yes / total
        result -= p * math.log2(p)

    if no > 0:
        p = no / total
        result -= p * math.log2(p)

    return result


# Information Gain
def information_gain(rows, column):
    total_entropy = entropy(rows)

    values = set(row[column] for row in rows)
    weighted_entropy = 0

    for value in values:
        subset = [row for row in rows if row[column] == value]

        weighted_entropy += (
            len(subset) / len(rows)
        ) * entropy(subset)

    return total_entropy - weighted_entropy


# Majority class
def majority_class(rows):
    yes = sum(row[4] == 'Yes' for row in rows)
    no = sum(row[4] == 'No' for row in rows)

    return 'Yes' if yes >= no else 'No'


# ID3 Algorithm
def id3(rows, columns):

    targets = [row[4] for row in rows]

    if all(target == 'Yes' for target in targets):
        return 'Yes'

    if all(target == 'No' for target in targets):
        return 'No'

    if len(columns) == 0:
        return majority_class(rows)

    gains = {}

    for column in columns:
        gains[column] = information_gain(rows, column)

    best_column = max(gains, key=gains.get)
    best_attribute = attributes[best_column]

    tree = {best_attribute: {}}

    remaining_columns = [
        column for column in columns
        if column != best_column
    ]

    values = set(row[best_column] for row in rows)

    for value in values:

        subset = [
            row for row in rows
            if row[best_column] == value
        ]

        tree[best_attribute][value] = id3(
            subset,
            remaining_columns
        )

    return tree


# Draw Decision Tree
def draw_tree(tree):

    fig, ax = plt.subplots(figsize=(12, 7))

    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')

    # Nodes
    nodes = {
        'Outlook': (6, 7),
        'Sunny': (2, 5.5),
        'Overcast': (6, 5.5),
        'Rain': (10, 5.5),

        'Humidity': (2, 4),
        'Yes1': (6, 4),

        'Wind': (10, 4),

        'High': (1, 2.5),
        'Normal': (3, 2.5),

        'Weak': (9, 2.5),
        'Strong': (11, 2.5),

        'No1': (1, 1),
        'Yes2': (3, 1),
        'Yes3': (9, 1),
        'No2': (11, 1)
    }

    # Draw connecting lines
    connections = [
        ('Outlook', 'Sunny', 'Sunny'),
        ('Outlook', 'Overcast', 'Overcast'),
        ('Outlook', 'Rain', 'Rain'),

        ('Sunny', 'Humidity', ''),

        ('Overcast', 'Yes1', ''),

        ('Rain', 'Wind', ''),

        ('Humidity', 'High', 'High'),
        ('Humidity', 'Normal', 'Normal'),

        ('Wind', 'Weak', 'Weak'),
        ('Wind', 'Strong', 'Strong'),

        ('High', 'No1', ''),
        ('Normal', 'Yes2', ''),

        ('Weak', 'Yes3', ''),
        ('Strong', 'No2', '')
    ]

    for start, end, label in connections:

        x1, y1 = nodes[start]
        x2, y2 = nodes[end]

        ax.plot(
            [x1, x2],
            [y1, y2],
            linewidth=1.5
        )

        if label:
            x = (x1 + x2) / 2
            y = (y1 + y2) / 2

            ax.text(
                x,
                y + 0.15,
                label,
                ha='center',
                fontsize=11
            )

    # Decision nodes
    decision_nodes = [
        ('Outlook', 6, 7),
        ('Humidity', 2, 4),
        ('Wind', 10, 4)
    ]

    for text, x, y in decision_nodes:
        ax.text(
            x,
            y,
            text,
            ha='center',
            va='center',
            fontsize=14,
            fontweight='bold',
            bbox=dict(
                boxstyle='round,pad=0.5',
                edgecolor='black',
                facecolor='lightblue'
            )
        )

    # Branch nodes
    branch_nodes = [
        ('Sunny', 2, 5.5),
        ('Overcast', 6, 5.5),
        ('Rain', 10, 5.5),
        ('High', 1, 2.5),
        ('Normal', 3, 2.5),
        ('Weak', 9, 2.5),
        ('Strong', 11, 2.5)
    ]

    for text, x, y in branch_nodes:
        ax.text(
            x,
            y,
            text,
            ha='center',
            va='center',
            fontsize=12,
            bbox=dict(
                boxstyle='round,pad=0.3',
                edgecolor='black',
                facecolor='white'
            )
        )

    # Result nodes
    result_nodes = [
        ('Yes', 6, 4),
        ('No', 1, 1),
        ('Yes', 3, 1),
        ('Yes', 9, 1),
        ('No', 11, 1)
    ]

    for text, x, y in result_nodes:

        face = 'lightgreen' if text == 'Yes' else 'lightcoral'

        ax.text(
            x,
            y,
            text,
            ha='center',
            va='center',
            fontsize=12,
            fontweight='bold',
            bbox=dict(
                boxstyle='round,pad=0.4',
                edgecolor='black',
                facecolor=face
            )
        )

    plt.title(
        'ID3 Decision Tree - Play Tennis',
        fontsize=16,
        fontweight='bold'
    )

    output_path = 'decision_tree.png'
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    print(f"\nDecision tree saved to: {output_path}")
    plt.close(fig)


# Main Program
print("ID3 DECISION TREE")
print("-----------------")

print("\nEntropy of complete dataset:")
print(round(entropy(data), 4))

print("\nInformation Gain:")

for i in range(4):
    gain = information_gain(data, i)
    print(attributes[i], "=", round(gain, 4))

# Generate ID3 tree
tree = id3(data, [0, 1, 2, 3])

print("\nDecision Tree:")
print(tree)

# Display graphical tree
draw_tree(tree)