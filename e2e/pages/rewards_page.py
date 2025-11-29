from pages.base_page import BasePage
from playwright.async_api import APIRequestContext
from playwright.sync_api import expect


class RewardsPage(BasePage):
    def __init__(self, page):
        self.page = page
        self.point_remaining_header = page.get_by_text("Ponts Remaining")
        self.points_remaining = self.point_remaining_header.locator("+ .card-body")
        self.point_redeemed_header = page.get_by_text("Ponts Redeemed")
        self.points_redeemed = self.point_redeemed_header.locator("+ .card-body")
        self.bonus_link = page.get_by_role("link")
        self.bonus_command = page.get_by_text("Need more points? Earn bonus points")
        self.forfeit_link = page.get_by_role("link", name="forfeit all points")
        self.hide_sidebar = page.get_by_role("link", name="Hide")
        self.claim_my_rewards_button = page.get_by_role("button", name="Claim my rewards")

    def validate_remaining_points_are_displayed(self, points):
        current_points_amount = float(self.points_remaining.inner_text())
        assert current_points_amount == points

    def add_bonus(self, points):
        expect(self.bonus_command).to_be_visible()
        self.bonus_link.filter(has_text=f"{points}").first.click()

    def forfeit_bonus(self):
        self.hide_sidebar.click()
        self.forfeit_link.click()
        expect(self.forfeit_link).not_to_be_visible()

    def validate_user_cannot_claim_rewards(self):
        expect(self.claim_my_rewards_button).to_be_visible()
        expect(self.claim_my_rewards_button).to_be_disabled()

    def claim_rewards(self):
        self.claim_my_rewards_button.click()

    def get_current_remaining_points(self):
        return float(self.points_remaining.inner_text())

    def get_current_redeemed_points(self):
        return float(self.points_redeemed.inner_text())

    def get_cookies(self):
        csrftoken = next((c["value"] for c in self.page.context.cookies() if c["name"] == "csrftoken"), None)
        return csrftoken

    def redeem_reward(self, reward):
        card = self.page.locator(".card").filter(has_text=reward)
        reward_button = card.locator("div > a", has_text="Redeem this Reward").first
        reward_button.click()

    def un_redeem_reward(self, reward):
        card = self.page.locator(".card").filter(has_text=reward)
        reward_button = card.locator("div > a", has_text="Un-redeem").first
        reward_button.click()
