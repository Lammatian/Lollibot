WHITE_THRESHOLD = 0.4
SMOOTHING_FACTOR = 5


class LineCounter:
    def __init__(self):
        self.max_input = (1020, 1020, 1020)
        self.previous_inputs = []

    def calibrate(self, white_input):
        self.max_input = white_input

    def input(self, value):
        scaled_value = tuple(map(lambda r, s: r / s, value, self.max_input))
        self.previous_inputs.append(scaled_value)

    def smoothed_input(self, end_index):
        if end_index < SMOOTHING_FACTOR:
            return False

        start_index = end_index - SMOOTHING_FACTOR

        values = self.previous_inputs[start_index:end_index]
        values_binary = map(lambda v: sum(v)/3 >= WHITE_THRESHOLD, values)

        most_common = sum(values_binary) > (SMOOTHING_FACTOR / 2)

        return most_common

    def last_value(self):
        return self.smoothed_input(len(self.previous_inputs))

    def count_lines(self):
        last_value = False
        switches = 0
        for i in range(1,len(self.previous_inputs)):
            new_value = self.smoothed_input(i)
            if new_value and not last_value:
                switches += 1

            last_value = new_value

        return switches
