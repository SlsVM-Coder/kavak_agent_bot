from app.services.recommendation_service import find_exact_model_year, recommend_cars


def test_find_exact_match():
    res = find_exact_model_year("Corolla 2020", threshold=80)
    assert len(res) == 1
    assert res[0]["model"] == "Corolla"


def test_recommend_fallback():
    # no exact → deberíamos recibir <=3 resultados
    res = recommend_cars("Nissan", limit=3)
    assert isinstance(res, list)
    assert len(res) <= 3
