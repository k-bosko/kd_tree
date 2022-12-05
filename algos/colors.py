def get_colors(color_file):
    colors = []
    for line in color_file.readlines():
        parsed = list(
            map(lambda e: int(e), line.split(','))
        )
        colors.append(parsed)
    return colors