import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from pages.base_page import BasePage
from pages.email_page import EmailPage
from pages.rewards_page import RewardsPage
from pages.sign_in import SignInPage
from pages.sign_up import SignUpPage


@pytest.mark.require_auth
@pytest.mark.regression
def test_redeem_points_amount(page):
    """
    - Log into the system with a valid user
    - Redeem reward by reward name
    - Points redeemed are the same as cost of reward
    """
    print(test_redeem_points_amount.__doc__)
    chosen_reward = "Potion of Endless Coffee"
    amount_points_after_redeem = 0
    cost_of_reward = 0
    rewards_page = RewardsPage(page)
    page.goto("/")
    rewards_page.add_bonus(15)

    rewards_page.redeem_reward(chosen_reward)
    cost_of_reward = rewards_page.get_cost_of_reward(chosen_reward)
    amount_points_after_redeem = rewards_page.get_current_redeemed_points()

    assert (
        amount_points_after_redeem == cost_of_reward
    ), (f"The chosen award {chosen_reward} costs {cost_of_reward}pts. "
       f"Redeem points are {amount_points_after_redeem} points but user should have {cost_of_reward} redeemed points."
    )

@pytest.mark.require_auth
@pytest.mark.regression
def test_redeem_un_redeem(page):
    """
    - Log into the system with a valid user
    - Redeem reward by reward name
    - Unredeem reward by reward name
    - Points redeemed are updated accordingly
    """
    print(test_redeem_un_redeem.__doc__)
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
    ), f"Expected the amount of redeemed points after redeeming {amount_points_after_redeem} to be higher than before {amount_points_after_un_redeem}."

@pytest.mark.require_auth
@pytest.mark.regression
def test_redeem_reward(page):
    """
    - Log into the system with a valid user
    - Adds bonus
    - Redeem reward by reward name
    - User sees a sucessfull alert message
    - Remaining points are updated accordingly (calculation: points before - cost of reward)
    """
    print(test_redeem_reward.__doc__)
    chosen_reward = "Potion of Endless Coffee"
    confirmation_alert = f"You successfully claimed the following rewards: {chosen_reward}"
    amount_points_before_claiming = 0
    amount_points_after_claiming = 0
    expected_result = 0
    cost_of_reward = 0
    rewards_page = RewardsPage(page)
    page.goto("/")

    rewards_page.add_bonus(15)
    amount_points_before_claiming = rewards_page.get_current_remaining_points()

    rewards_page.redeem_reward(chosen_reward)
    cost_of_reward = rewards_page.get_cost_of_reward(chosen_reward)
    rewards_page.claim_rewards()

    rewards_page.validate_alert_message(confirmation_alert)
    amount_points_after_claiming = rewards_page.get_current_remaining_points()
    expected_result = amount_points_before_claiming - float(cost_of_reward)

    assert (
        amount_points_after_claiming == expected_result
    ), (f"The chosen award {chosen_reward} costs {cost_of_reward}pts. "
       f"as the remaining points were {amount_points_before_claiming} the user should have {expected_result} points "
       f"but has {amount_points_after_claiming} points"
    )

@pytest.mark.require_auth
@pytest.mark.regression
def test_user_cannot_claim_when_out_of_points(page, add_5_points):
    """
    - Log into the system with a valid user
    - Forfeit points
    - Validate claim button is disabled
    """
    print(test_user_cannot_claim_when_out_of_points.__doc__)
    expected_remaining_points = 0
    remaining_points = 0
    rewards_page = RewardsPage(page)
    page.goto("/")
    rewards_page.forfeit_bonus()
    remaining_points = rewards_page.get_current_remaining_points()
    rewards_page.validate_user_cannot_claim_rewards()
    assert (
        remaining_points == expected_remaining_points
    ), (f"Remaining points are {remaining_points} points."
       f"but it should be {expected_remaining_points} points as the bonus were forfeited."
    )


@pytest.mark.require_auth
@pytest.mark.regression
def test_add_bonus(page):
    """
    - Log into the system with a valid user
    - Adds bonus
    - Refresh page
    - Bonus is there
    - Total points amount is correct
    """
    print(test_add_bonus.__doc__)
    rewards_page = RewardsPage(page)
    amount_points_remaining_before = 0
    amount_points_remaining_after = 0
    total_points = 0
    bonus = 15
    page.goto("/")
    amount_points_remaining_before = rewards_page.get_current_remaining_points()
    rewards_page.add_bonus(bonus)
    amount_points_remaining_after = rewards_page.get_current_remaining_points()
    total_points = amount_points_remaining_before + bonus
    page.reload()

    assert (
            amount_points_remaining_after == total_points
        ), (f"Points after adding bonus were {amount_points_remaining_after} points"
            f"but should be {total_points} points."
        )

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


@pytest.mark.regression
def test_links(page):
    """
    - Open links
    - Status code is 200
    """
    print(test_links.__doc__)
    links = ["holistiplan", "Home", "Sign Up", "Sign In", "About"]
    base_page = BasePage(page)
    page.goto("/")
    for linkTitle in links:
        base_page.ensure_page_is_stable()
        page.get_by_role("link", name=linkTitle).first.click()
        response = page.goto(page.url)
        assert response.status == 200, f"Expected status code 200 in link {page.url} but got {response.status}"
