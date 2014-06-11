from flask import make_response, current_app
from flask.ext import restful
from flask.ext.login import current_user, login_required
from flask.ext.restful import abort, reqparse, marshal
import datetime
import requests
import requests_cache
import urllib
from urlparse import urlparse, parse_qs
from together.models import User, Playlist, db, PlaylistElement

api = restful.Api()
requests_cache.install_cache()


class UserPlaylistsResource(restful.Resource):

    @restful.marshal_with(Playlist.resource_fields)
    @login_required
    def get(self, user_id):
        if user_id != current_user.id:
            abort(403)
        user = User.query.get(user_id)
        return user.playlists.all()

    def post(self, user_id):
        if user_id != current_user.id:
            abort(403)
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        args = parser.parse_args()
        playlist = Playlist(
            name=args['name'],
            user=current_user._get_current_object(),
            last_updated=datetime.datetime.utcnow())
        playlist.update_slug()
        db.session.add(playlist)
        db.session.commit()
        return marshal(playlist, Playlist.resource_fields), 201


class UserPlaylistResource(restful.Resource):

    @restful.marshal_with(Playlist.resource_fields)
    @login_required
    def get(self, user_id, playlist_slug):
        if current_user.id != user_id:
            abort(403)
        playlist = Playlist.query.filter_by(user_id=user_id, slug=playlist_slug).first()
        if playlist is None:
            abort(404, message="Playlist not found.")
        return playlist

    def put(self, user_id, playlist_slug):
        if current_user.id != user_id:
            abort(403)

        parser = reqparse.RequestParser()
        parser.add_argument('videoId', type=str)
        args = parser.parse_args()

        playlist = Playlist.query.filter_by(user_id=user_id, slug=playlist_slug).first()
        if playlist is None:
            abort(404, message="Playlist not found.")

        if 'videoId' in args:
            if 'http' in args['videoId']:
                url = urlparse(args['videoId'])
                query = parse_qs(url.query)
                if 'v' in query:
                    args['videoId'] = query['v'][0]
                else:
                    abort(400, message="Invalid Youtube URL.")
            request = requests.get("https://www.googleapis.com/youtube/v3/videos?" + urllib.urlencode(dict(
                part='snippet',
                id=args['videoId'],
                key=current_app.config['YOUTUBE_API']
            )))
            video = request.json()
            if len(video['items']) == 0:
                abort(404, message="Video not found.")
            video = video['items'][0]['snippet']

            element = PlaylistElement(
                youtube_id=args['videoId'],
                title=video['title'],
                thumbnail=video['thumbnails']['default']['url'],
                added_at=datetime.datetime.utcnow(),
                added_by_id=current_user.id,
                playlist_id=playlist.id
            )
            db.session.add(element)
            db.session.commit()

            return marshal(element, PlaylistElement.resource_fields), 200

    @restful.marshal_with(Playlist.resource_fields)
    @login_required
    def post(self, user_id, playlist_slug):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        args = parser.parse_args()
        if current_user.id != user_id:
            abort(403)
        playlist = Playlist.query.filter_by(user_id=user_id, slug=playlist_slug).first()
        if playlist is None:
            abort(404, message="Playlist not found.")
        if args['name'] != "":
            playlist.name = args['name']
            playlist.update_slug()
        db.session.add(playlist)
        db.session.commit()
        return playlist, 200


class UserPlaylistVideoResource(restful.Resource):

    @login_required
    def delete(self, user_id, playlist_slug, video_id):
        if current_user.id != user_id:
            abort(403)
        playlist = Playlist.query.filter_by(user_id=user_id, slug=playlist_slug).first()
        if playlist is None:
            abort(404, message="Playlist not found.")

        video = playlist.elements.filter_by(id=video_id).first()
        if video is None:
            abort(404, message="Video not found in playlist.")

        db.session.delete(video)
        db.session.commit()


class YoutubeSearch(restful.Resource):

    @login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('query', type=str, required=True, location='args')
        args = parser.parse_args()
        req = requests.get("https://www.googleapis.com/youtube/v3/search?" + urllib.urlencode(dict(
            part='snippet',
            q=args['query'],
            type='video',
            videoEmbeddable='true',
            key=current_app.config['YOUTUBE_API']
        )))
        return make_response(req.text, 200)


def json_user():
    if current_user.is_authenticated():
        return dict(user={
            'id': current_user.id,
            'name': current_user.name
        })
    else:
        return dict(user={})

api.add_resource(UserPlaylistsResource, '/api/<int:user_id>/playlists', strict_slashes=False)
api.add_resource(UserPlaylistResource, '/api/<int:user_id>/playlists/<playlist_slug>', strict_slashes=False)
api.add_resource(UserPlaylistVideoResource, '/api/<int:user_id>/playlists/<playlist_slug>/videos/<int:video_id>', strict_slashes=False)
api.add_resource(YoutubeSearch, '/api/youtube/search', strict_slashes=False)

