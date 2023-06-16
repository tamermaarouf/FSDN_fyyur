#--------------------------> Configuration <-------------------------#
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# TODO: implement any missing fields, as a database migration using Flask-Migrate
artist_genre = db.Table('artist_genre',
                        db.Column('artist_id', db.Integer, db.ForeignKey('artists.id')),
                        db.Column('genre_id', db.Integer, db.ForeignKey('genres.id')))

venue_genre = db.Table('venue_genre',
                        db.Column('venue_id', db.Integer, db.ForeignKey('venues.id')),
                        db.Column('genre_id', db.Integer, db.ForeignKey('genres.id')))

venue_artist = db.Table('venue_artist',
                        db.Column('venue_id', db.Integer, db.ForeignKey('venues.id')),
                        db.Column('artist_id', db.Integer, db.ForeignKey('artists.id')))

class Venue(db.Model):
    __tablename__ = 'venues'
    #----------------------------> MAPPER <------------------------#
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.relationship('Genre', secondary=venue_genre, backref=db.backref('venu', lazy=True))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(120), default="")
    events = db.relationship('Show', backref='venues')
    venueArtist = db.relationship('Artist', secondary=venue_artist, backref=db.backref('venues', lazy=True))

    def __repr__(self):
      return f'<Venue {self.id}, {self.name}>'

class Genre(db.Model):
    __tablename__ = 'genres'
    #----------------------------> MAPPER <------------------------#
    id = db.Column(db.Integer, primary_key = True)
    genre = db.Column(db.String(80), nullable = False)
    def __repr__(self):
      return f'<Genre {self.id}, {self.genre}>'

class Artist(db.Model):
    __tablename__ = 'artists'
    #----------------------------> MAPPER <------------------------#
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(), default="")
    event_artists = db.relationship('Show', backref='artists')
    genre = db.relationship('Genre', secondary=artist_genre, backref=db.backref('artists', lazy=True))

    def __repr__(self):
      return f'<Artist {self.id}, {self.name}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

    # TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'event'
    #----------------------------> MAPPER <------------------------#
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))

    def __repr__(self):
      return f'<ArtEventist {self.venue_id}, {self.start_time}, {self.artist_id}>'