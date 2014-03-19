# -*- coding: utf-8 -*-
from flask import Blueprint, url_for, g, render_template, abort, request
from sqlalchemy.orm import contains_eager
from sqlalchemy.exc import IntegrityError

from .login import need_login
from ..user import User, LoveArtist
from ..album import Artist
from ..db import session

bp = Blueprint('user', __name__, template_folder='templates/user')

@bp.route('/me/', methods=['GET'])
@need_login
def me():
    return redirect(url_for('.user', user_id=g.current_user.id))


@bp.route('/<int:user_id>/', methods=['GET'])
@need_login
def user(user_id):
    user = session.query(User)\
           .filter(User.id == user_id)\
           .all()
    if not user:
        abort(404)
    is_me = (user[0].id == g.current_user.id)
    return render_template('index.html', user=user[0], me=is_me)


@bp.route('/<int:user_id>/love_artist/', methods=['POST'])
@need_login
def add_love_artist(user_id):
    user = session.query(User)\
           .filter(User.id == user_id)\
           .all()
    if not user:
        abort(404)
    if user[0].id != g.current_user.id:
        abort(403)
    name = request.form.get('artist_name', None)
    if not name:
        abort(400)
    a = session.query(Artist)\
        .filter(Artist.name == name)\
        .all()
    if not a:
        artist = Artist(name=name)
        session.add(artist)
        love_artist = []
    else:
        artist = a[0]
        love_artist = session.query(LoveArtist)\
                      .filter(LoveArtist.artist_id == artist.id)\
                      .filter(LoveArtist.user_id == user[0].id)\
                      .all()
    if not love_artist:
        rel = LoveArtist(artist=artist, user=user[0])
        session.add(rel)
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        abort(500)
    return 'added'


@bp.route('/<int:user_id>/love_artist/', methods=['GET'])
@need_login
def love_artist(user_id):
    user = sesison.query(User)\
           .options(contains_eager(User.love_artist))\
           .filter(User.id == user_id)\
           .all()
    return render_template('love_artist.html',
                           love_artists=user[0].love_artists)