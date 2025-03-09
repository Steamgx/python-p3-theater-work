from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, MetaData
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Define naming convention for migrations
convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

# Use declarative base with metadata
Base = declarative_base(metadata=metadata)

class Role(Base):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True)
    character_name = Column(String, nullable=False)
    
    auditions = relationship("Audition", back_populates="role", cascade="all, delete")

    def actors(self):
        return [audition.actor for audition in self.auditions]
    
    def locations(self):
        return [audition.location for audition in self.auditions]
    
    def lead(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return hired_auditions[0] if hired_auditions else "No actor has been hired for this role"
    
    def understudy(self):
        hired_auditions = [audition for audition in self.auditions if audition.hired]
        return hired_auditions[1] if len(hired_auditions) > 1 else "No actor has been hired for understudy for this role"

class Audition(Base):
    __tablename__ = 'auditions'
    
    id = Column(Integer, primary_key=True)
    actor = Column(String, nullable=False)
    location = Column(String, nullable=False)
    phone = Column(Integer, nullable=False)
    hired = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'))
    
    role = relationship("Role", back_populates="auditions")
    
    def call_back(self):
        self.hired = True

# Database setup
engine = create_engine("sqlite:///moringa_theater.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Migration example: Adding data
role1 = Role(character_name="Hamlet")
audition1 = Audition(actor="John Doe", location="New York", phone=1234567890, role=role1)
session.add(role1)
session.add(audition1)
session.commit()
