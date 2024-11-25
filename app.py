from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user, login_required
from flask_bootstrap import Bootstrap5
from sqlalchemy import Integer, String, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
import os
from io import BytesIO
from dotenv import load_dotenv
# Forms from forms.py
from forms import LoginForm, VoteForm

load_dotenv()

# Initialize flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('POSTGRES_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bootstrap configuration
Bootstrap5(app)

# Configure Flask Login
login_manager = LoginManager()
login_manager.init_app(app)

# Get logged in user (current user)
@login_manager.user_loader
def load_user(student_id):
    return db.get_or_404(Student, student_id)

# Class for db
class Base(DeclarativeBase):
    pass

# Initialize db
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
def load_database(sheet: BytesIO) -> None:
    # TODO: Receive excel file containing data
    # TODO: Hash and salt pin of registering users before passing into db
    # TODO: Save data into the db
    pass


@app.route("/", methods=["GET"])
def home():
    response = db.session.execute((db.Select(Student)))
    students = response.scalars().all()
    # print(students[0].pin)
    return render_template("index.html", logged_in=current_user.is_authenticated)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        matric_no = form.matric_no.data
        pin = form.pin.data
        
        # print(matric_no, pin)

        student = db.session.execute(db.Select(Student).where(Student.matric_no == matric_no)).scalar()
        print(type(pin), type(student.pin))
        # Check if the student is registered in the db
        if not student:
            flash("Matric no. '{}' not registered!".format(matric_no))
            return redirect(url_for("login"))
        # Check if the pin entered by the student is correct
        elif not pin == student.pin:
            print(student.pin, pin)
            flash("Incorrect pin! Please try again.")
            return redirect(url_for("login"))
        else:
            # If the details are correct, log the user in
            print(pin, student.pin)
            # print("Before:", current_user.is_authenticated)
            login_user(student)
            flash("Logged in successfully!")
            # print("After:", current_user.is_authenticated)
            return redirect(url_for("home"))
    return render_template("login.html", form=form, logged_in=current_user.is_authenticated)

@app.route("/vote", methods=["GET", "POST"])
@login_required
def vote():
    # TODO: Different voting forms for different levels? or custom forms per level
    # TODO: Or current user's level determines the form from the backend login here!
    # TODO: Same for, conditionally send the candidates to populate the form based on criteria (level/dept)
    pass

@app.route("/logout", methods=["GET"])
def logout():
    # Log the current user out
    logout_user()
    print(current_user.is_authenticated)
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True, port=8000)
