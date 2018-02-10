WHITE_THRESHOLD = 0.4
SMOOTHING_FACTOR = 5


class LineCounter(object):
    def __init__(self):
        self.max_input = 100
        self.line_count = 0
        self.previous_inputs = []

    def reset(self):
        self.line_count = 0
        self.previous_inputs = []

    def calibrate(self, white_input):
        self.max_input = white_input

    def register_input(self, value):
        scaled_value = value / self.max_input
        value_binary = scaled_value >= WHITE_THRESHOLD
        self.previous_inputs.append(value_binary)

        last_value = self.__smoothed_input(len(self.previous_inputs) - 1)
        cur_value = self.__smoothed_input(len(self.previous_inputs))
        if cur_value and not last_value:
            self.line_count += 1

    def __smoothed_input(self, end_index):
        if end_index == 0:
            return False

        start_index = max(end_index - SMOOTHING_FACTOR, 0)

        values = self.previous_inputs[start_index:end_index]

        most_common = sum(values) > (SMOOTHING_FACTOR / 2)

        return most_common

    def last_value(self):
        return self.__smoothed_input(len(self.previous_inputs))

    def count_lines(self):
        return self.line_count
