# MusicDownloader
Allows direct YouTube to MP3 downloads from terminal with the following features:
  - Lets you pass a list of songs as an argument
  - Lets you make a simple, direct download (no confirmation) or a complete one, with multiple results to choose from
  - Focused on speed (no need to try torrents. Simple, straight-forward and working).

Requirements:
1. Linux with python3 (probably lower versions work as well)
2. Chrome driver (https://chromedriver.chromium.org/). Add the path to the EXECUTABLE_CHROMEDRIVER_PATH variable
3. Edit the MUSIC_DIRECTORY variable to contain your own path
4. Enjoy!

# Note for debugging #
It may be usefull to comment out the '--headless' and '--disable-gpu' options to have a visual feedback on what is happening.
Planning to use requests to the websites instead of selenium for performance.
