# Spotilytics: Your Spotify Streaming History Anytime

![Spotilytics](https://github.com/varospaxo/spotilytics/assets/64273563/9bb683d3-1437-479e-ad5c-32109f8e2fb0)


Why wait for Spotify Wrapped when you can download your own data anytime and view your streaming history all year round using Spotilytics. Spotilytics provides you with multiple interfaces to extract data from your Spotify account. Currently works only on Windows OS with Python 3.10+ installed.

You might wonder, why not use the Spotify API? Well, the Spotify API requires user login and can be a privacy concern for some individuals. Therefore, downloading your entire data offline and analyzing it with this open-source tool makes more sense.

## Steps to Get the Data

1. Go to [Spotify Account Privacy Settings](https://www.spotify.com/us/account/privacy/).
2. Select 'Account Data' (Preparation time: 5 days).
3. Click on the link in the confirmation email sent to your inbox.
4. Wait for 5 days to receive your Spotify data.
5. Once the data is received, download the zip file and save it.

## Steps to Run Spotilytics

1. Clone the repository - Spotilytics GitHub Repository:
```sh
 git clone https://github.com/varospaxo/spotilytics/
 ```
2. Change your directory to `spotilytics`:
  ```sh
   cd spotilytics
   ```
3. To run `Spotilytics GUI`, use the command:
  ```sh
   python Interface.py
   ```
<B>OR</B> To run `Spotilytics CLI`, use the command:
  ```sh
   python Grand.py
   ```
<B>OR</B> To run `Spotilytics CLI with HTML output`, use the command:
  ```sh
   python Flask.py
   ```
4. Once Spotilytics is running, select the zip file (for GUI) or provide the path to the zip file without quotes (for CLI).
5. The data will be extracted automatically and displayed as output.

## Features of Spotilytics
&#9679; Extracts Account Identity Data.<br>
&#9679; Extracts Personal User Data.<br>
&#9679; Shows total playtime.<br>
&#9679; Displays Top 10 Tracks from last year.<br>
&#9679; Displays Top 10 Artists from last year.<br>
&#9679; Shows Top 10 Search Queries from last year.<br>

Enjoy exploring your Spotify streaming history throughout the year with Spotilytics!<br>


<p align="center"><img src="https://github.com/varospaxo/spotilytics/assets/64273563/cc193c6b-79cc-45d4-81ba-2999e2c8155d"</img></p>
