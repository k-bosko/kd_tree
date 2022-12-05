import random

n_colors = [128, 256, 512, 1024, 2048, 4096, 8192]

all_colors = []
for r in range(256):
    for g in range(256):
        for b in range(256):
            all_colors.append((str(r), str(g), str(b)))

random.shuffle(all_colors)

for n_col in n_colors:
    print(f"Generating {n_col} colors")
    color_palette = []
    step = (256*256*256) // n_col
    for i in range(n_col):
        # print(f'will take: {step*i} - {all_colors[step * i]}')
        color_palette.append(all_colors[step * i])

    with open(f"./color_palette/{n_col}_colors.txt", "w") as f:
        for c in color_palette:
            colors_str = ",".join(c) + "\n"
            f.writelines(colors_str)
