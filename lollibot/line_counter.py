WHITE_THRESHOLD = 0.4
SMOOTHING_FACTOR = 5


class LineCounter(object):
    def __init__(self):
        self.max_input = (1020, 1020, 1020)
        self.previous_inputs = []

    def calibrate(self, white_input):
        self.max_input = white_input

    def register_input(self, value):
        scaled_value = tuple(map(lambda r, s: r / s, value, self.max_input))
        value_binary = sum(scaled_value) / 3 >= WHITE_THRESHOLD
        self.previous_inputs.append(value_binary)

    def __smoothed_input(self, end_index):
        if end_index < SMOOTHING_FACTOR:
            return False

        start_index = end_index - SMOOTHING_FACTOR

        values = self.previous_inputs[start_index:end_index]

        most_common = sum(values) > (SMOOTHING_FACTOR / 2)

        return most_common

    def last_value(self):
        return self.__smoothed_input(len(self.previous_inputs))

    def count_lines(self):
        last_value = False
        switches = 0
        for i in range(1, len(self.previous_inputs)):
            new_value = self.__smoothed_input(i)
            if new_value and not last_value:
                switches += 1

            last_value = new_value

        return switches
