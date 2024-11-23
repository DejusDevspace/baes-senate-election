from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_login import UserMixin
from sqlalchemy import Text, Integer, String, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRES_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Table for students participating election
class Student(UserMixin, db.Model):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    matric_no: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    pin: Mapped[int] = mapped_column(Integer, nullable=False)
     # Relationship with Votes
    votes = relationship("Vote", back_populates="student", cascade="all, delete-orphan")


# Table for the candidates
class Candidate(db.Model):
    __tablename__ = "candidates"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    position: Mapped[str] = mapped_column(String(255), nullable=False)
    votes_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # Relationship with Votes
    votes = relationship("Vote", back_populates="candidate", cascade="all, delete-orphan")



# Table for the votes
class Vote(db.Model):
    __tablename__ = "votes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Foreign key to students
    voter: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    # Foreign key to candidates
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    
    # Relationships to other tables
    student = relationship("Student", back_populates="votes")
    candidate = relationship("Candidate", back_populates="votes")


# with app.app_context():
#     db.create_all()

# Function to upload data of registered students into the db
def load_database():
    # TODO: Receive excel file containing data
    # TODO: Hash and salt pin of registering users before passing into db
    # TODO: Save data into the db
    pass


@app.route("/", methods=["GET"])
def get_notes():
    result = db.session.execute(db.Select(Student))
    users = result.scalars().all()
    # print(users[0].matric_no)
    return render_template("index.html")

@app.route("/vote", methods=["GET", "POST"])
def vote():
    pass


if __name__ == '__main__':
    app.run()
