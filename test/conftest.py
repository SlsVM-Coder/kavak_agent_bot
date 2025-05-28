import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.recommendation_service import CATALOG_CSV_PATH


@pytest.fixture(autouse=True)
def fake_catalog(tmp_path, monkeypatch):
    fake = tmp_path / "catalog.csv"
    fake.write_text(
        "stock_id,make,model,year,price\n1,Toyota,Corolla,2020,300000")
    monkeypatch.setenv("CATALOG_CSV_PATH", str(fake))
    yield


@pytest.fixture
def client():
    return TestClient(app)
