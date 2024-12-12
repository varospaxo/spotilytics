import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import zipfile
import os
import json
from datetime import datetime
from collections import Counter

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

def process_zip():
    zip_file_path = filedialog.askopenfilename(filetypes=[("ZIP Files", "*.zip")])

    if zip_file_path:
        unzipped_dir = extract_zip(zip_file_path)

        if unzipped_dir:
            result_text.delete(1.0, tk.END)  # Clear previous results
            result_text.insert(tk.END, f"Unzipped to: \n{unzipped_dir}".replace("\\", "/"))
            result_text.config(foreground="#1DB954", background="#191414")  # Set text colors

            # Specify the directory where your JSON files are located
            directory = str(unzipped_dir+'\\Spotify Extended Streaming History\\')  # Replace with the actual directory path
            result_text.insert(tk.END, f"\nWorking Directory: \n{directory}".replace("\\", "/"))

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
            top_10_tracks = find_top_n(all_data, "master_metadata_track_name", 10)
            top_10_artists = find_top_n(all_data, "master_metadata_album_artist_name", 10)
            top_10_albums = find_top_n(all_data, "master_metadata_album_album_name", 10)
            unique_devices = set(entry["platform"] for entry in all_data)
            total_play_count = len(all_data)

            # Display results
            result_text.insert(tk.END, "\n\n---Streaming Analytics---\n")
            result_text.insert(tk.END, f"Start of dataset: {data_start}\nEnd of dataset: {data_end}\n\n")
            result_text.insert(tk.END, f"Total Playtime: {total_listening_time:.2f} minutes\n")
            result_text.insert(tk.END, f"Total Play Count: {total_play_count} times\n")
            result_text.insert(tk.END, f"Most Active Hour: {most_active_time_range}\n")

            result_text.insert(tk.END, "\nTop 10 Tracks:\n")
            for i, (track, count) in enumerate(top_10_tracks, start=1):
                minutes_played = sum(entry['ms_played'] for entry in all_data if entry['master_metadata_track_name'] == track) / 60000
                result_text.insert(tk.END, f"{i}. {track} - {minutes_played:.2f} minutes ({count} times)\n")

            result_text.insert(tk.END, "\nTop 10 Artists:\n")
            for i, (artist, count) in enumerate(top_10_artists, start=1):
                minutes_played = sum(entry['ms_played'] for entry in all_data if entry['master_metadata_album_artist_name'] == artist) / 60000
                result_text.insert(tk.END, f"{i}. {artist} - {minutes_played:.2f} minutes ({count} times)\n")

            result_text.insert(tk.END, "\nTop 10 Albums:\n")
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

# Create the main application window
app = tk.Tk()
app.title("Spotilytics (Extended Streaming History)")

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
