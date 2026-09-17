# Candidate Elimination Algorithm
# Experiment: Implementation of Candidate Elimination Algorithm

# Training Dataset
data = [
    ['Sunny', 'Warm', 'Normal', 'Strong', 'Yes'],
    ['Sunny', 'Warm', 'High', 'Strong', 'Yes'],
    ['Rainy', 'Cold', 'High', 'Strong', 'No'],
    ['Sunny', 'Warm', 'High', 'Weak', 'Yes']
]

# Attribute names
attributes = ['Sky', 'AirTemp', 'Humidity', 'Wind']

# Number of attributes
num_attributes = len(attributes)


# ---------------------------------------------------------
# Display a hypothesis
# ---------------------------------------------------------
def display_hypothesis(h):
    return '<' + ', '.join(h) + '>'


# ---------------------------------------------------------
# Display a boundary
# ---------------------------------------------------------
def display_boundary(boundary):
    if len(boundary) == 0:
        return '{}'

    return '{ ' + ', '.join(display_hypothesis(h) for h in boundary) + ' }'


# ---------------------------------------------------------
# Check whether hypothesis covers an instance
# ---------------------------------------------------------
def covers(hypothesis, instance):

    for h, value in zip(hypothesis, instance):

        if h == '?':
            continue

        if h == 'Ø':
            return False

        if h != value:
            return False

    return True


# ---------------------------------------------------------
# Check whether h1 is more general than or equal to h2
# ---------------------------------------------------------
def more_general_or_equal(h1, h2):

    for a, b in zip(h1, h2):

        if a == '?':
            continue

        if a == b:
            continue

        if b == 'Ø':
            continue

        return False

    return True


# ---------------------------------------------------------
# Minimal generalization of S
# ---------------------------------------------------------
def minimal_generalization(s, instance):

    new_s = s.copy()

    for i in range(num_attributes):

        if new_s[i] == 'Ø':
            new_s[i] = instance[i]

        elif new_s[i] != instance[i]:
            new_s[i] = '?'

    return new_s


# ---------------------------------------------------------
# Minimal specializations of G
# ---------------------------------------------------------
def minimal_specializations(g, instance):

    specializations = []

    domains = [
        ['Sunny', 'Rainy'],
        ['Warm', 'Cold'],
        ['Normal', 'High'],
        ['Strong', 'Weak']
    ]

    for i in range(num_attributes):

        if g[i] == '?':

            for value in domains[i]:

                if value != instance[i]:

                    new_g = g.copy()
                    new_g[i] = value
                    specializations.append(new_g)

        elif g[i] != 'Ø' and g[i] == instance[i]:

            # If the current value matches the negative example,
            # replace it with other possible values.
            for value in domains[i]:

                if value != instance[i]:

                    new_g = g.copy()
                    new_g[i] = value
                    specializations.append(new_g)

    return specializations


# ---------------------------------------------------------
# Remove hypotheses from S that are not general enough
# ---------------------------------------------------------
def prune_S(S, G):

    result = []

    for s in S:

        valid = False

        for g in G:

            if more_general_or_equal(g, s):
                valid = True
                break

        if valid:
            result.append(s)

    return result


# ---------------------------------------------------------
# Remove hypotheses from G that are not general enough
# ---------------------------------------------------------
def prune_G(G, S):

    result = []

    for g in G:

        valid = False

        for s in S:

            if more_general_or_equal(g, s):
                valid = True
                break

        if valid:
            result.append(g)

    return result


# ---------------------------------------------------------
# Remove duplicate hypotheses
# ---------------------------------------------------------
def remove_duplicates(boundary):

    unique = []

    for h in boundary:

        if h not in unique:
            unique.append(h)

    return unique


# ---------------------------------------------------------
# Candidate Elimination Algorithm
# ---------------------------------------------------------
def candidate_elimination(data):

    # Most Specific Boundary
    S = [['Ø'] * num_attributes]

    # Most General Boundary
    G = [['?'] * num_attributes]

    print("\nINITIALIZATION")
    print("==============")
    print("S (Most Specific Boundary):")
    print(display_boundary(S))

    print("\nG (Most General Boundary):")
    print(display_boundary(G))

    # Process every training instance
    for step, row in enumerate(data, start=1):

        instance = row[:num_attributes]
        target = row[num_attributes]

        print("\n" + "=" * 65)
        print("Processing D" + str(step))
        print("=" * 65)

        print("Instance :", instance)
        print("Target   :", target)

        # -------------------------------------------------
        # POSITIVE INSTANCE
        # -------------------------------------------------
        if target == 'Yes':

            print("\nPositive Instance")

            # Remove G members that do not cover the positive example
            G = [
                g for g in G
                if covers(g, instance)
            ]

            # Generalize S if necessary
            new_S = []

            for s in S:

                if covers(s, instance):
                    new_S.append(s)

                else:
                    generalized = minimal_generalization(s, instance)

                    # Generalization must be more specific than
                    # at least one member of G
                    for g in G:

                        if more_general_or_equal(g, generalized):
                            new_S.append(generalized)
                            break

            S = remove_duplicates(new_S)

            # Remove S hypotheses that are inconsistent with G
            S = prune_S(S, G)

        # -------------------------------------------------
        # NEGATIVE INSTANCE
        # -------------------------------------------------
        else:

            print("\nNegative Instance")

            # Remove S members that cover the negative example
            S = [
                s for s in S
                if not covers(s, instance)
            ]

            new_G = []

            for g in G:

                if covers(g, instance):

                    # Specialize G
                    specializations = minimal_specializations(
                        g,
                        instance
                    )

                    for specialization in specializations:

                        # Specialization must be more general
                        # than at least one member of S
                        for s in S:

                            if more_general_or_equal(
                                specialization,
                                s
                            ):
                                new_G.append(specialization)
                                break

                else:
                    new_G.append(g)

            G = remove_duplicates(new_G)

            # Remove G hypotheses that are inconsistent with S
            G = prune_G(G, S)

        # -------------------------------------------------
        # Display current boundaries
        # -------------------------------------------------
        print("\nAfter processing D" + str(step) + ":")

        print("\nS Boundary:")
        print(display_boundary(S))

        print("\nG Boundary:")
        print(display_boundary(G))


    # -----------------------------------------------------
    # Final Version Space
    # -----------------------------------------------------
    print("\n\n" + "=" * 65)
    print("FINAL VERSION SPACE BOUNDARIES")
    print("=" * 65)

    print("\nFinal S (Most Specific Boundary):")
    print(display_boundary(S))

    print("\nFinal G (Most General Boundary):")
    print(display_boundary(G))

    print("\n" + "=" * 65)
    print("Candidate Elimination completed successfully.")
    print("=" * 65)


# ---------------------------------------------------------
# Main Program
# ---------------------------------------------------------
print("=" * 65)
print("CANDIDATE ELIMINATION ALGORITHM")
print("=" * 65)

print("\nAttributes:")
print(attributes)

print("\nTraining Dataset:")
print("-" * 65)

print(
    "{:<8} {:<12} {:<12} {:<12} {:<12} {:<10}".format(
        "Instance",
        "Sky",
        "AirTemp",
        "Humidity",
        "Wind",
        "Target"
    )
)

print("-" * 65)

for i, row in enumerate(data, start=1):

    print(
        "{:<8} {:<12} {:<12} {:<12} {:<12} {:<10}".format(
            "D" + str(i),
            row[0],
            row[1],
            row[2],
            row[3],
            row[4]
        )
    )

print("-" * 65)

# Run Candidate Elimination
candidate_elimination(data)