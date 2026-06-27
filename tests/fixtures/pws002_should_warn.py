def test_login(page):
    page.goto("/login")
    page.wait_for_timeout(3000)
