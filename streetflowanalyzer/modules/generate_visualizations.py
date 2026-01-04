import os, cv2
from ultralytics.models import YOLO
from typing import Dict, List


def generate_visualizations(
    model: YOLO, 
    examples_to_visualize: Dict, 
    source_dir: str, 
    output_dir: str, 
    conf: float) -> List[Dict]:
    """Создаёт визуальные артефакты (изображения с аннотациями) для отчёта."""
    annotated_results: List[Dict] = []
    
    os.makedirs(output_dir, exist_ok=True)
    
    for filename, report in examples_to_visualize.items():
        original_path = os.path.join(source_dir, filename)

        results = model(original_path, conf=conf, verbose=False)
        annotated_img = results[0].plot()

        save_path = os.path.join(output_dir, f"highlight_{filename}")
        cv2.imwrite(save_path, annotated_img)
        
        stats_text = (
            f"Имя файла: {report['filename']}\n"
            f"Тип сцены: {report.get('scene_type', 'N/A')}\n"
            f"Всего ТС: {report['total_vehicles']}\n"
            f"  - Легковые автомобили: {report.get('car', 0)}\n"
            f"  - Грузовики: {report.get('truck', 0)}\n"
            f"Плотность объектов: {report['density']:.2%}\n"
            f"Средний размер объекта: {report['avg_bbox_area']:.0f} пикс."
        )
        
        annotated_results.append({
            'path': save_path,
            'report': report,
            'stats': stats_text
        })
 
    return annotated_results
