#!/usr/bin/env python3
#
# This file tests the password validator defined in 'password_validator.py'.

from hypothesis import given, strategies as st
import pytest

from password_validation import password_is_valid


# Regular unit test suite
@pytest.mark.parametrize(
    "_input, _expected",
    [
        ("", False),
        ("ohautoeauna", False),
        ("732814084212", False),
        ("OAHUETNASU", False),
        ("&*&*()&", False),
        ("789&(*&(ht", False),
        ("aBcD1234@", True),
    ],
)
def test_password_matches_validation_for_inputs(_input, _expected):
    assert password_is_valid(_input) == _expected


# `hypothesis` test suite
@given(st.from_regex(r"(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]){8,}"))
def test_password_matches_validation_for_arbitrary_inputs(_input):
    assert password_is_valid(_input)
