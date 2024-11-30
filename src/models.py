import os
import sys
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from eralchemy2 import render_er

# User (Usuario): Para almacenar la información del usuario, como nombre, correo electrónico, contraseña, etc.
# Post (Publicación): Para representar las publicaciones que un usuario hace, incluyendo imagen, título, y la fecha de publicación.
# Comment (Comentario): Para los comentarios en las publicaciones de los usuarios.
# Like (Me Gusta): Para representar los "me gusta" de los usuarios en las publicaciones.
# Follow (Seguir): Para representar las relaciones de seguidores entre los usuarios.

Base = declarative_base()

# Modelo para la entidad 'User' (Usuario)
class User(Base):
    __tablename__ = 'user'  
    id = Column(Integer, primary_key=True) 
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)  
    password = Column(String(100), nullable=False)  
    bio = Column(String(250))  
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Usando timezone.utc para la fecha y hora actual en UTC
    # Relación con otras tablas
    posts = relationship('Post', back_populates='user')  # Un usuario puede tener muchas publicaciones
    followers = relationship('Follow', foreign_keys='Follow.user_id', back_populates='user')  # Usuarios que siguen a este usuario
    following = relationship('Follow', foreign_keys='Follow.follower_id', back_populates='follower')  # Usuarios a los que sigue este usuario
    comments = relationship('Comment', back_populates='user')  # Comentarios que el usuario ha hecho
    likes = relationship('Like', back_populates='user')  # Likes que el usuario ha dado

# Modelo para la entidad 'Post' (Publicacion)
class Post(Base):
    __tablename__ = 'post'  
    id = Column(Integer, primary_key=True)  
    image_url = Column(String(250), nullable=False)  
    caption = Column(String(250))  
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))  
    user_id = Column(Integer, ForeignKey('user.id'))  
    # Relación con otras tablas
    user = relationship('User', back_populates='posts')  # Un post pertenece a un usuario
    comments = relationship('Comment', back_populates='post')  # Un post puede tener muchos comentarios
    likes = relationship('Like', back_populates='post')  # Un post puede tener muchos likes


# Modelo para la entidad 'Comment' (Comentario)
class Comment(Base):
    __tablename__ = 'comment'  
    id = Column(Integer, primary_key=True)  
    content = Column(String(250), nullable=False)  
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey('user.id'))  
    post_id = Column(Integer, ForeignKey('post.id'))  
    # Relación con otras tablas
    user = relationship('User', back_populates='comments')  # El comentario es hecho por un usuario
    post = relationship('Post', back_populates='comments')  # El comentario es sobre una publicación

# Modelo para la entidad 'Like' (Me Gusta)
class Like(Base):
    __tablename__ = 'like'  
    id = Column(Integer, primary_key=True)  
    user_id = Column(Integer, ForeignKey('user.id'))  
    post_id = Column(Integer, ForeignKey('post.id'))  
    # Relación con otras tablas
    user = relationship('User', back_populates='likes')  # El 'me gusta' es dado por un usuario
    post = relationship('Post', back_populates='likes')  # El 'me gusta' es dado en una publicación

# Modelo para la entidad 'Follow' (Seguir)
class Follow(Base):
    __tablename__ = 'follow'  
    id = Column(Integer, primary_key=True)  
    user_id = Column(Integer, ForeignKey('user.id'))  
    follower_id = Column(Integer, ForeignKey('user.id')) 
    # Relación con otras tablas
    user = relationship('User', foreign_keys=[user_id], back_populates='followers')  # El usuario que es seguido
    follower = relationship('User', foreign_keys=[follower_id], back_populates='following')  # El usuario que sigue a otro


# Funcionalidades opcionales
# Historias
class Story(Base):
    __tablename__ = 'story'
    id = Column(Integer, primary_key=True)
    image_url = Column(String(250), nullable=False)
    caption = Column(String(250))  # Opcional
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=False)  # Hora de expiración
    user_id = Column(Integer, ForeignKey('user.id'))  # Quien sube la historia
    # Relación con historias
    User.stories = relationship('Story', back_populates='user')


    def is_expired(self):
        return datetime.now(timezone.utc) > self.expires_at
    
    class User(Base):
         __tablename__ = 'user'
        # ... otros campos
         stories = relationship('Story', back_populates='user')  # Relación con historias

# Mensajes directos
class DirectMessage(Base):
    __tablename__ = 'direct_message'
    id = Column(Integer, primary_key=True)
    content = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    sender_id = Column(Integer, ForeignKey('user.id'))  # Quien envió el mensaje
    receiver_id = Column(Integer, ForeignKey('user.id'))  # Quien recibe el mensaje
    # Relaciones con los usuarios
    sender = relationship('User', foreign_keys=[sender_id], back_populates='sent_messages')
    receiver = relationship('User', foreign_keys=[receiver_id], back_populates='received_messages')

User.sent_messages = relationship('DirectMessage', foreign_keys=[DirectMessage.sender_id], back_populates='sender')
User.received_messages = relationship('DirectMessage', foreign_keys=[DirectMessage.receiver_id], back_populates='receiver')






## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
