import os
import sys
import shutil
import glob
import time
import datetime
import random
import string
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

HOME = os.path.expanduser("~")
DEFAULT_SANDBOX = os.path.join(HOME, "file_tools_sandbox")  # безпечна пісочниця за замовчуванням

def ts(path):
    "Повертає відформатований часовий штамп для файлу, використовуючи getctime."
    try:
        t = os.path.getctime(path)
        return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return f"error:{e}"

def safe_mkdir(path):
    # Створити папку, якщо не існує
    if not os.path.exists(path):
        os.makedirs(path)

def write_log(text_widget, message, newline=True):
    # Записати повідомлення у текстовий віджет та прокрутити вниз
    text_widget.insert(tk.END, message + ("\n" if newline else ""))
    text_widget.see(tk.END)

def human_size(path):
    # Повернути розмір файлу у читабельному вигляді
    try:
        s = os.path.getsize(path)
    except:
        return "?"
    for unit in ["B","KB","MB","GB"]:
        if s < 1024:
            return f"{s:.0f}{unit}"
        s /= 1024
    return f"{s:.1f}TB"


# Генерація зразкових даних
def create_sample_files_for_task1(folder):
    """
    Завдання 1:
    - Створює 10-12 файлів різних типів та штучно виставляє їхні часи зміни,
      щоб симулювати старі та нові файли.
    Коментар:
    - Використовує os.utime для зміни часу модифікації/доступу.
    """
    safe_mkdir(folder)
    names = ["a.txt","b.txt","notes.doc","script.py","image.jpg","data.csv","report.pdf","z.log","x.bin","readme.md","alpha.txt"]
    now = time.time()
    for i, name in enumerate(names):
        p = os.path.join(folder, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(f"Sample file {name}\nCreated for task1 demo.\n")
        # розподіляємо часи модифікації на різні дні
        age = (i - len(names)//2) * 86400  # зміщення у секундах (дні)
        t = now + age
        os.utime(p, (t, t))

def create_sample_folders_for_task2(base):
    """
    Завдання 2:
    - Створює дві папки з деякими дубльованими файлами (однакове ім'я + розмір)
      та іншими унікальними файлами.
    """
    f1 = os.path.join(base, "folderA")
    f2 = os.path.join(base, "folderB")
    safe_mkdir(f1); safe_mkdir(f2)
    # спільні дублікати
    common = {
        "dup1.txt": "This is duplicate file 1\n",
        "dup2.bin": "BINARYDATA" * 10,
        "shared.md": "# shared\n"
    }
    for name, content in common.items():
        p1 = os.path.join(f1, name)
        p2 = os.path.join(f2, name)
        with open(p1, "w", encoding="utf-8") as f: f.write(content)
        with open(p2, "w", encoding="utf-8") as f: f.write(content)
    # унікальні файли в кожній папці
    for i in range(5):
        with open(os.path.join(f1, f"uniqueA_{i}.txt"), "w", encoding="utf-8") as f:
            f.write("A"+str(i))
        with open(os.path.join(f2, f"uniqueB_{i}.txt"), "w", encoding="utf-8") as f:
            f.write("B"+str(i))

def create_sample_tree_for_task3(base):
    """
    Завдання 3:
    - Створює папку з 4 підпапками, у кожній по кілька файлів різних типів.
    """
    safe_mkdir(base)
    subnames = ["sub1","sub2","sub3","sub4"]
    exts = [".py", ".txt", ".doc", ".jpg", ".json"]
    for sub in subnames:
        d = os.path.join(base, sub)
        safe_mkdir(d)
        for i in range(6):
            ext = random.choice(exts)
            name = f"file_{i}{ext}"
            with open(os.path.join(d, name), "w", encoding="utf-8") as f:
                f.write(f"This is {name} in {sub}\n")

def create_sample_for_task4(base):
    """
    Завдання 4:
    - Створює одну папку з 11 файлами трьох типів (.txt, .py, .jpg)
      для тестування розподілу по типам.
    """
    safe_mkdir(base)
    types = [".txt", ".py", ".jpg"]
    for i in range(11):
        ext = types[i % len(types)]
        p = os.path.join(base, f"task4_{i}{ext}")
        # .jpg записано як текстовий файл для простоти
        with open(p, "w", encoding="utf-8") as f:
            f.write(f"sample {i} of type {ext}\n")

# Реалізації завдань
def task1_find_oldest_newest(folder, text_widget):
    """
    Завдання 1:
    - Оглядає папку (без рекурсії) на наявність файлів.
    - Сортує за часом створення (os.path.getctime).
    - Виводить два найдавніші та два найновіші файли та повний список для порівняння.
    Коментар:
    - getctime може відрізнятися по значенню в залежності від ОС.
    """
    write_log(text_widget, f"Task 1: Scanning folder: {folder}")
    try:
        entries = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    except Exception as e:
        write_log(text_widget, f"Error reading folder: {e}")
        return
    if not entries:
        write_log(text_widget, "No files found.")
        return
    entries.sort(key=lambda p: os.path.getctime(p))
    write_log(text_widget, "\nFull list (sorted by creation time):")
    for p in entries:
        write_log(text_widget, f"{os.path.basename(p):30} {ts(p)} size={human_size(p)}")
    write_log(text_widget, "\nTwo oldest:")
    for p in entries[:2]:
        write_log(text_widget, f"{os.path.basename(p):30} {ts(p)}")
    write_log(text_widget, "\nTwo newest:")
    for p in entries[-2:]:
        write_log(text_widget, f"{os.path.basename(p):30} {ts(p)}")
    write_log(text_widget, "-"*60)

def task2_find_duplicates(folder1, folder2, text_widget):
    """
    Завдання 2:
    - Знаходить дублікати файлів за критерієм ім'я + розмір у двох папках.
    - Виводить імена файлів та шляхи в яких вони знаходяться.
    Коментар:
    - Це швидка евристика; для надійнішої перевірки можна використовувати хеші (md5/sha1).
    """
    write_log(text_widget, f"Task 2: Comparing folders:\n  A: {folder1}\n  B: {folder2}")
    def map_files(folder):
        d = {}
        try:
            for f in os.listdir(folder):
                p = os.path.join(folder, f)
                if os.path.isfile(p):
                    d[f] = os.path.getsize(p)
        except Exception as e:
            write_log(text_widget, f"Error reading {folder}: {e}")
        return d
    m1 = map_files(folder1)
    m2 = map_files(folder2)
    duplicates = []
    for name, size in m1.items():
        if name in m2 and m2[name] == size:
            duplicates.append((name, size))
    if duplicates:
        write_log(text_widget, "\nDuplicates found (name, size):")
        for name, size in duplicates:
            write_log(text_widget, f"{name:30} {size} bytes  locations: {os.path.join(folder1,name)} , {os.path.join(folder2,name)}")
    else:
        write_log(text_widget, "No duplicates found by name+size.")
    write_log(text_widget, "-"*60)

def task3_list_by_type(parent_folder, extension, text_widget):
    """
    Завдання 3:
    - Для батьківської папки з кількома підпапками перераховує файли з вказаним розширенням
      по всіх неглибоких підпапках (тільки перший рівень).
    Коментар:
    - Розширення може бути передане з крапкою або без; функція нормалізує його.
    """
    write_log(text_widget, f"Task 3: Listing *.{extension} files in immediate subfolders of {parent_folder}")
    ext = extension if extension.startswith(".") else "." + extension
    try:
        subs = [os.path.join(parent_folder, d) for d in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, d))]
    except Exception as e:
        write_log(text_widget, f"Error reading parent folder: {e}")
        return
    result = []
    for s in subs:
        for f in os.listdir(s):
            if os.path.isfile(os.path.join(s,f)) and os.path.splitext(f)[1].lower() == ext.lower():
                result.append((s, f))
    if result:
        write_log(text_widget, f"Found {len(result)} files with extension {ext}:")
        for s,f in result:
            write_log(text_widget, f"{os.path.join(s,f)}")
    else:
        write_log(text_widget, f"No files with extension {ext} found in immediate subfolders.")
    write_log(text_widget, "-"*60)

