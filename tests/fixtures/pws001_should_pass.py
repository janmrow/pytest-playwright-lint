from time import sleep


def test_login(page):
    page.goto("/login")
    sleep(3)
