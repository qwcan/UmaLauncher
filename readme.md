# Uma Launcher
Software that enhances the Uma Musume experience.

[Frequently Asked Questions](FAQ.md)

For questions and feedback, join the Discord server:

[![Uma Launcher Discord server](https://discordapp.com/api/guilds/1416044589877559497/widget.png?style=banner2)](https://discord.gg/wvGHW65C6A)

## Requirements (Optional but recommended)
### NOTE: The original version of CarrotJuicer available on GitHub does not work with the current Japanese Version of Uma Musume.<br> Either use one of the updated forks or get the dll from the Hachimi Discord server.
The global version of Uma Launcher requires CarrotBlender, also available on the Hachimi Discord server. The install instructions are the same as CarrotJuicer.
<details>
  <summary>CarrotJuicer</summary>
  
- [CarrotJuicer](https://github.com/hayaunderscore/CarrotJuicer) (Not made by me.)
  - CarrotJuicer/CarrotBlender require a build of Hachimi with plugin support, preferably [Hachimi-Edge](https://github.com/kairusds/Hachimi-Edge/releases/latest).<br>
  Use the installer exe to install Hachimi (you may need to restart your computer after installation).<br>
  See [the Hachimi-Edge website](https://hachimi.noccu.art/) for details.
  - Download the latest version, preferably from the Hachimi discord server.
  - Copy the .dll file into the `hachimi` folder in the game's install directory.
  - Edit the `config.json` file in that folder to add the dll to the `load_libraries` list.<br>
  For example, if the file is named `carrotjuicer.dll` then the line should be `"load_libraries": ["hachimi\\carrotjuicer.dll"],`
  - While optional, CarrotJuicer allows Uma Launcher to extract information from the network packets the game sends/receives. This information is necessary to determine the current status of the game, and needed for most of the features of Uma Launcher to work.

</details>

## Download
Download the latest version's `UmaLauncher.exe` (JP DMM), `UmaLauncher (Global).exe` (Global Steam), or `UmaLauncher (Steam).exe` (JP Steam).

[![Latest release](https://img.shields.io/github/v/release/qwcan/UmaLauncher)](https://github.com/qwcan/UmaLauncher/releases/latest)

## Usage
Download the latest release's `UmaLauncher.exe` and run it. Right-click the horseshoe icon in the system tray to change the settings or close Uma Launcher.

On first launch or when you change the game's location, you may be asked to select the installation location for the game if you are not using the default location.

When a new version of Uma Launcher is available, you will be notified on startup. You may choose to update, or postpone the update temporarily or permanently.

## Features
### Launch Uma Musume simply by running one file
- The program automatically launches the game through DMM and closes it without needing any extra interaction.
  - Exceptions are: Logging into DMM and confirming game updates.
- The script will ask for administrator privileges to interact with the Uma Musume window.
### Better Discord rich presence for Uma Musume
![An example of the training rich presence.](assets/rich-presence.png)

*An example of the training rich presence during training.*
- Shows which home screen you're on.
- Shows training and concert details extracted from the game's packets. **(CarrotJuicer required)**
- (Still work-in-progress.)
### Automatic GameTora training event helper
**(CarrotJuicer required)**

![An example of the automatic training event helper scrolling to the training event.](assets/event-helper.gif)

*An example of the automatic training event helper scrolling to the training event.*
- Automatically start a browser window with the current trained character and support cards.
- Automatically selects and scrolls to event choices when needed.
- Displays a useful table of the current training facilities' details.
  - Customize the table's rows and settings to your liking.
- Supports Edge, Chrome and Firefox browsers.
### Inspect your training runs
**(CarrotJuicer required)**

![An example of the training run CSV, imported into Excel. (Only a subset of columns is shown.)](assets/training-csv-excel.png)

*An example of a training run CSV, imported into Excel. (Only a subset of columns is shown.)*
- With the 'Track trainings' setting enabled, your training runs will be saved as a gzip file in the `training_logs` folder. This folder will be automatically created next to the exe.
- Use the 'Export Training CSV' option in the tray icon menu to export the training logs to a CSV file.
- CSVs can be generated without launching the exe by dragging and dropping logs from the `training_logs` folder onto the exe.
- [CSV format documentation](Training_Analyzer_Documentation.md)
### Quality-of-life features
![An image showing the different settings in the tray icon.](assets/tray-icon.png)

*An image showing the different settings in the tray icon.*
- Various options to enable/disable during gameplay by right-clicking the horse shoe icon in the system tray/taskbar:
  - Locking and remembering the game window position for portrait and landscape mode separately.
    - This also includes the automatic training event helper.
  - Automatically resizing the game to the largest possible size on your screen.
  - Take screenshots.

## Disclaimer
Uma Launcher is in no way associated with Uma Musume, Cygames Inc., DMM or DMM Games/EXNOA LLC.
It is the developer's belief that this tool is harmless to the above companies and brands and merely acts as a tool to improve the user experience.  

## License
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)  
This code is available under the GNU GPLv3 license.

## Credits
Credits for included libraries can be found in the [credits file](CREDITS.txt).
