from time import perf_counter
import pandas as pd
from algos.colors import get_colors
from algos.custom_kdtree import CustomKDTreeConverter
from algos.naive import NaiveConverter
from algos.scipy_kdtree import ScipyKDTreeConverter
from glob import glob
from collections import defaultdict
from PIL import Image
import numpy as np

def get_input_paths():
    types = ('*.png', '*.jpg')
    image_paths = []
    for files in types:
        image_paths.extend(glob(f"./input_images/{files}"))
    color_paths = glob("./color_palette/*.txt")
    return image_paths, color_paths

def get_save_path(src_path, converter_name, colors_num):
    filebase, ext = src_path.split("/")[-1].split(".")
    save_path = f"./output_images/{filebase}_{converter_name}_{colors_num}.{ext}"
    return save_path


image_files, color_files = get_input_paths()
results_dict = defaultdict(list)

for colors_f in color_files:
    with open(colors_f, "r") as f:
        colors = get_colors(f)
    num_colors = len(colors)
    results_dict["num_output_colors"].append(num_colors)
    print(f"Processing {num_colors} colors")

    for image_f in image_files:
        results_dict["input_file"].append(image_f.split("/")[-1])
        is_image_read = False
        for converter_name in ["scipy", "kd-tree", "naive"]:
        # for converter_name in ["scipy", "kd-tree"]:
            if converter_name == "scipy":
                converter = ScipyKDTreeConverter(image_f, colors)
            elif converter_name == "kd-tree":
                converter = CustomKDTreeConverter(image_f, colors)
            else:
                converter = NaiveConverter(image_f, colors)
            if not is_image_read:
                input_colors = np.unique(converter.input_image.reshape(-1, converter.input_image.shape[-1]), axis=0, return_counts=True)
                results_dict["image_resolution"].append(sum(input_colors[1]))
                results_dict["num_input_colors"].append(len(input_colors[0]))
                is_image_read = True

            print(f"===== Start {converter_name} conversion")
            start_time = perf_counter()
            converter.convert()
            time = perf_counter() - start_time
            print(f'===== Timing: {time}')
            image_out = get_save_path(image_f, converter_name, num_colors)
            converter.save_file(image_out)

            # save results
            results_dict[f"time_{converter_name}"].append(round(time, 2))

df = pd.DataFrame(results_dict)
df = df.reindex(columns=['input_file', 'image_resolution', 'num_input_colors', 'num_output_colors', 'time_naive', 'time_kd-tree', 'time_scipy'])
df.to_csv('results.csv', index=False)
