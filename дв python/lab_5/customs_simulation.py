# customs_simulation.py - основний модуль (сценарій диспетчера пункту прикордонного контролю)
# використовує my_queue.Queue та declarations.incoming_declarations і при виконанні створює файл protocol.txt 
# з детальним протоколом дій.

from my_queue import Queue, QueueError, NotFoundError, DuplicatePlateError, QueueFullError, DeclarationValidationError
from declarations import incoming_declarations, Declaration
import datetime
import sys

PROTOCOL_FILE = "protocol.txt"

def log(msg: str):
    """Допоміжна функція - вивід в консоль та запис у файл протоколу."""
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(PROTOCOL_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def run_scenario():
    # очищуємо попередній протокол
    open(PROTOCOL_FILE, "w", encoding="utf-8").close()
    log("Початок сценарію: моделювання митного контролю для вантажних авто.")

    # створюємо дві черги: general і green corridor
    general = Queue("general", max_size=30)
    green = Queue("green_corridor", max_size=10)

    # розміщуємо авто у списку прибуваючих в довільному порядку
    log("Завантаження вхідних декларацій у системний список (не в чергу).")
    declarations = list(incoming_declarations)  # крок - вхідний список

    # ставимо частину авто в загальну чергу, частину - у зелений коридор
    log("Розподіл перших 10 авто: деякі у green corridor (спрощено за умовою).")
    for i, decl in enumerate(declarations):
        try:
            if i % 5 == 0:
                green.enqueue(decl)
                log(f"ENQUEUE to green_corridor: plate={decl.plate}, goods={decl.goods_name}")
            else:
                general.enqueue(decl)
                log(f"ENQUEUE to general: plate={decl.plate}, goods={decl.goods_name}")
        except QueueError as e:
            log(f"Помилка при додаванні {decl.plate}: {e}")

    # закінчити огляд і дозволити перетин кордону - читаємо з черги
    log("Операція: завершити огляд (dequeue) 2 авто з зеленого коридору.")
    for _ in range(2):
        try:
            decl = green.dequeue()
            log(f"DEQUEUE from green_corridor: plate={decl.plate} - дозвіл на перетин кордону (проїхав).")
        except NotFoundError as e:
            log(f"DEQUEUE error: {e}")

    # перемістити авто з однієї черги в кінець другої
    log("Операція: перемістити авто 'TRK-998' з general до green_corridor.")
    try:
        moved = general.move_plate_to("TRK-998", green)
        log(f"MOVE plate TRK-998 to green_corridor: owner={moved.owner}, goods={moved.goods_name}")
    except QueueError as e:
        log(f"MOVE error: {e}")

    # викреслити авто з черги (немає дозволу)
    log("Операція: видалити авто 'OP-444' (документи невалідні) з general.")
    try:
        removed = general.remove_by_plate("OP-444")
        log(f"REMOVE plate OP-444 from general: owner={removed.owner}, reason=documents invalid")
    except NotFoundError as e:
        log(f"REMOVE error: {e}")

    # скласти перелік авто, які везуть вказаний товар
    log("Операція: список авто, що везуть 'Electronics' у general.")
    el_list = general.list_by_goods("Electronics")
    if el_list:
        for pos, plate, owner, val in el_list:
            log(f"Electronics in general: pos={pos}, plate={plate}, owner={owner}, value={val}")
    else:
        log("No Electronics found in general.")

    # яке авто має товар найбільшої вартості?
    log("Операція: авто з найвищою вартістю товару в green_corridor.")
    max_decl = green.vehicle_with_max_value()
    if max_decl:
        log(f"MAX VALUE in green_corridor: plate={max_decl.plate}, goods={max_decl.goods_name}, value={max_decl.goods_value}")
    else:
        log("green_corridor is empty for max value check.")

    # таблиця товарів і цін, перевезених через кордон (підсумок) - для general
    log("Операція: підсумок товарів у general (goods_summary).")
    summary = general.goods_summary()
    for name, total in summary.items():
        log(f"SUMMARY general: goods={name}, total_value={total}")

    # які авто прямують до Одеси?
    log("Операція: які авто в general прямують до Одеси?")
    odessa_list = general.list_by_destination("Odessa")
    if odessa_list:
        for pos, plate, owner, dest in odessa_list:
            log(f"To Odessa in general: pos={pos}, plate={plate}, owner={owner}, dest={dest}")
    else:
        log("No vehicles to Odessa in general.")

    # додаткові операції
    # 1) контроль перевезення наркотичних/вибухових
    log("Додаткова операція: перевірка на наявність небезпечних вантажів в обох чергах.")
    for q in (general, green):
        flags = q.flag_hazardous()
        if flags:
            for pos, plate, hz in flags:
                log(f"Hazardous in {q.name}: pos={pos}, plate={plate}, hazard={hz}")
        else:
            log(f"No hazardous items in {q.name}.")

    # 2) пріоритизація термінового перевезення
    log("Додаткова операція: пріоритизувати plate 'AV-777' в general (перемістити на початок).")
    try:
        general.prioritize_plate("AV-777")
        log("Prioritize AV-777: done.")
    except NotFoundError as e:
        log(f"Prioritize error: {e}")

    # 3) перевірка історії огляду
    log("Додаткова операція: отримати історію огляду для 'PR-009'.")
    hist = general.inspection_history_stub("PR-009")
    log(f"Inspection history stub for PR-009: {hist}")

    # 4) спроба некоректних операцій, щоб показати захист
    log("Тепер демонструємо некоректні операції (очікувані помилки) для протоколу.")
    # a) додати дубль номера
    try:
        duplicate = declarations[0]
        general.enqueue(duplicate)  # цей plate вже є
        log("ERROR: duplicate enqueue succeeded unexpectedly.")
    except DuplicatePlateError as e:
        log(f"Expected DuplicatePlateError caught: {e}")
    except QueueError as e:
        log(f"Other QueueError during duplicate test: {e}")

    # b) видалити неіснуючий plate
    try:
        general.remove_by_plate("NO-SUCH-PLATE")
        log("ERROR: removed non-existent plate unexpectedly.")
    except NotFoundError as e:
        log(f"Expected NotFoundError caught: {e}")

    # c) dеqueue з пустої черги: спочатку очистимо green, потім ще раз виконаємо dequeue
    log("Очищаємо green_corridor і пробуємо ще один dequeue (має виникнути помилка).")
    try:
        # видалити всі
        while True:
            green.dequeue()
    except NotFoundError:
        log("green_corridor cleaned.")
    try:
        green.dequeue()
        log("ERROR: extra dequeue from empty green succeeded unexpectedly.")
    except NotFoundError as e:
        log(f"Expected NotFoundError caught on extra dequeue: {e}")

    # d) спроба перемістити авто в переповнену чергу: задамо маленький max_size і заповнимо
    log("Тест переміщення у переповнену чергу: створимо міні-чергу з max_size=1 і спробуємо move_plate_to.")
    small = Queue("small", max_size=1)
    # додати до small один елемент
    try:
        small.enqueue(declarations[1])
        log("small.enqueue succeeded.")
        # спробуємо перемістити інше авто у small з general
        general.move_plate_to(declarations[2].plate, small)
        log("ERROR: move to full queue succeeded unexpectedly.")
    except QueueFullError as e:
        log(f"Expected QueueFullError caught: {e}")
    except QueueError as e:
        log(f"Other QueueError during move to full queue: {e}")

    # підсумок
    log("Підсумок: розмір черг по завершенні сценарію.")
    log(f"general size: {general.size()}")
    log(f"green_corridor size: {green.size()}")
    log("Кінець сценарію.")

if __name__ == "__main__":
    try:
        run_scenario()
    except Exception as e:
        print("Unhandled exception:", e)
        raise