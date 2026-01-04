import os, cv2, csv, argparse
from ultralytics.models import YOLO
from tqdm import tqdm
import numpy as np

# typing:
from streetflowanalyzer.modules import ImageMetrics, TrafficThresholds
from ultralytics.engine.results import Results
from typing import Any, List, Dict
from pathlib import Path

# modules:
from streetflowanalyzer.modules import get_valid_image_paths
from streetflowanalyzer.modules import analyze_image_metrics
from streetflowanalyzer.modules import classify_scene
from streetflowanalyzer.modules import find_highlight_examples
from streetflowanalyzer.modules import generate_visualizations
from streetflowanalyzer.modules import PDFReport


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Инструмент для анализа дорожного трафика на основе YOLOv8.",
        formatter_class=argparse.RawTextHelpFormatter 
    )
    parser.add_argument(
        "mode", 
        choices=['experiment', 'report'],
        help="Режим работы скрипта:\n"
             " 'experiment' - запуск одного прогона для сбора CSV-статистики.\n"
             " 'report' - полный цикл анализа с генерацией PDF-отчёта."
    )
    parser.add_argument(
        "--conf", 
        type=float, 
        default=0.45, 
        help="Порог уверенности (confidence) для детекции. (По умолчанию: 0.45)"
    )

    args = parser.parse_args()
    # constants:
    SOURCE_PATH: str = 'data/dataset'
    TARGET_CLASSES: list[str] = ['car', 'truck']
    MODEL_NAME: str = 'yolov8n.pt'
    THRESHOLDS: TrafficThresholds = TrafficThresholds(
        jam_count = 10,       # Порог количества для пробки
        jam_density = 0.3,    # Порог плотности для пробки
        heavy_count = 5,      # Порог количества для плотного движения
        single_density = 0.15 # Порог плотности для крупного объекта
    )
    
    # Выбор режима работы на основе аргументов
    if args.mode == 'experiment':
        # Получаем список валидных изображений
        image_paths: List[Path] = get_valid_image_paths(SOURCE_PATH)
        model = YOLO(MODEL_NAME)
        # Готовимся собирать отчёты со всех изображений
        all_reports: List[Dict] = []
        
        # Основной цикл обработки, обёрнутый в tqdm для наглядности
        for path in tqdm(image_paths, desc=f"Анализ [conf={args.conf}]"):
            try:
                # Читаем изображение и получаем его размеры
                image = cv2.imread(str(path))
                h, w, _ = image.shape
                # Запускаем инференс с заданным `conf`
                results: List[Results] = model(image, conf=args.conf, verbose=False)
                # Извлекаем метрики из результатов детекции
                metrics: ImageMetrics = analyze_image_metrics(results[0].boxes, int(h * w), model.names, TARGET_CLASSES) #type:ignore
                # Дополняем отчёт информацией об изображении
                metrics['scene_type'] = classify_scene(metrics, THRESHOLDS)
                metrics['filename'] = str(path)
                all_reports.append(metrics.model_dump())
            except Exception as e:
                print(f"Критическая ошибка при обработке файла {path}: {e}")
        # Сохранение результатов в CSV-файл
        if all_reports:
            # Создаём папку для экспериментов, если она ещё не существует
            os.makedirs('experiments', exist_ok=True)
            # Имя файла будет отражать параметр, с которым проводился эксперимент
            csv_path = os.path.join('experiments', f'analysis_conf_{args.conf}.csv')

            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                # Заголовки берём из ключей первого словаря в списке
                writer = csv.DictWriter(f, fieldnames=all_reports[0].keys())
                writer.writeheader()
                writer.writerows(all_reports)

    elif args.mode == 'report':
        REPORT_OUTPUT_DIR = 'report_output'
        # Загружаем модель и собираем данные
        model = YOLO(MODEL_NAME)
        image_paths = get_valid_image_paths(SOURCE_PATH)
        
        all_reports = []
        for path in tqdm(image_paths, desc="Анализ изображений"):
            image = cv2.imread(str(path))
            h, w, _ = image.shape
            results = model(image, conf=args.conf, verbose=False)
            
            metrics = analyze_image_metrics(results[0].boxes, int(h * w), model.names, TARGET_CLASSES)
            metrics['scene_type'] = classify_scene(metrics, THRESHOLDS)
            metrics['filename'] = os.path.basename(path)
            all_reports.append(metrics.model_dump())

        if not all_reports:
            exit()
            
        # Курируем данные и создаём визуализации
        top_examples = find_highlight_examples(all_reports)
        annotated_examples = generate_visualizations(model, top_examples, SOURCE_PATH, REPORT_OUTPUT_DIR, args.conf)
        
        # Сборка PDF-отчёта
        pdf = PDFReport()
        pdf.add_page()
        
        # Общая сводка
        pdf.chapter_title("1. Общая сводка по проанализированным данным")
        total_vehicles_found = sum(r['total_vehicles'] for r in all_reports)
        total_cars = sum(r.get('car', 0) for r in all_reports)
        total_trucks = sum(r.get('truck', 0) for r in all_reports)
        scene_counts = {scene: len([r for r in all_reports if r['scene_type'] == scene]) for scene in ['Traffic Jam', 'Heavy Traffic', 'Sparse Traffic', 'Single Big Object', 'Empty']}

        summary_text = (
            f"Всего обработано изображений: {len(all_reports)}\n"
            f"Использованный порог уверенности: {args.conf}\n\n"
            f"ОБЩАЯ СТАТИСТИКА ТРАНСПОРТА:\n"
            f"  - Всего найдено ТС: {total_vehicles_found}\n"
            f"  - Легковые автомобили: {total_cars}\n"
            f"  - Грузовики: {total_trucks}\n\n"
            f"КЛАССИФИКАЦИЯ СЦЕН:\n"
            f"  - Пробка/Затор: {scene_counts['Traffic Jam']} изображений\n"
            f"  - Плотное движение: {scene_counts['Heavy Traffic']} изображений\n"
            f"  - Свободная дорога: {scene_counts['Sparse Traffic']} изображений\n"
            f"  - Аномалии (крупный объект): {scene_counts['Single Big Object']} изображений\n"
            f"  - Пустые сцены: {scene_counts['Empty']} изображений"
        )
        pdf.chapter_body(summary_text)

        # Визуальные примеры
        pdf.chapter_title("2. Примеры показательных сцен")
        sorted_examples = sorted(annotated_examples, key=lambda x: x['report']['density'], reverse=True)
        
        for i, example in enumerate(sorted_examples):
            title = f"Пример #{i+1}: {example['report']['filename']}"
            pdf.add_image_section(title, example['path'], example['stats'])

        # Сохранение файла
        pdf_output_path = os.path.join(REPORT_OUTPUT_DIR, "traffic_analysis_report.pdf")
        pdf.output(pdf_output_path)
        