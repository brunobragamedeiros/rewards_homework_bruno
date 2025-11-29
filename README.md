# Holistiplan Homework

Welcome to holistiplan's example rewards take home project!

## Basic Commands

### Running the site

This app integrates with a Vue frontend located in `vue_frontend`.

##### With Docker

The Vite dev server will automatically run in docker when started with the local.yml configuration.

```sh
docker-compose -f local.yml up --build -d
```

Once the docker containers are up, you can visit the site at http://localhost:3000

### Setting Up Your Users

A default user has already been created with the following credentials:

- _Email_: `someone@holistiplan.com`
- _Password_: `bfx!wkp3zve3WUX*guq`

To create another **normal user account** (if you need to), just go to Sign Up and fill out the form. Once you submit it,
you'll see a "Verify Your E-mail Address" page. Go to your docker desktop holistiplan/django container log output
to see a simulated email verification message. Copy the link into your browser. Now the user's email should be
verified and ready to go.


## Instructions
This task is simply intended to give us a look at how you would test a simple project and document what you find.  The assignment has a time cap of 4 hours as we do not what to monopolize your personal time. Additionally, this time does not need to be done in one large block.

For this exercise you will be required to do two tasks:

### Manual Testing

First, we would like you to spend some time in the UI. Do some exploratory testing. We have left some bugs for you to find. Make sure you go through the system to find these bugs. After you are satisfied document your findings including the following:

- Name of the bug
- What is happening?
- How do you reproduce it?
- Your thoughts on how severe it is. There is no scale here just looking for how you articulate.

The findings should be directed at developers who might have written the system.

### Automated Testing

Next, we would like to see you write some automated test. While we would prefer any coding to be done in Python, you may choose your testing library (e.g. Selenium, Cyprus, Playwright).

Your goal will be to pick which parts of the user experience need to be tested most and automate them. You do not need to test the whole site. Just pick a couple areas you feel are most important

## Deliverables

The final deliverable should be a repo you create with the following:

- The documentation from the Manual Testing. Please use markdown or text for this.
- Any code for the automated testing
- Readme on how to build/run the automated testing
- Documentation from the automated testing task. Also markdown.

Please make sure to reach if you have any questions.
