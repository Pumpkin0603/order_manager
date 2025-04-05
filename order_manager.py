import json
from typing import List, Dict, Tuple, Optional

INPUT_FILE = "orders.json"
OUTPUT_FILE = "output_orders.json"

def main() -> None:

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
            print("新增訂單。")
        elif choice == "2":
            print("顯示訂單報表。")
        elif choice == "3":
            print("出餐處理。")
        elif choice == "4":
            print("已離開程式。")
            break
        else:
            print("=> 請輸入有效的選項（1-4）")

if __name__ == "__main__":
    main()