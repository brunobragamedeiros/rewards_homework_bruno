import os
import random
import string

import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

AUTH_FILE = "auth.json"
load_dotenv()


@pytest.fixture(scope="function")
def context(request, ensure_auth_state):
    url = os.getenv("BASE_URL")
    storage_state_file = AUTH_FILE if "require_auth" in request.keywords else None

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        ctx = browser.new_context(base_url=url, record_video_dir="videos", storage_state=storage_state_file)
        yield ctx

        ctx.close()
        browser.close()


@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    page.set_default_timeout(10000)
    page.set_default_navigation_timeout(50000)
    yield page
    page.close()


@pytest.fixture(scope="session")
def ensure_auth_state():
    url = os.getenv("BASE_URL")
    username = os.getenv("USER_ADDRESS")
    password = os.getenv("USER_PASSWORD")
    if os.path.exists(AUTH_FILE):
        print("auth.json was found")
        return

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(base_url=url)
        page = context.new_page()
        page.set_default_timeout(50000)
        page.set_default_navigation_timeout(50000)
        page.goto("/accounts/login/")
        page.get_by_placeholder("Email address").fill(username)
        page.get_by_placeholder("Password").fill(password)
        page.get_by_role("button", name="Sign In").click()
        context.storage_state(path=AUTH_FILE)
        browser.close()


@pytest.fixture
def add_5_points(page):
    base_url = os.getenv("BASE_URL")

    csrftoken = next((c["value"] for c in page.context.cookies() if c["name"] == "csrftoken"), None)
    response = page.request.post(
        f"{base_url}/bonus/",
        data={"numPoints": 5.0},  # it always adds 5 regardless the specified amount - needs to be improved
        headers={
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        },
    )
    # Print status code
    print("Status code:", response.status)

    # Try to parse JSON, fallback to text
    try:
        data = response.json()
        print("Response JSON:", data)
    except Exception:
        text = response.text()
        print("Response Text:", text)

    yield


@pytest.fixture
def logout(page):
    yield
    page.goto("/accounts/logout/")
    page.get_by_role("button", name="Sign Out").click()
    assert page.get_by_text("You have signed out.").is_visible()


def _random_string(length=10, chars=string.ascii_letters + string.digits):
    return "".join(random.choice(chars) for _ in range(length))


@pytest.fixture
def random_email():
    local = _random_string(8).lower()
    domain = _random_string(5).lower()
    return f"{local}@{domain}.com"


@pytest.fixture
def random_password():
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + "!@#$%^&*()?"
    return _random_string(12, chars)
