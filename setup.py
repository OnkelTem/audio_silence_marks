import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="audio_silence_marks",
    version="0.0.1",
    description="Tool for creating silence marks for audio files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OnkelTem/audio_silence_marks",
    author="OnkelTem",
    author_email="aneganov@gmail.com",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "docopt",
    ],
    entry_points={
        "console_scripts": ["audio_silence_marks=audio_silence_marks.main:main"],
    },
    python_requires=">=3.6",
)
