def calculate_financing_plan(
    price: float,
    down_payment: float,
    years: int,
    annual_rate: float = 0.10
) -> dict:
    principal = price - down_payment
    monthly_rate = annual_rate / 12
    n = years * 12
    if monthly_rate == 0:
        monthly = principal / n
    else:
        monthly = (principal * monthly_rate) / (1 - (1 + monthly_rate)**-n)
    total_paid = monthly * n + down_payment
    return {
        "monthly_payment_amount": monthly,
        "total_amount_paid":       total_paid,
    }
