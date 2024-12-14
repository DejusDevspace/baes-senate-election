from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user, login_required
from flask_bootstrap import Bootstrap5
from sqlalchemy import Integer, String, ForeignKey, and_
from werkzeug.security import check_password_hash
import os
from dotenv import load_dotenv
from typing import List, Any, Dict
from datetime import datetime
import json
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
    user = db.get_or_404(Student, student_id)
    if user:
        return User(user.id, user.level, user.matric_no, user.department, user.surname, user.pin)
    return None

# Class for db
class Base(DeclarativeBase):
    pass

# Initialize db
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Time voting ends
VOTING_ENDTIME = datetime(2024, 12, 14, 21, 15, 0)

# Table for students participating election
class Student(UserMixin, db.Model):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    matric_no: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    department: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    pin: Mapped[int] = mapped_column(String(255), nullable=False)
    # Relationship with Votes
    votes = relationship("Vote", back_populates="student", cascade="all, delete-orphan")


# Table for the candidates
class Candidate(db.Model):
    __tablename__ = "candidates"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    position: Mapped[str] = mapped_column(String(255), nullable=False)
    level: Mapped[str] = mapped_column(Integer, nullable=False)
    department: Mapped[str] = mapped_column(String(50), nullable=False)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    votes_count: Mapped[int] = mapped_column(Integer, default=0)
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

# Object for logged_in user
class User(UserMixin):
    def __init__(self, id, level, matric_no, department, surname, pin):
        self.id = id
        self.level = level
        self.matric_no = matric_no
        self.department = department
        self.surname = surname
        self.pin = pin

# with app.app_context():
    # db.create_all()

def jsonify_data(data: List[Any]) -> List[Dict]:
    json_data = []
    try:
        for val in data:
            json_data.append(
                {"name": val.name, "votes_count": val.votes_count}
            )
        return json_data
    except Exception as e:
        print("Error compiling data data:\n", e)

def load_poll_data():
    if current_user.is_authenticated:
        try:
            chairman_candidates = db.session.execute(
                db.Select(Candidate).where(Candidate.position == "Chairman")
            ).scalars().all()
            head_candidates = db.session.execute(
                db.Select(Candidate).where(
                    and_(
                        Candidate.position == "Head",
                        Candidate.department == current_user.department,
                        Candidate.level == current_user.level
                    )
                )
            ).scalars().all()
            secretary_candidates = db.session.execute(
                db.Select(Candidate).where(Candidate.position == "Secretary")
            ).scalars().all()
            head_candidates = jsonify_data(head_candidates)
            chairman_candidates = jsonify_data(chairman_candidates)
            secretary_candidates = jsonify_data(secretary_candidates)

            # print(head_candidates, "\n", chairman_candidates)
            return head_candidates, chairman_candidates, secretary_candidates
        except Exception as e:
            print(e)
    else:
        return None


@app.route("/", methods=["GET"])
def home():
    # if current_user.is_authenticated:
    #     head_candidates, chairman_candidates, secretary_candidates = load_poll_data()
    #     voters = db.session.execute(
    #         db.Select(Student)
    #     ).scalars().all()
    #     render_template(
    #         "index.html",
    #         logged_in=current_user.is_authenticated,
    #         head_candidates=head_candidates,
    #         chairman_candidates=chairman_candidates,
    #         secretary_candidates=secretary_candidates,
    #         total_voters=len(voters)
    #     )
    voters = db.session.execute(db.Select(Student)).scalars().all()
    # print(voters)
    # print(len(voters))
    return render_template(
        "index.html",
        logged_in=current_user.is_authenticated,
        total_voters=len(voters)
    )

