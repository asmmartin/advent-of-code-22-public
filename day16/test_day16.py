# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=redefined-outer-name


from unittest.mock import patch
import pytest

import day16

INPUT_SAMPLE = (
    'Valve AA has flow rate=0; tunnels lead to valves DD, II, BB\n'
    'Valve BB has flow rate=13; tunnels lead to valves CC, AA\n'
    'Valve CC has flow rate=2; tunnels lead to valves DD, BB\n'
    'Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE\n'
    'Valve EE has flow rate=3; tunnels lead to valves FF, DD\n'
    'Valve FF has flow rate=0; tunnels lead to valves EE, GG\n'
    'Valve GG has flow rate=0; tunnels lead to valves FF, HH\n'
    'Valve HH has flow rate=22; tunnel leads to valve GG\n'
    'Valve II has flow rate=0; tunnels lead to valves AA, JJ\n'
    'Valve JJ has flow rate=21; tunnel leads to valve II'
)

@pytest.fixture
def sample_graph():

    return day16.Graph(
        valve_names=['AA', 'BB', 'CC', 'DD', 'EE', 'FF', 'GG', 'HH', 'II', 'JJ'],
        valve_flow_rates=[0, 13, 2, 20, 3, 0, 0, 22, 0, 21],
        tunnels={
            'AA': ['DD', 'II', 'BB'],
            'BB': ['CC', 'AA'],
            'CC': ['DD', 'BB'],
            'DD': ['CC', 'AA', 'EE'],
            'EE': ['FF', 'DD'],
            'FF': ['EE', 'GG'],
            'GG': ['FF', 'HH'],
            'HH': ['GG'],
            'II': ['AA', 'JJ'],
            'JJ': ['II']
        }
    )

def test_valve():
    valve_aa = day16.Valve(name='AA')
    valve_bb = day16.Valve(name='BB', flow_rate=13)

    assert valve_aa.flow_rate == 0
    assert valve_bb.flow_rate == 13
    assert valve_aa.name == 'AA'
    assert valve_aa.neighbours == set()
    assert valve_aa.distances == {}

def test_graph():
    graph = day16.Graph(
        valve_names=['AA', 'BB', 'CC', 'DD', 'EE', 'FF', 'GG', 'HH', 'II', 'JJ'],
        valve_flow_rates=[0, 13, 2, 20, 3, 0, 0, 22, 0, 21],
        tunnels={
            'AA': ['DD', 'II', 'BB'],
            'BB': ['CC', 'AA'],
            'CC': ['DD', 'BB'],
            'DD': ['CC', 'AA', 'EE'],
            'EE': ['FF', 'DD'],
            'FF': ['EE', 'GG'],
            'GG': ['FF', 'HH'],
            'HH': ['GG'],
            'II': ['AA', 'JJ'],
            'JJ': ['II']
        }
    )
    assert graph

def test_graph_from_str():
    graph = day16.Graph.from_str(INPUT_SAMPLE)
    assert graph

def test_graph_relevant_valves(sample_graph):
    assert len(sample_graph.relevant_valves) == 7

def test_graph_compute_valve_distances(sample_graph):
    sample_graph.compute_valve_distances('AA')
    sample_graph.compute_valve_distances('JJ')
    assert sample_graph.valves['AA'].distances == {
        'DD': 1, 'BB': 1, 'CC': 2, 'EE': 2, 'JJ': 2, 'HH': 5
    }
    assert sample_graph.valves['JJ'].distances == {
        'DD': 3, 'BB': 3, 'CC': 4, 'EE': 4, 'HH': 7
    }

def test_graph_compute_all_distances(sample_graph):
    with patch('day16.Graph.compute_valve_distances') as compute_dist_mock:
        sample_graph.compute_all_distances()
    assert compute_dist_mock.call_count == len(sample_graph.relevant_valves)

def test_graph_calculate_max_preasure_release(sample_graph):
    sample_graph.compute_all_distances()
    max_released_preasure = sample_graph.calculate_max_preasure_release()

    assert max_released_preasure == 1651

def test_generate_distribution_combinations():
    combinations = day16.generate_distribution_combinations([1, 2, 3, 4])
    assert combinations == [
        ([1, 2], [3, 4]),
        ([1, 3], [2, 4]),
        ([1, 4], [2, 3]),
    ]

def test_graph_calculate_max_preasure_release_with_help(sample_graph):
    sample_graph.compute_all_distances()
    max_released_preasure = sample_graph.calculate_max_preasure_release_with_help()

    assert max_released_preasure == 1707
