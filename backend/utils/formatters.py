from datetime import datetime
from typing import Dict, Any, Union

def format_currency(amount: float) -> str:
    """Format currency values with 2 decimal places."""
    return f"${amount:.2f}"

def format_datetime(dt: datetime) -> str:
    """Format datetime to string."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def format_sales_summary(summary: Dict[str, float]) -> Dict[str, str]:
    """Format sales summary with currency formatting."""
    return {k: format_currency(v) for k, v in summary.items()}

def format_order_response(order: Dict[str, Any]) -> Dict[str, Any]:
    """Format order response with proper currency and datetime formatting."""
    formatted = order.copy()
    formatted['total_amount'] = format_currency(order['total_amount'])
    formatted['created_at'] = format_datetime(order['created_at'])
    if order.get('completed_at'):
        formatted['completed_at'] = format_datetime(order['completed_at'])
    return formatted