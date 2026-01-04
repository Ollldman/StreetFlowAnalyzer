from typing import Dict, List


def find_highlight_examples(all_reports: List[Dict], top_n: int=3) -> Dict:
    """Находит наиболее показательные примеры в наборе данных."""
    if len(all_reports) < top_n:
        print(f"  -> Найдено всего {len(all_reports)} отчётов, будут использованы все.")
        return {r['filename']: r for r in all_reports}

    most_crowded: List[Dict] = sorted(all_reports, key=lambda r: r['total_vehicles'], reverse=True)[:top_n]
    most_dense: List[Dict] = sorted(all_reports, key=lambda r: r['density'], reverse=True)[:top_n]

    top_examples: Dict = {r['filename']: r for r in most_crowded}

    top_examples.update({r['filename']: r for r in most_dense})

    return top_examples