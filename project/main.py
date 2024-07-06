import os

from dataItaly import InfrastructureData
from grafici import catigory_graf, plot_colored_scatter, plot_top_categories, plot_water_related_nodes_with_map, plot_least_top_categories
import overpy

from project.database1 import create_file, insert_data_to_file


def main():
    bbox_rome_center = (12.4715, 41.8723, 12.5119, 41.8955)
    infra_data = InfrastructureData()
    try:
        data = infra_data.fetch_data(bbox_rome_center)
    except overpy.OverpassTooManyRequests:
        print("API limit exceeded. Please try again later.")
        data = None

    # bbox = bbox_rome_center
    # host = "localhost"
    # database = "Hackathon2"
    # user = "postgres"
    # password = "0000000000"
    # port = "5432"
    # create_database(database, user, password, host, port)
    # conn = create_connection(database, user, password, host)
    # directory = "data_files"

    clean_data, unclean_data = infra_data.process_data(data)
    print("clean_data\n", clean_data)
    print("unclean_data\n",unclean_data)
    a=infra_data.amenity_dictionary(clean_data)
    print("amenity_dictionary\n",a)
    coordinates, categories = infra_data.get_coordinates_and_categories(clean_data)
    print("get_coordinates_and_categories\n",coordinates, categories)
    water_nodes = infra_data.get_water_related_nodes(unclean_data)
    print("water_nodes\n",water_nodes)

    for category, nodes in clean_data.items():
        filename = f"{category}_{len(nodes)}.txt"
        directory = "C:/Users/inger/PycharmProjects/Hackathon2_DataAnalyst/project/categories_files"
        file_path = create_file(directory, filename)
        for node in nodes:
            insert_data_to_file(file_path, node)

    if data:
        water_nodes = infra_data.get_water_related_nodes(unclean_data)
        plot_water_related_nodes_with_map(water_nodes)

        coordinates, categories = infra_data.get_coordinates_and_categories(clean_data)
        plot_colored_scatter(coordinates, categories)

        amenity_dictionary = infra_data.amenity_dictionary(clean_data)
        n = len(amenity_dictionary)
        quarter_n = n // 4

        first_quarter_items = dict(list(amenity_dictionary.items())[:quarter_n])
        second_quarter_items = dict(list(amenity_dictionary.items())[quarter_n: 2 * quarter_n])
        third_quarter_items = dict(list(amenity_dictionary.items())[2 * quarter_n: 3 * quarter_n])
        fourth_quarter_items = dict(list(amenity_dictionary.items())[3 * quarter_n:])

        catigory_graf(first_quarter_items, 'Amenity Category Distribution First Part.png')
        catigory_graf(second_quarter_items, 'Amenity Category Distribution Second Part.png')
        catigory_graf(third_quarter_items, 'Amenity Category Distribution Third Part.png')
        catigory_graf(fourth_quarter_items, 'Amenity Category Distribution Fourth Part.png')

        top_categories = infra_data.get_top_categories(categories)
        plot_top_categories(coordinates, categories, top_categories)

        top_least_categories = infra_data.get_least_top_catigories(categories)
        plot_least_top_categories(coordinates, categories, top_least_categories)

    else:
        print("No data retrieved or saved. Check your query or API connection.")

if __name__ == "__main__":
    main()
