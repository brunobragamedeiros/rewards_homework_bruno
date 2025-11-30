from pages.base_page import BasePage
from playwright.sync_api import expect


class SignUpPage(BasePage):
    def __init__(self, page):
        self.page = page
        self.email_field = page.get_by_placeholder("Email address")
        self.password_field = page.get_by_placeholder("Password", exact=True)
        self.password_confirmation_field = page.get_by_placeholder("Password (again)")
        self.sign_up_button = page.get_by_role("button", name="Sign Up")

    def sign_up(self, email, password, password_confirmation):
        self.ensure_page_is_stable()
        self.email_field.fill(email)
        self.password_field.fill(password)
        self.password_confirmation_field.fill(password_confirmation)
        self.sign_up_button.click()
