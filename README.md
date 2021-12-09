# Create silence marks for your audio files

Creates a list of "silences" timecodes in audio files using **FFmpeg** and its filter 
[silencedetect](https://ffmpeg.org/ffmpeg-filters.html#silencedetect).

Currently, only [Audipo](https://play.google.com/store/apps/details?id=jp.ne.sakura.ccice.audipo&hl=en_US&gl=US)
player marks format is supported.

## Prerequisites

- [Python 3.8+](https://www.python.org/)
- [FFmpeg](https://ffmpeg.org/)
- Linux (haven't tested on Windows/Mac yet)

## Installation

```
$ pip install audio_silence_marks
```

## Usage

Run the tool against one file or a directory tree:

```
$ audio_silence_marks . file.mp3 > marks.audipomark
$ audio_silence_marks . '**/*.mp3' > marks.audipomark
```

Then upload this file to your phone's directory `Interal Storage/Audipo/Mark`, e.g.: 
```
$ adb push marks.audipomark /storage/emulated/0/Audipo/Mark/
```

Open your Audipo player, go to `Menu > Preferences` and click on `Import all marks` item.
Restart the player.

## Result

Example:

|                                                   Unit 23                                                    |                         Unit 24                                                                              |
|:------------------------------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------------------------------:|
| ![image](https://user-images.githubusercontent.com/114060/99715000-5cd86780-2ab7-11eb-8707-b7235bebebf3.png) | ![image](https://user-images.githubusercontent.com/114060/99714622-dc196b80-2ab6-11eb-977d-cd3d58ff1786.png) | 

## Processing audiobooks

The script accepts two parameters which highly affect the output, i.e. the amount and the positions of the marks.
They are: 

- `--noise`, `-n` - noise tolerance in decibels (negated for convenience).

  Acts like a reverse noise gate, passing through parts with the volume below defined. The default value is `50` (which makes `-50dB`).

- `--duration`, `-d` - duration of silence in milliseconds. 

  Sets the minimum duration of silence. The default value is `1000` (ms).

Thus, even a book with some background music which level is less than of the speech, can be successfully marked by `--noise` parameter tuning.

An example profile for a regular book:

```
audio_silence_marks -d 400 -n 30 . book.mp3 > marks.audipomark 
```

This sets `-30dB` noise level and `400` millisecond minimum silence duration.

## Docs

```
$ audio_silence_marks --help

Usage: audio_silence_marks [OPTIONS] PATH GLOB

  Processes audio files using FFmpeg filter silencedetect and outputs Audipo
  markers JSON with the list of spots placed in the middle of silence
  intervals.

  More info on using GLOBS: https://docs.python.org/3.8/library/glob.html

Arguments:
  PATH  is a path to files. E.g: "."  [required]
  GLOB  argument is a pattern for selecting files. E.g.: '**/*.mp3'
        [required]


Options:
  -t, --target [audipo]           Target format for marks.  [default: audipo]
  -n, --noise INTEGER             Maximum volume of the noise treated as
                                  silence in -dB  [default: 50]

  -d, --duration INTEGER          Minimum length of the silent interval in
                                  milliseconds [default: 1000]

  -l, --list                      Simply lists matched files. Useful for GLOB
                                  debugging.  [default: False]

  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.
```
