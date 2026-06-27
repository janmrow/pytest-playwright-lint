def test_login(page):
    page.goto("/login")
    page.get_by_role("button", name="Sign in").click()
