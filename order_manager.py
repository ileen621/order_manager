import json
import os

INPUT_FILE = "orders.json"
OUTPUT_FILE = "output_orders.json"


def load_data(filename: str) -> list:
    """讀取指定檔案的 JSON 資料，若檔案不存在則返回空列表。"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_orders(filename: str, orders: list) -> None:
    """將訂單列表儲存為 JSON 檔案。"""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(orders, file, indent=4, ensure_ascii=False)


def calculate_order_total(order: dict) -> int:
    """計算單筆訂單的總金額。"""
    total = 0
    for item in order["items"]:
        total += item["price"] * item["quantity"]
    return total


def print_order_report(data: list, title: str = "訂單報表", single: bool = False) -> None:
    """顯示訂單報表，可顯示單筆訂單或多筆訂單。"""
    print(f"\n==================== {title} ====================")
    if single:
        orders = [data]
    else:
        orders = data

    for i, order in enumerate(orders):
        if not single:
            print(f"訂單 #{i + 1}")
        print(f"訂單編號: {order['order_id']}")
        print(f"客戶姓名: {order['customer']}")
        print("-" * 50)
        print("商品名稱\t單價\t數量\t小計")
        print("-" * 50)
        for item in order["items"]:
            print(f"{item['name']}\t{item['price']}\t{item['quantity']}\t{item['price'] * item['quantity']}")
        print("-" * 50)
        print(f"訂單總額: {calculate_order_total(order):,}")
        print("=" * 50)


def add_order(orders: list) -> str:
    """新增訂單至列表，若訂單編號重複則返回錯誤訊息。"""
    order_id = input("請輸入訂單編號：").upper()

    # 檢查訂單編號是否重複
    if any(order["order_id"] == order_id for order in orders):
        return f"錯誤：訂單編號 {order_id} 已存在！"

    customer = input("請輸入顧客姓名：")
    items = []
    while True:
        name = input("請輸入訂單項目名稱（輸入空白結束）：")
        if not name:
            break
        while True:  # 內部迴圈處理價格輸入
            try:
                price = int(input("請輸入價格："))
                if price < 0:
                    print("=> 錯誤：價格不能為負數，請重新輸入")
                    continue  # 價格錯誤，繼續輸入價格
                break  # 價格輸入正確，跳出內部迴圈
            except ValueError:
                print("=> 錯誤：價格必須為整數，請重新輸入")
                continue  # 價格輸入錯誤，繼續輸入價格

        while True:  # 內部迴圈處理數量輸入
            try:
                quantity = int(input("請輸入數量："))
                if quantity <= 0:
                    print("=> 錯誤：數量必須為正整數，請重新輸入")
                    continue  # 數量錯誤，繼續輸入數量
                break  # 數量輸入正確，跳出內部迴圈
            except ValueError:
                print("=> 錯誤：數量必須為整數，請重新輸入")
                continue  # 數量輸入錯誤，繼續輸入數量

        items.append({"name": name, "price": price, "quantity": quantity})

    if not items:
        return "=> 至少需要一個訂單項目"

    orders.append({"order_id": order_id, "customer": customer, "items": items})
    return f"=> 訂單 {order_id} 已新增！"


def process_order(orders: list) -> tuple:
    """處理訂單並將其轉移到已完成訂單。"""
    print("\n======== 待處理訂單列表 ========")
    for i, order in enumerate(orders):
        print(f"{i + 1}. 訂單編號: {order['order_id']} - 客戶: {order['customer']}")
    print("================================")

    while True:
        choice = input("請選擇要出餐的訂單編號 (輸入數字或按 Enter 取消): ")
        if not choice:
            return None, None
        try:
            index = int(choice) - 1
            if 0 <= index < len(orders):
                order = orders.pop(index)
                return f"=> 訂單 {order['order_id']} 已出餐完成", order
            else:
                print("=> 錯誤：請輸入有效的數字")
        except ValueError:
            print("=> 錯誤：請輸入有效的數字")


def main():
    """程式主流程，包含選單迴圈和各功能的調用。"""
    orders = load_data(INPUT_FILE)
    output_orders = load_data(OUTPUT_FILE)

    while True:
        print("\n***************選單***************")
        print("1. 新增訂單")
        print("2. 顯示訂單報表")
        print("3. 出餐處理")
        print("4. 離開")
        print("**********************************")

        choice = input("請選擇操作項目(Enter 離開)：")
        if not choice:
            break

        if choice == "1":
            message = add_order(orders)
            print(message)
            if "=> 訂單" in message:
                save_orders(INPUT_FILE, orders)
        elif choice == "2":
            print_order_report(orders)
        elif choice == "3":
            message, processed_order = process_order(orders)
            if message:
                print(message)
                if processed_order:
                    print_order_report(processed_order, title="出餐訂單", single=True)
                    output_orders.append(processed_order)
                    save_orders(INPUT_FILE, orders)
                    save_orders(OUTPUT_FILE, output_orders)
        elif choice == "4":
            break
        else:
            print("=> 請輸入有效的選項 (1-4)")

# 這段程式碼原本的位置錯誤，它應該在 add_order 函數裡面
# if not items:
#     return "=> 至少需要一個訂單項目"



if __name__ == "__main__":
    main()

