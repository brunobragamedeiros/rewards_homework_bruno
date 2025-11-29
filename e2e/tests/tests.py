import logging
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pages.email_page import EmailPage
from pages.rewards_page import RewardsPage
from pages.sign_in import SignInPage
from pages.sign_up import SignUpPage


@pytest.mark.require_auth
@pytest.mark.regression
def test_redeem_un_redeem(page):
    """
    - Log into the system with a valid user
    - Redeem reward by reward name
    - Unredeem reward by reward name
    - Points redeemed are updated accordingly
    """
    print(test_add_bonus.__doc__)
    chosen_reward = "Potion of Endless Coffee"
    amount_points_after_redeem = 0
    amount_points_after_un_redeem = 0
    rewards_page = RewardsPage(page)
    page.goto("/")
    rewards_page.add_bonus(15)

    rewards_page.redeem_reward(chosen_reward)
    amount_points_after_redeem = rewards_page.get_current_redeemed_points()

    rewards_page.un_redeem_reward(chosen_reward)
    amount_points_after_un_redeem = rewards_page.get_current_redeemed_points()
    assert (
        amount_points_after_redeem > amount_points_after_un_redeem
    ), f"Expected the amount of redeemed points after redeeming {amount_points_after_redeem} to be higher than {amount_points_after_un_redeem}"


@pytest.mark.require_auth
@pytest.mark.regression
def test_redeem_reward(page):
    """
    - Log into the system with a valid user
    - Adds bonus
    - Redeem reward by reward name
    - User sees a sucessfull alert message
    """
    print(test_add_bonus.__doc__)
    chosen_reward = "Potion of Endless Coffee"
    confirmation_alert = f"You successfully claimed the following rewards: {chosen_reward}"
    amount_points_before_claiming = 0
    amount_points_after_claiming = 0
    rewards_page = RewardsPage(page)
    page.goto("/")
    rewards_page.add_bonus(15)
    amount_points_before_claiming = rewards_page.get_current_remaining_points()

    rewards_page.redeem_reward(chosen_reward)
    rewards_page.claim_rewards()
    rewards_page.validate_alert_message(confirmation_alert)
    amount_points_after_claiming = rewards_page.get_current_remaining_points()

    assert (
        amount_points_before_claiming > amount_points_after_claiming
    ), f"Expected the amount before claiming {amount_points_before_claiming} to be higher than {amount_points_after_claiming}"


@pytest.mark.require_auth
@pytest.mark.regression
def test_user_cannot_claim_when_out_of_points(page, add_5_points):
    """
    - Log into the system with a valid user
    - Forfeit points
    - Validate claim button is disabled
    """
    print(test_user_cannot_claim_when_out_of_points.__doc__)

    rewards_page = RewardsPage(page)
    page.goto("/")
    page.pause()
    rewards_page.forfeit_bonus()
    rewards_page.validate_remaining_points_are_displayed(0)
    rewards_page.validate_user_cannot_claim_rewards()


@pytest.mark.require_auth
@pytest.mark.regression
def test_add_bonus(page):
    """
    - Log into the system with a valid user
    - Adds bonus
    - Refresh page
    - Bonus is there
    """
    print(test_add_bonus.__doc__)
    rewards_page = RewardsPage(page)
    amount_points_remaining = 0

    page.goto("/")
    amount_points_remaining = rewards_page.get_current_remaining_points()
    rewards_page.add_bonus(15)
    page.reload()
    rewards_page.validate_remaining_points_are_displayed(amount_points_remaining + 15)


@pytest.mark.require_auth
@pytest.mark.regression
def test_primary_key(page):
    """
    - Log into the system with a valid user
    - Validate textual information
    - Attempt to remove primary email
    - User can not remove their own primary email
    """
    print(test_primary_key.__doc__)

    email_page = EmailPage(page)
    page.goto("/")
    email_page.open_link("My Profile")
    email_page.open_email_section()
    email_page.validate_page_header("E-mail Addresses")
    email_page.validate_page_description("The following e-mail addresses are associated with your account")
    email_page.validate_cannot_remove_primary_email("someone@holistiplan.com")


@pytest.mark.regression
def test_sign_up_confirmation(page, random_email, random_password):
    """
    - Sign up with new credentials
    - Validate email confirmation message
    - Attempt to login with new credentials
    - User can not login as the email is not yet verified
    """
    print(test_sign_up_confirmation.__doc__)

    sign_up_page = SignUpPage(page)
    sign_in_page = SignInPage(page)
    sign_up_header = "Sign Up"
    sign_up_text = "Already have an account? Then please sign in."
    confirmation_header = "Verify Your E-mail Address"
    confirmation_text = "We have sent an e-mail to you for verification. Follow the link provided to finalize the signup process. Please contact us if you do not receive it within a few minutes."
    confirmation_alert = f"Confirmation email sent to {random_email}."

    page.goto("/accounts/signup/")
    sign_up_page.validate_page_header(sign_up_header)
    sign_up_page.validate_page_description(sign_up_text)
    sign_up_page.sign_up(random_email, random_password, random_password)
    sign_up_page.validate_page_header(confirmation_header)
    sign_up_page.validate_page_description(confirmation_text)
    page.goto("/accounts/login/")
    sign_in_page.sign_in(random_email, random_password)
    sign_in_page.validate_page_header(confirmation_header)
    sign_in_page.validate_page_description(confirmation_text)
    sign_in_page.validate_alert_message(confirmation_alert)


@pytest.mark.smoke
def test_links(page):
    """
    - Open links
    - Status code is 200
    """
    print(test_links.__doc__)
    links = ["holistiplan", "Home", "Sign Up", "Sign In", "About"]
    page.goto("/")
    for linkTitle in links:
        page.get_by_role("link", name=linkTitle).first.click()
        response = page.goto(page.url)
        assert response.status == 200, f"Expected status code 200 in link {page.url} but got {response.status}"
