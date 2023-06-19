#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
import sys
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
import datetime
from flask_migrate import Migrate
from sqlalchemy.sql import func
from database_setup import app, db, Venue, Artist, Genre, artist_genre, Shows
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#
'''
def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime
'''
def format_datetime(date, format='%x %X'):
    # check whether the value is a datetime object
    if not isinstance(date, (datetime.date, datetime.datetime)):
        try:
            date = datetime.datetime.strptime(str(date), '%Y-%m-%d').date()
        except Exception:
            return date
    return date.strftime(format)

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
  city_distinct =  Venue.query.with_entities(Venue.city, Venue.state).distinct()
  for qv in city_distinct:
    data_venues = []
    for item in  Venue.query.filter(Venue.city==qv.city).filter(Venue.state==qv.state).all():
        data_venues.append({
          "id": item.id,
          "name": item.name
        })
    data.append({
      "city": qv.city,
      "state": qv.state,
      "venues": data_venues      
    })
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
    for event in record.show_venue:
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
  venueID = Venue.query.get(venue_id)
  genre_arr = []
  past_shows = []
  upcoming_shows = []
  past_shows_response={}
  upcoming_shows_response={}
  for vg in venueID.genres:
    genre_arr.append(vg.genre)
  past_shows_response = Shows.query.join(Artist).filter(Shows.venue_id==venue_id).filter(Shows.start_time<datetime.datetime.now()).all()
  for res in past_shows_response:
    past_shows.append({
      "artist_id": res.artist_id,
      "artist_name": res.artists.name,
      "artist_image_link": res.artists.image_link,
      "start_time": str(res.start_time)
    })
  upcoming_shows_response = Shows.query.join(Artist).filter(Shows.venue_id==venue_id).filter(Shows.start_time>datetime.datetime.now()).all()
  for up_res in upcoming_shows_response:
    upcoming_shows.append({
      "artist_id": up_res.artist_id,
      "artist_name": up_res.artists.name,
      "artist_image_link": up_res.artists.image_link,
      "start_time": str(up_res.start_time)
    })
  data={
    'id': venueID.id,
    "name": venueID.name,
    "genres": genre_arr,
    "address": venueID.address,
    "city": venueID.city,
    "state": venueID.state,
    "phone": venueID.phone,
    "website": venueID.website,
    "facebook_link": venueID.facebook_link,
    "seeking_talent": venueID.seeking_talent,
    "seeking_description": venueID.seeking_description,
    "image_link": venueID.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows_response),
    "upcoming_shows_count": len(upcoming_shows_response)
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
  form = VenueForm()
  # for key in request.form:
  #   print(key)
  name = request.form['name']
  genre_venue = request.form.getlist('genres')
  address = request.form['address']
  city = request.form['city']
  state = request.form['state']
  phone = request.form['phone']
  website = request.form['website_link']
  facebook_link = request.form['facebook_link']
  seeking_talent = True if request.form['seeking_talent'] == 'y' else False
  seeking_description = request.form['seeking_description']
  image_link = request.form['image_link']
  # print(name, genre_venue, address, city, state, phone,website, facebook_link, seeking_talent)
  error_in_insert = False
  # Insert form data into DB
  try:
    # creates the new venue with all fields but not genre yet
    create_venue =  Venue(name=name, address=address, city=city, state=state, phone=phone,image_link=image_link, facebook_link=facebook_link, 
                          website=website, seeking_talent=seeking_talent, seeking_description=seeking_description)
                          
    # for genre in genre_venue:
    #   print(genre)
    #   new_genre=Genre(genre=genre)
      
    new_genres = Genre(genre=genre_venue)
    create_venue.genres.append(new_genres)
    # db.session.refresh(create_venue)
    db.session.add(create_venue)
    db.session.commit()
  except Exception as e:
    error_in_insert = True
    print(f'Exception "{e}" in create_venue_submission()')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    if error_in_insert:
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
      flash('An error occured. Venue ' + request.form['name'] + '  Could not be listed!!')
    else:      
      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  delete_venue = Venue.query.get(venue_id)
  delete_name = delete_venue.name
  error_in_insert = False
  try:
    db.session.delete(delete_venue)
    db.session.commit()
  except:
    error_in_insert = True
    db.session.rollback()
  finally:
    db.session.close()
  if error_in_insert:
    # if error occur, error message pop up
    flash('An error occurred deleting venue' + delete_name)
  else:
    # if success, success message pop up
    flash('Successfully removed venue ' + delete_name)
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html')

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
    for event in record.show_artists:
      if ((event.start_time) > (datetime.datetime.now())):
        counter += 1
    resultSearch={
      "id": record.id,
      "name": record.name,
      "num_upcoming_shows": counter
    }
    response["data"].append(resultSearch)
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artistID = Artist.query.get(artist_id)
  genre_arr = []
  past_shows = []
  upcoming_shows = []
  past_shows_response={}
  upcoming_shows_response={}
  for vg in artistID.genre:
    genre_arr.append(vg.genre)
  past_shows_response = Shows.query.join(Venue).filter(Shows.artist_id==artist_id).filter(Shows.start_time<datetime.datetime.now()).all()
  for res in past_shows_response:
    past_shows.append({
      "venue_id": res.venue_id,
      "venue_name": res.venues.name,
      "venue_image_link": res.venues.image_link,
      "start_time": str(res.start_time)
    })
  upcoming_shows_response = Shows.query.join(Venue).filter(Shows.artist_id==artist_id).filter(Shows.start_time>datetime.datetime.now()).all()
  for up_res in upcoming_shows_response:
    upcoming_shows.append({
      "venue_id": up_res.venue_id,
      "venue_name": up_res.venues.name,
      "venue_image_link": up_res.venues.image_link,
      "start_time": str(up_res.start_time)
    })
  data={
    "id": artistID.id,
    "name": artistID.name,
    "genres": genre_arr,
    "city": artistID.city,
    "state": artistID.state,
    "phone": artistID.phone,
    "website": artistID.website,
    "facebook_link": artistID.facebook_link,
    "seeking_venue": artistID.seeking_venue,
    "seeking_description": artistID.seeking_description,
    "image_link": artistID.image_link,
    "past_shows": past_shows,           
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows_response),
    "upcoming_shows_count": len(upcoming_shows_response)  
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # TODO: populate form with fields from artist with ID <artist_id>
  # Get single artist entry
  res = Artist.query.get(artist_id)
  form = ArtistForm(obj=res)
  genres = {}
  for vg in res.genre:
    genres={
      "genre": vg.genre
      }
  artist={
    "id": res.id,
    "name": res.name,
    "genres": genres,
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
  form = ArtistForm()
  genres = []
  error_in_insert = False
  artist = Artist.query.get(artist_id)
  try:
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.image_link = request.form['image_link']
    genres = request.form.getlist('genres')
    artist.facebook_link = request.form['facebook_link']
    artist.website = request.form['website_link']
    artist.seeking_venue = True if request.form['seeking_venue'] == 'y' else False
    artist.seeking_description = request.form['seeking_description']
    print(genres)
    for genre in genres:
      genre_add = Genre(genre=genre)
      artist.genre.append(genre_add)
    # Send artist to table and commit
    db.session.commit()
  except Exception as e:
    error_in_insert = True
    db.session.rollback()
    print(e)
    print(sys.exc_info())
  finally:
    db.session.close()
  if error_in_insert: 
    # if error occur, error message pop up
    flash('An error occurred. Artist could not be updated.')
  if not error_in_insert: 
    # if success, success message pop up
    flash('Artist was successfully updated!')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)
  genres = {}
  for vg in venue.genres:
    genres={
      "genre": vg.genre
      }
  venue={
    "id": venue.id,
    "name": venue.name,
    "genres": genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm()
  genres = []
  error_in_insert = False
  venue = Venue.query.get(venue_id)
  try:
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.image_link = request.form['image_link']
    genres = request.form.getlist('genres')
    venue.facebook_link = request.form['facebook_link']
    venue.website = request.form['website_link']
    venue.seeking_venue = True if request.form['seeking_talent'] == 'y' else False
    venue.seeking_description = request.form['seeking_description']
    print(genres)
    for genre in genres:
      genre_add = Genre(genre=genre)
      venue.genres.append(genre_add)
    # Send artist to table and commit
    db.session.commit()
  except Exception as e:
    error_in_insert = True
    db.session.rollback()
    print(e)
    print(sys.exc_info())
  finally:
    db.session.close()
  if error_in_insert: 
    # if error occur, error message pop up
    flash('An error occurred. Venue could not be updated.')
  if not error_in_insert: 
    # if success, success message pop up
    flash('Venue was successfully updated!')

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  '''
  for artist_name in form:
    print(artist_name.name)
  '''
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  form = ArtistForm()
  # take data from the form
  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  phone = request.form['phone']
  image_link = request.form['image_link']
  genre_venue = request.form.getlist('genres')
  facebook_link = request.form['facebook_link']
  website = request.form['website_link']
  seeking_venue = True if request.form['seeking_venue'] == 'y' else False
  seeking_description = request.form['seeking_description']
  error_in_insert = False
  try:
    # creates the new artist with all fields except genre yet
    create_artist = Artist(name=name, city=city, state=state, phone=phone, 
                image_link=image_link, facebook_link= facebook_link, website= website, seeking_venue=seeking_venue, seeking_description=seeking_description)
    
    for genre in genre_venue:
      genre_add = Genre(genre=genre)
      create_artist.genre.append(genre_add)
    # Send artist to table and commit
    db.session.add(create_artist)
    db.session.commit()
  except Exception as e:
    error_in_insert = True
    print(f'Exception "{e}" in create_artist_submission()')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    if error_in_insert:
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    else:
      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data=[]
  # to get Venue and Artist many to many relationship (Show Class)
  artists_venues = Shows.query.join(Venue).join(Artist).all()
  for artist_venue in artists_venues:
    data.append({
        "venue_id": artist_venue.venue_id,
        "venue_name": artist_venue.venues.name,
        "artist_id": artist_venue.artist_id,
        "artist_name": artist_venue.artists.name,
        "artist_image_link": artist_venue.artists.image_link,
        "start_time": str(artist_venue.start_time)
    })
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
  form = ShowForm()
  for key in form:
    print(key.name)
  # take the data from the form
  artist_id = request.form['artist_id']
  venue_id = request.form['venue_id']
  start_time = request.form['start_time']
  error_in_insert = False
  try:
    show = Shows(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
    db.session.add(show)
    db.session.commit()
  except Exception as e:
    error_in_insert = True
    print(f'Exception "{e}" in create_artist_submission()')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error_in_insert:
    flash('An error occurred. Show could not be listed.')
  else:
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



'''
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
'''