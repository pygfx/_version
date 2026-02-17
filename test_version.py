"""A few basic tests for _version.py."""

# ruff: noqa: S101, S603, ANN

import subprocess
import sys

import _version

example_versions = [
    ("1", (1,)),
    ("1.2", (1, 2)),
    ("1.2.3", (1, 2, 3)),
    ("1.2.3", (1, 2, 3)),
    ("0.29.0.post4#g3175010", (0, 29, 0, "post4", "#g3175010")),
    ("2.6.0#gcd877db.dirty", (2, 6, 0, "#gcd877db", "dirty")),
    ("0.15.0.post16#g63b1a427.dirty", (0, 15, 0, "post16", "#g63b1a427", "dirty")),
    ("1.#foo", (1, "#foo")),
]


def test_version_to_tuple() -> None:
    """Test test_version_to_tuple function."""
    for v, ref in example_versions:
        t = _version.version_to_tuple(v)
        assert t == ref, f"{v} -> {t} != {ref}"


def test_run_as_script() -> None:
    """Test the basics of the CLI util."""
    # Plain call
    p = subprocess.run(
        [sys.executable, _version.__file__],
        capture_output=True,
        check=False,
    )
    assert p.returncode == 0
    assert p.stderr.decode().strip() == ""
    text = p.stdout.decode().strip()
    assert text == "PROJECT_NAME v0.0.0"

    # Use 'version'
    p = subprocess.run(
        [sys.executable, _version.__file__, "version"],
        capture_output=True,
        check=False,
    )
    assert p.returncode == 0
    assert p.stderr.decode().strip() == ""
    text = p.stdout.decode().strip()
    assert text == "PROJECT_NAME v0.0.0"

    # Use 'help'
    p = subprocess.run(
        [sys.executable, _version.__file__, "help"],
        capture_output=True,
        check=False,
    )
    assert p.returncode == 0
    assert p.stderr.decode().strip() == ""
    text = p.stdout.decode().strip()
    assert text.startswith("_version.py")
    assert "help" in text
    assert "bump" in text
    assert "update" in text

    # Use false command
    p = subprocess.run(
        [sys.executable, _version.__file__, "foobar"],
        capture_output=True,
        check=False,
    )
    assert p.returncode == 1
    assert p.stderr.decode().strip() == ""
    text = p.stdout.decode().strip()
    assert text.startswith("Unknown command")


# %%%%%


def run_tests(scope: dict) -> None:
    """Small util to run all tests."""
    for func in list(scope.values()):
        if callable(func) and func.__name__.startswith("test_"):
            sys.stdout.write(f"Running {func.__name__} ...\n")
            func()
    sys.stdout.write("Done\n")


if __name__ == "__main__":
    run_tests(globals())
