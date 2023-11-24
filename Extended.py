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

def main():
    # Read data from the JSON file
    with open("StreamingHistory1.json", "r", encoding='utf-8') as file:
        json_data = json.load(file)

    # Perform analytics
    total_listening_time = calculate_total_listening_time(json_data)
    most_active_time_range = find_most_active_time_range(json_data)
    data_start, data_end = find_data_start_and_end_span(json_data)
    top_10_tracks = find_top_n(json_data, "master_metadata_track_name", 10)
    top_10_artists = find_top_n(json_data, "master_metadata_album_artist_name", 10)
    top_10_albums = find_top_n(json_data, "master_metadata_album_album_name", 10)
    unique_devices = set(entry["platform"] for entry in json_data)

    # Display results
    print(f"Total Listening Time: {total_listening_time:.2f} minutes")
    print(f"Most Active Time Range: {most_active_time_range}")
    print(f"Data Start: {data_start}\nData End: {data_end}")
    print("\nTop 10 Tracks:")
    for track, count in top_10_tracks:
        print(f"{track}: {count} plays ({sum(entry['ms_played'] for entry in json_data if entry['master_metadata_track_name'] == track) / 60000:.2f} minutes)")
    print("\nTop 10 Artists:")
    for artist, count in top_10_artists:
        print(f"{artist}: {count} plays")
    print("\nTop 10 Albums:")
    for album, count in top_10_albums:
        print(f"{album}: {count} plays")
    print("\nUnique Devices:")
    for device in unique_devices:
        print(device)

if __name__ == "__main__":
    main()
