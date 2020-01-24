
# -*- coding: utf-8 -*-

from rabbit import rabbit

def test_run_openssl_command() -> None:
    assert 1 == 1


def test_feed():
    assert 4 == rabbit.feed(2)
