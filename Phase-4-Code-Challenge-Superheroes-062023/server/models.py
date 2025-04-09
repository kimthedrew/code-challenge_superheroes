from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    # Relationship configuration
    hero_powers = db.relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')
    powers = association_proxy('hero_powers', 'power')

    def to_dict(self, include_powers=False):
        data = {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name,
        }
        if include_powers:
            data['hero_powers'] = [hero_power.to_dict() for hero_power in self.hero_powers]
        return data

    def __repr__(self):
        return f'<Hero {self.id}, {self.name}, {self.super_name}>'

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    # Relationship configuration
    hero_powers = db.relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')
    heroes = association_proxy('hero_powers', 'hero')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

    def validate_description(self):
        if not self.description or len(self.description) < 20:
            raise ValueError("Description must be present and at least 20 characters long")
        
    def __init__(self, **kwargs):
        super(Power, self).__init__(**kwargs)
        self.validate_description()

    def __repr__(self):
        return f'<Power {self.id}, {self.name}, {self.description}>'

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))

    # Relationships
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')
    
    __table_args__ = (
        db.CheckConstraint(
            "strength IN ('Strong', 'Weak', 'Average')",
            name='check_strength_values'
        ),
    )
    
    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if strength not in valid_strengths:
            raise ValueError(f"Strength must be one of: {', '.join(valid_strengths)}")
        return strength


 
    def to_dict(self):
        return {
            'id': self.id,
            'hero_id': self.hero_id,
            'power_id': self.power_id,
            'strength': self.strength,
            'hero': {
                'id': self.hero.id,
                'name': self.hero.name,
                'super_name': self.hero.super_name
            },
            'power': {
                'id': self.power.id,
                'name': self.power.name,
                'description': self.power.description
            }
        }

    def __repr__(self):
        return f'<HeroPower {self.id}, {self.hero_id}, {self.power_id}, {self.strength}>'