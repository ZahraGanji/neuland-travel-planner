import nox

# Define the Python versions to test against
PYTHON_VERSIONS = ["3.11"]

# --- Nox Sessions ---

@nox.session(name="test")
def test(session: nox.Session) -> None:
    """
    Run the unit test suite using pytest.
    """
    
    # Install all other project dependencies from requirements.txt
    session.install("-r", "requirements.txt")
    session.install("pytest")
    # Run pytest.
    session.run("pytest", *session.posargs)

@nox.session(name="typing")
def typing(session: nox.Session) -> None:
    """
    Run the static type checker (mypy).
    """
    
    # Install other project dependencies.
    session.install("-r", "requirements.txt")
    
    # Run mypy on the source directory.
    session.run("mypy", "src")
