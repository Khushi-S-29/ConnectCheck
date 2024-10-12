from flask import Flask, render_template, request
import instaloader

app = Flask(__name__)

def login_instagram(username, password):
    loader = instaloader.Instaloader()
    try:
        loader.login(username, password)
        profile = instaloader.Profile.from_username(loader.context, username)
        return loader, profile
    except Exception as e:
        print(f"Login failed: {e}")
        return None, None

def get_followers(profile):
    return set(profile.get_followers())

def get_following(profile):
    return set(profile.get_followees())

def find_non_followers(followers, following):
    return following - followers

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template('index.html', error="Please provide both username and password.")

        loader, profile = login_instagram(username, password)
        if profile:
            followers = get_followers(profile)
            following = get_following(profile)
            non_followers = find_non_followers(followers, following)
            return render_template('index.html', non_followers=[user.username for user in non_followers])
        else:
            return render_template('index.html', error="Login failed. Check your credentials.")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
