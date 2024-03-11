# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import itertools
import re
import sys
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Iterable

def generate_distribution_combinations(lst: Iterable[Any]) -> list[tuple[Any, Any]]:
    '''Generate all possible combinations of distributing a list into two parts'''

    combinations = itertools.combinations(lst, len(lst)//2)
    results = []
    for combo in combinations:
        complement = list(set(lst) - set(combo))
        combo = list(combo)
        if (combo, complement) not in results and (complement, combo) not in results:
            results.append((combo, complement))
    return results

@dataclass(unsafe_hash=True)
class Valve:
    name: str
    flow_rate: int = 0
    neighbours: set = field(default_factory=set, compare=False)
    distances: dict[str, int] = field(default_factory=dict, compare=False)

class Graph:
    def __init__(
        self,
        valve_names: list[str],
        valve_flow_rates: list[int],
        tunnels: dict[str, list[str]]
    ):
        self.valves = {
            name: Valve(name, flow_rate)
            for name, flow_rate in zip(valve_names, valve_flow_rates)
        }

        for valve in self.valves.values():
            valve.neighbours = set(tunnels[valve.name])

    @property
    def relevant_valves(self):
        return {
            name: valve
            for name, valve in self.valves.items()
            if valve.flow_rate or name == 'AA'
        }

    def compute_valve_distances(self, valve_name: str):

        valve = self.valves[valve_name]

        known = set()
        to_visit = deque()

        to_visit.append((valve, 0))
        known.add(valve.name)

        while to_visit:
            current_valve, distance = to_visit.popleft()

            if current_valve.flow_rate and distance > 0:
                valve.distances[current_valve.name] = distance

            for neighbour_name in current_valve.neighbours:
                if neighbour_name in known:
                    continue
                known.add(neighbour_name)
                to_visit.append((self.valves[neighbour_name], distance + 1))

    def compute_all_distances(self):
        for valve in self.relevant_valves.values():
            self.compute_valve_distances(valve.name)

    def calculate_max_preasure_release(
        self,
        current_valve: Valve | None = None,
        opened_valves: list[Valve] = None,
        opened_times: list[int] = None,
        remaining_time: int = 30,
        excluded_valves: list[Valve] = None
    ):
        current_valve = current_valve or self.valves['AA']
        opened_valves = opened_valves or []
        opened_times = opened_times or []
        excluded_valves = excluded_valves or []

        rates = [
            sum(
                valve.flow_rate * time
                for valve, time in zip(opened_valves, opened_times)
            )
        ]

        for valve_name, distance in current_valve.distances.items():
            valve = self.valves[valve_name]
            if remaining_time < distance + 1:
                continue
            if valve in excluded_valves:
                continue
            if valve in opened_valves:
                continue
            if not valve.flow_rate:
                continue

            rates.append(self.calculate_max_preasure_release(
                current_valve=valve,
                opened_valves=opened_valves + [valve],
                opened_times=opened_times + [remaining_time - distance - 1],
                remaining_time=remaining_time - distance - 1,
                excluded_valves=excluded_valves
            ))

        return max(rates)

    def calculate_max_preasure_release_with_help(self):
        current_max = 0
        valves = [
            valve for name, valve in self.relevant_valves.items()
            if name != 'AA'
        ]

        combos = generate_distribution_combinations(valves)
        for index, combo in enumerate(combos):
            if not index % 50:
                print(f'Analyzing combo {index+1} of {len(combos)}')
            elf_max = self.calculate_max_preasure_release(
                remaining_time=26, excluded_valves=combo[0]
            )
            elephant_max = self.calculate_max_preasure_release(
                remaining_time=26, excluded_valves=combo[1]
            )
            current_max = max(current_max, elf_max + elephant_max)
        return current_max

    @classmethod
    def from_str(cls, text: str) -> 'Graph':
        names = []
        flow_rates = []
        tunnels = {}

        pattern = re.compile(r'^Valve (\w\w) .*rate=(\d+).*valves? (.*)')
        for line in text.splitlines():
            name, flow_rate, valve_tunnels = pattern.findall(line)[0]
            flow_rate = int(flow_rate)
            valve_tunnels = [tunnel.strip() for tunnel in valve_tunnels.split(',')]
            names.append(name)
            flow_rates.append(flow_rate)
            tunnels[name] = valve_tunnels

        return Graph(names, flow_rates, tunnels)

def main():
    input_text = sys.stdin.read()
    graph = Graph.from_str(input_text)
    graph.compute_all_distances()
    max_pressure_release = graph.calculate_max_preasure_release()
    print(f'The max pressure release is {max_pressure_release}')


    print()

    max_pressure_release_with_help = graph.calculate_max_preasure_release_with_help()
    print(f'The max pressure release with help is {max_pressure_release_with_help}')


if __name__ == '__main__':
    main()
