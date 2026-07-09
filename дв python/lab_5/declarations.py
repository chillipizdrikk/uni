# declarations.py - шаблон митної декларації як dataclass і список incoming_declarations з 18 елементів
from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class Declaration:
    # поля шаблону декларації
    truck_make: str           # марка/модель авто
    plate: str                # номер авто (унікальний у списку)
    owner: str                # власник / компанія
    date: str                 # дата у форматі YYYY-MM-DD
    origin: Tuple[str,str]    # (країна, місто)
    destination: Tuple[str,str] # (країна, місто)
    goods_name: str           # назва товару
    goods_value: float        # вартість товару у валюті (USD)
    contract: bool            # чи є договір перевезення
    weight: float             # вага вантажу в тоннах
    hazardous: List[str]      # список позначок про небезпеку, пустий список якщо немає
    documents_valid: bool     # чи валідні документи

# 18 елементів даних
incoming_declarations = [
    Declaration("Volvo", "D1093AH", "Green Day Co", "2025-10-25", ("Poland","Wroclaw"), ("Ukraine","Vinnytsia"), "Electronics", 25000.0, True, 12.5, [], True),
    Declaration("Scania", "B204XZ", "TransGlobal", "2025-10-25", ("Germany","Hamburg"), ("Ukraine","Kyiv"), "Automobile parts", 15000.0, True, 10.0, [], True),
    Declaration("MAN", "AA123BB", "LogiX", "2025-10-24", ("Romania","Cluj"), ("Ukraine","Odessa"), "Textiles", 8000.0, True, 8.4, [], True),
    Declaration("Mercedes", "TRK-998", "BlackSeaFreight", "2025-10-24", ("Turkey","Istanbul"), ("Ukraine","Odessa"), "Fruits", 4000.0, True, 9.0, [], True),
    Declaration("DAF", "KD-555", "AgroTrans", "2025-10-23", ("Poland","Gdansk"), ("Ukraine","Lviv"), "Grains", 12000.0, True, 20.0, [], True),
    Declaration("Iveco", "PLT-77", "FastCargo", "2025-10-23", ("Hungary","Budapest"), ("Ukraine","Uzhhorod"), "Machinery", 30000.0, True, 15.0, [], True),
    Declaration("Volvo", "ZZ9991", "NordicLines", "2025-10-22", ("Sweden","Malmo"), ("Ukraine","Kyiv"), "Furniture", 7000.0, False, 11.0, [], True),
    Declaration("Scania", "GHT-321", "EastLink", "2025-10-22", ("Bulgaria","Sofia"), ("Ukraine","Odesa"), "Paper", 2200.0, True, 6.0, [], True),
    Declaration("MAN", "MK-2020", "SeaCarrier", "2025-10-21", ("Romania","Bucharest"), ("Ukraine","Kyiv"), "Chemicals", 50000.0, True, 5.0, ["flammable"], True),
    Declaration("Mercedes", "OP-444", "QuickMove", "2025-10-21", ("Slovakia","Kosice"), ("Ukraine","Lviv"), "Textiles", 9000.0, True, 7.0, [], False),  # documents invalid
    Declaration("DAF", "TR-111", "BorderExpress", "2025-10-20", ("Poland","Rzeszow"), ("Ukraine","Chernivtsi"), "Electronics", 27000.0, True, 13.0, [], True),
    Declaration("Iveco", "AV-777", "Green Day Co", "2025-10-20", ("Lithuania","Vilnius"), ("Ukraine","Kyiv"), "Pharmaceuticals", 45000.0, True, 2.0, ["controlled_substance"], True),
    Declaration("Volvo", "OD-500", "OdessaTrans", "2025-10-19", ("Romania","Constanta"), ("Ukraine","Odessa"), "Seafood", 6000.0, True, 4.0, [], True),
    Declaration("Scania", "QW-908", "TransGlobal", "2025-10-19", ("Poland","Poznan"), ("Ukraine","Kharkiv"), "Metal scraps", 3000.0, True, 18.0, [], True),
    Declaration("MAN", "PL-321", "AgroTrans", "2025-10-18", ("Hungary","Debrecen"), ("Ukraine","Vinnytsia"), "Grains", 10000.0, True, 19.0, [], True),
    Declaration("Mercedes", "LM-404", "BlackSeaFreight", "2025-10-18", ("Turkey","Izmir"), ("Ukraine","Odesa"), "Machinery", 35000.0, True, 16.0, [], True),
    Declaration("DAF", "ED-808", "EastLink", "2025-10-17", ("Bulgaria","Varna"), ("Ukraine","Odessa"), "Electronics", 18000.0, True, 9.5, [], True),
    Declaration("Iveco", "PR-009", "SecureCargo", "2025-10-17", ("Germany","Munich"), ("Ukraine","Lviv"), "Explosives", 0.0, False, 1.0, ["explosive"], False),
]