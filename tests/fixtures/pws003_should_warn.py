def test_dashboard(page):
    page.goto("/dashboard")
    page.wait_for_load_state("networkidle")
