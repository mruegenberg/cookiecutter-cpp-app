""" Test the Cookiecutter template.

A template project is created in a temporary directory, the application and its
test suite are built, and both are executed.

"""
from json import loads
from pathlib import Path
from shlex import split
from subprocess import check_call
from tempfile import TemporaryDirectory

from cookiecutter.main import cookiecutter


def main() -> int:
    """ Execute the test.
    
    """
    template = Path(__file__).resolve().parents[1]
    defaults = loads(template.joinpath("cookiecutter.json").read_text())
    with TemporaryDirectory() as tmpdir:
        cookiecutter(str(template), no_input=True, output_dir=tmpdir)
        name = defaults["project_slug"]
        cwd = Path(tmpdir) / name
        for args in "-DCMAKE_BUILD_TYPE=Debug", "--build .":
            check_call(split(f"cmake {args:s}"), cwd=cwd)
        for command in f"./{name:s} -h", f"test/test_{name:s}":
            check_call(split(f"{command:s}"), cwd=cwd)
    return 0
    
    
# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(main())
