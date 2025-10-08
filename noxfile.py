import nox

# Define the Python versions to test against
PYTHON_VERSIONS = ["3.11"]

# --- Nox Sessions ---

@nox.session(name="test")
def test(session: nox.Session) -> None:
    """
    Run the unit test suite using pytest.
    """
    # Install the CPU-only version of PyTorch first to save space.
    # This is a common practice in CI environments that don't have GPUs.
    session.install("torch", "--index-url", "https://download.pytorch.org/whl/cpu")
    
    # Install all other project dependencies from requirements.txt
    session.install("-r", "requirements.txt")
    
    # Run pytest.
    session.run("pytest", *session.posargs)

@nox.session(name="typing")
def typing(session: nox.Session) -> None:
    """
    Run the static type checker (mypy).
    """
    # Install the CPU-only version of PyTorch first.
    session.install("torch", "--index-url", "https://download.pytorch.org/whl/cpu")
    
    # Install other project dependencies.
    session.install("-r", "requirements.txt")
    
    # Run mypy on the source directory.
    session.run("mypy", "src")
