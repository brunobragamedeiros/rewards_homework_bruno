from playwright.sync_api import expect


class BasePage:
    def __init__(self, page):
        self.page = page

    def validate_page_header(self, pageTitle):
        expect(self.page.get_by_role("heading", name=pageTitle)).to_be_visible()

    def validate_page_description(self, pageDescription):
        expect(self.page.get_by_text(pageDescription)).to_be_visible()

    def validate_alert_message(self, alertMessage):
        expect(self.page.get_by_text(alertMessage)).to_be_visible()

    def open_link(self, link):
        self.page.get_by_role("link", name=link).first.click()
