#!/usr/bin/env python3
#
# This file tests the basic web server defined in 'web_server.py'.

import pytest

from web_server import app


@pytest.fixture
def client():
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


def test_init_returns_ok(client):
    response = client.get("/init")
    assert response.status_code == 200


def test_test_returns_ok_with_params(client):
    response = client.get("/test?name=Ted&age=25")
    assert response.status_code == 200
