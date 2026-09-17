# Generate all possible PINs

even_digits = [0, 2, 4, 6, 8]

print("Possible PINs:")

count = 0

for a in even_digits:
    for b in even_digits:
        for c in even_digits:
            for d in even_digits:
                if a + b + c + d == 16:
                    print(f"{a}{b}{c}{d}")
                    count += 1

print("\nTotal possible PINs:", count)