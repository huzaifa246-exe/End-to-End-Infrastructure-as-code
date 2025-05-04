from flask import request, redirect, jsonify
from app import app, db
from app.models import URL
import random, string

def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json()
    url = data['url']
    short = generate_short_url()
    new_url = URL(original_url=url, short_url=short)
    db.session.add(new_url)
    db.session.commit()
    return jsonify({'short_url': short})

@app.route('/<short>')
def redirect_url(short):
    url = URL.query.filter_by(short_url=short).first_or_404()
    return redirect(url.original_url)
