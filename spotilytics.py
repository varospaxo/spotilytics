import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import zipfile
import os
import json
from collections import defaultdict
from datetime import datetime
from collections import Counter
import time
from fpdf import FPDF

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

def yearly():
    try:
        x = int(x_entry.get())
        if x <= 0:
            raise ValueError("The value of x must be a positive integer.")
    except ValueError:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Note: No value entered for number of results. Defaulting to top 10 results.")
        x=10

    zip_file_path = filedialog.askopenfilename(filetypes=[("ZIP Files", "*.zip")])

    if zip_file_path:
        unzipped_dir = extract_zip(zip_file_path)

        if unzipped_dir:
            result_text.delete(1.0, tk.END)  # Clear previous results
            result_text.insert(tk.END, "**** Spotilytics ****")
            result_text.insert(tk.END, "\n**** Spotify Yearly Streaming History ****")
            result_text.insert(tk.END, f"\nUnzipped to: {unzipped_dir}".replace("\\", "/"))
            result_text.config(foreground="#1DB954", background="#191414")  # Set text colors

            # Determine which directory exists: MyData or MyHistory
            if os.path.exists(os.path.join(unzipped_dir, "MyData/")):
                directory = os.path.join(unzipped_dir, "MyData/")
            elif os.path.exists(os.path.join(unzipped_dir, "Spotify Account Data/")):
                directory = os.path.join(unzipped_dir, "Spotify Account Data/")
            else:
                extended()
                # result_text.insert(tk.END, "\nError: Neither 'MyData' nor 'Spotify Account Data' folder found in the unzipped directory.")

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
            top_artists = sorted(artist_playtime.items(), key=lambda x: x[1], reverse=True)[:x]
            top_tracks = sorted(track_playtime.items(), key=lambda x: x[1], reverse=True)[:x]

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

            result_text.insert(tk.END, f"\n\nTop {x} Tracks:")
            for i, ((artist_name, track_name), total_track_playtime) in enumerate(top_tracks, 1):
                result_text.insert(tk.END, f"\n{i}. {track_name} by {artist_name} - {total_track_playtime:.2f} minutes"
                                      f" ({track_playcount[(artist_name, track_name)]} times)")

            result_text.insert(tk.END, f"\n\nTop {x} Artists:")
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
            top_10_search_queries = sorted_search_queries[:x]

            # Display the top 10 search queries and their frequencies
            result_text.insert(tk.END, f"\n\nTop {x} Search Queries:")
            for i, (query, frequency) in enumerate(top_10_search_queries, 1):
                result_text.insert(tk.END, f"\n{i}. '{query}' - {frequency} times")


        else:
            result_text.delete(1.0, tk.END)  # Clear previous results
            result_text.insert(tk.END, "\nError occurred while unzipping the file.")
def convert_timestamp(timestamp):
    return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')

def calculate_total_listening_time(data):
    return sum(entry["ms_played"] for entry in data) / 60000  # Convert milliseconds to minutes

def find_most_active_time_range(data):
    timestamps = [convert_timestamp(entry["ts"]) for entry in data]
    active_time_counts = Counter(timestamp.hour for timestamp in timestamps)
    most_active_hour = active_time_counts.most_common(1)[0][0]
    return f"{most_active_hour}:00 - {most_active_hour + 1}:00"

def find_data_start_and_end_span(data):
    timestamps = [convert_timestamp(entry["ts"]) for entry in data]
    return min(timestamps), max(timestamps)

def find_top_n(data, key, n):
    counter = Counter(entry[key] for entry in data)
    return counter.most_common(n)

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

