import os
from datetime import datetime
import matplotlib.pyplot as plt
import contextily as ctx
import pandas as pd
import tkinter as tk
from collections import defaultdict
def screen_size():
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    return screen_width,screen_height
def create_directory_with_timestamp():
    current_time = datetime.now().strftime("%H_%M")
    directory_name = f"graphs_{current_time}"
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    return directory_name
def plot_water_related_nodes_with_map(coordinates):
    screen_width, screen_height = screen_size()
    plt.figure(figsize=(screen_width / 100, screen_height / 100))
    df = pd.DataFrame(coordinates, columns=['Longitude', 'Latitude'])
    plt.scatter(df['Longitude'], df['Latitude'], alpha=0.6, edgecolors='k', s=30)
    ax = plt.gca()
    add_basemap(ax, crs='EPSG:4326', alpha=0.5)
    plt.title('Water-related Nodes')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    directory = create_directory_with_timestamp()
    name = os.path.join(directory, f'Water-related_Nodes.png')
    plt.savefig(name)
def plot_colored_scatter(coordinates, categories):
    screen_width, screen_height = screen_size()
    plt.figure(figsize=(screen_width / 100, screen_height / 100))
    for category in set(categories):
        x = [coord[1] for coord, cat in zip(coordinates, categories) if cat == category]
        y = [coord[0] for coord, cat in zip(coordinates, categories) if cat == category]
        plt.scatter(x, y, label=category, alpha=0.6, edgecolors='w', s=100)
    plt.title('Colored Scatter Plot of Categories')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    plt.grid(True)
    name = f'Colored Scatter Plot of Categories {max(coordinates)}.png'
    directory = create_directory_with_timestamp()
    save_path = os.path.join(directory, name)
    plt.savefig(save_path)
def plot_top_categories(coordinates, categories, top_categories):
    screen_width, screen_height = screen_size()
    plt.figure(figsize=(screen_width / 100, screen_height / 100))
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()
    for ax, category in zip(axes, top_categories):
        x = [coord[1] for coord, cat in zip(coordinates, categories) if cat == category]
        y = [coord[0] for coord, cat in zip(coordinates, categories) if cat == category]
        ax.scatter(x, y, label=category, alpha=0.6, edgecolor='k', s=30)
        ax.set_title(f'Distribution: {category}')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        add_basemap(ax, crs='EPSG:4326', alpha=0.5)
    name = f'Plot of Top Categories.png'
    directory = create_directory_with_timestamp()
    save_path = os.path.join(directory, name)
    plt.savefig(save_path)
    plt.tight_layout()
def plot_least_top_categories(coordinates, categories, top_categories):
    screen_width, screen_height = screen_size()
    plt.figure(figsize=(screen_width / 100, screen_height / 100))
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()
    for ax, category in zip(axes, top_categories):
        x = [coord[1] for coord, cat in zip(coordinates, categories) if cat == category]
        y = [coord[0] for coord, cat in zip(coordinates, categories) if cat == category]
        ax.scatter(x, y, label=category, alpha=0.6, edgecolor='k', s=30)
        ax.set_title(f'Distribution: {category}')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        add_basemap(ax, crs='EPSG:4326', alpha=0.5)
    name = f'Plot of Least Top Categories.png'
    directory = create_directory_with_timestamp()
    save_path = os.path.join(directory, name)
    plt.savefig(save_path)
    plt.tight_layout()
def catigory_graf(objects, name = f'Amenity Category Distribution.png'):
    grouped_objects = defaultdict(list)
    for obj, count in objects.items():
        grouped_objects[count].append(obj)
    labels = []
    sizes = []
    colors = []
    type_colors = {}
    color_palette = plt.cm.tab20.colors

    unique_types = set(objects.keys())
    for i, obj_type in enumerate(unique_types):
        type_colors[obj_type] = color_palette[i % len(color_palette)]

    for count, objs in grouped_objects.items():
        for obj in objs:
            labels.append(f"{obj} ({count})")
            sizes.append(count)
            colors.append(type_colors[obj])

    plt.figure(figsize=(14, 10))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')

    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for color in
               type_colors.values()]
    plt.legend(handles, type_colors.keys(), title='Типы объектов', bbox_to_anchor=(1.05, 1),
               loc='upper left')

    directory = create_directory_with_timestamp()
    save_path = os.path.join(directory, name)
    plt.savefig(save_path)
    plt.tight_layout()
    plt.title('Plot of Categories')


def add_basemap(ax, crs='EPSG:4326', alpha=0.5):
    ctx.add_basemap(ax, crs=crs, alpha=alpha)
