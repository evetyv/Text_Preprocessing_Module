

## Архитектура модуля

Модуль построен по **конвейерному принципу**: данные проходят через цепочку обработчиков, каждый делает свою часть работы.

```
src/
├── models.py              # Модели данных — сердце системы
├── file_loader.py         # Загрузка файлов (PDF, TXT)
├── text_normalizer.py     # Очистка и нормализация текста
├── formula_extractor.py   # Поиск и обработка математических формул
├── text_splitter.py       # Разбиение на смысловые блоки
├── metadata_extractor.py  # Извлечение метаданных
├── pipeline.py            # Главный конвейер (собирает всё вместе)
└── __init__.py           # Инициализация пакета
```


### Модели данных (`models.py`)

- **`Formula`** — математическая формула (оригинал, нормализованная версия, тип, позиция в тексте)
- **`TextChunk`** — текстовый блок (текст, формулы, метаданные)
- **`ProcessingResult`** — итоговый результат (все блоки + статистика)

##  Как использовать

```python
from src.pipeline import process_file

# Самый простой способ — одна функция на всё
result = process_file("лекция.pdf", "результат.json")

# Или без сохранения на диск (для передачи дальше)
result = process_file("лекция.pdf", output_path=None)
json_data = result.to_dict()  # Готовый JSON для генератора тестов
```

### Если нужна кастомизация:

```python
from src.pipeline import LectureProcessingPipeline
from src.text_splitter import SplitterType

# Создаём конвейер с нужными настройками
pipeline = LectureProcessingPipeline(
    detect_plain_text_formulas=True,  # Искать простые формулы
    splitter_type=SplitterType.SEMANTIC,  # Разбивать по смыслу
    min_chunk_size=100,  # Минимальный размер блока
    max_chunk_size=2000  # Максимальный размер блока
)

# Обрабатываем файл
result = pipeline.process("файл.pdf")

# Получаем результат
print(f"Обработано блоков: {len(result.chunks)}")
print(f"Найдено формул: {result.statistics.total_formulas}")
```

## Требования

- Python 3.10+
- Библиотеки (устанавливаются автоматически):
  - `PyMuPDF` — для работы с PDF
  - `pypdf2` — альтернатива для PDF
  - `python-docx` — для будущей поддержки DOCX
  - `nltk` — для обработки текста
  - `click` — для CLI (если нужен)

## Установка и запуск

1. **Склонировать репозиторий**
2. **Создать виртуальное окружение:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # или
   source venv/bin/activate  # Mac/Linux
   ```
3. **Установить зависимости:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Использовать как модуль** (см. примеры выше)
 
