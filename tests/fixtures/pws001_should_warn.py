import time


def test_login(page):
    page.goto("/login")
    time.sleep(3)
