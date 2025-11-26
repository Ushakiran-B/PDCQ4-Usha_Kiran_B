import datetime
import pytz
from flask import Blueprint, render_template, redirect, url_for, session, request
from app.oauth import create_flow, verify_id_token

bp = Blueprint('routes', __name__)


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



BASE = "FORMULAQSOLUTIONS"

def generate_diamond_pattern(lines):
    word = BASE
    n = len(word)
    half = lines // 2

    pattern = []

    for m in range(0, half + 1):
        start = (2 * m) % n
        L = 1 + 4 * min(m, half - m)

        substring = ''.join(word[(start + j) % n] for j in range(L))
        pattern.append(substring)

        if m < half:
            left_idx = (2 * m + 1) % n
            h = 4 * min(m, (half - 1) - m) + 1
            right_idx = (left_idx + h + 1) % n

            pair_line = (
                word[left_idx] +
                ("-" * h) +
                word[right_idx]
            )
            pattern.append(pair_line)

    return pattern



@bp.route('/design', methods=['POST'])
def design():
    if 'user' not in session:
        return redirect(url_for('routes.index'))

    try:
        lines = int(request.form.get('lines', '0'))
    except ValueError:
        lines = 0

    if not (1 <= lines <= 100):
        output = ["Please enter a number between 1 and 100."]
    else:
        output = generate_diamond_pattern(lines)

    user = session.get('user')
    india_tz = pytz.timezone('Asia/Kolkata')
    current_time = datetime.datetime.now(india_tz).strftime('%Y-%m-%d %H:%M:%S')

    return render_template('home.html', user=user, current_time=current_time, output=output)
