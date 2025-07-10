from typing import Optional
from fastapi import HTTPException, status

def validate_stock_operation(current_stock: int, quantity: int, operation: str) -> None:
    """Validate stock operations to prevent negative stock."""
    if operation == "decrease" and current_stock < quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Current: {current_stock}, Requested: {quantity}"
        )

def validate_order_status_transition(current_status: str, new_status: str) -> None:
    """Validate order status transitions."""
    valid_transitions = {
        "pending": ["completed", "cancelled"],
        "completed": [],
        "cancelled": []
    }

    if new_status not in valid_transitions.get(current_status, []):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status transition from {current_status} to {new_status}"
        )

def validate_cash_report_operation(closing_amount: Optional[float] = None) -> None:
    """Validate cash report operations."""
    if closing_amount is not None and closing_amount < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Closing amount cannot be negative"
        )