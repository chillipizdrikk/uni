import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
import json, os, copy, math

# Pillow для фільтрів (PIL)
try:
    from PIL import Image, ImageFilter, ImageTk, ImageOps
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# константи 
SEL_COLOR   = "#0078D7"
SEL_DASH    = (4, 4)
CANVAS_W    = 2000        # розмір віртуального полотна
CANVAS_H    = 2000


class GraphicsEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Графічний редактор — Лабораторна №10")
        self.root.geometry("980x700")

        # параметри малювання
        self.line_color  = "#000000"
        self.fill_color  = "#ffffff"
        self.line_width  = 2
        self.current_tool = "line"

        # стан фігур
        self.shapes: list[dict]   = []
        self.clipboard: list[dict] = []
        self.selected_idx: list[int] = []
        self.sel_rect_id = None

        # стан малювання
        self.drawing = False
        self.start_x = self.start_y = 0
        self.preview_id = None
        self.moving = False
        self.move_last_x = self.move_last_y = 0

        # undo/redo
        self._undo_stack: list = []
        self._redo_stack: list = []

        # фільтр-шар (PIL зображення на canvas)
        self._filter_image_id = None   # canvas-id photo-image після фільтру
        self._filter_photo    = None   # PhotoImage (зберігаємо, щоб не зібрав GC)

        # файл 
        self.is_modified  = False
        self.current_file = None

        self._build_menu()
        self._build_toolbar()
        self._build_canvas()
        self._build_statusbar()

    # побудова UI

    def _build_menu(self):
        mb = tk.Menu(self.root)

        fm = tk.Menu(mb, tearoff=0)
        fm.add_command(label="Новий файл",      accelerator="Ctrl+N", command=self.file_new)
        fm.add_command(label="Відкрити...",     accelerator="Ctrl+O", command=self.file_open)
        fm.add_command(label="Зберегти",        accelerator="Ctrl+S", command=self.file_save)
        fm.add_command(label="Зберегти як...",  accelerator="Ctrl+Shift+S", command=self.file_save_as)
        fm.add_separator()
        fm.add_command(label="Вийти",                                  command=self.app_exit)
        mb.add_cascade(label="Файл", menu=fm)

        em = tk.Menu(mb, tearoff=0)
        em.add_command(label="Скасувати (Undo)", accelerator="Ctrl+Z",   command=self.undo)
        em.add_command(label="Повернути (Redo)", accelerator="Ctrl+Y",   command=self.redo)
        em.add_separator()
        em.add_command(label="Вирізати",         accelerator="Ctrl+X",   command=self.edit_cut)
        em.add_command(label="Копіювати",        accelerator="Ctrl+C",   command=self.edit_copy)
        em.add_command(label="Вставити",         accelerator="Ctrl+V",   command=self.edit_paste)
        em.add_separator()
        em.add_command(label="Вибрати все",      accelerator="Ctrl+A",   command=self.edit_select_all)
        em.add_command(label="Зняти виокремлення",                        command=self.edit_deselect)
        em.add_command(label="Видалити виокремлені", accelerator="Delete",command=self.edit_delete_selected)
        mb.add_cascade(label="Правка", menu=em)

        fig = tk.Menu(mb, tearoff=0)
        fig.add_command(label="Лінія",       command=lambda: self.set_tool("line"))
        fig.add_command(label="Прямокутник", command=lambda: self.set_tool("rect"))
        fig.add_command(label="Еліпс",       command=lambda: self.set_tool("ellipse"))
        fig.add_separator()
        fig.add_command(label="Виокремлення/Переміщення", command=lambda: self.set_tool("select"))
        mb.add_cascade(label="Фігури", menu=fig)

        pr = tk.Menu(mb, tearoff=0)
        pr.add_command(label="Колір лінії...",   command=self.choose_line_color)
        pr.add_command(label="Колір заливки...", command=self.choose_fill_color)
        pr.add_command(label="Товщина лінії",    command=self.choose_line_width)
        mb.add_cascade(label="Властивості", menu=pr)

        filt = tk.Menu(mb, tearoff=0)
        filt.add_command(label="Інверсія",         command=lambda: self.apply_filter("invert"))
        filt.add_command(label="Відтінки сірого",  command=lambda: self.apply_filter("grayscale"))
        filt.add_command(label="Розмиття",         command=lambda: self.apply_filter("blur"))
        filt.add_command(label="Контур",           command=lambda: self.apply_filter("edges"))
        filt.add_separator()
        filt.add_command(label="Скасувати фільтр", command=self.remove_filter)
        mb.add_cascade(label="Фільтри", menu=filt)

        rot = tk.Menu(mb, tearoff=0)
        rot.add_command(label="Повернути на 90° за годинн.", command=lambda: self.rotate_all(90))
        rot.add_command(label="Повернути на 90° проти год.", command=lambda: self.rotate_all(-90))
        rot.add_command(label="Повернути на 180°",           command=lambda: self.rotate_all(180))
        rot.add_command(label="Дзеркало горизонтально",      command=lambda: self.mirror_all("h"))
        rot.add_command(label="Дзеркало вертикально",        command=lambda: self.mirror_all("v"))
        mb.add_cascade(label="Перетворення", menu=rot)

        self.root.config(menu=mb)

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

        tools = [("Лінія","line"),("Прямокутник","rect"),("Еліпс","ellipse"),("☑ Вибір","select")]
        self._tool_btns = {}
        for lbl, t in tools:
            b = tk.Button(tb, text=lbl, width=10, command=lambda x=t: self.set_tool(x))
            b.pack(side=tk.LEFT, padx=2, pady=2)
            self._tool_btns[t] = b

        tk.Frame(tb, width=2, bd=1, relief=tk.SUNKEN).pack(side=tk.LEFT, fill=tk.Y, padx=3)

        self.line_color_btn = tk.Button(tb, text="Лінія", width=7,
                                        bg=self.line_color, fg="white",
                                        command=self.choose_line_color)
        self.line_color_btn.pack(side=tk.LEFT, padx=2, pady=2)

        self.fill_color_btn = tk.Button(tb, text="Заливка", width=7,
                                        bg=self.fill_color,
                                        command=self.choose_fill_color)
        self.fill_color_btn.pack(side=tk.LEFT, padx=2, pady=2)

        tk.Frame(tb, width=2, bd=1, relief=tk.SUNKEN).pack(side=tk.LEFT, fill=tk.Y, padx=3)
        tk.Label(tb, text="Тов:").pack(side=tk.LEFT)
        self.width_var = tk.IntVar(value=self.line_width)
        tk.Spinbox(tb, from_=1, to=20, width=3,
                   textvariable=self.width_var,
                   command=self._sync_width).pack(side=tk.LEFT, padx=2)

        tk.Frame(tb, width=2, bd=1, relief=tk.SUNKEN).pack(side=tk.LEFT, fill=tk.Y, padx=3)
        tk.Button(tb, text="↩ Undo", command=self.undo).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(tb, text="↪ Redo", command=self.redo).pack(side=tk.LEFT, padx=2, pady=2)

        tk.Frame(tb, width=2, bd=1, relief=tk.SUNKEN).pack(side=tk.LEFT, fill=tk.Y, padx=3)
        # Кнопки фільтрів у тулбарі
        for lbl, flt in [("Інверс.", "invert"), ("Сірий", "grayscale"),
                          ("Розмит.", "blur"),   ("Контур", "edges")]:
            tk.Button(tb, text=lbl, width=7,
                      command=lambda f=flt: self.apply_filter(f)).pack(side=tk.LEFT, padx=1, pady=2)
        tk.Button(tb, text="✕ Фільтр", width=8,
                  command=self.remove_filter).pack(side=tk.LEFT, padx=1, pady=2)

        tk.Frame(tb, width=2, bd=1, relief=tk.SUNKEN).pack(side=tk.LEFT, fill=tk.Y, padx=3)
        tk.Button(tb, text="↻ 90°",  command=lambda: self.rotate_all(90)).pack(side=tk.LEFT, padx=1, pady=2)
        tk.Button(tb, text="↺ 90°",  command=lambda: self.rotate_all(-90)).pack(side=tk.LEFT, padx=1, pady=2)
        tk.Button(tb, text="↔",      command=lambda: self.mirror_all("h")).pack(side=tk.LEFT, padx=1, pady=2)
        tk.Button(tb, text="↕",      command=lambda: self.mirror_all("v")).pack(side=tk.LEFT, padx=1, pady=2)

        self._highlight_tool_btn()

    def _build_canvas(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        # вертикальна і горизонтальна смуги прокрутки
        vbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)

        hbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)

        # велике полотно
        self.canvas = tk.Canvas(
            frame,
            bg="white",
            cursor="crosshair",
            scrollregion=(0, 0, CANVAS_W, CANVAS_H),
            xscrollcommand=hbar.set,
            yscrollcommand=vbar.set,
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # прив'язуємо смуги до canvas
        vbar.config(command=self.canvas.yview)
        hbar.config(command=self.canvas.xview)

        # Прокрутка колесом миші
        self.canvas.bind("<MouseWheel>",       self._on_mousewheel)
        self.canvas.bind("<Shift-MouseWheel>", self._on_shift_mousewheel)
        # Linux
        self.canvas.bind("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind("<Button-5>", lambda e: self.canvas.yview_scroll( 1, "units"))

        # події малювання
        self.canvas.bind("<ButtonPress-1>",   self.on_mouse_down)
        self.canvas.bind("<B1-Motion>",       self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.canvas.bind("<Motion>",          self.on_mouse_hover)

        # границя полотна (вказує розмір робочої зони)
        self.canvas.create_rectangle(0, 0, CANVAS_W, CANVAS_H,
                                     outline="#CCCCCC", width=1, tags=("border",))

    def _build_statusbar(self):
        self.status_var = tk.StringVar(value="Готово | Інструмент: Лінія")
        tk.Label(self.root, textvariable=self.status_var,
                 bd=1, relief=tk.SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)

    # Завдання 1: прокрутка

    def _canvas_coords(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        return x, y

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_shift_mousewheel(self, event):
        self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

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
        r, g, b = int(hex_color[1:3],16), int(hex_color[3:5],16), int(hex_color[5:7],16)
        return (r*299 + g*587 + b*114)/1000 < 128

    # події миші 

    def on_mouse_hover(self, event):
        x, y = self._canvas_coords(event)
        self.status_var.set(
            f"Інструмент: {self.TOOL_NAMES[self.current_tool]} | "
            f"X={int(x)}  Y={int(y)} | фігур: {len(self.shapes)}")

    def on_mouse_down(self, event):
        x, y = self._canvas_coords(event)
        if self.current_tool == "select":
            hit = self._hit_shape(x, y)
            if hit is not None:
                if hit not in self.selected_idx:
                    self.selected_idx = [hit]
                    self._draw_selection_rect()
                self.moving = True
                self.move_last_x, self.move_last_y = x, y
            else:
                self.edit_deselect()
                self.drawing = True
                self.start_x, self.start_y = x, y
        else:
            self.drawing = True
            self.start_x, self.start_y = x, y
            self.preview_id = None

    def on_mouse_move(self, event):
        x, y = self._canvas_coords(event)
        if self.moving:
            dx, dy = x - self.move_last_x, y - self.move_last_y
            self._move_selected(dx, dy)
            self.move_last_x, self.move_last_y = x, y
            return
        if not self.drawing:
            return
        if self.current_tool == "select":
            if self.sel_rect_id:
                self.canvas.delete(self.sel_rect_id)
            self.sel_rect_id = self.canvas.create_rectangle(
                self.start_x, self.start_y, x, y,
                outline=SEL_COLOR, dash=SEL_DASH, width=1, tags=("sel_preview",))
        else:
            if self.preview_id:
                self.canvas.delete(self.preview_id)
            self.preview_id = self._draw_shape(
                self.current_tool, self.start_x, self.start_y, x, y,
                self.line_color, self.fill_color, self.line_width, tags=("preview",))

    def on_mouse_up(self, event):
        x, y = self._canvas_coords(event)
        if self.moving:
            self.moving = False
            self._push_undo()
            self.is_modified = True
            return
        if not self.drawing:
            return
        self.drawing = False
        if self.current_tool == "select":
            if self.sel_rect_id:
                self.canvas.delete(self.sel_rect_id)
                self.sel_rect_id = None
            x1, y1 = min(self.start_x, x), min(self.start_y, y)
            x2, y2 = max(self.start_x, x), max(self.start_y, y)
            self.selected_idx = [
                i for i, s in enumerate(self.shapes)
                if self._shape_in_rect(s, x1, y1, x2, y2)]
            self._draw_selection_rect()
            return
        if self.preview_id:
            self.canvas.delete(self.preview_id)
            self.preview_id = None
        if abs(x - self.start_x) < 2 and abs(y - self.start_y) < 2:
            return
        self._push_undo()
        shape = dict(type=self.current_tool,
                     x1=self.start_x, y1=self.start_y, x2=x, y2=y,
                     line_color=self.line_color, fill_color=self.fill_color,
                     line_width=self.line_width)
        shape["canvas_id"] = self._draw_shape(
            shape["type"], shape["x1"], shape["y1"], shape["x2"], shape["y2"],
            shape["line_color"], shape["fill_color"], shape["line_width"])
        self.shapes.append(shape)
        self._redo_stack.clear()
        self.is_modified = True

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
        snap = copy.deepcopy([{k:v for k,v in s.items() if k!="canvas_id"} for s in self.shapes])
        self._undo_stack.append(snap)
        if len(self._undo_stack) > 50:
            self._undo_stack.pop(0)

    def undo(self):
        if not self._undo_stack:
            self.status_var.set("Нема чого скасовувати"); return
        cur = copy.deepcopy([{k:v for k,v in s.items() if k!="canvas_id"} for s in self.shapes])
        self._redo_stack.append(cur)
        self.shapes = [{**s} for s in self._undo_stack.pop()]
        self.selected_idx = []
        self._redraw_all()
        self.is_modified = True

    def redo(self):
        if not self._redo_stack:
            self.status_var.set("Нема чого повертати"); return
        cur = copy.deepcopy([{k:v for k,v in s.items() if k!="canvas_id"} for s in self.shapes])
        self._undo_stack.append(cur)
        self.shapes = [{**s} for s in self._redo_stack.pop()]
        self.selected_idx = []
        self._redraw_all()
        self.is_modified = True

    # правка 

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
            {k:v for k,v in self.shapes[i].items() if k!="canvas_id"}
            for i in self.selected_idx])
        self.status_var.set(f"Скопійовано {len(self.clipboard)} фігур(у)")

    def edit_cut(self):
        if not self.selected_idx: return
        self._push_undo()
        self.edit_copy()
        for i in sorted(self.selected_idx, reverse=True):
            self.canvas.delete(self.shapes[i]["canvas_id"])
            self.shapes.pop(i)
        self.selected_idx = []; self.sel_rect_id = None
        self._redo_stack.clear(); self.is_modified = True

    def edit_paste(self):
        if not self.clipboard: return
        self._push_undo()
        self.edit_deselect()
        offset = 20; new_indices = []
        for shape in self.clipboard:
            ns = copy.deepcopy(shape)
            ns["x1"] += offset; ns["y1"] += offset
            ns["x2"] += offset; ns["y2"] += offset
            ns["canvas_id"] = self._draw_shape(
                ns["type"],ns["x1"],ns["y1"],ns["x2"],ns["y2"],
                ns["line_color"],ns["fill_color"],ns["line_width"])
            new_indices.append(len(self.shapes))
            self.shapes.append(ns)
        self._redo_stack.clear()
        self.selected_idx = new_indices
        self._draw_selection_rect()
        self.is_modified = True

    def edit_delete_selected(self):
        if not self.selected_idx: return
        self._push_undo()
        for i in sorted(self.selected_idx, reverse=True):
            self.canvas.delete(self.shapes[i]["canvas_id"])
            self.shapes.pop(i)
        self.selected_idx = []
        if self.sel_rect_id:
            self.canvas.delete(self.sel_rect_id)
            self.sel_rect_id = None
        self._redo_stack.clear(); self.is_modified = True

    def _move_selected(self, dx, dy):
        for i in self.selected_idx:
            s = self.shapes[i]
            s["x1"]+=dx; s["y1"]+=dy; s["x2"]+=dx; s["y2"]+=dy
            self.canvas.move(s["canvas_id"], dx, dy)
        self._draw_selection_rect()

    # Завдання 2: Фільтри зображення

    def _rasterize_canvas(self) -> "Image.Image | None":
        """Растеризувати поточне векторне полотно у PIL Image через ImageDraw."""
        if not PIL_AVAILABLE:
            messagebox.showerror("Помилка",
                "Бібліотека Pillow не встановлена.\nВиконайте: pip install Pillow")
            return None
        from PIL import ImageDraw
        img  = Image.new("RGB", (CANVAS_W, CANVAS_H), "white")
        draw = ImageDraw.Draw(img)
        for s in self.shapes:
            x1, y1, x2, y2 = s["x1"], s["y1"], s["x2"], s["y2"]
            lc = s["line_color"]
            fc = s["fill_color"]
            lw = max(1, int(s["line_width"]))
            # PIL потребує x1 <= x2, y1 <= y2
            bx1, bx2 = min(x1, x2), max(x1, x2)
            by1, by2 = min(y1, y2), max(y1, y2)
            if s["type"] == "line":
                draw.line([(x1, y1), (x2, y2)], fill=lc, width=lw)
            elif s["type"] == "rect":
                draw.rectangle([bx1, by1, bx2, by2], outline=lc, fill=fc, width=lw)
            elif s["type"] == "ellipse":
                draw.ellipse([bx1, by1, bx2, by2], outline=lc, fill=fc, width=lw)
        return img

    def apply_filter(self, filter_name: str):
        if not PIL_AVAILABLE:
            messagebox.showerror("Помилка", "Бібліотека Pillow не встановлена.\nВиконайте: pip install Pillow")
            return
        img = self._rasterize_canvas()
        if img is None:
            return

        # застосування фільтру 
        if filter_name == "invert":
            result = ImageOps.invert(img)
        elif filter_name == "grayscale":
            result = ImageOps.grayscale(img).convert("RGB")
        elif filter_name == "blur":
            result = img.filter(ImageFilter.GaussianBlur(radius=3))
        elif filter_name == "edges":
            # Контур: FIND_EDGES на градаціях сірого, потім повернути у RGB
            gray = ImageOps.grayscale(img)
            edges = gray.filter(ImageFilter.FIND_EDGES)
            result = edges.convert("RGB")
        else:
            return

        # Видалити попередній фільтр-шар
        self.remove_filter()

        # Показати результат на canvas поверх усього
        self._filter_photo = ImageTk.PhotoImage(result)
        self._filter_image_id = self.canvas.create_image(
            0, 0, anchor=tk.NW, image=self._filter_photo, tags=("filter_layer",))
        self.canvas.tag_raise("filter_layer")  # піднімаємо на верх — фільтр видимий
        names = {"invert": "Інверсія", "grayscale": "Відтінки сірого",
                 "blur": "Розмиття", "edges": "Контур"}
        self.status_var.set(
            f"Фільтр: {names.get(filter_name, filter_name)} | "
            f"натисніть '✕ Фільтр' щоб скасувати")

    def remove_filter(self):
        """Прибрати шар фільтру, повернути оригінальний вигляд."""
        if self._filter_image_id:
            self.canvas.delete(self._filter_image_id)
            self._filter_image_id = None
            self._filter_photo = None
            self.status_var.set("Фільтр скасовано")

    # Завдання 3: Обертання і дзеркало 

    def _shapes_bbox(self):
        """Повернути bounding box усіх фігур."""
        xs = [s["x1"] for s in self.shapes] + [s["x2"] for s in self.shapes]
        ys = [s["y1"] for s in self.shapes] + [s["y2"] for s in self.shapes]
        return min(xs), min(ys), max(xs), max(ys)

    def rotate_all(self, angle_deg: int):
        """Обернути всі фігури навколо центру їх bounding box."""
        if not self.shapes:
            return
        self._push_undo()
        bx1, by1, bx2, by2 = self._shapes_bbox()
        cx, cy = (bx1 + bx2) / 2, (by1 + by2) / 2

        # Для кратних 90° округлюємо тригонометрію до цілих, щоб уникнути float-сміття
        rad = math.radians(angle_deg)
        cos_a = round(math.cos(rad))
        sin_a = round(math.sin(rad))

        def rot(x, y):
            dx, dy = x - cx, y - cy
            return round(cx + dx * cos_a - dy * sin_a, 2), round(cy + dx * sin_a + dy * cos_a, 2)

        for s in self.shapes:
            s["x1"], s["y1"] = rot(s["x1"], s["y1"])
            s["x2"], s["y2"] = rot(s["x2"], s["y2"])

        self._redo_stack.clear()
        self._redraw_all()
        self.is_modified = True
        self.status_var.set(f"Обернуто на {angle_deg}°")

    def mirror_all(self, axis: str):
        """Дзеркальне відображення усіх фігур відносно центру їх bounding box."""
        if not self.shapes:
            return
        self._push_undo()
        bx1, by1, bx2, by2 = self._shapes_bbox()
        cx, cy = (bx1 + bx2) / 2, (by1 + by2) / 2

        for s in self.shapes:
            if axis == "h":          # відображення по вертикальній осі (ліво↔право)
                s["x1"] = round(2 * cx - s["x1"], 2)
                s["x2"] = round(2 * cx - s["x2"], 2)
            else:                    # відображення по горизонтальній осі (верх↔низ)
                s["y1"] = round(2 * cy - s["y1"], 2)
                s["y2"] = round(2 * cy - s["y2"], 2)

        self._redo_stack.clear()
        self._redraw_all()
        self.is_modified = True
        label = "горизонтально" if axis == "h" else "вертикально"
        self.status_var.set(f"Дзеркало {label}")

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
        self._filter_image_id = None
        self._filter_photo = None
        # Відновити рамку полотна
        self.canvas.create_rectangle(0, 0, CANVAS_W, CANVAS_H,
                                     outline="#CCCCCC", width=1, tags=("border",))
        for s in self.shapes:
            s["canvas_id"] = self._draw_shape(
                s["type"], s["x1"], s["y1"], s["x2"], s["y2"],
                s["line_color"], s["fill_color"], s["line_width"])

    def _draw_selection_rect(self):
        if self.sel_rect_id:
            self.canvas.delete(self.sel_rect_id)
            self.sel_rect_id = None
        if not self.selected_idx:
            return
        xs, ys = [], []
        for i in self.selected_idx:
            s = self.shapes[i]
            xs += [s["x1"],s["x2"]]; ys += [s["y1"],s["y2"]]
        pad = 4
        self.sel_rect_id = self.canvas.create_rectangle(
            min(xs)-pad, min(ys)-pad, max(xs)+pad, max(ys)+pad,
            outline=SEL_COLOR, dash=SEL_DASH, width=2, tags=("selection",))
        self.canvas.tag_raise("selection")

    def _hit_shape(self, x, y):
        for i in range(len(self.shapes)-1, -1, -1):
            s = self.shapes[i]
            lx1,ly1 = min(s["x1"],s["x2"])-4, min(s["y1"],s["y2"])-4
            lx2,ly2 = max(s["x1"],s["x2"])+4, max(s["y1"],s["y2"])+4
            if lx1<=x<=lx2 and ly1<=y<=ly2:
                return i
        return None

    @staticmethod
    def _shape_in_rect(s, rx1, ry1, rx2, ry2):
        cx = (s["x1"]+s["x2"])/2; cy = (s["y1"]+s["y2"])/2
        return rx1<=cx<=rx2 and ry1<=cy<=ry2

    # файл 

    def _check_save(self):
        if not self.is_modified: return True
        ans = messagebox.askyesnocancel("Зберегти?", "Малюнок змінено. Зберегти?")
        if ans is None: return False
        if ans: return self.file_save()
        return True

    def file_new(self):
        if not self._check_save(): return
        self.canvas.delete("all")
        self.shapes.clear()
        self._undo_stack.clear(); self._redo_stack.clear()
        self.selected_idx=[]; self.sel_rect_id=None
        self._filter_image_id=None; self._filter_photo=None
        self.is_modified=False; self.current_file=None
        self.canvas.create_rectangle(0,0,CANVAS_W,CANVAS_H,outline="#CCCCCC",width=1,tags=("border",))
        self.root.title("Графічний редактор — Лабораторна №10")

    def file_open(self):
        if not self._check_save(): return
        path = filedialog.askopenfilename(
            filetypes=[("JSON малюнки","*.json"),("Всі файли","*.*")])
        if not path: return
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            self.shapes = data.get("shapes",[])
            self._redraw_all()
            self._undo_stack.clear(); self._redo_stack.clear()
            self.selected_idx=[]
            self.is_modified=False; self.current_file=path
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
        self.current_file=path
        self.root.title(f"Графічний редактор — {os.path.basename(path)}")
        return True

    def _write_file(self, path):
        data = {"shapes":[{k:v for k,v in s.items() if k!="canvas_id"} for s in self.shapes]}
        try:
            with open(path,"w",encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.is_modified=False
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося зберегти файл:\n{e}")

    def app_exit(self):
        if self._check_save():
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    GraphicsEditor(root)
    root.mainloop()
