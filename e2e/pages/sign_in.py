from pages.base_page import BasePage
from playwright.sync_api import expect


class SignInPage(BasePage):
    def __init__(self, page):
        self.page = page
        self.email_field = page.get_by_placeholder("Email address")
        self.password_field = page.get_by_placeholder("Password")
        self.password_confirmation_field = page.get_by_placeholder("Password (again)")
        self.sign_in_button = page.get_by_role("button", name="Sign In")

    def sign_in(self, email, password):
        self.email_field.fill(email)
        self.password_field.fill(password)
        self.sign_in_button.click()
