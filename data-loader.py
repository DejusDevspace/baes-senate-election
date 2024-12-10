import json
import pandas as pd
from werkzeug.security import generate_password_hash
from app import db, Candidate, app, Student


# Function to upload data of registered students into the db
def load_voter_data(sheet: str) -> None:
    try:
        data = pd.read_excel(sheet)
        data.drop(columns=["Timestamp", "Email address"], inplace=True)
    except Exception as e:
        print("Unexpected error processing data:", e)
        return

    with app.app_context():
        try:
            for index, col in data.iterrows():
                # Extract user details
                matric_no = col["Matric Number"]
                surname =  col["Surname"]
                pin = str(col["4-digit Pin"]).strip()
                department = col["Department"]
                level = col["Level"]

                # Hashing the pin to save in db
                user_hashed_pin = generate_password_hash(
                    pin,
                    method="pbkdf2:sha256",
                    salt_length=8
                )

                print("Adding student: {}".format(index))

                # Add the student to the database session
                db.session.add(
                    Student(
                        matric_no=matric_no.strip(),
                        level=level,
                        department=department.strip(),
                        surname=surname.strip(),
                        pin=user_hashed_pin
                    )
                )

            # Commit all changes after successful addition
            db.session.commit()
            print("All students' data successfully uploaded.")

        except Exception as e:
            db.session.rollback()
            print(f"Error saving students to database: {e}")

# Function to upload data of the candidates into the db
def load_candidate_data(json_file: str) -> None:
    """Uploads the candidates' data to the database from a JSON file."""
    try:
        # Open and load the JSON file
        with open(json_file, "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.")
        return
    except json.JSONDecodeError:
        print("Error: JSON file is improperly formatted.")
        return
    except Exception as e:
        print(f"Unexpected error reading JSON file: {e}")
        return

    with app.app_context():
        try:
            for candidate in data:
                # Extract candidate details
                name = candidate.get("name")
                position = candidate.get("position")
                level = candidate.get("level")
                department = candidate.get("department")
                image = candidate.get("image")

                print(f"Adding candidate: {candidate}")

                # Add candidate to the database session
                db.session.add(
                    Candidate(
                        name=name,
                        position=position,
                        level=level,
                        department=department,
                        image=image
                    )
                )

            # Commit all changes after successful addition
            db.session.commit()
            print("All candidate data successfully uploaded.")

        except Exception as e:
            db.session.rollback()
            print(f"Error saving candidates to database: {e}")


if __name__ == "__main__":
    load_candidate_data("candidate_data.json")
    load_voter_data("baes-senate-election-registration.xlsx")
