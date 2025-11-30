from pages.base_page import BasePage
from playwright.sync_api import expect


class EmailPage(BasePage):
    def __init__(self, page):
        self.page = page
        self.email_button = page.get_by_role("button", name="E-Mail")
        self.remove_button = page.get_by_role("button", name="Remove")

    def validate_cannot_remove_primary_email(self, email):
        self.wait_dialog()
        self.ensure_page_is_stable()
        self.remove_button.click()
        expect(self.page.get_by_text(f"You cannot remove your primary email address ({email}).")).to_be_visible()

    def wait_dialog(self):
        def handle_dialog(dialog):
            assert dialog.message == "Do you really want to remove the selected e-mail address?"
            self.page.wait_for_timeout(2000)
            dialog.accept()

        self.page.on("dialog", handle_dialog)

    def open_email_section(self):
        self.ensure_page_is_stable()
        self.email_button.click()
