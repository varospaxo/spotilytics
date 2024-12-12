import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import zipfile
import os
import json
from collections import defaultdict
from datetime import datetime

def extract_zip(zip_file_path):
    try:
        # Get the directory where the ZIP file is located
        zip_dir = os.path.dirname(zip_file_path)

        # Create a folder to unzip the contents (use the ZIP file's name without the extension)
        unzip_dir = os.path.join(zip_dir, os.path.splitext(os.path.basename(zip_file_path))[0])

        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(unzip_dir)

        return unzip_dir
    except Exception as e:
        return str(e)

def process_zip():
    zip_file_path = filedialog.askopenfilename(filetypes=[("ZIP Files", "*.zip")])

    if zip_file_path:
        unzipped_dir = extract_zip(zip_file_path)

        if unzipped_dir:
            result_text.delete(1.0, tk.END)  # Clear previous results
            result_text.insert(tk.END, f"Unzipped to: {unzipped_dir}".replace("\\", "/"))
            result_text.config(foreground="#1DB954", background="#191414")  # Set text colors

            # Determine which directory exists: MyData or MyHistory
            if os.path.exists(os.path.join(unzipped_dir, "MyData/")):
                directory = os.path.join(unzipped_dir, "MyData/")
            elif os.path.exists(os.path.join(unzipped_dir, "Spotify Account Data/")):
                directory = os.path.join(unzipped_dir, "Spotify Account Data/")
            else:
                result_text.insert(tk.END, "\nError: Neither 'MyData' nor 'Spotify Account Data' folder found in the unzipped directory.")

            # Ensure the directory uses forward slashes for consistency in display
            directory = directory.replace("\\", "/")
            result_text.insert(tk.END, f"\nWorking Directory: {directory}")

            # Read and display data from Identity.json
            identityloc = str(directory+'Identity.json')
            with open(identityloc, 'r', encoding='utf-8') as identity_file:
                identity = json.load(identity_file)
            result_text.insert(tk.END, f"\n\n---Identity Data---")
            result_text.insert(tk.END, f"\nDisplay Name: {identity['displayName']}")
            result_text.insert(tk.END, f"\nFirst Name: {identity['firstName']}")
            result_text.insert(tk.END, f"\nLast Name: {identity['lastName']}")
            result_text.insert(tk.END, f"\nImage URL: {identity['imageUrl']}")
            result_text.insert(tk.END, f"\nLarge Image URL: {identity['largeImageUrl']}")
            result_text.insert(tk.END, f"\nTaste Maker Account: {identity['tasteMaker']}")
            result_text.insert(tk.END, f"\nVerified Account: {identity['verified']}")

            # Read and display data from Userdata.json
            userdataloc = str(directory + 'Userdata.json')
            # Read and display data from Userdata.json
            with open(userdataloc, 'r', encoding='utf-8') as userdata_file:
                userdata = json.load(userdata_file)
            result_text.insert(tk.END, f"\n\n---User Data---")
            result_text.insert(tk.END, f"\nUsername: {userdata['username']}")
            result_text.insert(tk.END, f"\nEmail: {userdata['email']}")
            result_text.insert(tk.END, f"\nCountry: {userdata['country']}")
            result_text.insert(tk.END, f"\nBirthdate: {userdata['birthdate']}")
            result_text.insert(tk.END, f"\nGender: {userdata['gender']}")
            result_text.insert(tk.END, f"\nMobile Number: {userdata['mobileNumber']}")
            result_text.insert(tk.END, f"\nCreation Time: {userdata['creationTime']}")

            # Initialize a list to store data from all JSON files
            all_data = []

            # Loop through files in the directory
            for filename in os.listdir(directory):
                if filename.startswith("StreamingHistory") and filename.endswith(".json") and not filename.startswith("StreamingHistory_podcast_"):
                    # Construct the full file path
                    file_path = os.path.join(directory, filename)
                    print (file_path)

                    # Load data from the JSON file with UTF-8 encoding
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)

                    # Append the data to the all_data list
                    all_data.extend(data)

            # Now, all_data contains the combined data from all JSON files starting with "StreamingHistory"
            # You can perform data analysis on this combined data as shown in your previous code
            # ...

            # Create dictionaries to store total playtime and play count for artists and tracks
            artist_playtime = {}
            artist_playcount = {}
            track_playtime = {}
            track_playcount = {}

            # Extract the endTime of the first and last result
            first_end_time = all_data[0]["endTime"]
            last_end_time = all_data[-1]["endTime"]

            # Calculate the total playtime and play count for each artist and track in minutes
            for entry in all_data:  # Use all_data instead of data
                artist_name = entry["artistName"]
                track_name = entry["trackName"]
                ms_played = entry["msPlayed"]

                # Convert milliseconds to minutes
                minutes_played = ms_played / 60000  # 1 minute = 60000 ms

                # Update the artist playtime and play count
                if artist_name in artist_playtime:
                    artist_playtime[artist_name] += minutes_played
                    artist_playcount[artist_name] += 1
                else:
                    artist_playtime[artist_name] = minutes_played
                    artist_playcount[artist_name] = 1

                # Update the track playtime and play count
                track_key = (artist_name, track_name)
                if track_key in track_playtime:
                    track_playtime[track_key] += minutes_played
                    track_playcount[track_key] += 1
                else:
                    track_playtime[track_key] = minutes_played
                    track_playcount[track_key] = 1

            # Sort the artists and tracks by total playtime in descending order
            top_artists = sorted(artist_playtime.items(), key=lambda x: x[1], reverse=True)[:10]
            top_tracks = sorted(track_playtime.items(), key=lambda x: x[1], reverse=True)[:10]

            # Calculate the total playtime and play count in minutes
            total_playtime_minutes = sum(entry["msPlayed"] / 60000 for entry in all_data)
            total_play_count = len(all_data)

            result_text.insert(tk.END, f"\n\n---Streaming Analytics---")

            # Display the results
            result_text.insert(tk.END, f"\nStart of dataset: {first_end_time}")
            result_text.insert(tk.END, f"\nEnd of dataset: {last_end_time}")

            result_text.insert(tk.END, f"\n\nTotal Playtime: {total_playtime_minutes:.2f} minutes")
            result_text.insert(tk.END, f"\nTotal Play Count: {total_play_count} times")
            
            # Initialize a dictionary to store play frequency for each hour of the day
            hour_play_count = defaultdict(int)

            # Convert endTime to hour and update the play count for each hour
            for entry in all_data:
                end_time_str = entry["endTime"]
                end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M")
                hour_play_count[end_time.hour] += 1

            # Find the most active hour range
            most_active_hour = max(hour_play_count, key=hour_play_count.get)
            most_active_hour_range = f"{most_active_hour:02}:00 - {most_active_hour + 1:02}:00"
            result_text.insert(tk.END, f"\nMost Active Hour: {most_active_hour_range}")

            result_text.insert(tk.END, f"\n\nTop 10 Tracks:")
            for i, ((artist_name, track_name), total_track_playtime) in enumerate(top_tracks, 1):
                result_text.insert(tk.END, f"\n{i}. {track_name} by {artist_name} - {total_track_playtime:.2f} minutes"
                                      f" ({track_playcount[(artist_name, track_name)]} times)")

            result_text.insert(tk.END, f"\n\nTop 10 Artists:")
            for i, (artist_name, total_artist_playtime) in enumerate(top_artists, 1):
                result_text.insert(tk.END, f"\n{i}. {artist_name} - {total_artist_playtime:.2f} minutes"
                                      f" ({artist_playcount[artist_name]} times)")

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

            # Display the top 10 search queries and their frequencies
            result_text.insert(tk.END, f"\n\nTop 10 Search Queries:")
            for i, (query, frequency) in enumerate(top_10_search_queries, 1):
                result_text.insert(tk.END, f"\n{i}. '{query}' - {frequency} times")


        else:
            result_text.delete(1.0, tk.END)  # Clear previous results
            result_text.insert(tk.END, "\nError occurred while unzipping the file.")

