# distance.py

class DistanceData:
    """
    Handles the distance and address data.
    """

    def __init__(self):
        self.address_list = []    # List of addresses
        self.distance_table = []  # 2D list of distances

    def load_addresses(self, filename):
        """
        Loads addresses from a CSV file.
        """
        with open(filename, 'r') as file:
            next(file)  # Skip header
            for line in file:
                data = line.strip().split(',')
                address = data[2].strip()
                if address not in self.address_list:
                    self.address_list.append(address)

    def load_distances(self, filename):
        """
        Loads distances from a CSV file.
        """
        with open(filename, 'r') as file:
            next(file)  # Skip header
            for line in file:
                data = line.strip().split(',')
                distances = []
                for d in data[1:]:
                    if d == '':
                        distances.append(0.0)
                    else:
                        distances.append(float(d))
                self.distance_table.append(distances)

    def get_distance(self, from_address, to_address):
        """
        Returns the distance between two addresses.
        """
        from_index = self.address_list.index(from_address)
        to_index = self.address_list.index(to_address)
        distance = self.distance_table[from_index][to_index]
        if distance == 0.0:
            distance = self.distance_table[to_index][from_index]
        return distance
