import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="javets-quiz-cli",
    version="0.0.1",
    description="CLI QUIZ USING PYTHON",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/uditvashisht/saral-square",
    author="Udit Vashisht",
    author_email="admin@saralgyaan.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["javets_quiz_cli"],
    include_package_data=True,
    install_requires=["rich" , "subprocess" , "typer"],
    entry_points={
        "console_scripts": [
            "quiz=javets_quiz_cli.__main__:main",
        ]
    },
)
