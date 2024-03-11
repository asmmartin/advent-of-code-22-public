# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import re
import sys

PointCoords = tuple[int, int]

class Sensor:
    def __init__(self, sensor_coords: PointCoords, beacon_coords: PointCoords):
        self.x, self.y = sensor_coords # pylint: disable=invalid-name
        self.beacon_x, self.beacon_y = beacon_coords

        self.beacon_distance = self.manhattan_distance_to(beacon_coords)

    def __eq__(self, __o: object) -> bool:
        return (
            isinstance(__o, Sensor) and
            self.x == __o.x and
            self.y == __o.y and
            self.beacon_x == __o.beacon_x and
            self.beacon_y == __o.beacon_y
        )

    def manhattan_distance_to(self, point: PointCoords) -> int:
        return abs(self.x - point[0]) + abs(self.y - point[1])

    def can_be_beacon(self, point: PointCoords) -> bool:
        return self.manhattan_distance_to(point) > self.beacon_distance

    def get_exclusion_area_intersection_with_line(
        self, line: int
    ) -> list[PointCoords]:
        delta = self.beacon_distance - abs(line - self.y)
        return [
            (x_coord, line)
            for x_coord in range(self.x - delta, self.x + delta + 1)
        ]

    def get_outline(self) -> set[PointCoords]:
        outline = set()
        for delta_y in range(0, self.beacon_distance + 2):
            delta_x = self.beacon_distance + 1 - delta_y

            outline.add((self.x + delta_x, self.y + delta_y))
            outline.add((self.x - delta_x, self.y + delta_y))
            outline.add((self.x + delta_x, self.y - delta_y))
            outline.add((self.x - delta_x, self.y - delta_y))

        return outline



    @classmethod
    def from_str(cls, string: str) -> 'Sensor':
        data = re.findall(
            'Sensor at x=(.+), y=(.+): closest beacon is at x=(.+), y=(.+)',
            string
        )[0]
        return cls(
            sensor_coords=(int(data[0]), int(data[1])),
            beacon_coords=(int(data[2]), int(data[3])),
        )

class Grid:
    def __init__(self, sensors: list[Sensor]) -> None:
        self.sensors = sensors

    @classmethod
    def from_str(cls, string: str) -> 'Grid':
        lines = string.splitlines()
        return cls(
            sensors=[Sensor.from_str(line) for line in lines]
        )

    def get_beacon_free_points(self, y_coord: int) -> list[PointCoords]:

        intersections = [
            sensor.get_exclusion_area_intersection_with_line(y_coord)
            for sensor in self.sensors
        ]

        known_beacons = {
            (sensor.beacon_x, sensor.beacon_y) for sensor in self.sensors
        }

        return list(set().union(*intersections) - known_beacons)

    def localize_distress_beacon(self, max_coord: int) -> PointCoords:
        for i_sensor, sensor in enumerate(self.sensors):
            print(f'Checking boundaries of sensor {i_sensor}...')
            outline = sensor.get_outline()
            for point in outline:
                if not 0 <= point[0] <= max_coord or not 0 <= point[1] <= max_coord:
                    continue
                for sensor in self.sensors:
                    if not sensor.can_be_beacon(point):
                        break
                else:
                    return point
        return None

def main():
    sensors_texts = sys.stdin.read()
    grid = Grid.from_str(sensors_texts)
    line_to_eval = 2_000_000
    beacon_free_points = grid.get_beacon_free_points(line_to_eval)
    print(f'Line {line_to_eval} has {len(beacon_free_points)} positions '
          'that cannot contain a beacon')

    print()
    distress_beacon = grid.localize_distress_beacon(4_000_000)
    print(f'Found {distress_beacon=}')
    print(f'Tuning frequency: {distress_beacon[0] * 4000000 + distress_beacon[1]}')


if __name__ == "__main__":
    main()
