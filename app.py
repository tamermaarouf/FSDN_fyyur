#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from sqlalchemy.sql import func
from database_setup import app, db, Venue, Artist, Genre, artist_genre, Event
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  # num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  query_venues = Venue.query.order_by(Venue.state).all()
  for qv in query_venues:
    print('id: ',qv.id)
    print('name: ',qv.name)
    print('genres', qv.genres)
    for qvGenre in qv.genres:
      print('ID:', qvGenre.id)
      print('Genre: ', qvGenre.genre)
    print('city', qv.city)
    print('state', qv.state)
    print('address', qv.address)
    print('phone', qv.phone)
    print('image_link', qv.image_link)
    print('facebook_link', qv.facebook_link)
    print('website', qv.website)
    print('seeking_talent', qv.seeking_talent)
    print('seeking_description', qv.seeking_description)
    print('event:', qv.events)
    for qvEvent in qv.events:
      print('ID: ', qvEvent.id) 
      print('start_time: ', qvEvent.start_time) 
      print('venue_id: ', qvEvent.venue_id) 
      print('artist_id: ', qvEvent.artist_id)
    print('venue_artist', qv.venueArtist)
    for va in qv.venueArtist:
      print('va', va)
      print('artist_name:>>><<<<<', va.name)
    print('------------------')
    venue_dict = {
      "city": qv.city,
      "state": qv.state,
      "venues": []
    }
    venuecol = {
      "id": qv.id,
      "name": qv.name
    }
    if len(data) > 0:
      for item in data:
        if qv.city == item['city']:
          item["venues"].append(venuecol)
        else:
          data.append(venue_dict)
    else:
      venue_dict["venues"].append(venuecol)
      data.append(venue_dict)
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_Term = request.form.get('search_term', '')
  query_Search = Venue.query.filter(Venue.name.like(f'%{search_Term}%'))
  counter = 0
  response={
    "count": query_Search.count(),
    "data": []
    }
  for record in query_Search:
    for event in record.events:
      if ((event.start_time) > (datetime.now())):
        counter += 1
    resultSearch={
      "id": record.id,
      "name": record.name,
      "num_upcoming_shows": counter  
    }
    response["data"].append(resultSearch)
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venuesID = Venue.query.filter_by(id=venue_id)
  genre_arr = []
  past_shows = []
  upcoming_shows = []
  past_shows_response={}
  upcoming_shows_response={}
  past_counter = 0
  up_counter = 0
  for vID in venuesID:
    for vg in vID.genres:
      genre_arr.append(vg.genre) 
    for EV in vID.events:
      if (EV.start_time) < (datetime.now()):
        artistID = Artist.query.filter(Artist.id==EV.artist_id)
        for AID in artistID:
          past_counter += 1
          past_shows_response={
            "artist_id": AID.id,
            "artist_name": AID.name,
            "artist_image_link": AID.image_link,
            "start_time": str(EV.start_time)
          }
          past_shows.append(past_shows_response)
      else:
          artistID = Artist.query.filter(Artist.id==EV.artist_id)
          for VA in artistID:
            up_counter += 1
            upcoming_shows_response={
              "artist_id": VA.id,
              "artist_name": VA.name,
              "artist_image_link": VA.image_link,
              "start_time": str(EV.start_time)
            }
            upcoming_shows.append(upcoming_shows_response)
    data={
      'id': vID.id,
      "name": vID.name,
      "genres": genre_arr,
      "address": vID.address,
      "city": vID.city,
      "state": vID.state,
     "phone": vID.phone,
      "website": vID.website,
      "facebook_link": vID.facebook_link,
      "seeking_talent": vID.seeking_talent,
      "seeking_description": vID.seeking_description,
      "image_link": vID.image_link,
      "past_shows": past_shows,
      "upcoming_shows": upcoming_shows,
      "past_shows_count": past_counter,
      "upcoming_shows_count": up_counter
    }
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = []
  query_artists = Artist.query.order_by(Artist.name).all()
  for qa in query_artists:
    res={
      "id": qa.id,
      "name": qa.name
    }
    data.append(res)
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_Artist = request.form.get('search_term', '')
  query_Artist = Artist.query.filter(Artist.name.ilike(f'%{search_Artist}%'))
  response={
    "count": query_Artist.count(),
    "data": []
    }
  counter = 0
  for record in query_Artist:
    for event in record.event_artists:
      if ((event.start_time) > (datetime.now())):
        counter += 1
    resultSearch={
      "id": record.id,
      "name": record.name,
      "num_upcoming_shows": counter                   ####---------------> Not Solve
    }
    response["data"].append(resultSearch)
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artistID = Artist.query.filter_by(id=artist_id)
  genre_arr = []
  past_shows = []
  upcoming_shows = []
  past_shows_response={}
  upcoming_shows_response={}
  past_counter = 0
  up_counter = 0
  for ArtID in artistID:
    for vg in ArtID.genre:
      genre_arr.append(vg.genre) 
    for EV in ArtID.event_artists:
      if (EV.start_time) < (datetime.now()):
        venueID = Venue.query.filter(Venue.id==EV.venue_id)
        for ven in venueID:
          past_counter += 1
          past_shows_response={
            "venue_id": ven.id,
            "venue_name": ven.name,
            "venue_image_link": ven.image_link,
            "start_time": str(EV.start_time)
          }
          past_shows.append(past_shows_response)
      else:
        venueID = Venue.query.filter(Venue.id==EV.venue_id)
        for VA in venueID:
          up_counter += 1
          upcoming_shows_response={
            "venue_id": VA.id,
            "venue_name": VA.name,
            "venue_image_link": VA.image_link,
            "start_time": str(EV.start_time)
          }
          upcoming_shows.append(upcoming_shows_response)
    data={
      "id": ArtID.id,
      "name": ArtID.name,
      "genres": genre_arr,
      "city": ArtID.city,
      "state": ArtID.state,
      "phone": ArtID.phone,
      "website": ArtID.website,
      "facebook_link": ArtID.facebook_link,
      "seeking_venue": ArtID.seeking_venue,
      "seeking_description": ArtID.seeking_description,
      "image_link": ArtID.image_link,
      "past_shows": past_shows,           ####---------------> Not Solve
      "upcoming_shows": upcoming_shows,       ####---------------> Not Solve
      "past_shows_count": past_counter,      ####---------------> Not Solve
      "upcoming_shows_count": up_counter   ####---------------> Not Solve
    }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # TODO: populate form with fields from artist with ID <artist_id>
  # Get single artist entry
  res = Artist.query.get(artist_id)
  artist={
    "id": res.id,
    "name": res.name,
    "genres": [],
    "city": res.city,
    "state": res.state,
    "phone": res.phone,
    "website": res.website,
    "facebook_link": res.facebook_link,
    "seeking_venue": res.seeking_venue,
    "seeking_description": res.seeking_description,
    "image_link": res.image_link
  }
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
'''
if __name__ == '__main__':
    app.run()
'''
# Or specify port manually:

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get('PORT', 2023))
    app.run(host='0.0.0.0', port=port)