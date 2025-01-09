import tkinter as tk
import psutil
import sqlite3
import time
from threading import Thread

class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")
        self.root.geometry("300x250")

        # Поле для ввода интервала обновления
        self.interval_label = tk.Label(root, text="Интервал обновления (сек):")
        self.interval_label.pack()

        self.interval_entry = tk.Entry(root)
        self.interval_entry.insert(0, "1")  # Значение по умолчанию: 1 секунда
        self.interval_entry.pack()

        # Метки для отображения информации
        self.cpu_label = tk.Label(root, text="ЦП: 0%")
        self.cpu_label.pack()

        self.ram_label = tk.Label(root, text="ОЗУ: 0/0 MB")
        self.ram_label.pack()

        self.disk_label = tk.Label(root, text="ПЗУ: 0/0 GB")
        self.disk_label.pack()

        # Кнопка для записи
        self.record_button = tk.Button(root, text="Начать запись", command=self.toggle_recording)
        self.record_button.pack()

        # Таймер
        self.timer_label = tk.Label(root, text="00:00")
        self.timer_label.pack()

        # Переменные состояния
        self.recording = False
        self.start_time = None
        self.timer_running = False  # Флаг для управления таймером
        self.db_conn = sqlite3.connect('system_monitor.db')
        self.create_table()

        # Запуск обновления информации
        self.update_system_info()

    def create_table(self):
        cursor = self.db_conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cpu_usage REAL,
                ram_usage REAL,
                disk_usage REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.db_conn.commit()

    def update_system_info(self):
        # Получаем интервал обновления из поля ввода
        try:
            interval = int(self.interval_entry.get())
            if interval < 1:
                interval = 1  # Минимальный интервал: 1 секунда
        except ValueError:
            interval = 1  # Если введено некорректное значение, используем 1 секунду

        # Получаем данные о системе
        cpu_usage = psutil.cpu_percent(interval=0.1)  # interval=0.1 для более точного измерения
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        # Обновляем метки
        self.cpu_label.config(text=f"ЦП: {cpu_usage}%")
        self.ram_label.config(text=f"ОЗУ: {ram.used / (1024 ** 2):.2f}/{ram.total / (1024 ** 2):.2f} MB")
        self.disk_label.config(text=f"ПЗУ: {disk.used / (1024 ** 3):.2f}/{disk.total / (1024 ** 3):.2f} GB")

        # Если запись активна, сохраняем данные в БД
        if self.recording:
            self.save_to_db(cpu_usage, ram.used / (1024 ** 2), disk.used / (1024 ** 3))

        # Планируем следующее обновление
        self.root.after(interval * 1000, self.update_system_info)

    def toggle_recording(self):
        if self.recording:
            # Останавливаем запись
            self.recording = False
            self.record_button.config(text="Начать запись")
            self.timer_running = False  # Останавливаем таймер
            self.timer_label.config(text="00:00")  # Сбрасываем таймер
            self.start_time = None
        else:
            # Начинаем запись
            self.recording = True
            self.record_button.config(text="Остановить")
            self.start_time = time.time()
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if self.recording and self.timer_running:
            elapsed_time = time.time() - self.start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            self.timer_label.config(text=f"{minutes:02}:{seconds:02}")
            self.root.after(1000, self.update_timer)  # Планируем следующее обновление таймера

    def save_to_db(self, cpu_usage, ram_usage, disk_usage):
        cursor = self.db_conn.cursor()
        cursor.execute('''
            INSERT INTO system_metrics (cpu_usage, ram_usage, disk_usage)
            VALUES (?, ?, ?)
        ''', (cpu_usage, ram_usage, disk_usage))
        self.db_conn.commit()

    def on_closing(self):
        self.db_conn.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()