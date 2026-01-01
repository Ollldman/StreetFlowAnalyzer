from pathlib import Path, PosixPath


def get_valid_image_paths(source_dir: str = "data/dataset") -> list[Path]:
    image_paths: list[Path] = []
    allowed_extensions: set[str] = {'.jpg', '.jpeg', '.png'}
    
    data_dir: Path = Path(source_dir)
    for file_name in data_dir.iterdir():
        if file_name.suffix in allowed_extensions:
            image_paths.append(file_name)
        else:
            continue
    return image_paths


