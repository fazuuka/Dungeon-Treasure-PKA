"""Run comparison without Pygame: python -m experiments.run_experiments"""
import csv
from pathlib import Path
from algorithms import ALGORITHMS
from experiments.scenarios import SCENARIOS, load_scenario


def collect():
    rows = []
    for scenario in SCENARIOS:
        dungeon = load_scenario(scenario)
        for name, algorithm in ALGORITHMS.items():
            result = algorithm(dungeon)
            rows.append({'scenario': scenario, 'algorithm': name,
                         'total_cost': result.total_cost, 'path_length': result.path_length,
                         'explored_nodes': result.explored_nodes,
                         'execution_ms': round(result.execution_ms, 4)})
    return rows


def main():
    rows = collect()
    output = Path(__file__).with_name('results.csv')
    with output.open('w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print('Scenario   Algorithm  Cost  Steps  Explored   Time(ms)')
    print('-' * 60)
    for row in rows:
        print(f"{row['scenario']:<10} {row['algorithm']:<10} {str(row['total_cost']):>4} "
              f"{row['path_length']:>6} {row['explored_nodes']:>9} {row['execution_ms']:>10.4f}")
    print(f'\nSaved to {output}')


if __name__ == '__main__':
    main()
