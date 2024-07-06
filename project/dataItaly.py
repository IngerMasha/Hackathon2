import json

import numpy as np
import overpy
from collections import Counter


class InfrastructureData:
    def __init__(self):
        self.api = overpy.Overpass()
    def fetch_data(self, bbox):
        query = f"""
        [out:json];
        (
          node["amenity"]({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]});
          way["amenity"]({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]});
          relation["amenity"]({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]});
        );
        out center;
        """
        try:
            result = self.api.query(query)
            return result
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
    def process_data(self, data):
        good_nodes = []
        bad_nodes = []

        def process_entity(entity):
            entity_id = entity.id
            entity_type = entity.tags.get('amenity', 'n/a')
            street = entity.tags.get('addr:street', 'n/a')
            house_number = entity.tags.get('addr:housenumber', 'n/a')
            latitude = getattr(entity, 'lat', None)
            longitude = getattr(entity, 'lon', None)

            if latitude and longitude:
                entity_data = (entity_id, entity_type, f"{street} {house_number}", float(latitude), float(longitude))
                if entity_type != 'n/a' and street != 'n/a' and house_number != 'n/a':
                    good_nodes.append(entity_data)
                else:
                    bad_nodes.append(entity_data)

        for node in data.nodes:
            process_entity(node)
        for way in data.ways:
            process_entity(way)
        for relation in data.relations:
            process_entity(relation)

        categorized_data = {}
        unclean_data = {}
        for node in good_nodes:
            node_id, node_type, address, latitude, longitude = node
            if node_type not in categorized_data:
                categorized_data[node_type] = []
            categorized_data[node_type].append(node)
        for node in bad_nodes:
            node_id, node_type, address, latitude, longitude = node
            if node_type not in unclean_data:
                unclean_data[node_type] = []
            unclean_data[node_type].append(node)


        return categorized_data, unclean_data
    def amenity_dictionary(self, data):
        amenity_counts = {}
        for category, nodes in data.items():
            amenity_counts[category] = len(nodes)

        sorted_items = sorted(amenity_counts.items(), key=lambda x: x[1], reverse=True)
        sorted_dict = {k: v for k, v in sorted_items}
        return sorted_dict
    def get_coordinates_and_categories(self, data):
        coordinates = []
        categories = []
        for category, nodes in data.items():
            for node in nodes:
                _, node_type, _, latitude, longitude = node
                coordinates.append((latitude, longitude))
                categories.append(node_type)
        return coordinates, categories
    def get_top_categories(self, categories):
        category_counts = Counter(categories)
        total_categories = len(category_counts)
        half_n = total_categories // 2
        top_categories = category_counts.most_common(half_n)
        return [category for category, count in top_categories]
    def get_least_top_catigories(self, categories):
        category_counts = Counter(categories)
        total_categories = len(category_counts)
        half_n = total_categories // 2
        bottom_categories = category_counts.most_common()[:-half_n - 1:-1]
        return [category for category, count in bottom_categories]
    def get_water_related_nodes(self, data):
        water_nodes_coordinates = []
        def parse_water(tags):
            if 'amenity' in tags and 'drinking_water' in tags['amenity']:
                return True
            return False
        for category, nodes in data.items():
            for node in nodes:
                if parse_water({'amenity': category}):
                    latitude, longitude = node[3], node[4]
                    water_nodes_coordinates.append((latitude, longitude))

        return water_nodes_coordinates

# bbox_rome_center = (12.4817, 41.8790, 12.5017, 41.8888)
# infra_data = InfrastructureData()
# data = infra_data.fetch_data(bbox_rome_center)
# if data:
#     for node in data.nodes:
#         print("Node data:")
#         print(json.dumps(node.tags, indent=4))
# else:
#     print("No data available.")