@app.route("/poll-data", methods=["GET"])
def poll_data():
    try:
        head_candidates, chairman_candidates, secretary_candidates = load_poll_data()
        return jsonify({
            "head_candidates": head_candidates,
            "chairman_candidates": chairman_candidates,
            "secretary_candidates": secretary_candidates
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if not current_user.is_authenticated:
        if form.validate_on_submit():
            matric_no = form.matric_no.data
            pin = form.pin.data

            # print(matric_no, pin)

            student = db.session.execute(db.Select(Student).where(Student.matric_no == matric_no)).scalar()
            # print(type(pin), type(student.pin))
            db.session.commit()
            # Check if the student is registered in the db
            if not student:
                flash("Matric no. '{}' not registered!".format(matric_no))
                return redirect(url_for("login"))
            # Check if the pin entered by the student is correct
            elif not check_password_hash(student.pin, pin):
                # print(student.pin, pin)
                flash("Incorrect pin! Please try again.")
                return redirect(url_for("login"))
            else:
                # If the details are correct, log the user in
                # print(pin, student.pin)
                # print("Before:", current_user.is_authenticated)
                login_user(student)
                # print("After:", current_user.is_authenticated)
                return redirect(url_for("vote"))
    else:
        return redirect(url_for("vote"))
    return render_template("login.html", form=form, logged_in=current_user.is_authenticated)

@app.route("/vote", methods=["GET", "POST"])
@login_required
def vote():
    if datetime.now() >= VOTING_ENDTIME:
        # Generate the link to the live poll
        live_poll_link = url_for('home', _external=True)
        # Embed the link in the message
        message = (
            f'Voting time has passed, you can no longer cast your vote! '
            f'You can visit the live poll instead: {live_poll_link}'
        )
        return jsonify({"error": message}), 403

    form = VoteForm()
    user = {
        "id": current_user.id,
        "level": current_user.level,
        "surname": current_user.surname,
        "matric_no": current_user.matric_no,
        "department": current_user.department,
    }
    # Query the db to find out if the user has voted
    try:
        voted = db.session.execute(
            db.Select(Vote).where(Vote.voter == user["id"] )
        ).scalars().all()
        print(voted)
        if voted:
            return render_template("voted.html", logged_in=current_user.is_authenticated)
    except Exception as e:
        print("Error loading user's vote", e)

    # Query candidates from the db
    # Head Candidates
    chairman_candidates = db.session.execute(
        db.Select(Candidate).where(Candidate.position == "Chairman")
    ).scalars().all()

    # Assistant General Secretary Candidates
    secretary_candidates = db.session.execute(
        db.Select(Candidate).where(Candidate.position == "Secretary")
    ).scalars().all()

    # Chairman Candidates
    head_candidates = db.session.execute(
        db.Select(Candidate).where(
            and_(
                Candidate.position == "Head",
                Candidate.department == user["department"],
                Candidate.level == user["level"],
            )
        )
    ).scalars().all()

    # Form submission logic
    if form.validate_on_submit():
        # Get the responses from the form
        head_vote = request.form.get("head_candidate")
        chairman_vote = request.form.get("chairman_candidate")
        secretary_vote = request.form.get("secretary_candidate")
        print("Head choice:", head_vote)
        print("Chairman choice:", chairman_vote)
        print("Secretary choice", secretary_vote)

        # Verify that user has voted in each category
        # if not head_vote or not chairman_vote:
        #     flash("Please select a candidate in each category!", "warning")
        #     return redirect(url_for("vote"))

        # Save votes to database
        try:
            if head_vote:
                # Query the db for the selected head candidate
                senate_head_cand = db.session.execute(
                    db.Select(Candidate).where(Candidate.id == head_vote)
                ).scalar_one_or_none()
                # Add the vote for the senate head
                db.session.add(
                    Vote(
                        voter=user["id"],
                        candidate_id=head_vote
                    )
                )
                # Add one to the candidates number of votes
                senate_head_cand.votes_count += 1

            if secretary_vote:
                # Query the db for the selected secretary candidate
                secretary_cand = db.session.execute(
                    db.Select(Candidate).where(Candidate.id == secretary_vote)
                ).scalar_one_or_none()
                # Add the vote for the secretary candidate
                db.session.add(
                    Vote(
                        voter=user["id"],
                        candidate_id=secretary_vote
                    )
                )
                # Add one to the candidate's number of votes
                secretary_cand.votes_count += 1

            if chairman_vote:
                # Query the db for the selected chairman candidate
                senate_chairman_cand = db.session.execute(
                    db.Select(Candidate).where(Candidate.id == chairman_vote)
                ).scalar_one_or_none()
                # Add the vote for the senate chairman
                db.session.add(
                    Vote(
                        voter=user["id"],
                        candidate_id=chairman_vote
                    )
                )
                # Add one to the candidates number of votes
                senate_chairman_cand.votes_count += 1

            # Commit the transaction
            db.session.commit()
            return render_template("success.html", logged_in=current_user.is_authenticated)
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while submitting your votes. Please try again.", "danger")
            print(e)
            return redirect(url_for("vote"))

    return render_template(
        "vote.html",
        form=form,
        user=user,
        logged_in=current_user.is_authenticated,
        head_candidates=head_candidates,
        chairman_candidates=chairman_candidates,
        secretary_candidates=secretary_candidates,
    )

@app.route("/logout", methods=["GET"])
def logout():
    # Log the current user out
    logout_user()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=False)
