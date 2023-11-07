from flask import Flask, render_template, request, redirect, url_for
import os
from zipfile import ZipFile
import zipfile
import os
import json
import random
import string

app = Flask(__name__)

# Corrected upload folder path
UPLOAD_FOLDER = 'uploads'  # Remove the leading slash
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'zip_file' not in request.files:
        return redirect(request.url)

    file = request.files['zip_file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        def generate_random_10_character_string():
            characters = string.ascii_letters + string.digits
            random_folder = ''.join(random.choice(characters) for _ in range(10))
            return random_folder

        random_folder = generate_random_10_character_string()
        print(random_folder)

        def extract_zip(zip_file_path):
            try:
                zip_dir = os.path.dirname(zip_file_path)
                unzip_dir = os.path.join(zip_dir, random_folder)  # Corrected path join

                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall(unzip_dir)

                return unzip_dir
            except Exception as e:
                return str(e)

        if __name__ == "__main__":
            zip_file_path = filename
            unzipped_dir = extract_zip(zip_file_path)

            if unzipped_dir:
                print(f"\nUnzipped to: {unzipped_dir}")
            else:
                print("\nError occurred while unzipping the file.")

        directory = os.path.join(unzipped_dir, 'MyData')  # Corrected path join

        # Create an HTML file to save the output
        html_output_file = os.path.join(unzipped_dir, "output.html")  # Corrected path join

        # The rest of the code remains the same

        with open(html_output_file, "w") as html_file:
            html_file.write("<html><head><title>Print Statement Outputs</title></head><body>")

            def write_to_html(content):
                html_file.write(content + "<br>")

            write_to_html("Working Directory: " + directory)

            # Write Identity Data
            identityloc = str(directory + 'Identity.json')
            with open(identityloc, 'r', encoding='utf-8') as identity_file:
                identity = json.load(identity_file)
            write_to_html("<h2>Identity Data</h2>")
            write_to_html("Display Name: " + identity["displayName"])
            write_to_html("First Name: " + identity["firstName"])
            write_to_html("Last Name: " + identity["lastName"])
            write_to_html("Image URL: " + identity["imageUrl"])
            write_to_html("Large Image URL: " + identity["largeImageUrl"])
            write_to_html("Taste Maker Account: " + str(identity["tasteMaker"]))
            write_to_html("Verified Account: " + str(identity["verified"]))

            # Write User Data
            userdataloc = str(directory + 'Userdata.json')
            with open(userdataloc, 'r', encoding='utf-8') as userdata_file:
                userdata = json.load(userdata_file)
            write_to_html("<h2>User Data</h2>")
            write_to_html("Username: " + userdata["username"])
            write_to_html("Email: " + userdata["email"])
            write_to_html("Country: " + userdata["country"])
            write_to_html("Birthdate: " + userdata["birthdate"])
            write_to_html("Gender: " + userdata["gender"])
            write_to_html("Mobile Number: " + userdata["mobileNumber"])
            write_to_html("Creation Time: " + userdata["creationTime"])
            
        # Initialize a list to store data from all JSON files
            all_data = []

            # Loop through files in the directory
            for filename in os.listdir(directory):
                if filename.startswith("StreamingHistory") and filename.endswith(".json"):
                    # Construct the full file path
                    file_path = os.path.join(directory, filename)

                    # Load data from the JSON file with UTF-8 encoding
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)

                    # Append the data to the all_data list
                    all_data.extend(data)

            # Now, all_data contains the combined data from all JSON files starting with "StreamingHistory"
            # You can perform data analysis on this combined data as shown in your previous code
            # ...

            # Create dictionaries to store total playtime for artists and tracks
            artist_playtime = {}
            track_playtime = {}

            # Extract the endTime of the first and last result
            first_end_time = all_data[0]["endTime"]
            last_end_time = all_data[-1]["endTime"]

            # Calculate the total playtime for each artist and track in minutes
            for entry in all_data:  # Use all_data instead of data
                artist_name = entry["artistName"]
                track_name = entry["trackName"]
                ms_played = entry["msPlayed"]

                # Convert milliseconds to minutes
                minutes_played = ms_played / 60000  # 1 minute = 60000 ms

                # Update the artist playtime
                if artist_name in artist_playtime:
                    artist_playtime[artist_name] += minutes_played
                else:
                    artist_playtime[artist_name] = minutes_played

                # Update the track playtime
                track_key = (artist_name, track_name)
                if track_key in track_playtime:
                    track_playtime[track_key] += minutes_played
                else:
                    track_playtime[track_key] = minutes_played

            # Sort the artists and tracks by total playtime in descending order
            top_artists = sorted(artist_playtime.items(), key=lambda x: x[1], reverse=True)[:10]
            top_tracks = sorted(track_playtime.items(), key=lambda x: x[1], reverse=True)[:10]

            # Calculate the total playtime in minutes
            total_playtime_minutes = sum(entry["msPlayed"] / 60000 for entry in all_data)

            # Print Streaming Analytics
            write_to_html("<h2>Streaming Analytics</h2>")
            write_to_html(f"Start of dataset: {first_end_time}")
            write_to_html(f"End of dataset: {last_end_time}")
            write_to_html(f"Total Playtime: {total_playtime_minutes:.2f} minutes")

            write_to_html("<h3>Top 10 Tracks:</h3>")
            for i, (track_key, total_track_playtime) in enumerate(top_tracks, 1):
                artist_name, track_name = track_key
                write_to_html(f"{i}. {track_name} by {artist_name} - {total_track_playtime:.2f} minutes")

            write_to_html("<h3>Top 10 Artists:</h3>")
            for i, (artist_name, total_artist_playtime) in enumerate(top_artists, 1):
                write_to_html(f"{i}. {artist_name} - {total_artist_playtime:.2f} minutes")


            # Replace 'your_file.json' with the path to your UTF-8 encoded JSON file
            file_path = directory + 'SearchQueries.json'
            # Load data from the JSON file with UTF-8 encoding
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Initialize a dictionary to store search query frequencies
            search_query_freq = {}

            # Extract and count unique search queries
            for entry in data:
                search_query = entry["searchQuery"]
                if search_query in search_query_freq:
                    search_query_freq[search_query] += 1
                else:
                    search_query_freq[search_query] = 1

            # Sort the search queries by frequency in descending order
            sorted_search_queries = sorted(search_query_freq.items(), key=lambda x: x[1], reverse=True)

            # Get the top 10 unique search queries
            top_10_search_queries = sorted_search_queries[:10]

            write_to_html("<h3>Top 10 Artists:</h3>")
            for i, (query, frequency) in enumerate(top_10_search_queries, 1):
                write_to_html(f"{i}. '{query}' - {frequency} times")

            # Close the HTML document
            html_file.write("</body></html>")
            source_path = '/uploads/'+random_folder+'/output.html'
            destination_path = '/templates/'+random_folder+'/output.html'
            os.rename(source_path, destination_path)
            
        return render_template('/uploads/'+random_folder+'/output.html')

if __name__ == '__main__':
    app.run(debug=True)
