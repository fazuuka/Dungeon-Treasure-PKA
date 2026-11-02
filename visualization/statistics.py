"""Formatting helpers for on-screen search metrics."""
def summary(result):
    if result is None:
        return [('Total cost', '-'), ('Path length', '-'),
                ('Explored nodes', '-'), ('Execution time', '-')]
    return [('Total cost', str(result.total_cost) if result.total_cost is not None else 'No path'),
            ('Path length', str(result.path_length) + ' steps'),
            ('Explored nodes', str(result.explored_nodes)),
            ('Execution time', f'{result.execution_ms:.3f} ms')]
