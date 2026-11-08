# Lab: Authenticating Users

## Features

A Flask API and React blog with a basic session-based login:

| Endpoint         | Method   | Behavior                                                                  |
| ---------------- | -------- | ------------------------------------------------------------------------- |
| `/login`         | `POST`   | Looks up a user by `username`, stores `user_id` in the session, returns the user (`200`). Returns `404` if the username doesn't exist. |
| `/logout`        | `DELETE` | Clears `user_id` from the session, returns no data (`204`).               |
| `/check_session` | `GET`    | Returns the logged-in user (`200`), or no data (`401`) if nobody is logged in. This keeps a user logged in across page refreshes. |

The session is stored in a signed cookie, which the React `proxy` setting in
`client/package.json` lets the browser send to the Flask server.

## Scenario

In this lab, we'll continue working on the blog site from the last lab and set
up a basic login feature.

## Tools & Resources

- [GitHub Repo](https://github.com/learn-co-curriculum/flask-authenticating-users-lab)
- [What is Authentication? - auth0](https://auth0.com/intro-to-iam/what-is-authentication)
- [API - Flask: class flask.session](https://flask.palletsprojects.com/en/2.2.x/api/#flask.session)

## Set Up

There is some starter code in place for a Flask API backend and a React
frontend. To get set up, run:

```bash
pipenv install && pipenv shell
npm install --prefix client
cd server
flask db upgrade
python seed.py
```

You can work on this lab by running the tests with `pytest -x`. It will also be
helpful to see what's happening during the request/response cycle by running the
app in the browser. You can run the Flask server with:

```bash
python app.py
```

And you can run React in another terminal with:

```bash
npm start --prefix client
```

You don't have to make any changes to the React code to get this lab working.
The React frontend has already defined a proxy in `package.json` as shown:

```json
"proxy": "http://localhost:5555",
```

The proxy avoids CORS issues and allows the server to set a session cookie to
store the user's login data.

## Instructions

### Task 1: Define the Problem

For our basic login feature, we'll need the following functionality:

- A user can log in by providing their username in a form.
- A user can log out.
- A user can remain logged in, even after refreshing the page.

We'll need to create the resources to handle each of these features.

### Task 2: Determine the Design

We'll need to build the following resources:

- `Login` is located at `/login`.

  - It has one route, `post()`.
  - `post()` gets a `username` from `request`'s JSON.
  - `post()` retrieves the user by `username` (we made these unique for you).
  - `post()` sets the session's `user_id` value to the user's `id`.
  - `post()` returns the user as JSON with a 200 status code.

- `Logout` is located at `/logout`.

  - It has one route, `delete()`.
  - `delete()` removes the `user_id` value from the session.
  - `delete()` returns no data and a 204 (No Content) status code.

- `CheckSession` is located at `/check_session`.
  - It has one route, `get()`.
  - `get()` retrieves the `user_id` value from the session.
  - If the session has a `user_id`, `get()` returns the user as JSON with a 200
    status code.
  - If the session does not have a `user_id`, `get()` returns no data and a 401
    (Unauthorized) status code.

### Task 3: Develop, Test, and Refine the Code

#### Step 1: Create Routes

- /login, post()
  - should handle the request to get username
  - find User in database by username. We'll need the id for the next step.
- /delete, delete()
- /check_session, get()

#### Step 2: Initialize, Retrieve, and/or Update Session

- Session: /login post()
  - set session['user_id'] to the found user's id
- Session: /logout delete()
  - remove the value for session['user_id']
- Session: /check_session get()
  - get current value of session['user_id'] (it may not exist)

#### Step 3: Return the Response

- Session: /login post()
  - return user as JSON with a 200 status code
- Session: /logout delete()
  - returns no data and a 204 (No Content) status code
- Session: /check_session get()
  - If the session has a `user_id`, `get()` returns the user as JSON with a 200
    status code.
  - If the session does not have a `user_id`, `get()` returns no data and a 401
    (Unauthorized) status code.

The tests are not looking for invalid users for /login, but if you have extra time, consider what response you should send if a user is not found with the given username.

#### Step 4: Test and Refine the Code

Run the test suite:

```bash
pytest
```

If any tests aren't passing, refine your code using each error message.

View the app in browser and test login, logout, and session persistence. Refine code if needed.

Feel free to also take a look at how the frontend logic is set up to use these endpoints.

#### Step 5: Commit and Push Git History

* Commit and push your code:

```bash
git add .
git commit -m "final solution"
git push
```

* If you created a separate feature branch, remember to open a PR on main and merge.

### Task 4: Document and Maintain

Best Practice documentation steps:
* Add comments to the code to explain purpose and logic, clarifying intent and functionality of your code to other developers.
* Update README text to reflect the functionality of the application following https://makeareadme.com. 
  * Add screenshot of completed work included in Markdown in README.
* Delete any stale branches on GitHub
* Remove unnecessary/commented out code
* If needed, update git ignore to remove sensitive data

## Important Submission Note

Before you submit your solution, you need to save your progress with git.

1. Add your changes to the staging area by executing `git add .`.
2. Create a commit by executing `git commit -m "Your commit message"`.
3. Push your commits to GitHub by executing `git push origin main`.

CodeGrade will grade your lab using the same tests as are provided in the `testing/` directory.