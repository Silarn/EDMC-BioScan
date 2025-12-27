# BioScan

## Summary

BioScan is a multipurpose exobiology tool for Elite Dangerous. It utilizes the plugin system of the [Elite Dangerous
Market Connector][EDMC] for backend journal processing and display.

## Core Functionality and Comparison

The core functionality of BioScan is to provide the best possible estimates for which species will be present on a
planet, much like the [Observatory] [BioInsights] plugin. With the latest updates, BioScan can be slightly more accurate
at ruling out certain bios with overlapping criteria. In a few edge cases, BioInsights may be slightly more accurate.
Determining region boundaries and proximity to nebulae can be hard.

There are a few key differences between each. BioScan is intended to be used as an active tool with a compact
interface which could be potentially overlaid onto the game. It also presents key information to help you navigate and
track flora while landing, moving, and scanning on a planet.

It supports both Horizons and Odyssey biologicals.

## Predictions

<img src="BioScan-FSS.png">

While collecting scan data of a system, planets with biological signals will be added to the main tracker. Based on the
properties of that planet (as well as your location in the galaxy, and the various stars and body types present), the
scroll pane will display all possible genera and species that could be on that body as well as the potential value range
of those possibilities. You can optionally display a complete breakdown of the possible species and variants.

## Scanning

<img src="BioScan-SAA-Prog-2.png">

