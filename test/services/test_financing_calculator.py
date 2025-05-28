from app.services.financing_calculator import calculate_financing_plan


def test_financing_plan():
    plan = calculate_financing_plan(price=100000, down_payment=20000, years=5)
    # pago mensual calculado = préstamo 80000 a 5 años @10%
    assert plan["total_amount_paid"] > 80000
    assert "monthly_payment_amount" in plan
