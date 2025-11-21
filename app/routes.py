import datetime
import pytz
from flask import Blueprint, render_template, redirect, url_for, session, request
from app.oauth import create_flow, verify_id_token

bp = Blueprint('routes', __name__)

# -------------------- Routes -------------------- #

@bp.route('/')
def index():
    user = session.get('user')
    if user:
        india_tz = pytz.timezone('Asia/Kolkata')
        current_time = datetime.datetime.now(india_tz).strftime('%Y-%m-%d %H:%M:%S')
        return render_template('home.html', user=user, current_time=current_time, output=None)
    return render_template('login.html')


@bp.route('/login')
def login():
    flow = create_flow()
    auth_url, state = flow.authorization_url(
        prompt='consent',
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(auth_url)


@bp.route('/callback')
def callback():
    state = session.get('state')
    flow = create_flow(state=state)
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    id_info = verify_id_token(credentials._id_token)

    session['user'] = {
        'name': id_info.get('name'),
        'email': id_info.get('email'),
        'picture': id_info.get('picture')
    }

    return redirect(url_for('routes.index'))


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.index'))


# -------------------- Pattern Design Logic -------------------- #

def build_raw_pattern(lines):
    base = "FORMULAQSOLUTIONS"
    n = len(base)
    result = []

    for i in range(lines):
        left = base[i % n]
        right = base[(n - 1 - i) % n]

        if i % 2 == 0:
            hyphens = 0
        else:
            hyphens = 2 * i - 1 if i < lines // 2 else 2 * (lines - i) - 1

        if hyphens <= 0:
            line = left + right if left != right else left
        else:
            line = left + ("-" * hyphens) + right

        result.append(line)

    return result


def generate_pattern_centered(lines):
    raw = build_raw_pattern(lines)
    max_len = max((len(s) for s in raw), default=0)
    centered = [(" " * ((max_len - len(line)) // 2) + line) for line in raw]
    return centered


@bp.route('/design', methods=['POST'])
def design():
    if 'user' not in session:
        return redirect(url_for('routes.index'))  # user not logged in

    try:
        lines = int(request.form.get('lines', '0'))
    except ValueError:
        lines = 0

    if not (1 <= lines <= 100):
        output = ["Please enter a number between 1 and 100."]
    else:
        output = generate_pattern_centered(lines)

    user = session.get('user')
    india_tz = pytz.timezone('Asia/Kolkata')
    current_time = datetime.datetime.now(india_tz).strftime('%Y-%m-%d %H:%M:%S')

    return render_template('home.html', user=user, current_time=current_time, output=output)
