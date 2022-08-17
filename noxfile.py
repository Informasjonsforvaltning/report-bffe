"""Nox sessions."""
import tempfile

import nox
from nox.sessions import Session
import nox_poetry

nox.options.envdir = ".cache"
locations = "src", "test", "noxfile.py"
nox.options.sessions = (
    "lint",
    "mypy",
    "unit_tests",
    "contract_tests",
    "integration_tests",
)


@nox_poetry.session(python="3.9")
def unit_tests(session: Session) -> None:
    """Run the unit test suite."""
    args = session.posargs
    session.install(
        ".",
        "pytest",
        "requests-mock",
        "pytest-mock",
    )
    session.run(
        "pytest",
        "-m unit",
        "-rA",
        *args,
    )


@nox_poetry.session(python="3.9")
def tests(session: Session) -> None:
    """Run the integration test suite."""
    args = session.posargs or ["--cov"]
    session.install(
        ".",
        "coverage[toml]",
        "pytest",
        "pytest-cov",
        "pytest-docker",
        "requests-mock",
        "pytest-mock",
        "pytest-aiohttp",
    )
    session.run(
        "pytest",
        "-rA",
        *args,
    )


@nox_poetry.session(python="3.9")
def contract_tests(session: Session) -> None:
    """Run the contract test suite."""
    args = session.posargs
    session.install(".", "pytest", "pytest-docker", "requests_mock", "pytest_mock")
    session.run(
        "pytest",
        "-m contract",
        "-rA",
        *args,
    )


@nox_poetry.session(python="3.9")
def integration_tests(session: Session) -> None:
    """Run the integration test suite."""
    args = session.posargs
    session.install(
        ".",
        "pytest",
        "pytest-docker",
        "requests-mock",
        "pytest-mock",
    )
    session.run(
        "pytest",
        "-m integration",
        "-rA",
        *args,
    )


@nox_poetry.session(python="3.9")
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@nox_poetry.session(python="3.9")
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-import-order",
        "pep8-naming",
    )
    session.run("flake8", *args)


@nox_poetry.session(python="3.9")
def coverage(session: Session) -> None:
    """Upload coverage data."""
    session.install("coverage[toml]", "codecov")
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)


@nox_poetry.session(python="3.9")
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    session.install("mypy")
    session.run("mypy", *args)


@nox_poetry.session(python="3.9")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install("safety")
        session.run(
            "safety", "check", f"--file={requirements.name}", "--output", "text"
        )
