# System Monitor Desktop Application

Это desktop-приложение для мониторинга загруженности системы (CPU, RAM, Disk) в реальном времени. Приложение работает на Linux и предоставляет возможность записи данных в базу данных SQLite.

## Возможности

- **Отображение текущей загруженности:**
  - ЦП (CPU)
  - ОЗУ (RAM)
  - ПЗУ (Disk)

- **Возможность задания интервала обновления данных (в секундах).**
- **Запись данных в базу данных SQLite.**
- **Таймер, отображающий время с начала записи.**

## Требования

- Python 3.6 или выше.
- Библиотека `psutil` для получения данных о системе.
- Библиотека `tkinter` для графического интерфейса (обычно входит в стандартную библиотеку Python).

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/GeorgeYulpatov/SystemMonitor.git
   cd SystemMonitorProject
   ```
2. Установите необходимые зависимости:

   ```bash
   pip install psutil
   ```

3. Убедитесь, что tkinter установлен в вашей системе. Если нет, установите его:

 - Для Debian/Ubuntu:
   ```bash
   sudo apt update
   sudo apt install python3-tk
   ```
 - Для Fedora:
   ```bash
   sudo dnf install python3-tkinter
   ```
 - Для Arch Linux:
   ```bash
   sudo pacman -S tk
   ```


## Запуск приложения
1. Перейдите в директорию проекта:

   ```bash
   cd SystemMonitorProject
   ```
2. Запустите приложение:
   ```bash
   python3 system_monitor.py
   ```
   
## Использование
1. Интервал обновления:

- Введите желаемый интервал обновления (в секундах) в поле "Интервал обновления (сек):".

- По умолчанию интервал равен 1 секунде.

2. Запись данных:

- Нажмите кнопку "Начать запись", чтобы начать запись данных в базу данных.

- Нажмите кнопку "Остановить", чтобы прекратить запись.

3. Таймер:

- Во время записи отображается таймер, показывающий время с начала записи.

4. База данных:

- Данные записываются в файл system_monitor.db (SQLite).

- Таблица system_metrics содержит следующие поля:

  - cpu_usage: Загруженность CPU в процентах.

  - ram_usage: Используемая оперативная память в МБ.

  - disk_usage: Используемое дисковое пространство в ГБ.

  - timestamp: Временная метка записи.

# Пример данных в базе данных
   ```sql
   sqlite3 system_monitor.db
   sqlite> SELECT * FROM system_metrics;
   ```

Пример вывода:

   ```
id | cpu_usage | ram_usage | disk_usage | timestamp
---|-----------|-----------|------------|-------------------
1  | 15.3      | 2048.50   | 50.25      | 2023-10-10 12:00:00
2  | 20.1      | 2050.00   | 50.30      | 2023-10-10 12:00:01
   ```
# Структура проекта
   ```
SystemMonitorProject/
├── system_monitor.py  # Основной файл приложения
├── system_monitor.db  # База данных SQLite (создается автоматически)
├── README.md          # Документация
└── requirements.txt   # Зависимости (опционально)
   ```
# Лицензия
Этот проект распространяется под лицензией MIT. Подробнее см. в файле LICENSE.
