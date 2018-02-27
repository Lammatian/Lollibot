# Line counting module

The Lollibot can count white crossing lines in order to determine where on the road it is and to be able to stop in the
middle of it.

## Usage

```python
import lollibot.movement.movement_control as movement_control
mc = movement_control.MovementControl()
mc.move_lines(3) # Lollibot moves until it sees the 3rd white line and then stops
mc.move_lines(-2) # Robot moves backwards until it sees the second white line 
```

## Notes

If the Lollibot colour sensor is already on the white line when the line counting starts, that line will be counted in
to the total.

## Line counting supporting classes

### `lollibot.movement.line_counter.LineCounter`

Stores the history of colour sensor measurements and uses them to determine the number of white lines passed.

The line counter uses fuzzy counting, so single erroneous input value does not register as a new line.

Main methods:
* `register_input(value)`: Registers the colour sensor data, value must be an integer from 0 to 100, as returned by the
colour sensor. The value of 0 would mean dark (black) surface, while 100 would be light (white) colour.
* `count_lines()`: Outputs the number of white lines the robot has seen in the sensor data fed through `register_input`

Configuration values:
* `COLOR_SENSOR_WHITE_THRESHOLD`: The threshold for colour sensor data to consider the value as white
* `LINE_COUNTER_SMOOTHING_FACTOR`: The number of latest input values to combine in order to decide the colour of the
measurement. Setting this setting higher makes the counter more resilient to erroneous inputs, but it takes longer to
detect a line change.

### `lollibot.movement.movement_control.MovementControl`

Coordinates EV3 motors, colour sensor and line counter in order to move the Lollibot on the road until and stop it when
it passes a desired amount of white crossing lines.

Main methods:
* `move_lines(count, direction)`: Moves the robot in a specified direction until it passes `count` number of lines.
Parameter `direction` should be 1 to move the robot forwards, -1 to move it backwards.

### `lollibot.ev3.line_color_sensor.LineColorSensor`

Wrapper for ev3 ColorSensor class, which sets up correct sensor mode and reads sensor values

Main methods:
*  `get()`: Returns the brightness value obtained from the sensor. Value range: 0-100.

### `lollibot.ev3.main_motors.MainMotors`

Runs main Lollibot motors.

Main methods:
* `move(direction)`: Turns on the motors. If `direction` is 1, the robot moves forwards, backwards if -1.
* `move_distance(distance)`: Turns on the motors and moves `distance` metres.
* `stop()`: Actively stops the main motors.