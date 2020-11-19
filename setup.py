from setuptools import setup

setup(
    name="audio_silence_marks",
    version="0.1",
    description="Tool for creating silence marks for audio files",
    url="https://github.com/onkeltem/audio_silence_marks/",
    author="OnkelTem",
    author_email="aneganov@gmail.com",
    license="MIT",
    packages=["audio_silence_marks"],
    install_requires=[
        "docopt",
    ],
    entry_points={
        "console_scripts": ["audio_silence_marks=audio_silence_marks.main:main"],
    },
    zip_safe=False,
)