After you've mapped a planet with biological signals, it will then pare down the list to the detected genera or species.
Once you've started to scan each species, it will display the final type and value of the sample as well as indicate the
scan progress. Additional info will be discussed in the [navigation](#navigation) section below.

Once fully analysed, the total system value (and possible first find value) will be shown at the bottom of the pane.

## Codex Entries

<img src="BioScan-Codex.png">

As of version 2.5, any potential species that has not yet been logged to your local region's codex will be marked. If
there are multiple possible species or variants (colors), those will be individually marked in the detailed breakdown.

This is marked by the 📝 memo emoji in front of the genus or variant. Species / variants you haven't seen before will
be marked with the 🌌 milky way emoji.

For best results, see [journal importing](#journal-importing).

## Navigation

The top of the pane will track all relevant bodies in the system, including a shorthand for the body type and the number
of signals detected there. This can help you quickly determine a DSS target. There are additional indicators for high
gravity `^G^` and extreme gravity `!G!` planets. High gravity is currently considered 1G or greater. Extreme gravity
is 2.7G or greater which makes it impossible to go on foot.

BioScan will track your movements and show just the relevant species data if you are currently located at a body of
interest, to help reduce clutter and scrolling. It will also give you the gravity of the planet to help you gauge your
landing. After you initiate a scan, you will get a display of the required sample distance and your current minimum
distance to a previous sample, which is updated in real time.

It will reset your scan progress if the previous scan wasn't completed and you start a different species. It can also
track scans with the composition scanner and will lock in the final species of the genus without requiring you to scan
biologicals one at a time. In this way you can lock in a species and value while completing the analysis of another
lifeform.

#### Waypoints

<img src="BioScan-Waypoints.png"><br><img src="BioScan-Active-Waypoint.png">

Scans with the comp. scanner will optionally log waypoints for any incomplete species. If you have an active scan, the
nearest waypoint for that species will display below the progress indicator. Waypoints within the minimum distance of
previous samples are excluded from the list. When you have no active scan, any remaining unanalyzed species will display
the nearest waypoint in the detailed species scroll list.

The waypoint indicator will display the distance to the waypoint, the compass heading toward that waypoint, and an
indicator for the direction and degrees to turn to face that heading. Note that waypoints will log your current
location, so for best results make the scan as close to the target species as possible.

#### Radar

When using the [overlay](#overlay-version-27), you can use an optional radar display. This shows markers for any scanned
bios relative to your facing direction. North is indicated on the border. The radar distance is configurable with both
linear and logarithmic scaling modes. It will also track your ship location.

### Persistent Data

As of version 2.0, BioScan now maintains a database of all relevant system data and scan progress. It segments scans,
waypoints, and codex data by commander. You can safely stop and restart EDMC without losing your data.

From version 2.6 forward, the database management is handled by the [ExploData] plugin/module. See that repository for
more details.

### Journal Importing

To facilitate accurate codex entry data, you can import your past journals into the persistent database. Clicking the
button in the bottom left of the settings panel will start the process. This can run in the background while you
continue to use EDMC / BioScan, and the progress will display at the bottom of the BioScan pane.

Despite using a few threads to help speed up the process, parsing several years of journal data can take a good amount
of time. As each journal is completed, it will get logged in the database. This process can be stopped and restarted. It
will pick up at the oldest unprocessed journal, though you will need to click the button in the settings to resume.

### EDSM Integration

Once per system, you can attempt to fetch any data from EDSM. This is helpful in systems that can't be scanned for one
reason or another. Unfortunately, EDSM's API does not currently provide access to biological signal info, so you will
have to manually look up signals if that data was not previously logged.

### Overlay (Version 2.7+)

BioScan can now make use of EDMCOverlay to draw predictions, signal summaries, and status info directly onto the game
window. The text color and anchor points are configurable. Suggestions welcome.

## Requirements
* [EDMC] version 5.7 and above (python 3.11)
  * Future releases will be targetted at EDMC 6.x and python 3.13
* SQLAlchemy python module (embedded in the exe distribution)
* (Optional) [ModernOverlay] / [EDMCOverlay] / [edmcoverlay2]

## Installation

* Download the [latest release] of both BioScan and ExploData
  * Appropriate versions of both are available on every release page
  * ExploData has multiple versions depending on how you run EDMC:
    * Users of the prebuilt Windows EXE must use the Windows EXE version of ExploData
    * Flatpak users must use the flatpak version, which is bundled with SQLAlchemy
    * Native python users should use the native python version (see additional instructions below)
  * If you use [Pioneer], make sure the version you're using is up-to-date with ExploData
* Extract the `.zip` archives that you downloaded into the EDMC `plugins` folder
  * This is accessible via the plugins tab in the EDMC settings window
  * The ExploData plugin directory must be named as it is packaged, or you will run into trouble loading dependencies
* For native python users:
  * If you use `venv`, install the SQLAlchemy requirement from the `requirements.txt` to the EDMC venv
  * For system python, run `pip install -r requirements.txt` within the ExploData plugin directory to install SQLAlchemy
  * Ensure the correct `pip` is used for your version of EDMC
* (Optional) Install [ModernOverlay] or another compatible overlay plugin for overlay support
  * Either 'EDMCOverlay' or 'edmcoverlay' should work as the plugin directory name
* Start or restart EDMC to register the plugin and run any necessary database migrations

## Acknowledgements

Conversion of system coordinates to regions thanks to klightspeed's [EliteDangerousRegionMap].

Species calculations are based on various sources, primarily the [Deep Space Network], the
[Codex NSP and Bio requirements spreadsheet][Bio req spreadsheet], and the [Canonn Biosheet].

Nebula locations pulled from the [Catalog of Galactic Nebulae] (thanks marx and contributors)

Procedurally generated nebula reference star coordinates pulled from [EDSM]'s API

## Roadmap

* Criteria details popout display
* Compass bearing hint at waypoint locations
* General graphical refinements
* Improved star luminosity calculations
* Voice support

## License

[BioScan plugin][BioScan] Copyright © 2024 Jeremy Rimpo

Licensed under the [GNU Public License (GPL)][GPLv2] version 2 or later.

[EDMC]: https://github.com/EDCD/EDMarketConnector/wiki
[EDSM]: https://www.edsm.net/
[Deep Space Network]: https://ed-dsn.net/
[Bio req spreadsheet]: https://docs.google.com/spreadsheets/d/1nV_UD_0kIxkWAHhAqvf62ILHpbYzdZpJ53CqPHn3qlA/
[Canonn Biosheet]: https://canonn.fyi/biosheet
[EliteDangerousRegionMap]: https://github.com/klightspeed/EliteDangerousRegionMap/
[Catalog of Galactic Nebulae]: https://forums.frontier.co.uk/threads/catalogue-of-galactic-nebulae-submit-your-planetary-nebulae.511743/
[BioScan]: https://github.com/Silarn/EDMC-BioScan
[Pioneer]: https://github.com/Silarn/EDMC-Pioneer
[ExploData]: https://github.com/Silarn/EDMC-ExploData
[Observatory]: https://github.com/Xjph/ObservatoryCore
[BioInsights]: https://edjp.colacube.net/observatory
[ModernOverlay]: https://github.com/SweetJonnySauce/EDMCModernOverlay
[EDMCOverlay]: https://github.com/inorton/EDMCOverlay
[edmcoverlay2]: https://github.com/pan-mroku/edmcoverlay2
[latest release]: https://github.com/Silarn/EDMC-BioScan/releases/latest
[GPLv2]: http://www.gnu.org/licenses/gpl-2.0.html
