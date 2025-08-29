# _version
Pragmatic version string management


## Purpose

* Use a hard-coded version string, so users and build tools can easily
  detect it from the source code.
* Include info from git, such as number of commits since last release,
  git hash, and dirty status.
* A simple module that is easy to maintain.
* A simple mechanism to update the module in projects that it's used in.


## Usage

The "installation":

* Add the `_version.py` to the root of your library (next to the `__init__.py`).
* Set the project name and __version__ string.
* In your `__init__.py`, use `from _version import __version__, version_info`.
* In `pyproject.toml` use `dynamic = ["version"]`.
* The Flit build tool will now detect your project version. Other tools may
  need an extra line, e.g. `[tool.hatch.version]` `path = "lib_name/_version.py"`.

When releasing:

* Just update the `__version__` string in `_version.py`.

To update the module:

* Run `python _version.py update`


## Examples

```
# End users who installed your lib using e.g. pip
0.12.0

# Dev on the same release, but installed from the repo
0.12.0+g15e3681e

# Dev on main, some time after the last release
0.12.0.post39+g93a91d54

# Dev making local changes
0.12.0.post39+g93a91d54.dirty
```

BTW, getting a version on the command line can be done with:
```
python -c "import pygfx; print(pygfx.__version__)"
```
