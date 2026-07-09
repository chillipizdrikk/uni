import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox
import json
import os

class GraphicsEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Графічний редактор — Лабораторна №8")
        self.root.geometry("900x650")

        # Стан 
        self.line_color = "#000000"
        self.fill_color = "#ffffff"
        self.line_width = 2
        self.current_tool = "line"
        self.shapes = []           # список збережених фігур (вектор)
        self.selected_shapes = []
        self.clipboard = []
        self.start_x = self.start_y = 0
        self.preview_id = None     # id тимчасової фігури
        self.is_modified = False
        self.current_file = None

        self._build_menu()
        self._build_toolbar()
        self._build_canvas()
        self._build_statusbar()

    # UI 

    def _build_menu(self):
        menubar = tk.Menu(self.root)

        # File
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Новий файл",      accelerator="Ctrl+N", command=self.file_new)
        file_menu.add_command(label="Відкрити...",     accelerator="Ctrl+O", command=self.file_open)
        file_menu.add_command(label="Зберегти",        accelerator="Ctrl+S", command=self.file_save)
        file_menu.add_command(label="Зберегти як...",  accelerator="Ctrl+Shift+S", command=self.file_save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Вийти",           accelerator="Alt+F4", command=self.app_exit)
        menubar.add_cascade(label="Файл", menu=file_menu)

        # Edit
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Вирізати", accelerator="Ctrl+X", command=self.edit_cut)
        edit_menu.add_command(label="Копіювати", accelerator="Ctrl+C", command=self.edit_copy)
        edit_menu.add_command(label="Вставити", accelerator="Ctrl+V", command=self.edit_paste)
        edit_menu.add_command(label="Видалити останню фігуру", command=self.edit_delete_last)
        edit_menu.add_command(label="Вибрати все", accelerator="Ctrl+A", command=self.edit_select_all)
        menubar.add_cascade(label="Правка", menu=edit_menu)

        # Figures
        fig_menu = tk.Menu(menubar, tearoff=0)
        fig_menu.add_command(label="Лінія",      command=lambda: self.set_tool("line"))
        fig_menu.add_command(label="Прямокутник",command=lambda: self.set_tool("rect"))
        fig_menu.add_command(label="Еліпс",      command=lambda: self.set_tool("ellipse"))
        menubar.add_cascade(label="Фігури", menu=fig_menu)

        # Properties
        prop_menu = tk.Menu(menubar, tearoff=0)
        prop_menu.add_command(label="Колір лінії...",    command=self.choose_line_color)
        prop_menu.add_command(label="Колір заливки...",  command=self.choose_fill_color)
        prop_menu.add_command(label="Товщина лінії",     command=self.choose_line_width)
        menubar.add_cascade(label="Властивості", menu=prop_menu)

        self.root.config(menu=menubar)
        # Клавіші
        self.root.bind("<Control-n>", lambda e: self.file_new())
        self.root.bind("<Control-o>", lambda e: self.file_open())
        self.root.bind("<Control-s>", lambda e: self.file_save())
        self.root.bind("<Control-S>", lambda e: self.file_save_as())
        self.root.bind("<Control-a>", lambda e: self.edit_select_all())
        self.root.bind("<Control-c>", lambda e: self.edit_copy())
        self.root.bind("<Control-x>", lambda e: self.edit_cut())
        self.root.bind("<Control-v>", lambda e: self.edit_paste())

    def _build_toolbar(self):
        tb = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        tb.pack(side=tk.TOP, fill=tk.X)

        tools = [("Лінія", "line"), ("Прямокутник", "rect"), ("Еліпс", "ellipse")]
        for label, tool in tools:
            btn = tk.Button(tb, text=label, width=10,
                            command=lambda t=tool: self.set_tool(t))
            btn.pack(side=tk.LEFT, padx=2, pady=2)

        ttk.Separator(tb, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=4)

        # Кольори
        self.line_color_btn = tk.Button(tb, text="Колір лінії", width=10,
                                         bg=self.line_color, fg="white",
                                         command=self.choose_line_color)
        self.line_color_btn.pack(side=tk.LEFT, padx=2, pady=2)

        self.fill_color_btn = tk.Button(tb, text="Заливка", width=8,
                                         bg=self.fill_color,
                                         command=self.choose_fill_color)
        self.fill_color_btn.pack(side=tk.LEFT, padx=2, pady=2)

        ttk.Separator(tb, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=4)

        tk.Label(tb, text="Товщина:").pack(side=tk.LEFT)
        self.width_var = tk.IntVar(value=self.line_width)
        sp = tk.Spinbox(tb, from_=1, to=20, width=4, textvariable=self.width_var,
                        command=self._update_width)
        sp.pack(side=tk.LEFT, padx=2)

        ttk.Separator(tb, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=4)
        tk.Button(tb, text="Скасувати останню", command=self.edit_delete_last).pack(side=tk.LEFT, padx=2, pady=2)

    def _build_canvas(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(frame, bg="white", cursor="crosshair")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>",   self.on_mouse_down)
        self.canvas.bind("<B1-Motion>",       self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

    def _build_statusbar(self):
        self.status_var = tk.StringVar(value="Готово | Інструмент: Лінія")
        bar = tk.Label(self.root, textvariable=self.status_var,
                       bd=1, relief=tk.SUNKEN, anchor=tk.W)
        bar.pack(side=tk.BOTTOM, fill=tk.X)

    # Tools

    def set_tool(self, tool):
        self.current_tool = tool
        names = {"line": "Лінія", "rect": "Прямокутник", "ellipse": "Еліпс"}
        self.status_var.set(f"Готово | Інструмент: {names[tool]}")

    def _update_width(self):
        self.line_width = self.width_var.get()

    def choose_line_color(self):
        color = colorchooser.askcolor(color=self.line_color, title="Колір лінії")[1]
        if color:
            self.line_color = color
            self.line_color_btn.config(bg=color)

    def choose_fill_color(self):
        color = colorchooser.askcolor(color=self.fill_color, title="Колір заливки")[1]
        if color:
            self.fill_color = color
            self.fill_color_btn.config(bg=color)

    def choose_line_width(self):
        win = tk.Toplevel(self.root)
        win.title("Товщина лінії")
        win.geometry("200x80")
        win.resizable(False, False)
        var = tk.IntVar(value=self.line_width)
        tk.Label(win, text="Товщина (1–20):").pack(pady=5)
        sp = tk.Spinbox(win, from_=1, to=20, textvariable=var, width=6)
        sp.pack()
        def ok():
            self.line_width = var.get()
            self.width_var.set(self.line_width)
            win.destroy()
        tk.Button(win, text="OK", command=ok).pack(pady=5)

    # Mouse events

    def on_mouse_down(self, event):
        # Check for shape selection
        items = self.canvas.find_overlapping(event.x-1, event.y-1, event.x+1, event.y+1)
        if items:
            for item in items:
                for i, s in enumerate(self.shapes):
                    if s["canvas_id"] == item:
                        if i in self.selected_shapes:
                            self.selected_shapes.remove(i)
                        else:
                            self.selected_shapes.append(i)
                        self._update_selection()
                        return
        # Else start drawing
        self.start_x, self.start_y = event.x, event.y
        self.preview_id = None

    def on_mouse_move(self, event):
        if self.preview_id:
            self.canvas.delete(self.preview_id)
        self.preview_id = self._draw_shape(
            self.current_tool,
            self.start_x, self.start_y, event.x, event.y,
            self.line_color, self.fill_color, self.line_width,
            tags=("preview",)
        )

    def on_mouse_up(self, event):
        if self.preview_id:
            self.canvas.delete(self.preview_id)
            self.preview_id = None
        # Зберігаємо фігуру
        shape = {
            "type":  self.current_tool,
            "x1": self.start_x, "y1": self.start_y,
            "x2": event.x,      "y2": event.y,
            "line_color": self.line_color,
            "fill_color": self.fill_color,
            "line_width": self.line_width,
        }
        shape_id = self._draw_shape(
            shape["type"], shape["x1"], shape["y1"],
            shape["x2"],  shape["y2"],
            shape["line_color"], shape["fill_color"], shape["line_width"]
        )
        shape["canvas_id"] = shape_id
        self.shapes.append(shape)
        self.is_modified = True

    # Draw helpers

    def _draw_shape(self, kind, x1, y1, x2, y2, lc, fc, lw, tags=()):
        kwargs = dict(outline=lc, fill=fc, width=lw, tags=tags)
        if kind == "line":
            return self.canvas.create_line(x1, y1, x2, y2,
                                           fill=lc, width=lw, tags=tags)
        elif kind == "rect":
            return self.canvas.create_rectangle(x1, y1, x2, y2, **kwargs)
        elif kind == "ellipse":
            return self.canvas.create_oval(x1, y1, x2, y2, **kwargs)

    def _redraw_all(self):
        self.canvas.delete("all")
        for s in self.shapes:
            sid = self._draw_shape(
                s["type"], s["x1"], s["y1"], s["x2"], s["y2"],
                s["line_color"], s["fill_color"], s["line_width"]
            )
            s["canvas_id"] = sid
        self._update_selection()

    #Edit ops

    def _update_selection(self):
        for i, s in enumerate(self.shapes):
            if i in self.selected_shapes:
                if s["type"] == "line":
                    self.canvas.itemconfig(s["canvas_id"], fill="red")
                else:
                    self.canvas.itemconfig(s["canvas_id"], outline="red")
            else:
                if s["type"] == "line":
                    self.canvas.itemconfig(s["canvas_id"], fill=s["line_color"])
                else:
                    self.canvas.itemconfig(s["canvas_id"], outline=s["line_color"])

    def edit_select_all(self):
        self.selected_shapes = list(range(len(self.shapes)))
        self._update_selection()

    def edit_copy(self):
        self.clipboard = [{k: v for k, v in self.shapes[i].items() if k != "canvas_id"} for i in self.selected_shapes]

    def edit_cut(self):
        self.edit_copy()
        for i in sorted(self.selected_shapes, reverse=True):
            s = self.shapes.pop(i)
            self.canvas.delete(s["canvas_id"])
        self.selected_shapes = []
        self.is_modified = True

    def edit_paste(self):
        if not self.clipboard:
            return
        offset_x, offset_y = 20, 20
        for shape in self.clipboard:
            new_shape = shape.copy()
            new_shape["x1"] += offset_x
            new_shape["y1"] += offset_y
            new_shape["x2"] += offset_x
            new_shape["y2"] += offset_y
            sid = self._draw_shape(new_shape["type"], new_shape["x1"], new_shape["y1"], new_shape["x2"], new_shape["y2"], new_shape["line_color"], new_shape["fill_color"], new_shape["line_width"])
            new_shape["canvas_id"] = sid
            self.shapes.append(new_shape)
        self.is_modified = True
        self.selected_shapes = list(range(len(self.shapes) - len(self.clipboard), len(self.shapes)))
        self._update_selection()

    def edit_delete_last(self):
        if self.shapes:
            s = self.shapes.pop()
            self.canvas.delete(s["canvas_id"])
            self.is_modified = True

    def not_done(self):
        messagebox.showinfo("Не реалізовано", "Ця операція ще не доступна.")

    # File ops

    def _check_save(self):
        """Повертає False якщо користувач скасував збереження."""
        if not self.is_modified:
            return True
        answer = messagebox.askyesnocancel(
            "Зберегти?", "Малюнок змінено. Зберегти перед виходом?")
        if answer is None:
            return False
        if answer:
            return self.file_save()
        return True

    def file_new(self):
        if not self._check_save():
            return
        self.canvas.delete("all")
        self.shapes.clear()
        self.selected_shapes = []
        self.is_modified = False
        self.current_file = None
        self.root.title("Графічний редактор — Лабораторна №8")

    def file_open(self):
        if not self._check_save():
            return
        path = filedialog.askopenfilename(
            filetypes=[("JSON малюнки", "*.json"), ("Всі файли", "*.*")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.shapes = data.get("shapes", [])
            self._redraw_all()
            self.selected_shapes = []
            self.is_modified = False
            self.current_file = path
            self.root.title(f"Графічний редактор — {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося відкрити файл:\n{e}")

    def file_save(self):
        if self.current_file:
            self._write_file(self.current_file)
            return True
        return self.file_save_as()

    def file_save_as(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON малюнки", "*.json"), ("Всі файли", "*.*")])
        if not path:
            return False
        self._write_file(path)
        self.current_file = path
        self.root.title(f"Графічний редактор — {os.path.basename(path)}")
        return True

    def _write_file(self, path):
        data = {"shapes": [
            {k: v for k, v in s.items() if k != "canvas_id"}
            for s in self.shapes
        ]}
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.is_modified = False
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося зберегти файл:\n{e}")

    def app_exit(self):
        if self._check_save():
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicsEditor(root)
    root.mainloop()