def task4_split_by_type(folder, text_widget, simulate=True):
    """
    Завдання 4:
    - У вказаній папці визначає розширення файлів.
    - Для кожного розширення створює окрему папку і переміщує (або копіює, якщо simulate=True) файли цього типу туди.
    Коментар:
    - Операція виконується лише після явного підтвердження якщо папка не у песочниці.
    """
    write_log(text_widget, f"Task 4: Splitting files by type in folder: {folder}")
    try:
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    except Exception as e:
        write_log(text_widget, f"Error reading folder: {e}")
        return
    if not files:
        write_log(text_widget, "No files to process.")
        return
    # Збіг розширень
    ext_map = {}
    for f in files:
        ext = os.path.splitext(f)[1].lower().lstrip(".")
        if ext == "":
            ext = "no_ext"
        ext_map.setdefault(ext, []).append(f)
    write_log(text_widget, f"Detected types: {', '.join(ext_map.keys())}")
    # створити папки та перемістити/скопіювати файли
    for ext, flist in ext_map.items():
        target = os.path.join(folder, f"folder_{ext}")
        write_log(text_widget, f"Preparing folder for .{ext}: {target}  (files: {len(flist)})")
        safe_mkdir(target)
        for f in flist:
            src = os.path.join(folder, f)
            dst = os.path.join(target, f)
            try:
                if simulate:
                    # копіюємо щоб уникнути руйнівних змін
                    shutil.copy2(src, dst)
                    write_log(text_widget, f"Copied {f} -> {target}")
                else:
                    # переміщаємо файл (видаляючи з початкової папки)
                    shutil.move(src, dst)
                    write_log(text_widget, f"Moved {f} -> {target}")
            except Exception as e:
                write_log(text_widget, f"Error processing {f}: {e}")
    write_log(text_widget, "Task 4 completed.")
    write_log(text_widget, "-"*60)

