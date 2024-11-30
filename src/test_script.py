from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base
from models import User, Post, Comment, Like, Story, DirectMessage
# Este código crea un usuario 
# publica una publicación
# agrega un comentario y 
# un "me gusta", crea una historia y envía un mensaje directo.


# Crear el motor de la base de datos
engine = create_engine('sqlite:///instagram.db', echo=True)

# Crear las tablas
Base.metadata.create_all(engine)

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

# Crear un usuario
user1 = User(username='luke', email='luke@starwars.com', password='maytheforce', bio='May the force be with you!')
session.add(user1)
session.commit()

# Crear una publicación
post1 = Post(image_url='http://image.url/1.jpg', caption='This is a cool post', user_id=user1.id)
session.add(post1)
session.commit()

# Crear un comentario en la publicación
comment1 = Comment(content='Nice post!', user_id=user1.id, post_id=post1.id)
session.add(comment1)
session.commit()

# Crear un "me gusta" en la publicación
like1 = Like(user_id=user1.id, post_id=post1.id)
session.add(like1)
session.commit()

# Crear una historia
story1 = Story(image_url='http://story.url/1.jpg', expires_at=datetime.now(timezone.utc), user_id=user1.id)
session.add(story1)
session.commit()

# Crear un mensaje directo
message1 = DirectMessage(content='Hey, check out my post!', sender_id=user1.id, receiver_id=user1.id)
session.add(message1)
session.commit()

# Cerrar la sesión
session.close()

