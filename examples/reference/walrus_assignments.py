numbers = [1, 2, 3, 4, 5]
for i in numbers:
    if (j := i + i // 2) > 3:
        print(j)
