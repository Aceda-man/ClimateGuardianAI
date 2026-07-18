import sqlite3
import bcrypt
import re

from database.database import get_connection


# ==================================================
# PASSWORD VALIDATION
# ==================================================
def validate_password(password):

    if len(password) < 8:
        return False, "Password must be at least 8 characters."

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain an uppercase letter."

    if not re.search(r"[a-z]", password):
        return False, "Password must contain a lowercase letter."

    if not re.search(r"\d", password):
        return False, "Password must contain a number."

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain a special character."

    return True, ""


# ==================================================
# HASHING
# ==================================================
def hash_text(text):

    return bcrypt.hashpw(
        text.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_hash(text, hashed):

    return bcrypt.checkpw(
        text.encode("utf-8"),
        hashed.encode("utf-8")
    )


# ==================================================
# CHECK EXISTING USER
# ==================================================
def user_exists(email, username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT email, username
        FROM users
        WHERE email=? OR username=?
        """,
        (
            email,
            username
        )
    )

    user = cursor.fetchone()

    conn.close()

    return user


# ==================================================
# REGISTER USER
# ==================================================
def register_user(
    full_name,
    email,
    username,
    password,
    state,
    lga,
    community,
    user_type,
    security_question,
    security_answer
):

    valid, message = validate_password(password)

    if not valid:
        return False, message

    existing = user_exists(email, username)

    if existing:

        if existing["email"] == email:
            return False, "Email already exists."

        if existing["username"] == username:
            return False, "Username already exists."

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users(

            full_name,
            email,
            username,
            password,
            state,
            lga,
            community,
            user_type,
            security_question,
            security_answer

        )

        VALUES(?,?,?,?,?,?,?,?,?,?)

        """,
        (
            full_name,
            email,
            username,
            hash_text(password),
            state,
            lga,
            community,
            user_type,
            security_question,
            hash_text(
                security_answer.strip().lower()
            )
        )
    )

    conn.commit()
    conn.close()

    return True, "Account created successfully."


# ==================================================
# LOGIN
# ==================================================
def login_user(identifier, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username=? OR email=?
        """,
        (
            identifier,
            identifier
        )
    )

    user = cursor.fetchone()

    conn.close()

    if user is None:
        return None

    if verify_hash(password, user["password"]):
        return dict(user)

    return None


# ==================================================
# GET SECURITY QUESTION
# ==================================================
def get_security_question(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT security_question
        FROM users
        WHERE email=?
        """,
        (email,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return row["security_question"]

    return None


# ==================================================
# VERIFY SECURITY ANSWER
# ==================================================
def verify_security_answer(email, answer):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT security_answer
        FROM users
        WHERE email=?
        """,
        (email,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return False

    return verify_hash(
        answer.strip().lower(),
        row["security_answer"]
    )


# ==================================================
# RESET PASSWORD
# ==================================================
def reset_password(email, new_password):

    valid, message = validate_password(new_password)

    if not valid:
        return False, message

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE users
        SET password=?
        WHERE email=?
        """,
        (
            hash_text(new_password),
            email
        )
    )

    conn.commit()
    conn.close()

    return True, "Password reset successful."