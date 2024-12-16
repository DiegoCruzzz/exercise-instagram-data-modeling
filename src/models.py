import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from datetime import datetime
from eralchemy2 import render_er

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    
    posts = relationship('Post', back_populates='usuario')
    comments = relationship('Comment', back_populates='usuario')
    likes = relationship('Like', back_populates='usuario')
    followers = relationship('Follow', foreign_keys='Follow.followed_id', back_populates='followed')
    following = relationship('Follow', foreign_keys='Follow.follower_id', back_populates='follower')

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    caption = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    
    usuario = relationship('Usuario', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    likes = relationship('Like', back_populates='post')

class Follow(Base):
    __tablename__ = 'follow'
    id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    followed_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    
    follower = relationship('Usuario', foreign_keys=[follower_id], back_populates='following')
    followed = relationship('Usuario', foreign_keys=[followed_id], back_populates='followers')

class Like(Base):
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    
    usuario = relationship('Usuario', back_populates='likes')
    post = relationship('Post', back_populates='likes')

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    
    usuario = relationship('Usuario', back_populates='comments')
    post = relationship('Post', back_populates='comments')


try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
