"""A few basic tests for _version.py."""

# ruff: noqa: S101, S603, ANN

import subprocess
import sys

import _version

example_git_output = [
    (("", "", "", ""), "0.0.0"),
    (("", "", "unknown", ""), "0.0.0"),
    (("", "", "unknown", "dirty"), "0.0.0+unknown.dirty"),
    (("0.0.0", "", "abcd", ""), "0.0.0"),
    (("0.0.0", "", "abcd", "dirty"), "0.0.0+abcd.dirty"),
    (("0.0.0", "1", "abcd", ""), "0.0.0.post1+abcd"),
    (("0.0.0", "1", "abcd", "dirty"), "0.0.0.post1+abcd.dirty"),
]


def test_get_extended_version() -> None:
    """Test get_extended_version function."""
    for args, ref in example_git_output:
        v = _version.get_extended_version(*args)
        assert v == ref, f"{args} -> {v} != {ref}"


def test_failsafe() -> None:
    """Test that in case anything errors, we don't crash."""
    ori_repo_dir = _version.repo_dir
    del _version.repo_dir

    try:
        v = _version.get_version()
        assert v == "0.0.0"

    finally:
        _version.repo_dir = ori_repo_dir


example_versions = [
    ("1", (1,)),
    ("1.2", (1, 2)),
    ("1.2.3", (1, 2, 3)),
    ("1.2.3", (1, 2, 3)),
    ("1.2.3.post9", (1, 2, 3, "post", 9)),
    ("1.2.3.post10", (1, 2, 3, "post", 10)),
    ("0.29.0.post4+g3175010", (0, 29, 0, "post", 4)),
    (
        "2.6.0+gcd877db.dirty",
        (
            2,
            6,
            0,
        ),
    ),
    ("0.15.0.post16+g63b1a427.dirty", (0, 15, 0, "post", 16)),
    ("2.6.1+from_tag_2_6_0.post3.g72c1d22", (2, 6, 1)),
    ("1.+foo", (1,)),
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
