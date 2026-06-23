"""Tests for restocking-related API endpoints."""
import pytest
import sys
from pathlib import Path

server_path = Path(__file__).parent.parent.parent / "server"
sys.path.insert(0, str(server_path))

import main as app_module


@pytest.fixture(autouse=True)
def clear_restocking_orders():
    app_module.restocking_orders.clear()
    yield
    app_module.restocking_orders.clear()


class TestDemandUnitCost:
    def test_demand_forecasts_include_unit_cost(self, client):
        response = client.get("/api/demand")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        for item in data:
            assert "unit_cost" in item
            assert isinstance(item["unit_cost"], float)
            assert item["unit_cost"] > 0
