# Afterscrape #

### Description ###
Webinterface for displaying and editing game's metadata on [Retropie](https://retropie.org.uk/).

## Motivation ##
Retropie's [Emulationstation](http://www.emulationstation.org/) has a build in scraper but with a lot of roms it can take a lot of work to get all the metadata. Emulationstation supports snap video but it will not scrape them. Thankfully there is [steven selph's scraper](https://github.com/sselph/scraper/wiki) to automate the scraping process and get snap video's as a bonus. But still after scraping I see myself manually editing a lot of roms because I'm not content with the data it had scraped. Also there are not enough options in SS scraper to really set all the metadata the way I want. And lastly I would like an overview of all the roms in one screen. So I decided to build my own software.

I chose HTML5, python and Flask as they are fast and simple enough to work in a raspberry pi (currently developing on pi 3).

## Features ##
currently working:
* list all systems from default roms-folder
* list all roms from selected system
  * show if game in xml-file
  * show if game has image
  * show if game has video
* display game's metadata from xml-file
  * support for image
  * support for video

currently in development:
* manual edit game's metadata
* scrape game's metadata from [TheGamesDB](http://thegamesdb.net/)

planned:
* scrape metadata from other sources
* scrape metedata fields from selected source
* display image / video media info
* more to come...

### disclaimer ###
English is not my native language, excuse me for my spelling. Programming is not my profession but my hobby. My code can look weird and wrong, that is because I'm learning.

Any help would be appreciated.
