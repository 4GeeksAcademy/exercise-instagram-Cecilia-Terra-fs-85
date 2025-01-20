import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, create_engine
from sqlalchemy.orm import relationship, declarative_base
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True) #id
    username = Column(String(50), nullable=False)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False) #column asi le digo que esta columna es el email, string que soporta un numero X de caracteres

    posts = relationship("Post", back_populates="user")# back_populates para las bidimensionales, moverme de una tabla  la otra, el post esta relacionada con user y el user esta relacionado con su post,
    comments = relationship("Comment", back_populates="user")# relaciono al usuario con su id con su post y su id
    followers = relationship("Follower", foreign_keys='Follower.user_from_id')
    following = relationship("Follower", foreign_keys='Follower.user_to_id')

class Post(Base):#cada post pertenece a un usuario concreto, pero un usuario puede tener muchos post(relacion de 1 usuario a muchos post)
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True) #id
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False) # user_id  -  foreingKey viene del usuario que es quien hace el post

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    media = relationship("Media", back_populates="post")

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True) #id
    comment_text = Column(String(255), nullable=False) #el texo que el usuario comenta
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False) #le traigo la id del autoh que es la id del usuario
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False) #le traigo la id del post, el usuario tiene un id y crea un pos con un id

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")#un post puede tener muchos comentarios, tambien esta el usuario que hace el post, comments se relaciona con las dos tablas

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(Enum('image', 'video', name='media_types'), nullable=False)# tengo que usar enum para restringir los valores especificos, en el caso de media, video e imagen, no se podra ingresar un numero o string, tengo que tener el lugar donde almaceno media(URL)
    url = Column(String(250), nullable=False)#URL donde tengo los videos o fotos, si no tengo URL, no tengo de donde sacar media
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)#el post puede contener media, relacion Post con Media

    post = relationship("Post", back_populates="media")

class Follower(Base):
    __tablename__ = 'followers'
    user_from_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    user_to_id = Column(Integer, ForeignKey('users.id'), primary_key=True)#muchos a muchos, puedes seguir a muchos y te pueden seguir muchos, solo trabajo con id de usuarios que siguen y son seguidos, se relacionan con el usuario(sigue y es seguido)

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e





