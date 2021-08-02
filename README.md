
# hckrnws

A [hackernews](https://news.ycombinator.com/) client for fetching top posts and servers them chronologically with user specific features.


❗ If the project had login issues, please pull the latest changes and run it again.

## Features

- Management command to fetch new posts (run as CRON job)
- Chronologically sorted posts
- Delete or mark posts as read
- Fully secure with Token based authentication

  
## Demo

Registration
![registerpage](https://user-images.githubusercontent.com/35267629/127806000-d0def59b-6fe7-4e24-b539-992cb5124adc.png)

Registration error handling  
![registererrors](https://user-images.githubusercontent.com/35267629/127806153-cd412981-a807-4eb2-b016-9de3a61bfc14.png)

Login page and error handling
![loginerrors](https://user-images.githubusercontent.com/35267629/127805986-7770b91c-e47d-45e8-9647-a8737450529e.png)

Chronologically sorted posts
![posts](https://user-images.githubusercontent.com/35267629/127805993-4afe8b78-f832-4d9d-a575-836a2131bec1.png)

Read posts are highlighted for the user
![read_posts](https://user-images.githubusercontent.com/35267629/127805998-1cfebad4-fd4b-4b43-9819-57f38229bf84.png)

Post order before deleting a post from the user's dashboard
![posts_before_del](https://user-images.githubusercontent.com/35267629/127806316-3c0c72d4-a2ea-44df-b2b3-1bb9003fbedd.png)

Post order after deleting the post
![posts_after_del](https://user-images.githubusercontent.com/35267629/127805996-b8d67bc6-71e0-432a-adc7-cf19378a1d65.png)

Normal posts with comment count
 
![normal_comments](https://user-images.githubusercontent.com/35267629/127805988-344137ac-6bda-4313-b367-24e3b82513cd.png)

Discussion posts without comment count

![discussion](https://user-images.githubusercontent.com/35267629/127805985-76f4e280-04a1-4994-9911-d7fa3e8cdf9f.png)

API response for fetching posts and their status for a user
![api_response](https://user-images.githubusercontent.com/35267629/127806676-27f0a56e-b1f3-40b3-a276-fadbb87134d0.png)
## Run Locally

### Clone the project

```bash
  git clone https://github.com/imnitishng/hkrnws
  cd hkrnws
```

### Setup backend
Create python virtual environment, install python dependencies, fetch hackernews posts and run serve them via the backend server

```bash
  # Setup python
  cd hkrnws-backend
  python3 -m venv ./venv
  source ./venv/bin/activate
  pip install -r requirements.txt

  # Run migrations and fetch some posts
  python manage.py makemigrations && python manage.py migrate
  python manage.py fetch_posts

  # Run server
  python manage.py runserver
```

### Setup frontend
Install node dependencies

```bash
  cd hkrnws-frontend
  npm install
```

Start the server

```bash
  npm run start
```

Open [http://localhost:3000/](http://localhost:3000/) on the machine to use the app.
## Running management command to fetch new posts 

To fetch and update posts from hackernews, run

```bash
  python manage.py fetch_posts
```

  
## Roadmap

- Add dockerfile and containerize the app for easier development and deployment

- Add more post sorting techniques

- Deploy the app

- Add backend tests to improve coverage

  