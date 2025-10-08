"""This module implements our CI function calls."""
import nox


@nox.session(name="test")
def run_test(session):
    """Run pytest."""
    session.install("-r", "requirements.txt")
    session.install("pytest")
    session.run("pytest")




@nox.session(name="typing")
def mypy(session):
    """Check type hints."""
    session.install("-r", "requirements.txt")
    session.install("mypy")
    session.run(
        "mypy",
        "src",
    )


