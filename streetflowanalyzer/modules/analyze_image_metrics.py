from typing import Dict, List
from torch import Tensor
from ultralytics.engine.results import Boxes
import numpy as np

from streetflowanalyzer.modules import ImageMetrics

def analyze_image_metrics(
    detections: Boxes, 
    image_area: int, 
    model_names: Dict[int, str], 
    target_classes: List[str]) -> ImageMetrics:
    """Анализирует результат детекции и возвращает метрики."""
    total_objects: int = 0
    areas_of_objects: List[int] = []
    image_height, image_width = detections.orig_shape
    union_mask = np.zeros((image_height, image_width), dtype=np.uint8)
    objects_counts_dict: Dict[str, int] = {name: 0 for name in target_classes}
    
    for box in detections:
        name_detected_object: str = model_names[int(box.cls[0])]
        
        if name_detected_object not in target_classes:
            continue
        
        objects_counts_dict[name_detected_object] += 1
        total_objects += 1
        coords = box.xyxy
        if isinstance(coords, Tensor):
            xyxy = coords.detach().cpu().numpy().astype(int)
        else:
            xyxy = coords.astype(int)

        x1, y1, x2, y2 = xyxy[0]
        union_mask[y1:y2, x1:x2] = 255
        object_area: int = (x2 - x1) * (y2 - y1)
        areas_of_objects.append(object_area)
        
    total_area: int = np.count_nonzero(union_mask).astype(int)
    
    density: float = total_area / image_area if image_area > 0 else 0.0
    avg_bbox_area: float =\
        np.mean(areas_of_objects).astype(float) if areas_of_objects else 0.0
    metrics = ImageMetrics(**{
        "total_vehicles":total_objects,
        "density":round(density, 4),
        "avg_bbox_area":round(avg_bbox_area, 2),
        **objects_counts_dict,
    })
    return metrics
