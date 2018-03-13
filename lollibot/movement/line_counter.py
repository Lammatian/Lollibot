from lollibot.config import config


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

    def threshold(self, value):
        scaled_value = value / self.max_input
        return scaled_value >= config.COLOR_SENSOR_WHITE_THRESHOLD

    def register_input(self, value):
        value_binary = self.threshold(value)
        self.previous_inputs.append(value_binary)

        last_value = self.__smoothed_input(len(self.previous_inputs) - 1)
        cur_value = self.__smoothed_input(len(self.previous_inputs))
        if cur_value and not last_value:
            self.line_count += 1

    def __smoothed_input(self, end_index):
        if end_index == 0:
            return False

        start_index = max(end_index - config.LINE_COUNTER_SMOOTHING_FACTOR, 0)

        values = self.previous_inputs[start_index:end_index]

        most_common = sum(values) > (config.LINE_COUNTER_SMOOTHING_FACTOR / 2)

        return most_common

    def last_value(self):
        return self.__smoothed_input(len(self.previous_inputs))

    def count_lines(self):
        return self.line_count
