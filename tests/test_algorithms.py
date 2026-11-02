import unittest
from algorithms import ALGORITHMS
from experiments.scenarios import SCENARIOS, load_scenario
from game.map import DungeonMap


class TestAlgorithms(unittest.TestCase):
    def test_all_scenarios(self):
        for scenario in SCENARIOS:
            dungeon = load_scenario(scenario)
            outputs = {name: fn(dungeon) for name, fn in ALGORITHMS.items()}
            for name, result in outputs.items():
                with self.subTest(scenario=scenario, algorithm=name):
                    self.assertTrue(result.path, 'Scenario should be solvable')
                    self.assertEqual(result.path[0], dungeon.start)
                    self.assertEqual(result.path[-1], dungeon.goal)
                    self.assertEqual(result.total_cost, dungeon.cost_of_path(result.path))
                    self.assertEqual(result.path_length, len(result.path) - 1)
                    for a, b in zip(result.path, result.path[1:]):
                        self.assertIn(b, list(dungeon.neighbors(a)))
            self.assertEqual(outputs['UCS'].total_cost, outputs['A*'].total_cost)
            self.assertLessEqual(outputs['UCS'].total_cost, outputs['Greedy'].total_cost)

    def test_weighted_detour(self):
        dungeon = DungeonMap(['SLLLT', '.....'])
        self.assertEqual(ALGORITHMS['UCS'](dungeon).total_cost, 6)
        self.assertEqual(ALGORITHMS['A*'](dungeon).total_cost, 6)

    def test_unreachable(self):
        dungeon = DungeonMap(['S#T', '###', '...'])
        for fn in ALGORITHMS.values():
            self.assertIsNone(fn(dungeon).total_cost)


if __name__ == '__main__':
    unittest.main()
