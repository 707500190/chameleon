from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.bilibili.com/")
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="频道").click()
    page1 = page1_info.value
    page1.get_by_role("link", name="搞笑", exact=True).click()
    page1.get_by_role("link", name="知识 24").click()
    with page1.expect_popup() as page2_info:
        page1.get_by_role("link", name="1.4万  453").click()
    page2 = page2_info.value

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
