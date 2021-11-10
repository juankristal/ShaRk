class Hold:
    """
    Obtains for each note the additional "strain" created by having an LN pressed
    in the other finger of the same hand
    """
    def __init__(self, smoother_function):
        self.smoother_function = smoother_function

    def calculate(self, hit_objects):
        difficulties = []
        for i, hit_object in enumerate(hit_objects):
            same_hand_column = 2 * (hit_object.column // 2) + (hit_object.column + 1) % 2
            j = i
            while hit_objects[j].column != same_hand_column and j > 0:
                j -= 1

            if j < 0:
                continue

            if hit_objects[j].lnend > hit_object.timestamp:
                d1 = hit_objects[j].lnend - hit_object.timestamp
                d2 = hit_object.timestamp - hit_objects[j].timestamp

                difficulties.append(self.smoother_function(d1) * self.smoother_function(d2))

        return difficulties

