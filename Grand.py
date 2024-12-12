import zipfile
import os
import json

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

if __name__ == "__main__":
    zip_file_path = input("Enter the path to the ZIP file: ")
    x=10
    x=int(input("Enter the number of top artists and tracks to display: "))
    
    unzipped_dir = extract_zip(zip_file_path)

    if unzipped_dir:
        print(f"\nUnzipped to: {unzipped_dir}")
    else:
        print("\nError occurred while unzipping the file.")

# Specify the directory where your JSON files are located
    if os.path.exists(os.path.join(unzipped_dir, "MyData/")):
        directory = os.path.join(unzipped_dir, "MyData/")
    elif os.path.exists(os.path.join(unzipped_dir, "Spotify Account Data/")):
        directory = os.path.join(unzipped_dir, "Spotify Account Data/")
    else:
        print("\nError: Neither 'MyData' nor 'Spotify Account Data' folder found in the unzipped directory.")
print ("Working Directory: " + directory)
# Read and display data from Identity.json
identityloc = str(directory+'Identity.json')
with open(identityloc, 'r', encoding='utf-8') as identity_file:
    identity = json.load(identity_file)
print("\n---Identity Data---")
print("Display Name:", identity["displayName"])
print("First Name:", identity["firstName"])
print("Last Name:", identity["lastName"])
print("Image URL:", identity["imageUrl"])
print("Large Image URL:", identity["largeImageUrl"])
print("Taste Maker Account:", identity["tasteMaker"])
print("Verified Account:", identity["verified"])

# Read and display data from Userdata.json
userdataloc = str(directory + 'Userdata.json')
# Read and display data from Userdata.json
with open(userdataloc, 'r', encoding='utf-8') as userdata_file:
    userdata = json.load(userdata_file)
print("\n---User Data---")
print("Username:", userdata["username"])
print("Email:", userdata["email"])
print("Country:", userdata["country"])
print("Birthdate:", userdata["birthdate"])
print("Gender:", userdata["gender"])
print("Mobile Number:", userdata["mobileNumber"])
print("Creation Time:", userdata["creationTime"])
print()

# Initialize a list to store data from all JSON files
all_data = []

# Loop through files in the directory
for filename in os.listdir(directory):
    if filename.startswith("StreamingHistory") and filename.endswith(".json") and not filename.startswith("StreamingHistory_podcast_"):
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
top_artists = sorted(artist_playtime.items(), key=lambda x: x[1], reverse=True)[:x]
top_tracks = sorted(track_playtime.items(), key=lambda x: x[1], reverse=True)[:x]

# Calculate the total playtime in minutes
total_playtime_minutes = sum(entry["msPlayed"] / 60000 for entry in all_data)

print("\n---Streaming Analytics---")

# Display the results
print(f"Start of dataset: {first_end_time}")
print(f"End of dataset: {last_end_time}")

print(f"\nTotal Playtime: {total_playtime_minutes:.2f} minutes")

print("\nTop 10 Tracks:")
for i, (track_key, total_track_playtime) in enumerate(top_tracks, 1):
    artist_name, track_name = track_key
    print(f"{i}. {track_name} by {artist_name} - {total_track_playtime:.2f} minutes")

print("\nTop 10 Artists:")
for i, (artist_name, total_artist_playtime) in enumerate(top_artists, 1):
    print(f"{i}. {artist_name} - {total_artist_playtime:.2f} minutes")

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
print("\nTop 10 Search Queries:")
for i, (query, frequency) in enumerate(top_10_search_queries, 1):
    print(f"{i}. '{query}' - {frequency} times")
    
print()