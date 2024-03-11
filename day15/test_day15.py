# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name

from day15 import Sensor, Grid

SAMPLE_INPUT = (
    'Sensor at x=2, y=18: closest beacon is at x=-2, y=15\n'
    'Sensor at x=9, y=16: closest beacon is at x=10, y=16\n'
    'Sensor at x=13, y=2: closest beacon is at x=15, y=3\n'
    'Sensor at x=12, y=14: closest beacon is at x=10, y=16\n'
    'Sensor at x=10, y=20: closest beacon is at x=10, y=16\n'
    'Sensor at x=14, y=17: closest beacon is at x=10, y=16\n'
    'Sensor at x=8, y=7: closest beacon is at x=2, y=10\n'
    'Sensor at x=2, y=0: closest beacon is at x=2, y=10\n'
    'Sensor at x=0, y=11: closest beacon is at x=2, y=10\n'
    'Sensor at x=20, y=14: closest beacon is at x=25, y=17\n'
    'Sensor at x=17, y=20: closest beacon is at x=21, y=22\n'
    'Sensor at x=16, y=7: closest beacon is at x=15, y=3\n'
    'Sensor at x=14, y=3: closest beacon is at x=15, y=3\n'
    'Sensor at x=20, y=1: closest beacon is at x=15, y=3\n'
)

def test_sensor():
    sensor = Sensor((2, 18), (-2, 15))
    assert sensor.x, sensor.y == (2, 18)
    assert sensor.beacon_x, sensor.beacon_y == (-2, 15)

def test_sensor_from_str():

    sensor = Sensor.from_str('Sensor at x=2, y=18: closest beacon is at x=-2, y=15')
    assert sensor == Sensor((2, 18), (-2, 15))

def test_sensor_manhattan_distance_to():

    sensor = Sensor((2, 18), (-2, 15))
    assert sensor.manhattan_distance_to((-2, 15)) == 7
    assert sensor.manhattan_distance_to((2, 25)) == 7

def test_sensor_can_be_beacon():

    sensor = Sensor((2, 18), (-2, 15))
    assert sensor.can_be_beacon((1000, 1000))
    assert not sensor.can_be_beacon((2, 20))
    assert not sensor.can_be_beacon((2, 25))

def test_sensor_get_exclusion_area_intersection_with_line():
    sensor = Sensor((8, 7), (2, 10))
    intersection = sensor.get_exclusion_area_intersection_with_line(5)
    assert len(intersection) == 15

def test_sensor_get_outline():
    sensor = Sensor((8, 7), (2, 10))
    outline = sensor.get_outline()
    assert outline == {
        (8, -3),
        (7, -2), (9, -2),
        (6, -1), (10, -1),
        (5, 0), (11, 0),
        (4, 1), (12, 1),
        (3, 2), (13, 2),
        (2, 3), (14, 3),
        (1, 4), (15, 4),
        (0, 5), (16, 5),
        (-1, 6), (17, 6),
        (-2, 7), (18, 7),
        (-1, 8), (17, 8),
        (0, 9), (16, 9),
        (1, 10), (15, 10),
        (2, 11), (14, 11),
        (3, 12), (13, 12),
        (4, 13), (12, 13),
        (5, 14), (11, 14),
        (6, 15), (10, 15),
        (7, 16), (9, 16),
        (8, 17)
    }


def test_grid():
    grid = Grid.from_str(SAMPLE_INPUT)
    assert len(grid.sensors) == 14

def test_grid_get_beacon_free_points():
    grid = Grid.from_str(SAMPLE_INPUT)

    assert len(grid.get_beacon_free_points(y_coord=10)) == 26

def test_grid_localize_distress_beacon():
    grid = Grid.from_str(SAMPLE_INPUT)
    distress_beacon = grid.localize_distress_beacon(max_coord=20)
    assert distress_beacon == (14, 11)
