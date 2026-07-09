import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
import json, os, copy

SEL_COLOR  = "#0078D7"   # колір рамки виокремлення
SEL_DASH   = (4, 4)      # пунктир виокремлення

class GraphicsEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Графічний редактор — Лабораторна №9")
        self.root.geometry("960x680")

        # параметри малювання
        self.line_color = "#000000"
        self.fill_color = "#ffffff"
        self.line_width = 2
        self.current_tool = "line"   # line | rect | ellipse | select

        # стан фігур
        self.shapes: list[dict] = []      # всі зафіксовані фігури
        self.clipboard: list[dict] = []   # буфер обміну
        self.selected_idx: list[int] = [] # індекси виокремлених фігур
        self.sel_rect_id = None           # canvas-id рамки виокремлення

        # стан поточного малювання
        self.drawing = False
        self.start_x = self.start_y = 0
        self.preview_id = None

        # стан переміщення виокремлених фігур
        self.moving = False
        self.move_last_x = self.move_last_y = 0

        # UNDO / REDO (стек знімків стану self.shapes)
        self._undo_stack: list[list[dict]] = []
        self._redo_stack: list[list[dict]] = []

        # файл
        self.is_modified = False
        self.current_file = None

        self._build_menu()
        self._build_toolbar()
        self._build_canvas()
        self._build_statusbar()

    # побудова інтерфейсу

    def _build_menu(self):
        mb = tk.Menu(self.root)

        # Файл
        fm = tk.Menu(mb, tearoff=0)
        fm.add_command(label="Новий файл", accelerator="Ctrl+N", command=self.file_new)
        fm.add_command(label="Відкрити...", accelerator="Ctrl+O", command=self.file_open)
        fm.add_command(label="Зберегти", accelerator="Ctrl+S", command=self.file_save)
        fm.add_command(label="Зберегти як...", accelerator="Ctrl+Shift+S", command=self.file_save_as)
        fm.add_separator()
        fm.add_command(label="Вийти", command=self.app_exit)
        mb.add_cascade(label="Файл", menu=fm)

        # Правка
        em = tk.Menu(mb, tearoff=0)
        em.add_command(label="Скасувати (Undo)", accelerator="Ctrl+Z",  command=self.undo)
        em.add_command(label="Повернути (Redo)", accelerator="Ctrl+Y",  command=self.redo)
        em.add_separator()
        em.add_command(label="Вирізати", accelerator="Ctrl+X", command=self.edit_cut)
        em.add_command(label="Копіювати", accelerator="Ctrl+C", command=self.edit_copy)
        em.add_command(label="Вставити", accelerator="Ctrl+V", command=self.edit_paste)
        em.add_separator()
        em.add_command(label="Вибрати все", accelerator="Ctrl+A", command=self.edit_select_all)
        em.add_command(label="Зняти виокремлення",                       command=self.edit_deselect)
        em.add_command(label="Видалити виокремлені",accelerator="Delete",command=self.edit_delete_selected)
        mb.add_cascade(label="Правка", menu=em)

        # Фігури
        fig = tk.Menu(mb, tearoff=0)
        fig.add_command(label="Лінія",      command=lambda: self.set_tool("line"))
        fig.add_command(label="Прямокутник",command=lambda: self.set_tool("rect"))
        fig.add_command(label="Еліпс",      command=lambda: self.set_tool("ellipse"))
        fig.add_separator()
        fig.add_command(label="Виокремлення/Переміщення", command=lambda: self.set_tool("select"))
        mb.add_cascade(label="Фігури", menu=fig)

        # Властивості
        pr = tk.Menu(mb, tearoff=0)
        pr.add_command(label="Колір лінії...",   command=self.choose_line_color)
        pr.add_command(label="Колір заливки...", command=self.choose_fill_color)
        pr.add_command(label="Товщина лінії",    command=self.choose_line_width)
        mb.add_cascade(label="Властивості", menu=pr)

        self.root.config(menu=mb)

        # гарячі клавіші
        bind = self.root.bind
        bind("<Control-n>", lambda e: self.file_new())
        bind("<Control-o>", lambda e: self.file_open())
        bind("<Control-s>", lambda e: self.file_save())
        bind("<Control-S>", lambda e: self.file_save_as())
        bind("<Control-z>", lambda e: self.undo())
        bind("<Control-y>", lambda e: self.redo())
        bind("<Control-a>", lambda e: self.edit_select_all())
        bind("<Control-c>", lambda e: self.edit_copy())
        bind("<Control-x>", lambda e: self.edit_cut())
        bind("<Control-v>", lambda e: self.edit_paste())
        bind("<Delete>",    lambda e: self.edit_delete_selected())
        bind("<Escape>",    lambda e: self.on_escape())

    def _build_toolbar(self):
        tb = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        tb.pack(side=tk.TOP, fill=tk.X)

        tools = [("Лінія","line"),("Прямокутник","rect"),("Еліпс","ellipse"),("☑ Виокремити","select")]
        self._tool_btns = {}
        for lbl, tool in tools:
            b = tk.Button(tb, text=lbl, width=11, command=lambda t=tool: self.set_tool(t))
            b.pack(side=tk.LEFT, padx=2, pady=2)
            self._tool_btns[tool] = b

        tk.Frame(tb, width=2, bd=1, relief=tk.SUNKEN).pack(side=tk.LEFT, fill=tk.Y, padx=4)

        self.line_color_btn = tk.Button(tb, text="Колір лінії", width=10,
                                        bg=self.line_color, fg="white",
                                        command=self.choose_line_color)
        self.line_color_btn.pack(side=tk.LEFT, padx=2, pady=2)

        self.fill_color_btn = tk.Button(tb, text="Заливка", width=8,
                                        bg=self.fill_color,
                                        command=self.choose_fill_color)
        self.fill_color_btn.pack(side=tk.LEFT, padx=2, pady=2)

        tk.Frame(tb, width=2, bd=1, relief=tk.SUNKEN).pack(side=tk.LEFT, fill=tk.Y, padx=4)

        tk.Label(tb, text="Товщина:").pack(side=tk.LEFT)
        self.width_var = tk.IntVar(value=self.line_width)
        tk.Spinbox(tb, from_=1, to=20, width=4,
                   textvariable=self.width_var,
                   command=self._sync_width).pack(side=tk.LEFT, padx=2)

        tk.Frame(tb, width=2, bd=1, relief=tk.SUNKEN).pack(side=tk.LEFT, fill=tk.Y, padx=4)
        tk.Button(tb, text="↩ Undo", command=self.undo).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(tb, text="↪ Redo", command=self.redo).pack(side=tk.LEFT, padx=2, pady=2)

        self._highlight_tool_btn()

    def _build_canvas(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(frame, bg="white", cursor="crosshair")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        c = self.canvas
        c.bind("<ButtonPress-1>",   self.on_mouse_down)
        c.bind("<B1-Motion>",       self.on_mouse_move)
        c.bind("<ButtonRelease-1>", self.on_mouse_up)
        c.bind("<Motion>",          self.on_mouse_hover)

    def _build_statusbar(self):
        self.status_var = tk.StringVar(value="Готово | Інструмент: Лінія")
        tk.Label(self.root, textvariable=self.status_var,
                 bd=1, relief=tk.SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)

    # інструменти

    TOOL_NAMES = {"line":"Лінія","rect":"Прямокутник","ellipse":"Еліпс","select":"Виокремлення"}
    CURSORS    = {"line":"crosshair","rect":"crosshair","ellipse":"crosshair","select":"arrow"}

    def set_tool(self, tool):
        self.current_tool = tool
        self.edit_deselect()
        self.canvas.config(cursor=self.CURSORS[tool])
        self.status_var.set(f"Готово | Інструмент: {self.TOOL_NAMES[tool]}")
        self._highlight_tool_btn()

    def _highlight_tool_btn(self):
        for t, b in self._tool_btns.items():
            b.config(relief=tk.SUNKEN if t == self.current_tool else tk.RAISED)

    def _sync_width(self):
        self.line_width = self.width_var.get()

    def choose_line_color(self):
        c = colorchooser.askcolor(color=self.line_color, title="Колір лінії")[1]
        if c:
            self.line_color = c
            self.line_color_btn.config(bg=c, fg="white" if self._dark(c) else "black")

    def choose_fill_color(self):
        c = colorchooser.askcolor(color=self.fill_color, title="Колір заливки")[1]
        if c:
            self.fill_color = c
            self.fill_color_btn.config(bg=c, fg="white" if self._dark(c) else "black")

    def choose_line_width(self):
        win = tk.Toplevel(self.root)
        win.title("Товщина лінії")
        win.geometry("200x80")
        win.resizable(False, False)
        var = tk.IntVar(value=self.line_width)
        tk.Label(win, text="Товщина (1–20):").pack(pady=5)
        tk.Spinbox(win, from_=1, to=20, textvariable=var, width=6).pack()
        def ok():
            self.line_width = var.get()
            self.width_var.set(self.line_width)
            win.destroy()
        tk.Button(win, text="OK", command=ok).pack(pady=5)

    @staticmethod
    def _dark(hex_color):
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        return (r*299 + g*587 + b*114) / 1000 < 128

    # події миші

    def on_mouse_hover(self, event):
        x, y = event.x, event.y
        self.status_var.set(
            f"Інструмент: {self.TOOL_NAMES[self.current_tool]} | "
            f"X={x}  Y={y} | фігур: {len(self.shapes)}"
        )

    # натиснення
    def on_mouse_down(self, event):
        x, y = event.x, event.y

        if self.current_tool == "select":
            # чи натиснули на існуючу фігуру?
            hit = self._hit_shape(x, y)
            if hit is not None:
                if hit not in self.selected_idx:
                    self.selected_idx = [hit]
                    self._draw_selection_rect()
                # починаємо переміщення
                self.moving = True
                self.move_last_x, self.move_last_y = x, y
            else:
                # починаємо виокремлення прямокутником
                self.edit_deselect()
                self.drawing = True
                self.start_x, self.start_y = x, y
        else:
            # звичайне малювання
            self.drawing = True
            self.start_x, self.start_y = x, y
            self.preview_id = None

    # рух
    def on_mouse_move(self, event):
        x, y = event.x, event.y

        if self.moving:
            dx, dy = x - self.move_last_x, y - self.move_last_y
            self._move_selected(dx, dy)
            self.move_last_x, self.move_last_y = x, y
            return

        if not self.drawing:
            return

        if self.current_tool == "select":
            # показуємо рамку виокремлення
            if self.sel_rect_id:
                self.canvas.delete(self.sel_rect_id)
            self.sel_rect_id = self.canvas.create_rectangle(
                self.start_x, self.start_y, x, y,
                outline=SEL_COLOR, dash=SEL_DASH, width=1, tags=("sel_preview",))
        else:
            # показуємо preview фігури
            if self.preview_id:
                self.canvas.delete(self.preview_id)
            self.preview_id = self._draw_shape(
                self.current_tool, self.start_x, self.start_y, x, y,
                self.line_color, self.fill_color, self.line_width,
                tags=("preview",))

    # відпускання
    def on_mouse_up(self, event):
        x, y = event.x, event.y

        # завершення переміщення
        if self.moving:
            self.moving = False
            self._push_undo()
            self.is_modified = True
            return

        if not self.drawing:
            return
        self.drawing = False

        # завершення виокремлення рамкою
        if self.current_tool == "select":
            if self.sel_rect_id:
                self.canvas.delete(self.sel_rect_id)
                self.sel_rect_id = None
            x1, y1 = min(self.start_x, x), min(self.start_y, y)
            x2, y2 = max(self.start_x, x), max(self.start_y, y)
            self.selected_idx = [
                i for i, s in enumerate(self.shapes)
                if self._shape_in_rect(s, x1, y1, x2, y2)
            ]
            self._draw_selection_rect()
            return

        # завершення малювання фігури
        if self.preview_id:
            self.canvas.delete(self.preview_id)
            self.preview_id = None

        # не малюємо нульові фігури (клік без руху)
        if abs(x - self.start_x) < 2 and abs(y - self.start_y) < 2:
            return

        self._push_undo()
        shape = dict(
            type=self.current_tool,
            x1=self.start_x, y1=self.start_y, x2=x, y2=y,
            line_color=self.line_color, fill_color=self.fill_color,
            line_width=self.line_width,
        )
        shape["canvas_id"] = self._draw_shape(
            shape["type"], shape["x1"], shape["y1"], shape["x2"], shape["y2"],
            shape["line_color"], shape["fill_color"], shape["line_width"])
        self.shapes.append(shape)
        self._redo_stack.clear()
        self.is_modified = True

    # Esc: скасувати поточне малювання
    def on_escape(self):
        if self.drawing:
            self.drawing = False
            if self.preview_id:
                self.canvas.delete(self.preview_id)
                self.preview_id = None
            if self.sel_rect_id:
                self.canvas.delete(self.sel_rect_id)
                self.sel_rect_id = None
            self.status_var.set("Малювання скасовано (Esc)")
        elif self.moving:
            self.moving = False
        elif self.selected_idx:
            self.edit_deselect()

    # undo / redo 

    def _push_undo(self):
        """Зберегти поточний стан у стек Undo."""
        snapshot = copy.deepcopy([
            {k: v for k, v in s.items() if k != "canvas_id"}
            for s in self.shapes
        ])
        self._undo_stack.append(snapshot)
        if len(self._undo_stack) > 50:
            self._undo_stack.pop(0)

    def undo(self):
        if not self._undo_stack:
            self.status_var.set("Нема чого скасовувати")
            return
        # зберегти поточний стан у Redo
        current = copy.deepcopy([
            {k: v for k, v in s.items() if k != "canvas_id"}
            for s in self.shapes
        ])
        self._redo_stack.append(current)
        # відновити попередній
        self.shapes = [{**s} for s in self._undo_stack.pop()]
        self.selected_idx = []
        self._redraw_all()
        self.is_modified = True

    def redo(self):
        if not self._redo_stack:
            self.status_var.set("Нема чого повертати")
            return
        current = copy.deepcopy([
            {k: v for k, v in s.items() if k != "canvas_id"}
            for s in self.shapes
        ])
        self._undo_stack.append(current)
        self.shapes = [{**s} for s in self._redo_stack.pop()]
        self.selected_idx = []
        self._redraw_all()
        self.is_modified = True

    # операції правки

    def edit_select_all(self):
        self.selected_idx = list(range(len(self.shapes)))
        self._draw_selection_rect()

    def edit_deselect(self):
        self.selected_idx = []
        if self.sel_rect_id:
            self.canvas.delete(self.sel_rect_id)
            self.sel_rect_id = None

    def edit_copy(self):
        self.clipboard = copy.deepcopy([
            {k: v for k, v in self.shapes[i].items() if k != "canvas_id"}
            for i in self.selected_idx
        ])
        self.status_var.set(f"Скопійовано {len(self.clipboard)} фігур(у)")

    def edit_cut(self):
        if not self.selected_idx:
            return
        self._push_undo()
        self.edit_copy()
        for i in sorted(self.selected_idx, reverse=True):
            self.canvas.delete(self.shapes[i]["canvas_id"])
            self.shapes.pop(i)
        self.selected_idx = []
        self.sel_rect_id = None
        self._redo_stack.clear()
        self.is_modified = True

    def edit_paste(self):
        """Вставити зі зсувом +20,+20 відносно оригіналу."""
        if not self.clipboard:
            return
        self._push_undo()
        self.edit_deselect()
        offset = 20
        new_indices = []
        for shape in self.clipboard:
            ns = copy.deepcopy(shape)
            ns["x1"] += offset; ns["y1"] += offset
            ns["x2"] += offset; ns["y2"] += offset
            ns["canvas_id"] = self._draw_shape(
                ns["type"], ns["x1"], ns["y1"], ns["x2"], ns["y2"],
                ns["line_color"], ns["fill_color"], ns["line_width"])
            new_indices.append(len(self.shapes))
            self.shapes.append(ns)
        self._redo_stack.clear()
        self.selected_idx = new_indices
        self._draw_selection_rect()
        self.is_modified = True

    def edit_delete_selected(self):
        if not self.selected_idx:
            return
        self._push_undo()
        for i in sorted(self.selected_idx, reverse=True):
            self.canvas.delete(self.shapes[i]["canvas_id"])
            self.shapes.pop(i)
        self.selected_idx = []
        if self.sel_rect_id:
            self.canvas.delete(self.sel_rect_id)
            self.sel_rect_id = None
        self._redo_stack.clear()
        self.is_modified = True

    # переміщення фігур

    def _move_selected(self, dx, dy):
        for i in self.selected_idx:
            s = self.shapes[i]
            s["x1"] += dx; s["y1"] += dy
            s["x2"] += dx; s["y2"] += dy
            self.canvas.move(s["canvas_id"], dx, dy)
        self._draw_selection_rect()

    # допоміжні

    def _draw_shape(self, kind, x1, y1, x2, y2, lc, fc, lw, tags=()):
        kw = dict(outline=lc, fill=fc, width=lw, tags=tags)
        if kind == "line":
            return self.canvas.create_line(x1, y1, x2, y2, fill=lc, width=lw, tags=tags)
        elif kind == "rect":
            return self.canvas.create_rectangle(x1, y1, x2, y2, **kw)
        elif kind == "ellipse":
            return self.canvas.create_oval(x1, y1, x2, y2, **kw)

    def _redraw_all(self):
        self.canvas.delete("all")
        self.sel_rect_id = None
        for s in self.shapes:
            s["canvas_id"] = self._draw_shape(
                s["type"], s["x1"], s["y1"], s["x2"], s["y2"],
                s["line_color"], s["fill_color"], s["line_width"])

    def _draw_selection_rect(self):
        """Намалювати пунктирну рамку навколо всіх виокремлених фігур."""
        if self.sel_rect_id:
            self.canvas.delete(self.sel_rect_id)
            self.sel_rect_id = None
        if not self.selected_idx:
            return
        xs, ys = [], []
        for i in self.selected_idx:
            s = self.shapes[i]
            xs += [s["x1"], s["x2"]]; ys += [s["y1"], s["y2"]]
        pad = 4
        self.sel_rect_id = self.canvas.create_rectangle(
            min(xs)-pad, min(ys)-pad, max(xs)+pad, max(ys)+pad,
            outline=SEL_COLOR, dash=SEL_DASH, width=2, tags=("selection",))
        self.canvas.tag_raise("selection")

    def _hit_shape(self, x, y) -> int | None:
        """Повернути індекс фігури під курсором (остання зверху), або None."""
        for i in range(len(self.shapes) - 1, -1, -1):
            s = self.shapes[i]
            x1, y1, x2, y2 = s["x1"], s["y1"], s["x2"], s["y2"]
            lx1, ly1 = min(x1, x2)-4, min(y1, y2)-4
            lx2, ly2 = max(x1, x2)+4, max(y1, y2)+4
            if lx1 <= x <= lx2 and ly1 <= y <= ly2:
                return i
        return None

    @staticmethod
    def _shape_in_rect(s, rx1, ry1, rx2, ry2) -> bool:
        """Чи потрапляє центр фігури у прямокутник виокремлення."""
        cx = (s["x1"] + s["x2"]) / 2
        cy = (s["y1"] + s["y2"]) / 2
        return rx1 <= cx <= rx2 and ry1 <= cy <= ry2

    # файлові операції

    def _check_save(self):
        if not self.is_modified:
            return True
        ans = messagebox.askyesnocancel("Зберегти?", "Малюнок змінено. Зберегти?")
        if ans is None: return False
        if ans: return self.file_save()
        return True

    def file_new(self):
        if not self._check_save(): return
        self.canvas.delete("all")
        self.shapes.clear()
        self._undo_stack.clear(); self._redo_stack.clear()
        self.selected_idx = []; self.sel_rect_id = None
        self.is_modified = False; self.current_file = None
        self.root.title("Графічний редактор — Лабораторна №9")

    def file_open(self):
        if not self._check_save(): return
        path = filedialog.askopenfilename(
            filetypes=[("JSON малюнки","*.json"),("Всі файли","*.*")])
        if not path: return
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            self.shapes = data.get("shapes", [])
            self._redraw_all()
            self._undo_stack.clear(); self._redo_stack.clear()
            self.selected_idx = []
            self.is_modified = False; self.current_file = path
            self.root.title(f"Графічний редактор — {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося відкрити файл:\n{e}")

    def file_save(self):
        if self.current_file:
            self._write_file(self.current_file); return True
        return self.file_save_as()

    def file_save_as(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON малюнки","*.json"),("Всі файли","*.*")])
        if not path: return False
        self._write_file(path)
        self.current_file = path
        self.root.title(f"Графічний редактор — {os.path.basename(path)}")
        return True

    def _write_file(self, path):
        data = {"shapes": [
            {k: v for k, v in s.items() if k != "canvas_id"}
            for s in self.shapes]}
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
    GraphicsEditor(root)
    root.mainloop()