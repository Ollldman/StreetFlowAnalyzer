from typing import List


from streetflowanalyzer.modules import ImageMetrics
from streetflowanalyzer.modules import TrafficThresholds

def classify_scene(report: ImageMetrics, thresholds: TrafficThresholds) -> str:
# def classify_scene() -> str:
    scene_class_names: List[str] = [
        'Traffic Jam',
        'Heavy Traffic',
        'Sparse Traffic',
        'Single Big Object',
        'Empty'
    ]
    # Empty
    if report.total_vehicles == 0:
        return scene_class_names[4]
    
    # 'Traffic Jam'
    if report.density >= thresholds.jam_density \
        and report.total_vehicles >= thresholds.jam_count:
        return scene_class_names[0]
    
    # 'Heavy Traffic'
    elif report.total_vehicles >= thresholds.heavy_count:
        return scene_class_names[1]
    
    # Single Big Object
    elif report.density >= thresholds.single_density \
        and report.total_vehicles == 1:
        return scene_class_names[3]
    
    # 'Sparse Traffic'
    elif thresholds.jam_density > report.density \
        and report.total_vehicles < thresholds.heavy_count:
        return scene_class_names[2]
    
    
