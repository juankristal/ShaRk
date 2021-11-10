# TO-DO: Make the window non-rigid by weighting over a bell curve over (-2,2) instead


class Density:
    """
    Obtains the density calculation for each note in the map by counting the
    amount of notes around the note in a timing window of size bin_size
    """
    def __init__(self, smoother_function, bin_size):
        self.smoother_function = smoother_function
        self.bin_size = bin_size

    def calculate_difficulty(self, hit_objects):
        difficulties = []
        window_start = 0  # Current index of the note that first enters in the window
        window_end = 0  # Same but for last

        for hit_object in hit_objects:
            difficulty = 0
            # Find the new first note that is inside the window
            # (pretty sure this can be calculated in a more efficient way)
            while hit_objects[window_start].timestamp < (hit_object.timestamp - self.bin_size / 2):
                window_start += 1

            # Find the new last note that is inside the window
            while hit_objects[window_end].timestamp < (hit_object.timestamp + self.bin_size / 2) and \
                    window_end < len(hit_objects) - 1:
                window_end += 1

            for j in range(window_start, window_end + 1):
                distance = ((hit_objects[j].timestamp - hit_object.timestamp) / (self.bin_size / 2)) * 3
                difficulty += self.smoother_function(distance)
            # The note count is simply the index difference

            difficulties.append(difficulty)

        return difficulties

