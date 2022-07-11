from models import db, User, Feedback
from app import app

db.drop_all()
db.create_all()

User.query.delete()


user1 = User.register(username='HockeyLover445', password='password123',
                      email='hockeylover445@gmail.com', first_name='Garrett', last_name='Smith')
user2 = User.register(username='c_Taylor', password='i<3mydog',
                      email='ctaylor1994@gmail.com', first_name='Chad', last_name='Taylor')

db.session.add(user1)
db.session.add(user2)
db.session.commit()

feedback1 = Feedback(title='This website is great!',
                     content='My experience on this website has been excellent. I enjoy coming here daily!', username='HockeyLover445')
feedback2 = Feedback(title='I found a bug',
                     content='Today I had a problem posting. The developers need to fix this!', username='HockeyLover445')

db.session.add(feedback1)
db.session.add(feedback2)
db.session.commit()