def extended():
    try:
        x = int(x_entry.get())
        if x <= 0:
            raise ValueError("The value of x must be a positive integer.")
    except ValueError:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Note: No value entered for number of results. Defaulting to top 10 results.")
        x=10
    
    zip_file_path = filedialog.askopenfilename(filetypes=[("ZIP Files", "*.zip")])

    if zip_file_path:
        unzipped_dir = extract_zip(zip_file_path)

        if unzipped_dir:
            # x=10
            result_text.delete(1.0, tk.END)  # Clear previous results
            result_text.insert(tk.END, "**** Spotilytics ****")
            result_text.insert(tk.END, "\n**** Spotify Extended Streaming History ****")
            result_text.insert(tk.END, f"\nUnzipped to: {unzipped_dir}".replace("\\", "/"))
            result_text.config(foreground="#1DB954", background="#191414")  # Set text colors

            # Determine which directory exists: MyData or MyHistory
            if os.path.exists(os.path.join(unzipped_dir, "Spotify Extended Streaming History/")):
                directory = os.path.join(unzipped_dir, "Spotify Extended Streaming History/")
            else:
                yearly()
                # result_text.insert(tk.END, "\nError: 'Spotify Extended Streaming History' folder found in the unzipped directory. Retry again!!!")

            # Specify the directory where your JSON files are located
            # directory = str(unzipped_dir+'\\Spotify Extended Streaming History\\')  # Replace with the actual directory path
            result_text.insert(tk.END, f"\nWorking Directory: {directory}".replace("\\", "/"))

            # Initialize a list to store data from all JSON files
            all_data = []

            # Loop through files in the directory
            for filename in os.listdir(directory):
                if filename.startswith("Streaming_History_Audio") and filename.endswith(".json"):
                    # Construct the full file path
                    file_path = os.path.join(directory, filename)

                    # Load data from the JSON file with UTF-8 encoding
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)

                    # Append the data to the all_data list
                    all_data.extend(data)

            # Perform analytics
            total_listening_time = calculate_total_listening_time(all_data)
            most_active_time_range = find_most_active_time_range(all_data)
            data_start, data_end = find_data_start_and_end_span(all_data)
            top_10_tracks = find_top_n(all_data, "master_metadata_track_name", x)
            top_10_artists = find_top_n(all_data, "master_metadata_album_artist_name", x)
            top_10_albums = find_top_n(all_data, "master_metadata_album_album_name", x)
            unique_devices = set(entry["platform"] for entry in all_data)
            total_play_count = len(all_data)

            # Display results
            result_text.insert(tk.END, "\n\n---Streaming Analytics---\n")
            result_text.insert(tk.END, f"Start of dataset: {data_start}\nEnd of dataset: {data_end}\n\n")
            result_text.insert(tk.END, f"Total Playtime: {total_listening_time:.2f} minutes\n")
            result_text.insert(tk.END, f"Total Play Count: {total_play_count} times\n")
            result_text.insert(tk.END, f"Most Active Hour: {most_active_time_range}\n")

            result_text.insert(tk.END, f"\nTop {x} Tracks:\n")
            for i, (track, count) in enumerate(top_10_tracks, start=1):
                minutes_played = sum(entry['ms_played'] for entry in all_data if entry['master_metadata_track_name'] == track) / 60000
                result_text.insert(tk.END, f"{i}. {track} - {minutes_played:.2f} minutes ({count} times)\n")

            result_text.insert(tk.END, f"\nTop {x} Artists:\n")
            for i, (artist, count) in enumerate(top_10_artists, start=1):
                minutes_played = sum(entry['ms_played'] for entry in all_data if entry['master_metadata_album_artist_name'] == artist) / 60000
                result_text.insert(tk.END, f"{i}. {artist} - {minutes_played:.2f} minutes ({count} times)\n")

            result_text.insert(tk.END, f"\nTop {x} Albums:\n")
            for i, (album, count) in enumerate(top_10_albums, start=1):
                result_text.insert(tk.END, f"{i}. {album} - {count} times\n")

            result_text.insert(tk.END, "\nUnique Devices (Unordered):\n")
            i=0
            for device in unique_devices:
                i=i+1
                result_text.insert(tk.END, f"{i}. {device}\n")

        else:
            result_text.delete(1.0, tk.END)  # Clear previous results
            result_text.insert(tk.END, "\nError occurred while unzipping the file.")
            
def save_as_pdf():
    content = result_text.get(1.0, tk.END)  # Get all text from the text widget
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Split content into lines and add them to the PDF
    for line in content.split("\n"):
        pdf.cell(200, 10, txt=line, ln=True, align='L')
    
    # Save the PDF to a file
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        pdf.output(file_path)
        print(f"PDF saved to: {file_path}")
        result_text.delete(1.0, tk.END)  # Clear previous results
        result_text.insert(tk.END, f"PDF saved to: {file_path}")

# Create the main application window
app = tk.Tk()
app.title("Spotilytics (Account Data)")

# Change the application icon (replace 'your_icon.ico' with your icon file path)
app.iconbitmap('logo.ico')

# Create and configure a frame for the file selection and extraction
frame = tk.Frame(app)
frame.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

# Load and display an image before the button
image = PhotoImage(file="logo.png")  # Replace with the path to your image file
image = image.subsample(10)  # Subsample the image to fit in a 500x175 area
image_label = tk.Label(frame, image=image)
image_label.grid(row=0, column=0, columnspan=2, pady=10)

x_label = tk.Label(frame, text="Enter number of top results (x):", fg="#191414")
x_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

x_entry = tk.Entry(frame, width=10)
x_entry.grid(row=1, column=1, sticky="e", padx=10, pady=5)

# Add radio buttons
radio_var = tk.StringVar()

# Set the default selection
radio_var.set("yearly")

radio1 = tk.Radiobutton(frame, text="Yearly", value="yearly", variable=radio_var, fg="#191414")
radio1.grid(row=2, column=0, padx=10, pady=5, sticky="w")

radio2 = tk.Radiobutton(frame, text="Extended", value="extended", variable=radio_var, fg="#191414")
radio2.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Button to trigger action based on radio button selection
def on_button_click():
    selected_option = radio_var.get()  # Get the selected radio button value
    if selected_option == "yearly":
        yearly()  # Call the corresponding function
    elif selected_option == "extended":
        extended()  # Call the corresponding function

select_button = tk.Button(frame, text="Select ZIP File", command=on_button_click, bg="#1DB954", fg="#191414", width=45, height=3)
select_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Increase the button text size
button_font = ("Helvetica", 12)  # You can adjust the font size (12) as needed
select_button.config(font=button_font)

# Button for saving output as PDF
save_button = tk.Button(frame, text="Output data as PDF.", command=save_as_pdf, bg="#1DB954", fg="#191414", width=20, height=2)
save_button.grid(row=4, column=0, columnspan=2, pady=10)

# Create a text widget for displaying the results and make it longer
result_text = tk.Text(app, wrap=tk.WORD, width=80, height=20)  # Adjust the width and height as needed
result_text.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

# Configure row and column weights to make the text widget expandable
app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(0, weight=1)

# Set the background and foreground colors for the text widget
result_text.config(background="#191414", foreground="#1DB954")

# Run the application
app.mainloop()