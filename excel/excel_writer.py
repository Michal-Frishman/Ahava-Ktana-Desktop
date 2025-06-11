import os
import json
from openpyxl import Workbook
from datetime import datetime
from typing import Union, List, Dict
import logging as lg
logger = lg.getLogger("OrderExport")
logger.setLevel(lg.INFO)
formatter = lg.Formatter('%(asctime)s - %(levelname)s - %(message)s')

def setup_logger(log_dir: str) -> None:
    log_path = os.path.join(log_dir, "export_orders.log")
    file_handler = lg.FileHandler(log_path, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)



def parse_json_orders(orders: Union[str, List[Dict]]) -> Union[List[Dict], None]:
    if isinstance(orders, str):
        try:
            orders = json.loads(orders)
        except json.JSONDecodeError:
            logger.error("Invalid JSON format.")
            return None

    if not isinstance(orders, list) or not all(isinstance(o, dict) for o in orders):
        logger.error("Invalid structure – must be a list of dictionaries.")
        return None

    if not orders:
        logger.warning("No orders provided.")
        return None

    return orders


def create_output_folder(base_dir: str) -> str:
    today = datetime.today().strftime("%Y-%m-%d")
    full_path = os.path.join(base_dir, today)
    os.makedirs(full_path, exist_ok=True)
    setup_logger(full_path)
    logger.info(f"Output directory created: {full_path}")
    return full_path


def split_orders(orders: List[Dict], chunk_size: int) -> List[List[Dict]]:
    return [orders[i:i + chunk_size] for i in range(0, len(orders), chunk_size)]


def write_excel_file(orders_chunk: List[Dict], output_path: str, file_index: int) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Orders"

    headers = list(orders_chunk[0].keys())
    ws.append(headers)

    for order in orders_chunk:
        ws.append([order.get(k, "") for k in headers])

    today = datetime.today().strftime("%Y-%m-%d")
    filename = f"orders_{today}_{file_index}.xlsx"
    full_path = os.path.join(output_path, filename)
    wb.save(full_path)
    logger.info(f"Saved file: {full_path}")


def save_orders_to_excel(
    orders: Union[str, List[Dict]],
    output_dir: str = "data",
    max_per_file: int = 24
) -> bool:
    try:
        parsed_orders = parse_json_orders(orders)
        if parsed_orders is None:
            return False

        folder_path = create_output_folder(output_dir)
        chunks = split_orders(parsed_orders, max_per_file)

        for i, chunk in enumerate(chunks, start=1):
            write_excel_file(chunk, folder_path, i)
        logger.info(f"Successfully saved {len(chunks)} Excel file(s).")
        return True

    except Exception as e:
        logger.exception(f"Unexpected error occurred: {e}")
        return False
