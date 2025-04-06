import json
from typing import List, Dict, Tuple, Optional

INPUT_FILE = "orders.json"
OUTPUT_FILE = "output_orders.json"

def load_data(filename: str) -> List[Dict]:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_orders(filename: str, orders: List[Dict]) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=4)

def add_order(orders: List[Dict]) -> str:
    order_id = input("請輸入訂單編號：").strip()
    if any(order['order_id'] == order_id for order in orders):
        return f"=> 錯誤：訂單編號 {order_id} 已存在！"
    
    customer = input("請輸入顧客姓名：").strip()
    items = []
    while True:
        name = input("請輸入訂單項目名稱（輸入空白結束）：").strip()
        if not name:
            break
        
        # 單價輸入驗證
        while True:
            try:
                price = int(input("請輸入價格："))
                if price <= 0:
                    print("=> 錯誤：價格不能為負數，請重新輸入")
                    continue  
                break
            except ValueError:
                print("=> 錯誤：價格或數量必須為整數，請重新輸入")
        
        # 數量輸入驗證
        while True:
            try:
                quantity = int(input("請輸入數量："))
                if quantity <= 0:
                    print("=> 錯誤：數量必須為正整數，請重新輸入")
                    continue  
                break
            except ValueError:
                print("=> 錯誤：價格或數量必須為整數，請重新輸入")
        
        items.append({"name": name, "price": price, "quantity": quantity})
    
    if not items:
        return "=> 至少需要一個訂單項目"
    
    orders.append({"order_id": order_id, "customer": customer, "items": items})
    save_orders(INPUT_FILE, orders)
    return f"=> 訂單 {order_id}  已新增！"

def print_order_report(data: List[Dict], title: str = "訂單報表", single: bool = False) -> None:
    if not data:
        print("目前沒有訂單。")
        return

    print(f"\n{'='*20} {title} {'='*20}")
    for idx, order in enumerate(data, 1):   
        print(f"訂單 #{idx}")
        print(f"訂單編號: {order['order_id']}")
        print(f"客戶姓名: {order['customer']}")
        print("-" * 50)
        print(f"{'商品名稱 '}{'單價':<6}{'數量':<6}{'小計'}")
        print("-" * 50)
        total = 0
        for item in order['items']:
            subtotal = item['price'] * item['quantity']
            total += subtotal
            print(f"{item['name']}\t {item['price']:<8}{item['quantity']:<8}{subtotal}")
        print("-" * 50)
        print(f"訂單總額: {total:,}")
        print("=" * 50)
        print(" ")

def process_order(orders: List[Dict]) -> Tuple[str, Optional[Dict]]:

    if not orders:
        return ("目前無待處理訂單。", None)

    print("\n======== 待處理訂單列表 ========")
    for idx, order in enumerate(orders, 1):
        print(f"{idx}. 訂單編號: {order['order_id']} - 客戶: {order['customer']}")
    print("================================")

    while True:
        selection = input("請選擇要出餐的訂單編號 (輸入數字或按 Enter 取消): ").strip()
        if not selection:
            return ("=> 取消出餐操作。", None)
        if not selection.isdigit() or not (1 <= int(selection) <= len(orders)):
            print("=> 錯誤：請輸入有效的數字。")
            continue
        index = int(selection) - 1
        order = orders.pop(index)
        return (f" 訂單 {order['order_id']} 已出餐完成\n出餐訂單詳細資料：", order)

def main() -> None:
    _orders = load_data(INPUT_FILE)
    done_orders = load_data(OUTPUT_FILE)
    while True:
        print("***************選單***************")
        print("1. 新增訂單")
        print("2. 顯示訂單報表")
        print("3. 出餐處理")
        print("4. 離開")
        print("**********************************")
        choice = input("請選擇操作項目(Enter 離開)：").strip()
        if choice == "":
            print("已離開程式。")
            break
        elif choice == "1":
            result = add_order(_orders)
            print(result)
        elif choice == "2":
            print_order_report(_orders)
        elif choice == "3":
            message, processed = process_order(_orders)
            print(f"=> {message}")
            if processed:
                done_orders.append(processed)
                save_orders(INPUT_FILE, _orders)
                save_orders(OUTPUT_FILE, done_orders)
                print_order_report([processed], title="出餐訂單", single=True)
        elif choice == "4":
            print("已離開程式。")
            break
        else:
            print("=> 請輸入有效的選項（1-4）")

if __name__ == "__main__":
    main()
