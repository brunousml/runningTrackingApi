from setuptools import setup
import os
import uuid

try:  # for pip >= 10
    # noinspection PyProtectedMember,PyPackageRequirements
    from pip._internal.req import parse_requirements
except ImportError:  # for pip <= 9.0.3
    # noinspection PyPackageRequirements
    from pip.req import parse_requirements


def requirements(path):
    items = parse_requirements(path, session=uuid.uuid1())
    return [";".join((str(r.req), str(r.markers))) if r.markers else str(r.req) for r in items]


tests_require = requirements(os.path.join(os.path.dirname(__file__), "requirements.txt"))
install_requires = requirements(os.path.join(os.path.dirname(__file__), "requirements.txt"))

setup(
    name="sample-flask-project",
    version="1.0.0",
    author="",
    author_email="",
    python_requires='>=3.4.5',
    test_suite="tests",
    install_requires=install_requires,
    tests_require=tests_require
)
