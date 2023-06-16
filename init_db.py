from database_setup import app
from database_setup import db, Venue, Artist, Genre, Show 
from flask_migrate import Migrate
from flask import Flask

with app.app_context():
    # db.drop_all()
    venue1 = Venue(id=1, name='The Musical Hop', address='1015 Folsom Street', city= 'San Francisco', state= 'CA', phone= '123-123-1234',
                image_link='https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
                facebook_link= 'https://www.facebook.com/TheMusicalHop', website='https://www.themusicalhop.com',
                seeking_talent=True, seeking_description='We are on the lookout for a local artist to play every two weeks. Please call us.')

    venue2 = Venue(id=2, name='The Dueling Pianos Bar', address='335 Delancey Street', city= 'New York', state= 'NY', phone= '914-003-1132',
                image_link='https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80', 
                facebook_link= 'https://www.facebook.com/theduelingpianos', website='https://www.theduelingpianos.com')

    venue3 = Venue(id=3, name='Park Square Live Music & Coffee"', address='34 Whiskey Moore Ave', city= 'San Francisco', state= 'CA', phone= '415-000-1234', 
                image_link='https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80', 
                facebook_link= 'https://www.facebook.com/ParkSquareLiveMusicAndCoffee', website= 'https://www.parksquarelivemusicandcoffee.com')
    
    artist1 = Artist(id=4, name='Guns N Petals', city= 'San Francisco', state= 'CA', phone= '326-123-5000', 
                image_link='https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80', 
                facebook_link= 'https://www.facebook.com/mattquevedo923251523', website= 'https://www.gunsnpetalsband.com', seeking_venue=True, seeking_description='Looking for shows to perform at in the San Francisco Bay Area!')
    
    artist2 = Artist(id=5, name='Matt Quevedo', city= 'New York', state= 'NY', phone= '300-400-5000', 
                image_link='https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80', 
                facebook_link= 'https://www.facebook.com/GunsNPetals')
    
    artist3 = Artist(id=6, name='The Wild Sax Band', city= 'San Francisco', state= 'CA', phone= '432-325-5432', 
                image_link='https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80')
    
    event1 = Show(start_time='2019-05-21T21:30:00.000Z', venues=venue1, artists=artist1)    
    event2 = Show(start_time='2019-06-15T23:00:00.000Z', venues=venue3, artists=artist2)    
    event3 = Show(start_time='2035-04-01T20:00:00.000Z', venues=venue3, artists=artist3)    
    event4 = Show(start_time='2035-04-08T20:00:00.000Z', venues=venue3, artists=artist3)    
    event5 = Show(start_time='2035-04-015T20:00:00.000Z', venues=venue3, artists=artist3)
    

    
    genre1 = Genre(genre='Alternative')
    genre2 = Genre(genre='Blues')
    genre3 = Genre(genre='Classical')
    genre4 = Genre(genre='Country')
    genre5 = Genre(genre='Electronic')
    genre6 = Genre(genre='Folk')
    genre7 = Genre(genre='Funk')
    genre8 = Genre(genre='Hip-Hop')
    genre9 = Genre(genre='Heavy Metal')
    genre10 = Genre(genre='Instrumental')
    genre11 = Genre(genre='Jazz')
    genre12 = Genre(genre='Musical Theatre')
    genre13 = Genre(genre='Pop')
    genre14 = Genre(genre='Punk')
    genre15 = Genre(genre='R&B')
    genre16 = Genre(genre='Reggae')
    genre17 = Genre(genre='Rock n Roll')
    genre18 = Genre(genre='Soul')
    genre19 = Genre(genre='Other')

    artist1.genre.append(genre17)
    artist2.genre.append(genre11)
    artist3.genre.append(genre11)
    artist3.genre.append(genre3)

    venue1.genres.append(genre11)
    venue1.genres.append(genre16)
    venue1.genres.append(genre3)
    venue1.genres.append(genre6)
    venue1.genres.append(genre19)
    venue2.genres.append(genre3)
    venue2.genres.append(genre15)
    venue2.genres.append(genre8)
    venue3.genres.append(genre17)
    venue3.genres.append(genre11)
    venue3.genres.append(genre3)
    venue3.genres.append(genre6)

    venue1.venueArtist.append(artist1)
    venue3.venueArtist.append(artist2)
    venue3.venueArtist.append(artist3)
    venue3.venueArtist.append(artist3)
    venue3.venueArtist.append(artist3)

    db.session.add_all([venue1, venue2, venue3])
    db.session.add_all([artist1, artist2, artist3])
    db.session.add_all([genre1, genre2, genre3, genre4, genre5, genre6, genre7, genre8, genre9, genre10, genre11, genre12, genre13, genre14, genre15, genre16, genre17, genre18, genre19])
    db.session.add_all([event1, event2, event3])
    db.session.commit()
  