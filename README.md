# BioScan plugin for [EDMC]

## WORK IN PROGRESS
This plugin is heavily a WIP. Expect bugs. Please report any errors that might be caught in the debug log.

---

BioScan is a utility for Explorers and Exobiologists that attempts to determine the possible value range of biological
signals on bodies. It uses data such as the atmosphere, gravity, volcanism, surface temperature, body type, and local
star type to make the best guess as to what types of fauna will be present.

Once done, it will summarize the possible value ranges for all qualifying genus and species.

After you've mapped a planet with biological signals, it will then pare down the list to the detected genera.
And finally, once you've started to scan each species it will display the final type and value of the sample as well as
indicate the scan progress.

Once fully analysed, the total system value (and possible first footfall value) will be shown at the bottom of the pane.

## Requirements
* EDMC version 5 and above

## Installation
* Download the [latest release]
* Extract the `.zip` archive that you downloaded into the EDMC `plugins` folder
  * This is accessible via the plugins tab in the EDMC settings window
* Start or restart EDMC to register the new plugin

## Acknowledgements

Species calculations are based on various sources, primarily the 
[Deep Space Network](https://ed-dsn.net/) and the
[Codex NSP and Bio requirements spreadsheet][Bio req spreadsheet].

## Roadmap

* Add calculations for additional pre-Odyssey biologicals as they have more particular requirements
* Track when near a planet and focus the data view for that planet
* Add settings for visibility and display options
* Add info about sample distance requirements

## License

[BioScan plugin][BioScan] Copyright © 2023 Jeremy Rimpo

Licensed under the [GNU Public License (GPL)][GPLv2] version 2 or later.

[EDMC]: https://github.com/EDCD/EDMarketConnector/wiki
[BioScan]: https://github.com/Silarn/EDMC-BioScan
[latest release]: https://github.com/Silarn/EDMC-BioScan/releases/latest
[GPLv2]: http://www.gnu.org/licenses/gpl-2.0.html
[Bio req spreadsheet]: https://docs.google.com/spreadsheets/d/1nV_UD_0kIxkWAHhAqvf62ILHpbYzdZpJ53CqPHn3qlA/
