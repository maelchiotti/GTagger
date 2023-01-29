# Changelog

## v1.2.5

- Tags management:
  - Greatly improved the speed of the lyrics search by using multithreading

## v1.2.4

- Files support:
    - A file, multiple files or a directory can be dragged and dropped in GTagger.
    - The state indicator can be clicked to play the track in the default application.
- Tracks display and management:
    - Added buttons to (de)select the tracks.
    - Added a button to show the full lyrics of a track in a popup window.
    - Added a button to copy the lyrics of a track to the clipboard.
- Settings:
    - The position of the toolbar is now automatically saved in the settings.

## v1.2.3

- Layout:
    - Improved the toolbar to make it movable.
- Tracks display and management:
    - Greatly improved the responsiveness of the list of tracks.
    - Added a clear button for the token and filter inputs.
    - Added the choice to match case or not when filtering.
    - Added the ability sort the tracks by title.
    - Removed the compact layout because it didn't fit with the way the track layouts are now managed.
- Tags management:
    - Improved the detection of wrong lyrics.
    - Improved the search of tracks.

## v1.2.2

- Tracks display and management:
    - All tracks can be selected by hitting `Ctrl+A`, and deselected by hitting `Ctrl+D`.

## v1.2.1

- Miscellaneous:
    - Changed all icons to use [qtawesome](https://github.com/spyder-ide/qtawesome) MDI6 icons instead of SVG files.

## v1.2.0

- Files support:
    - Added support for `.flac` files.
- Tracks display and management:
    - Added a filter by text (that hides tracks not containing the text in their title or artists), and a filter to hide
      tracks already containing lyrics.
    - Added a compact mode which contains only core information on the tracks. The user can switch between the normal
      and the compact mode thanks to a button in the status bar.
    - Added a colored state indicator to replace the text one.
    - Tracks are now added in a thread to avoid locking the GUI.
    - Deactivated the add files and add folder buttons when tags are being read.
- Tags management:
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
    - Added an information window.
    - Added a help window.
    - Added icons to the windows.
- Miscellaneous:
    - Removed the light theme because it was hard to maintain with the new functionalities.
    - Removed the need for [LyricsGenius](https://github.com/johnwmillr/LyricsGenius), now
      that [wrap-genius](https://github.com/fedecalendino/wrap-genius) allows to fetch the lyrics.

## v1.1.0

- Tracks display and management:
    - Added a custom display to show the information of the tracks.
    - Added the display of the track duration.
    - Improved the display of the new lyrics.
- Miscellaneous:
    - Added a toggleable dark theme (on by default).

## v1.0.0

- Initial release.
