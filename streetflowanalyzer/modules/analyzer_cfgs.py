from typing import Any
from pydantic import BaseModel, model_validator

class ImageMetrics(BaseModel):
    """Represents detection metrics derived from an analyzed image.

    This model validates the output dictionary returned by the `analyze_image_metrics`
    function. It enforces the presence and correct types of core metrics while allowing
    arbitrary additional fields that correspond to object class counts (e.g., 'car', 'truck').

    Expected fixed fields:
    - `total_vehicles`: Total number of detected objects belonging to the target classes.
    - `density`: Ratio of the total area covered by detected objects to the entire image area (0.0 to 1.0).
    - `avg_bbox_area`: Average area (in pixels) of bounding boxes for detected objects.

    Additional fields:
    - Any other top-level key is interpreted as a class name from `target_classes` and must be a
      non-negative integer representing the count of detected instances of that class.

    Validation:
    - All additional fields (beyond the three fixed ones) are validated to be non-negative integers.
    - Float fields are expected to be finite numbers (Pydantic's default float validation applies).

    Example:
        >>> metrics = ImageMetrics(
        ...     total_vehicles=5,
        ...     car=3,
        ...     truck=2,
        ...     density=0.1234,
        ...     avg_bbox_area=1500.0
        ... )
    """
    total_vehicles: int
    density: float
    avg_bbox_area: float

    # Разрешаем дополнительные поля (для подсчёта по классам)
    model_config = {"extra": "allow"}

    @model_validator(mode="after")
    def validate_class_counts(self) -> "ImageMetrics":
        # Проверяем, что все дополнительные поля — целые >= 0
        for key, value in self.__dict__.items():
            if key not in {"total_vehicles", "density", "avg_bbox_area"}:
                if not isinstance(value, int) or value < 0:
                    raise ValueError(f"Field '{key}' must be a non-negative integer.")
        return self

    def __setitem__(self, key:str, value: Any):
        self.__setattr__(key, value)
    
    def __getitem__(self, key: str):
        return self.__getattribute__(key)
    
    def keys(self):
        return self.__dict__.keys()

class TrafficThresholds(BaseModel):
    """Defines threshold values for classifying traffic conditions based on detection metrics.

    This model validates a configuration dictionary containing numeric thresholds used to
    interpret object detection results in traffic monitoring scenarios.

    Expected fields:
    - `jam_count`: Minimum number of detected vehicles required to classify the scene as a "traffic jam".
    - `jam_density`: Minimum object coverage density (ratio of occupied pixels to total image area)
                     to classify as a "traffic jam".
    - `heavy_count`: Minimum vehicle count to indicate "heavy traffic" (but not necessarily a jam).
    - `single_density`: Minimum density threshold to consider a single large object (e.g., a bus or truck)
                        as significant enough to influence traffic assessment.

    All values must be non-negative numbers. The model ensures type safety and serves as a
    contract for configuration loading (e.g., from JSON or YAML files).

    Example:
        >>> thresholds = TrafficThresholds(
        ...     jam_count=10,
        ...     jam_density=0.3,
        ...     heavy_count=5,
        ...     single_density=0.15
        ... )
    """

    jam_count: int
    jam_density: float
    heavy_count: int
    single_density: float