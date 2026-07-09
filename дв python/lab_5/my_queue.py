# queue.py - клас Queue для моделювання черги вантажних авто на митному контролі.
# містить базові методи черги, методи, пов'язані із задачею, та засоби контролю/захисту.
from dataclasses import is_dataclass
from threading import Lock
import re
from typing import List, Optional, Any

# регулярний вираз для мінімальної перевірки номера авто
PLATE_RE = re.compile(r'^[A-Z0-9\-]{3,10}$', re.I)

class QueueError(Exception):
    pass

class DeclarationValidationError(QueueError):
    pass

class DuplicatePlateError(QueueError):
    pass

class QueueFullError(QueueError):
    pass

class NotFoundError(QueueError):
    pass

class Queue:
    """
    Клас черги для митного контролю.
    name: назва черги (для логування)
    max_size: максимальна довжина черги (None — без обмеження)
    """

    def __init__(self, name: str, max_size: Optional[int] = None):
        self.name = name
        self._items: List[Any] = []
        self._lock = Lock()  # захист при паралельній роботі
        self.max_size = max_size

    # 1) методи базової черги
    def enqueue(self, decl):
        """
        Додати декларацію в кінець черги.
        decl: dataclass або словник декларації
        Викидає:
          - DeclarationValidationError, якщо дані некоректні
          - DuplicatePlateError, якщо такий номер вже є в черзі
          - QueueFullError, якщо черга заповнена
        """
        with self._lock:
            self._validate_declaration(decl)
            plate = self._get_plate(decl)
            if self._plate_in_queue(plate):
                raise DuplicatePlateError(f"Plate {plate} already in queue {self.name}")
            if self.max_size is not None and len(self._items) >= self.max_size:
                raise QueueFullError(f"Queue {self.name} is full (max_size={self.max_size})")
            self._items.append(decl)

    def dequeue(self):
        """
        Видалити та повернути перший елемент черги (якщо є).
        Повертає декларацію або викидає NotFoundError, якщо черга пуста.
        """
        with self._lock:
            if not self._items:
                raise NotFoundError(f"Queue {self.name} is empty")
            return self._items.pop(0)

    def peek(self):
        """
        Повернути перший елемент без видалення. Викидає NotFoundError, якщо пуста.
        """
        with self._lock:
            if not self._items:
                raise NotFoundError(f"Queue {self.name} is empty")
            return self._items[0]

    def is_empty(self) -> bool:
        with self._lock:
            return len(self._items) == 0

    def size(self) -> int:
        with self._lock:
            return len(self._items)

    def clear(self):
        """Очистити чергу."""
        with self._lock:
            self._items.clear()

    def to_list(self) -> List[Any]:
        """Повернути копію списку декларацій (потокобезпечно)."""
        with self._lock:
            return list(self._items)

    # 2) допоміжні та захисні методи
    def _validate_declaration(self, decl):
        """Перевірка структури декларації. Підтримуються dataclass або dict."""
        required_keys = {'truck_make','plate','owner','date','origin','destination',
                         'goods_name','goods_value','contract','weight','hazardous','documents_valid'}
        if is_dataclass(decl):
            decl_keys = set(decl.__dataclass_fields__.keys())
        elif isinstance(decl, dict):
            decl_keys = set(decl.keys())
        else:
            raise DeclarationValidationError("Declaration must be dataclass or dict")
        missing = required_keys - decl_keys
        if missing:
            raise DeclarationValidationError(f"Missing keys in declaration: {missing}")
        # перевірка номера авто
        plate = self._get_plate(decl)
        if not isinstance(plate, str) or not PLATE_RE.match(plate):
            raise DeclarationValidationError(f"Invalid plate format: {plate}")
        # перевірка грошей
        val = self._get_field(decl, 'goods_value')
        try:
            if float(val) < 0:
                raise DeclarationValidationError("goods_value must be non-negative")
        except Exception:
            raise DeclarationValidationError("goods_value must be numeric")

    def _get_field(self, decl, key):
        if is_dataclass(decl):
            return getattr(decl, key)
        else:
            return decl.get(key)

    def _get_plate(self, decl) -> str:
        return str(self._get_field(decl, "plate"))

    def _plate_in_queue(self, plate: str) -> bool:
        return any(self._get_plate(d) == plate for d in self._items)

    # 3) методи, пов'язані із задачею
    def remove_by_plate(self, plate: str):
        """
        Видалити авто з черги за номером (наприклад, за відсутністю дозволу).
        Повертає видалену декларацію або викидає NotFoundError.
        """
        with self._lock:
            for i, d in enumerate(self._items):
                if self._get_plate(d) == plate:
                    return self._items.pop(i)
            raise NotFoundError(f"Plate {plate} not found in queue {self.name}")

    def move_plate_to(self, plate: str, dest_queue: 'Queue'):
        """
        Перевести авто з цієї черги в кінець dest_queue.
        Перевірки: source має містити авто, dest_queue не має дубля (у той же час).
        Повертає відправлену декларацію.
        """
        # блокування обох черг за іменем для уникнення deadlock - lock ordering
        queues = sorted([self, dest_queue], key=lambda q: q.name)
        with queues[0]._lock:
            with queues[1]._lock:
                # знаходимо в source (self)
                for i, d in enumerate(self._items):
                    if self._get_plate(d) == plate:
                        # перевірка, що в dest немає такого номера
                        if dest_queue._plate_in_queue(plate):
                            raise DuplicatePlateError(f"Plate {plate} already in destination queue {dest_queue.name}")
                        decl = self._items.pop(i)
                        if dest_queue.max_size is not None and len(dest_queue._items) >= dest_queue.max_size:
                            # повернення назад - вставимо назад в початкову позицію
                            self._items.insert(i, decl)
                            raise QueueFullError(f"Destination queue {dest_queue.name} is full")
                        dest_queue._items.append(decl)
                        return decl
                raise NotFoundError(f"Plate {plate} not found in source queue {self.name}")

    def list_by_goods(self, goods_name: str) -> List[tuple]:
        """
        Повернути перелік кортежів (позиція, plate, owner, goods_value) для авто, що везуть goods_name.
        Пошук нечутливий до регістру.
        """
        with self._lock:
            res = []
            for idx, d in enumerate(self._items, start=1):
                if str(self._get_field(d, 'goods_name')).lower() == goods_name.lower():
                    res.append((idx, self._get_plate(d), self._get_field(d, 'owner'), float(self._get_field(d,'goods_value'))))
            return res

    def vehicle_with_max_value(self):
        """
        Повернути декларацію авто з найвищою вартістю товару в цій черзі.
        Якщо черга пуста — повертає None.
        """
        with self._lock:
            if not self._items:
                return None
            # знайдемо максимум за goods_value
            max_decl = max(self._items, key=lambda d: float(self._get_field(d, 'goods_value')))
            return max_decl

    def goods_summary(self):
        """
        Повернути словник {goods_name: total_value} по всіх авто в черзі.
        """
        with self._lock:
            summary = {}
            for d in self._items:
                name = str(self._get_field(d,'goods_name'))
                val = float(self._get_field(d,'goods_value'))
                summary[name] = summary.get(name, 0.0) + val
            return summary

    def list_by_destination(self, city_name: str) -> List[tuple]:
        """
        Повернути список авто (позиція, plate, owner, destination) що прямують до city_name.
        Пошук нечутливий до регістру і дивиться в поле 'destination' (очікується tuple (country,city))
        """
        with self._lock:
            res = []
            for idx, d in enumerate(self._items, start=1):
                dest = self._get_field(d,'destination')
                if isinstance(dest, (list,tuple)) and len(dest) >= 2:
                    city = str(dest[1])
                    if city.lower() == city_name.lower():
                        res.append((idx, self._get_plate(d), self._get_field(d,'owner'), dest))
            return res

    # 4) додаткові операції
    def flag_hazardous(self):
        """
        Повернути список авто, що мають у полі 'hazardous' ненульовий список/рядок.
        Кожний елемент: (позиція, plate, hazardous_info)
        """
        with self._lock:
            res = []
            for idx, d in enumerate(self._items, start=1):
                hz = self._get_field(d,'hazardous')
                if hz:
                    res.append((idx, self._get_plate(d), hz))
            return res

    def prioritize_plate(self, plate: str):
        """
        Перемістити авто з даним plate на початок черги (наприклад, для термінового розмитнення).
        Повертає True якщо успішно, інакше викидає NotFoundError.
        """
        with self._lock:
            for i, d in enumerate(self._items):
                if self._get_plate(d) == plate:
                    item = self._items.pop(i)
                    self._items.insert(0, item)
                    return True
            raise NotFoundError(f"Plate {plate} not found to prioritize in {self.name}")

    def inspection_history_stub(self, plate: str) -> dict:
        """
        Заглушка для історії огляду. Повертаємо згенерований словник для демонстрації контролю.
        """
        # повертаємо псевдо-дані для спрощення
        return {
            "plate": plate,
            "past_inspections": [
                {"date":"2025-03-12","result":"clean"},
                {"date":"2024-11-02","result":"minor_issue"}
            ],
            "flags": []
        }