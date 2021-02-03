#!/usr/bin/env python3
#
# This file tests the basic web server defined in 'web_server.py'.

import json
import urllib

from hypothesis import given, strategies as st, note
import pytest

from web_server import app


# Regular integration testing.
@pytest.fixture
def client():
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


def test_init_returns_ok(client):
    response = client.get("/init")
    json_response = json.loads(response.data)
    assert json_response.get("status") == 200


def test_test_returns_ok_with_params(client):
    response = client.get("/test?name=Ted&age=25")
    json_response = json.loads(response.data)
    assert json_response.get("status") == 200


# `hypothesis` testing.
@given(st.from_regex(r"\A\d{1,}\Z"), st.integers().filter(lambda x: x >= 18))
def test_test_returns_ok_with_arbitrary_inputs(client, name, age):
    url_string = f"/test?name={urllib.parse.quote(name.encode('utf-8'))}&age={age}"
    response = client.get(url_string)
    json_response = json.loads(response.data)
    assert json_response.get("status") == 200
