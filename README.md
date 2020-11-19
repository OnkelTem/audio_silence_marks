# Create silence marks for your audio files

Creates lists of silent spots in audio files using [FFmpeg](https://ffmpeg.org/) filter 
[silencedetect](https://ffmpeg.org/ffmpeg-filters.html#silencedetect).

Currently only [Audipo](https://play.google.com/store/apps/details?id=jp.ne.sakura.ccice.audipo&hl=en_US&gl=US)
player marks format is supported.

**This tool is under development, don't expect much for now.**

## Prerequisites

- [Python 3.8+](https://www.python.org/)
- Linux (haven't tested on Windows/Mac yet)

## Installation

`pip install` is in development.

## Usage

Run the tool against one file or a directory tree:

```
$ audio_silence_marks . file.mp3 > marks.audipomark
$ audio_silence_marks . '**/*.mp3' > marks.audipomark
```

Then upload this file to your phone's directory `Interal Storage/Audipo/Mark`, e.g.: 
```
$ adb push marks.audipomark > /storage/emulated/0/Audipo/Mark/
```

Open your Audipo player, go to `Menu > Preferences` and click on `Import all marks` item.
Restart the player.

It may not work right away due to some issues with paths. 


## Docs

```
$ audio_silence_marks --help

Usage:
  audio_silence_marks PATH GLOB [-f FORMAT] [-l] [-n NOISE_THRESHOLD] [-d DURATION]

Processes audio file FILE using FFMPEG and outputs Audipo markers JSON with the list of
spots placed in the middle of silence intervals.

Arguments:
  PATH                Path to files. [Default: '.']
  GLOB                Glob patter for selecting files. [Default: '**/*.mp3']
                      @see: https://docs.python.org/3.8/library/glob.html
Options:
  -f FORMAT           Marks output format. [Default: audipo]
  -l                  Simply list files not doing anything. Useful for globs debugging.
  -n NOISE_THRESHOLD  Maximum volume of the noise treated as silence in dB [Default: -50]
  -d DURATION         Minimum length of the silent interval in seconds [Default: 1]
```

**Note**: `NOISE_THRESHOLD` and `DURATION` doesn't have any effect yet.