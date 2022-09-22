# Changelog

## v1.2.0

- Files support:
  - Added support for `.flac` files.

- Tracks display and managment:
  - Added a filter by text (that hides tracks not containing the text in their title or artists), and a filter to hide tracks already containing lyrics.
  - Added a compact mode which contains only core informations on the tracks. The user can switch between the normal and the compact mode thanks to a button in the status bar.
  - Added a colored state indicator to replace the text one.
  - Tracks are now added in a thread to avoid locking the GUI.
  - Deactivated the add files and add folder buttons when tags are being read.

- Tags managment:
  - Added a progression bar that shows the progression of:
    - The reading of the tags,
    - The search of the lyrics,
    - The saving of the tags.
  - Added a button to stop the search of the lyrics.
  - Keep original tag version and formatting.

- Settings:
  - Added a setting to not overwrite already existing lyrics.
  - Settings are now saved on the computer.

- Windows:
  - Added an informations window.
  - Added a help window.
  - Added icons to the windows.

- Miscellaneous:
  - Removed the light theme because it was hard to maintain with the new functionnalities.
  - Removed the need for [LyricsGenius](https://github.com/johnwmillr/LyricsGenius), now that [wrap-genius](https://github.com/fedecalendino/wrap-genius) allows to fetch the lyrics.

## v1.1.0

- Tracks display and managment:
  - Added a custom display to show the informations of the tracks.
  - Added the display of the track duration.
  - Improved the display of the new lyrics.

- Miscellaneous:
  - Added a togglable dark theme (on by default).

## v1.0.0

- Initial release.
