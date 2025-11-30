
# Automation Overview


Let's talk about automation!

I created **8 test cases** covering some interesting aspects of the system.  
These test cases are categorized into the following tags:

- **smoke**
- **nightly**
- **regression**


| Title | Goal | Why? | Tag |
|------|------|------|------|
| Redeem points |Verify if after redeeming rewards the points redeemed are equal the cost of the reward | Critical workflow | Regression |
| Redeem/Unredeem | Similar as the previous test but now focused on the behavior of unredeeming rewards, the redeem points must update accordingly | Critical workflow | Regression |
| Redeem reward | Verify if user is able to redeem rewards and checks if remaining points are updated accordingly | Critical workflow | Regression |
| Can not claim when out of points | Verify if user can not claim rewards when points = 0 | Critical workflow | Regression |
| Add bonus | Verify if user is able to add points, remaining points must update accordingly | Critical workflow | Regression |
| Primary key | Verify if user can not remove their own primary key | This is not a critical workflow but from past experience I need to say it is valuable to have this test, it will make supports team very happy | Nightly
| Sign up confirmation | Verify if user can not login after signing up and not confirming the address | Not very critical as well but it is an important security check point as it prevents the creation of fake accounts | Nightly
| Links | Check if links in the page return 200 | It hurts to have 404 pages in prod, to prevent overlooked 404s on rarely accessed pages, I created this test case as a safety check | Smoke |

## Run tests


### Prerequisites
- Ensure the system is running at: `http://localhost:3030`.

### Steps


##### 1. Navigate to the test directory

    cd e2e

##### Create Environment File

Create a `.env` file in the e2e folder with the following content:

    BASE_URL=http://localhost:3000
    USER_ADDRESS=your_user_address_here
    USER_PASSWORD=your_password_here

##### 2. Create and activate a virtual environment

    python -m venv venv

`source venv/bin/activate`  for Linux/macOS
`venv\Scripts\activate`  for Windows

##### 3. Install required packages

    pip install -r requirements.txt

##### 4. Install playwright browsers

    playwright install

##### Run tests

    pytest tests/tests.py --reruns 2 --html=report.html --self-contained-html

You can also add markers for specific groups. Example:

    Smoke:
        pytest -m smoke tests/tests.py --reruns 2 --html=report.html --self-contained-html
    
    Regression:
        pytest -m regression tests/tests.py --reruns 2 --html=report.html --self-contained-html
    
    Nightly:
        pytest -m nightly rests/tests.py --reruns 2 --html=report.html --self-contained-html

### Continuous integration

This was my first time coding with Playwright + Pytest. As I found the homework interesting, I wanted to see how it would perform in CI. I created a very basic workflow (thanks for sharing the CI.yaml, most of the setup was easily reused!) with video upload and pytest-html report generation. I found out the tests in CI are running less stable than locally, but it was a great learning experience to set up the CI workflow.

### Remaining challenges

While I did my best to cover the key areas having in mind the system goal and my past experience, there are a few topics that I'd like to have improved in this test suite

 - CI: As already mentioned, tests in CI should be more stable. Currently there are 2 tests running as known failures (redeem points return wrong count and about link returning 404) but in CI there are around 4 tests failing
 - Parallelization: it is currently missing in this workflow. The test suite relies on a pre-defined user for tests requiring login, which prevents parallel execution because the shared resource would conflict if used simultaneously by multiple tests
 - Playwright request: to set up data for the tests I added a fixture to add bonus in a POST request, this fixture works but not as intended. Looks like the `numPoints` added in request data are not considered but the request adds 5 points regardless - to make the fixture widely used this should be improved
 - Pytest-html: it would be beneficial to have more content on the html such as screenshots, in this version there are only the steps defined in the test code

### Highlights

Few things that I see as achievements in the current work

- Suite of tests saves authentication for scenarios that require login, reducing repetitive steps
- Detailed logs to help debug points assertions
- Structured code following the Page Object Model (POM) pattern for maintainability and readability
- Intelligent element interaction: retrieves or interacts with specific elements reliably (redeeming a reward by name instead of redeeming by index)
