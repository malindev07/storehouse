from dataclasses import dataclass


@dataclass
class StoreHouse:
    service_id:str
    
    
@dataclass
class Position:
    id:str
    category:str
    sub_category:str
    name:str
    description:str
    balance:int # остаток
    min_balance:int # минимальный остаток
    purchase_price:float # цена закупки
    sale_price:float # цена продажи
    markup:float # наценка
    

    
    

    