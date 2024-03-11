# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=invalid-name

import pytest
from day18 import Cube, Droplet, Point, Face

@pytest.fixture
def example_cubes_coords():
    return (
        (2,2,2),
        (1,2,2),
        (3,2,2),
        (2,1,2),
        (2,3,2),
        (2,2,1),
        (2,2,3),
        (2,2,4),
        (2,2,6),
        (1,2,5),
        (3,2,5),
        (2,1,5),
        (2,3,5)
    )
@pytest.fixture
def cubes_with_air():
    return [
        Cube(1, 1, 0), Cube(2, 1, 0),
        Cube(1, 0, 1), Cube(2, 0, 1),
        Cube(0, 1, 1), Cube(3, 1, 1),
        Cube(1, 2, 1), Cube(2, 2, 1),
        Cube(1, 1, 2), Cube(2, 1, 2)
    ]

# TODO: Definición de Cube
def test_cube():
    assert Cube(x=1, y=1, z=2)
    assert Cube(x=5, y=1, z=3)

def test_droplet():
    assert Droplet()

def test_point():
    assert Point(x=1, y=1, z=4)
    assert Point(x=1, y=1, z=0)

def test_face():
    a, b = Point(x=0, y=0, z=0), Point(x=1, y=1, z=0)
    assert Face(a, b)

def test_face_wrong_coords():
    a, b = Point(x=0, y=0, z=0), Point(x=1, y=2, z=0)
    with pytest.raises(ValueError):
        Face(a, b)
    a, b = Point(x=0, y=0, z=0), Point(x=0, y=0, z=0)
    with pytest.raises(ValueError):
        Face(a, b)

def test_cube_faces():
    cube = Cube(x=0, y=0, z=0)

    assert cube.faces == {
        Face(Point(0, 0, 0), Point(0, 1, 1)),
        Face(Point(0, 0, 0), Point(1, 0, 1)),
        Face(Point(0, 0, 0), Point(1, 1, 0)),
        Face(Point(0, 0, 1), Point(1, 1, 1)),
        Face(Point(0, 1, 0), Point(1, 1, 1)),
        Face(Point(1, 0, 0), Point(1, 1, 1))
    }
    assert len(cube.faces) == 6

def test_droplet_faces():
    droplet = Droplet(cubes=[Cube(x=1, y=1, z=1), Cube(x=2, y=1, z=1)])
    assert len(droplet.faces) == 10

def test_droplet_enclosing_volume(cubes_with_air):
    droplet = Droplet(cubes_with_air)
    assert droplet.enclosing_volume == (Point(-1, -1, -1), Point(4, 3, 3))

def test_droplet_get_internal_air_cubes(cubes_with_air):

    droplet = Droplet(cubes=cubes_with_air)

    assert len(droplet.get_internal_air_cubes()) == 2

def test_example_droplet_faces(example_cubes_coords):
    cubes = [Cube(*coords) for coords in example_cubes_coords]
    droplet = Droplet(cubes=cubes)

    assert len(droplet.faces) == 64

def test_example_droplet_external_faces(example_cubes_coords):
    cubes = [Cube(*coords) for coords in example_cubes_coords]
    droplet = Droplet(cubes=cubes)

    assert len(droplet.external_faces) == 58