# Create the main application window
app = tk.Tk()
app.title("Spotilytics (Account Data)")

# Change the application icon (replace 'your_icon.ico' with your icon file path)
app.iconbitmap('spotilytics.ico')

# Create and configure a frame for the file selection and extraction
frame = tk.Frame(app)
frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# Load and display an image before the button
image = PhotoImage(file="Spotilytics.png")  # Replace with the path to your image file
image = image.subsample(10)  # Subsample the image to fit in a 500x175 area
image_label = tk.Label(frame, image=image)
image_label.grid(row=0, column=0, padx=10, pady=10)

select_button = tk.Button(frame, text="Select ZIP File", command=process_zip, bg="#1DB954", fg="#191414", width=45, height=3)
select_button.grid(row=1, column=0, padx=10, pady=10)

# Increase the button text size
button_font = ("Helvetica", 12)  # You can adjust the font size (12) as needed
select_button.config(font=button_font)

# Create a text widget for displaying the results and make it longer
result_text = tk.Text(app, wrap=tk.WORD, width=80, height=25)  # Adjust the width and height as needed
result_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Configure row and column weights to make the text widget expandable
app.grid_rowconfigure(2, weight=1)
app.grid_columnconfigure(0, weight=1)

# Set the background and foreground colors for the text widget
result_text.config(background="#191414", foreground="#1DB954")

app.mainloop()