# Графічний інтерфейс
class FileToolsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File and Directory Tools (tkinter)")
        self.geometry("900x600")
        self._build_ui()

    def _build_ui(self):
        # Меню
        menubar = tk.Menu(self)
        sandbox_menu = tk.Menu(menubar, tearoff=0)
        sandbox_menu.add_command(label="Create sandbox and sample data", command=self.create_sandbox_dialog)
        sandbox_menu.add_separator()
        sandbox_menu.add_command(label="Open sandbox folder", command=lambda: self.open_path(DEFAULT_SANDBOX))
        menubar.add_cascade(label="Sandbox", menu=sandbox_menu)
        menubar.add_command(label="Export results", command=self.export_results)
        self.config(menu=menubar)

        # Верхня панель: кнопки та опції
        top = ttk.Frame(self)
        top.pack(side=tk.TOP, fill=tk.X, padx=6, pady=6)

        # Завдання 1
        b1 = ttk.Button(top, text="Task 1: Oldest/Newest", command=self.run_task1)
        b1.grid(row=0, column=0, padx=3, pady=3)

        # Завдання 2
        b2 = ttk.Button(top, text="Task 2: Find duplicates", command=self.run_task2)
        b2.grid(row=0, column=1, padx=3, pady=3)

        # Завдання 3
        b3 = ttk.Button(top, text="Task 3: List by type", command=self.run_task3)
        b3.grid(row=0, column=2, padx=3, pady=3)

        # Завдання 4
        b4 = ttk.Button(top, text="Task 4: Split by type", command=self.run_task4)
        b4.grid(row=0, column=3, padx=3, pady=3)

        # Прапорець симуляції (щоб уникнути руйнівних операцій)
        self.simulate_var = tk.BooleanVar(value=True)
        c = ttk.Checkbutton(top, text="Simulate (copy instead of move/delete)", variable=self.simulate_var)
        c.grid(row=0, column=4, padx=10, pady=3, sticky=tk.W)

        # Кнопки швидкої генерації зразків у песочниці
        sample_frame = ttk.LabelFrame(top, text="Quick samples (sandbox)")
        sample_frame.grid(row=1, column=0, columnspan=5, sticky=tk.W+tk.E, padx=3, pady=3)
        ttk.Button(sample_frame, text="Create sample for Task1", command=self.sample_task1).grid(row=0,column=0,padx=3,pady=3)
        ttk.Button(sample_frame, text="Create sample for Task2", command=self.sample_task2).grid(row=0,column=1,padx=3,pady=3)
        ttk.Button(sample_frame, text="Create sample for Task3", command=self.sample_task3).grid(row=0,column=2,padx=3,pady=3)
        ttk.Button(sample_frame, text="Create sample for Task4", command=self.sample_task4).grid(row=0,column=3,padx=3,pady=3)

        # Основна текстова область для логів/результатів
        text_frame = ttk.Frame(self)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        self.text = tk.Text(text_frame, wrap=tk.NONE)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # вертикальний скролбар
        vsb = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text.yview)
        vsb.pack(side=tk.LEFT, fill=tk.Y)
        self.text.configure(yscrollcommand=vsb.set)
        # горизонтальний скролбар
        hsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.text.xview)
        hsb.pack(fill=tk.X)
        self.text.configure(xscrollcommand=hsb.set)

        # Нижня панель з інструкцією та кнопкою експорту
        bottom = ttk.Frame(self)
        bottom.pack(side=tk.BOTTOM, fill=tk.X, padx=6, pady=6)
        ttk.Label(bottom, text="Result export:").grid(row=0,column=0,sticky=tk.W)
        ttk.Button(bottom, text="Export results to results.txt", command=self.export_results).grid(row=0,column=1,padx=3)

    def open_path(self, path):
        # Відкрити шлях у файловому менеджері платформи
        if not os.path.exists(path):
            messagebox.showinfo("Open folder", f"Path does not exist:\n{path}")
            return
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform.startswith("darwin"):
            os.system(f'open "{path}"')
        else:
            os.system(f'xdg-open "{path}"')

    def create_sandbox_dialog(self):
        # Створити песочницю, якщо її ще немає
        if os.path.exists(DEFAULT_SANDBOX):
            if not messagebox.askyesno("Sandbox exists", f"{DEFAULT_SANDBOX} already exists.\nOverwrite/create missing?"):
                return
        safe_mkdir(DEFAULT_SANDBOX)
        write_log(self.text, f"Sandbox created at: {DEFAULT_SANDBOX}")

    def sample_task1(self):
        # Генерувати зразки для завдання 1
        folder = os.path.join(DEFAULT_SANDBOX, "task1")
        create_sample_files_for_task1(folder)
        write_log(self.text, f"Sample for task1 created at: {folder}")
        self.open_path(DEFAULT_SANDBOX)

    def sample_task2(self):
        # Генерувати зразки для завдання 2
        base = os.path.join(DEFAULT_SANDBOX, "task2")
        create_sample_folders_for_task2(base)
        write_log(self.text, f"Sample for task2 created at: {base}")
        self.open_path(DEFAULT_SANDBOX)

    def sample_task3(self):
        # Генерувати зразки для завдання 3
        base = os.path.join(DEFAULT_SANDBOX, "task3")
        create_sample_tree_for_task3(base)
        write_log(self.text, f"Sample for task3 created at: {base}")
        self.open_path(DEFAULT_SANDBOX)

    def sample_task4(self):
        # Генерувати зразки для завдання 4
        base = os.path.join(DEFAULT_SANDBOX, "task4")
        create_sample_for_task4(base)
        write_log(self.text, f"Sample for task4 created at: {base}")
        self.open_path(DEFAULT_SANDBOX)

    def run_task1(self):
        # Запустити завдання 1: вибір папки та обробка
        folder = filedialog.askdirectory(title="Select folder for Task 1 (non-recursive scan)", initialdir=DEFAULT_SANDBOX)
        if not folder:
            return
        write_log(self.text, f"\n[RUN] Task 1 at {folder}")
        task1_find_oldest_newest(folder, self.text)

    def run_task2(self):
        # Запустити завдання 2: вибір двох папок
        folder1 = filedialog.askdirectory(title="Select first folder (A) for Task 2", initialdir=DEFAULT_SANDBOX)
        if not folder1:
            return
        folder2 = filedialog.askdirectory(title="Select second folder (B) for Task 2", initialdir=DEFAULT_SANDBOX)
        if not folder2:
            return
        write_log(self.text, f"\n[RUN] Task 2 comparing {folder1} and {folder2}")
        task2_find_duplicates(folder1, folder2, self.text)

    def run_task3(self):
        # Запустити завдання 3: вибір батьківської папки та введення розширення
        parent = filedialog.askdirectory(title="Select parent folder (with 4 immediate subfolders) for Task 3", initialdir=DEFAULT_SANDBOX)
        if not parent:
            return
        # простий діалог для введення розширення
        ext = simple_input_dialog(self, "Extension", "Enter file extension to list (e.g. txt, py, jpg):")
        if not ext:
            return
        write_log(self.text, f"\n[RUN] Task 3 in {parent} for .{ext}")
        task3_list_by_type(parent, ext, self.text)

    def run_task4(self):
        # Запустити завдання 4: вибір папки та виконання розподілу
        folder = filedialog.askdirectory(title="Select folder with files to split (Task 4)", initialdir=DEFAULT_SANDBOX)
        if not folder:
            return
        simulate = self.simulate_var.get()
        if not simulate:
            # підтвердження руйнівної дії поза песочницею
            if not folder.startswith(DEFAULT_SANDBOX):
                ok = messagebox.askyesno("Confirm destructive op", "You are about to MOVE files outside the sandbox. Are you sure?")
                if not ok:
                    write_log(self.text, "Operation cancelled by user.")
                    return
            else:
                ok = messagebox.askyesno("Confirm move", f"This will MOVE files from {folder} into subfolders. Proceed?")
                if not ok:
                    write_log(self.text, "Operation cancelled by user.")
                    return
        write_log(self.text, f"\n[RUN] Task 4 in {folder}  simulate={simulate}")
        task4_split_by_type(folder, self.text, simulate=simulate)

    def export_results(self):
        # Зберегти текст з області логів у файл
        save = filedialog.asksaveasfilename(title="Save results to text file", defaultextension=".txt", initialdir=DEFAULT_SANDBOX, initialfile="results.txt")
        if not save:
            return
        try:
            with open(save, "w", encoding="utf-8") as f:
                f.write(self.text.get("1.0", tk.END))
            messagebox.showinfo("Export complete", f"Results saved to:\n{save}")
            write_log(self.text, f"Results exported to: {save}")
        except Exception as e:
            messagebox.showerror("Save error", str(e))


def simple_input_dialog(parent, title, prompt):
    # Простіший діалог для отримання рядка від користувача (модальний)
    d = tk.Toplevel(parent)
    d.title(title)
    d.transient(parent)
    d.grab_set()
    ttk.Label(d, text=prompt).pack(padx=10, pady=6)
    entry = ttk.Entry(d)
    entry.pack(padx=10, pady=6)
    entry.focus_set()
    result = {"value": None}
    def ok():
        result["value"] = entry.get().strip()
        d.destroy()
    def cancel():
        d.destroy()
    btnf = ttk.Frame(d)
    btnf.pack(pady=6)
    ttk.Button(btnf, text="OK", command=ok).pack(side=tk.LEFT, padx=6)
    ttk.Button(btnf, text="Cancel", command=cancel).pack(side=tk.LEFT, padx=6)
    parent.wait_window(d)
    return result["value"]

if __name__ == "__main__":
    app = FileToolsApp()
    app.mainloop()