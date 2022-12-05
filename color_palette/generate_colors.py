n_colors = 100
all_colors = 256*256*256
step = all_colors // n_colors

all_colors = []
for r in range(256):
    for g in range(256):
        for b in range(256):
            all_colors.append((str(r), str(g), str(b)))

color_palette = []
for i in range(n_colors):
    # print(f'will take: {step*i} - {all_colors[step * i]}')
    color_palette.append(all_colors[step * i])

with open(f"./color_palette/{n_colors}_colors.txt", "w") as f:
    for c in color_palette:
        colors_str = ",".join(c) + "\n"
        f.writelines(colors_str)
