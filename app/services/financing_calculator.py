def calculate_financing_plan(
    vehicle_price: float,
    down_payment_amount: float,
    term_years: int,
    annual_interest_rate: float = 0.10
) -> dict:
    # Monto a financiar
    financed_amount = vehicle_price - down_payment_amount
    # Convertir anos a meses
    loan_term_months = term_years * 12
    # Tasa de interes mensual
    monthly_interest_rate = annual_interest_rate / 12

    # Formula de amortizacion francesa para pagar un annuity
    monthly_payment_amount = (
        financed_amount * monthly_interest_rate
    ) / (
        1 - (1 + monthly_interest_rate) ** -loan_term_months
    )

    # Total que pagara el cliente (enganche + sumatoria de pagos mensuales)
    total_amount_paid = down_payment_amount + \
        (monthly_payment_amount * loan_term_months)

    return {
        "financed_amount":        round(financed_amount, 2),
        "loan_term_months":       loan_term_months,
        "monthly_interest_rate":  round(monthly_interest_rate, 6),
        "monthly_payment_amount": round(monthly_payment_amount, 2),
        "total_amount_paid":      round(total_amount_paid, 2),
        "annual_interest_rate":   annual_interest_rate
    }
