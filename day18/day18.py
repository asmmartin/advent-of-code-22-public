# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=invalid-name

# Idea: Cada cubo tiene 6 caras. Procesar cubo a cubo de forma que:
# - Detectar 6 caras del cubo
# - Caras que ya estuvieran expuestas de antes: No exponer
# - Caras que no se contabilizaran: Exponer
# Cara máximo compartida por 2 cubos. No hay que preocuparse por repetidas.

# Idea parte 2: Hay que eliminar de la cuenta las caras interiores
# 1) Detectar cubos aire interiores
# 2) Calcular caras teniendo en cuenta cubos aire + cubos lava

from dataclasses import dataclass, field
from collections import deque
from pathlib import Path

@dataclass(frozen=True)
class Cube:

    x: int
    y: int
    z: int


    @property
    def faces(self):
        x, y, z = self.x, self.y, self.z
        return {
            Face(Point(x  , y  , z  ), Point(x  , y+1, z+1)),
            Face(Point(x  , y  , z  ), Point(x+1, y  , z+1)),
            Face(Point(x  , y  , z  ), Point(x+1, y+1, z  )),
            Face(Point(x  , y  , z+1), Point(x+1, y+1, z+1)),
            Face(Point(x  , y+1, z  ), Point(x+1, y+1, z+1)),
            Face(Point(x+1, y  , z  ), Point(x+1, y+1, z+1))
        }


@dataclass(frozen=True)
class Point:

    x: int
    y: int
    z: int


@dataclass(frozen=True)
class Face:

    corner_a: Point
    corner_b: Point

    def __init__(self, corner_a: Point, corner_b: Point):
        if (
            abs(corner_b.x - corner_a.x) +
            abs(corner_b.y - corner_a.y) +
            abs(corner_b.z - corner_a.z)
        ) != 2:
            raise ValueError('Face points are not valid')
        super().__setattr__('corner_a', corner_a)
        super().__setattr__('corner_b', corner_b)

@dataclass
class Droplet:
    cubes: list[Cube] = field(default_factory=list)

    @property
    def faces(self):
        faces = set()
        for cube in self.cubes:
            faces.symmetric_difference_update(cube.faces)
        return faces

    @property
    def external_faces(self):
        faces = set()
        for cube in self.cubes:
            faces.symmetric_difference_update(cube.faces)
        for cube in self.get_internal_air_cubes():
            faces.symmetric_difference_update(cube.faces)
        return faces

    @property
    def enclosing_volume(self) -> tuple[Point, Point]:
        x_coords = [cube.x for cube in self.cubes]
        y_coords = [cube.y for cube in self.cubes]
        z_coords = [cube.z for cube in self.cubes]

        min_point = Point(min(x_coords)-1, min(y_coords)-1, min(z_coords)-1)
        max_point = Point(max(x_coords)+1, max(y_coords)+1, max(z_coords)+1)

        return min_point, max_point

    def get_internal_air_cubes(self) -> list[Cube]:
        min_point, max_point = self.enclosing_volume
        cubes_in_volume = {
            Cube(x=x, y=y, z=z)
            for x in range(min_point.x, max_point.x + 1)
            for y in range(min_point.y, max_point.y + 1)
            for z in range(min_point.z, max_point.z + 1)
        }
        lava_cubes = set(self.cubes)

        # DFS
        visited = set()
        to_visit = deque([Cube(max_point.x, max_point.y, max_point.z)])

        while to_visit:
            cube = to_visit.pop()
            if cube not in visited:
                visited.add(cube)
                cubes_in_volume.remove(cube)

                # Check neighbours
                possible_neighbours = [
                    Cube(cube.x+1, cube.y, cube.z),
                    Cube(cube.x-1, cube.y, cube.z),
                    Cube(cube.x, cube.y+1, cube.z),
                    Cube(cube.x, cube.y-1, cube.z),
                    Cube(cube.x, cube.y, cube.z+1),
                    Cube(cube.x, cube.y, cube.z-1),
                ]
                for neighbour in possible_neighbours:
                    if neighbour in lava_cubes or neighbour in visited:
                        continue
                    if not min_point.x <= neighbour.x <= max_point.x:
                        continue
                    if not min_point.y <= neighbour.y <= max_point.y:
                        continue
                    if not min_point.z <= neighbour.z <= max_point.z:
                        continue
                    to_visit.append(neighbour)

        return list(cubes_in_volume - lava_cubes)

def main(input_path: str):
    cubes_coords_str = Path(input_path).read_text(encoding='utf-8')
    cubes_coords = [line.split(',') for line in cubes_coords_str.splitlines()]
    cubes_coords = [
        (int(coords[0]), int(coords[1]), int(coords[2]))
        for coords in cubes_coords
    ]
    cubes = [Cube(*coords) for coords in cubes_coords]
    droplet = Droplet(cubes=cubes)

    print(f'Faces (and therefore, area) of the droplet: {len(droplet.faces)}')
    print(
        'External faces (and therefore, external area) of the droplet: '
        f'{len(droplet.external_faces)}'
    )

if __name__ == "__main__":
    INPUT_PATH = './input.txt'
    main(INPUT_PATH)
