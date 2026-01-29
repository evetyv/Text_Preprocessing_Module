"""
Командный интерфейс для системы обработки лекций.
"""

import argparse
import sys
import logging
from pathlib import Path

from src.pipeline import process_file, PipelineConfig
from src.text_splitter import SplitterType

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def main():
    """Основная функция CLI."""
    parser = argparse.ArgumentParser(
        description='Система обработки учебных материалов для генерации тестов',
        epilog='Пример: python -m src.cli process --input lecture.pdf --output result.json'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Команды')
    
    # Команда process
    process_parser = subparsers.add_parser('process', help='Обработка файла')
    process_parser.add_argument('--input', '-i', required=True, 
                               help='Входной файл (PDF, TXT)')
    process_parser.add_argument('--output', '-o', default='output.json',
                               help='Выходной JSON файл (по умолчанию: output.json)')
    process_parser.add_argument('--splitter', '-s', default='paragraph',
                               choices=['paragraph', 'semantic', 'fixed_size', 'mixed'],
                               help='Стратегия разбиения текста (по умолчанию: paragraph)')
    process_parser.add_argument('--min-chunk', type=int, default=100,
                               help='Минимальный размер блока в символах')
    process_parser.add_argument('--max-chunk', type=int, default=2000,
                               help='Максимальный размер блока в символах')
    process_parser.add_argument('--no-plain-text-formulas', action='store_true',
                               help='Не искать plain-text формулы')
    process_parser.add_argument('--verbose', '-v', action='store_true',
                               help='Подробный вывод')
    
    # Команда info
    info_parser = subparsers.add_parser('info', help='Информация о системе')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if args.command == 'process':
        process_command(args)
    elif args.command == 'info':
        info_command()
    else:
        parser.print_help()


def process_command(args):
    """Обработка команды process."""
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"Ошибка: файл не найден: {args.input}")
        sys.exit(1)
    
    # Преобразуем строку splitter в SplitterType
    splitter_type = SplitterType(args.splitter)
    
    # Конфигурация конвейера
    config = {
        'detect_plain_text_formulas': not args.no_plain_text_formulas,
        'splitter_type': splitter_type,
        'min_chunk_size': args.min_chunk,
        'max_chunk_size': args.max_chunk
    }
    
    print(f"Обработка файла: {args.input}")
    print(f"Стратегия разбиения: {args.splitter}")
    print(f"Поиск plain-text формул: {'да' if config['detect_plain_text_formulas'] else 'нет'}")
    print(f"Размер блоков: {args.min_chunk}-{args.max_chunk} символов")
    print("-" * 50)
    
    try:
        # Обрабатываем файл
        result = process_file(
            file_path=args.input,
            output_path=args.output,
            **config
        )
        
        print(f"Обработка завершена успешно!")
        print(f"Результат сохранен в: {args.output}")
        print()
        print("Статистика:")
        print(f"   Файл: {result.source_file}")
        print(f"   Блоков: {result.statistics.total_chunks}")
        print(f"   Формул: {result.statistics.total_formulas}")
        print(f"   Время обработки: {result.statistics.processing_time_seconds:.2f} сек")
        print(f"   Размер файла: {result.statistics.input_file_size_bytes} байт")
        
    except Exception as e:
        print(f"Ошибка при обработке: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def info_command():
    """Обработка команды info."""
    print("=" * 50)
    print("Система обработки учебных материалов")
    print("=" * 50)
    print()
    print("Поддерживаемые форматы:")
    print("   • TXT - текстовые файлы")
    print("   • PDF - документы PDF")
    print()
    print("Компоненты системы:")
    print("   1. Загрузка файлов (FileLoader)")
    print("   2. Нормализация текста (TextNormalizer)")
    print("   3. Поиск формул (FormulaExtractor)")
    print("   4. Разбиение на блоки (TextSplitter)")
    print("   5. Извлечение метаданных (MetadataExtractor)")
    print("   6. Формирование вывода (JSON)")
    print()
    print("Выходной формат (JSON):")
    print("   • process_id - уникальный идентификатор обработки")
    print("   • source_file - исходный файл")
    print("   • processed_at - время обработки")
    print("   • statistics - статистика обработки")
    print("   • chunks - массив текстовых блоков")
    print()
    print("Использование:")
    print("   python -m src.cli process --input lecture.pdf --output result.json")
    print("   python -m src.cli process -i lecture.txt -o output.json --splitter semantic")
    print("=" * 50)


