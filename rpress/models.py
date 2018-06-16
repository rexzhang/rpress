#!/usr/bin/env python
# coding=utf-8


import uuid

from flask_sqlalchemy import BaseQuery
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql

from rpress.constants import POST, TERM, PUBLISH_FSM_DEFINE
from rpress.database import db
from rpress.runtimes.password import generate_password_hash, check_password_hash


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    created_time = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
    )

    def __repr__(self):
        """don't forget overload!"""
        return '{}'.format(self.id)


class BaseModelObject(BaseModel):
    """base model - Object"""
    __abstract__ = True

    # last update time
    updated_time = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
    )


class BaseModelRecord(BaseModel):
    """base model - record/log"""
    __abstract__ = True


class User(BaseModelObject):
    __tablename__ = 'users'

    name = Column(String(50), unique=True, nullable=False)

    password = Column(String(255))
    email = Column(String(32), unique=True)
    display = Column(String(50), unique=True)

    def check_password(self, password):
        return check_password_hash(hashed_password=self.password, password=password)

    def change_password(self, password):
        self.password = generate_password_hash(password=password)
        return

    def __init__(self, **kwargs):
        password = kwargs.get('password')
        if password:
            kwargs['password'] = generate_password_hash(password=password)

        super().__init__(**kwargs)
        return

    def __repr__(self):
        return '<User:{}|{}>'.format(self.id, self.name)


post_term_relations = db.Table(
    'post_term_relations',
    db.Column('term_id', postgresql.UUID(as_uuid=True), db.ForeignKey('terms.id')),
    db.Column('post_id', postgresql.UUID(as_uuid=True), db.ForeignKey('posts.id'))
)


class PostQuery(BaseQuery):
    """"""

    def search(self, site, keywords):
        """"""
        criteria = []

        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(db.or_(Post.title.ilike(keyword),
                                   Post.name.ilike(keyword),
                                   Post.content.ilike(keyword),
                                   # Post.terms.ilike(keyword)
                                   ))

        query = reduce(db.and_, criteria)
        return self.filter_by(site=site).filter(query)


class Post(BaseModelObject):
    """"""
    query_class = PostQuery

    __tablename__ = 'posts'
    _uuid_foreign_key_list_ = ['site_id', 'author_id', 'reviser_id']

    site_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('sites.id'), nullable=False)
    site = relationship('Site')

    author_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    author = relationship('User', foreign_keys=[author_id])

    reviser_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    reviser = relationship('User', foreign_keys=[reviser_id])

    type = Column(String(4), default=POST.TYPE.BLOG)  # blog/page
    name = Column(String(128))
    terms = relationship(
        "Term",
        secondary=post_term_relations,
        backref="posts"
    )

    title = Column(String(128))
    content = Column(Text)

    published = Column(Boolean, default=False)
    publish_status = Column(
        # published 为 True 时才有意义 #修改过程版本存放在另外一个表中
        String(20),
        default=PUBLISH_FSM_DEFINE.DEFAULT_STATE
    )
    published_time = Column(DateTime(timezone=True))

    comments = relationship('Comment', back_populates='post')
    allow_comment = Column(Boolean, default=True)

    def __init__(self, **kwargs):
        if kwargs.get('reviser') is None and kwargs.get('author') is not None:
            kwargs['reviser'] = kwargs['author']

        if kwargs.get('reviser_id') is None and kwargs.get('author_id') is not None:
            kwargs['reviser_id'] = kwargs['author_id']

        # TODO: !!!convert title to %xx if name==None
        super().__init__(**kwargs)
        return

    def __repr__(self):
        return '<Post:{}|{}>'.format(self.id, self.title)


class Term(BaseModelObject):
    __tablename__ = 'terms'

    site_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('sites.id'), nullable=False)
    site = relationship('Site', foreign_keys=[site_id], back_populates='terms')

    type = Column(String(50), default=TERM.TYPE.CATEGORY)  # tag/category

    name = Column(String(50))
    desc = Column(Text, nullable=True)

    def __repr__(self):
        return '<Term:{}|{}>'.format(self.id, self.name)


class Comment(BaseModelRecord):
    __tablename__ = 'comments'

    post_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('posts.id'), nullable=False)
    post = relationship('Post', back_populates='comments')

    commenter_name = Column(String(50))
    commenter_email = Column(String(32), nullable=True)
    commenter_ip = Column(String(19), nullable=True)
    commenter_url = Column(Text, nullable=True)

    content = Column(Text)

    def __repr__(self):
        return '<Comment:{}|{}|{}>'.format(self.id, self.post_id, self.author_name)


class Site(BaseModelObject):
    __tablename__ = 'sites'

    domain = Column(String(50), unique=True, nullable=False)

    settings = relationship('SiteSetting', back_populates='site')
    terms = relationship('Term', back_populates='site')

    def __repr__(self):
        return '<Site:{}|{}>'.format(self.id, self.domain)


class SiteSetting(BaseModelObject):
    """"""
    __tablename__ = 'site_settings'

    site_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('sites.id'), nullable=False)
    site = relationship('Site', foreign_keys=[site_id], back_populates='settings')

    key = Column(String(128))
    value = Column(Text())

    def __repr__(self):
        return '<SiteSetting:{}|{}>'.format(self.id, self.key)
