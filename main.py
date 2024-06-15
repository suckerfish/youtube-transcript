# This script takes a youtube video ID and timestamps as inputs. It pulls the transcript between those timestamps
# and uses it in an LLM most likely for summary, but this is adjustable.
from youtube_transcript_api import YouTubeTranscriptApi
from gemini import Gemini
from pplx import Perplex
import os
from nicegui import ui

video_id = input("Provide video id: ")
my_transcript = YouTubeTranscriptApi.get_transcript(video_id)


def hhmmss_to_seconds(time_str):
    parts = time_str.split(':')
    # Pad the list to ensure it always has three elements.
    while len(parts) < 3:
        parts.insert(0, '0')  # Inserts '0' at the beginning if parts are missing
    h, m, s = map(int, parts)
    return h * 3600 + m * 60 + s


def filter_entries(entries, start_time_str=None, end_time_str=None):
    # Convert start time from HH:MM:SS to seconds or default to zero
    start_time = hhmmss_to_seconds(start_time_str) if start_time_str else 0
    # Convert end time from HH:MM:SS to seconds or
    end_time = hhmmss_to_seconds(end_time_str) if end_time_str else float('inf')
    # Function to filter entries within a specified time range.
    filtered_entries = []
    for entry in entries:
        entry_end = entry['start'] + entry['duration']
        # Check if the entry falls within the time range
        if entry['start'] <= end_time and entry_end >= start_time:
            filtered_entries.append(entry)
    return filtered_entries


# Ask how much transcript they want
start_time_str = input("Start time in format HH:MM:SS (default is 00:00:00): ")
end_time_str = input("End time in format HH:MM:SS (default is until end): ")

# Filter the entries based on timestamps
filtered = filter_entries(my_transcript, start_time_str, end_time_str)
# structure the transcript
curated_transcript = ' '.join(i["text"] for i in filtered)

ai = Perplex()

ai.ask(f"Please give a systematic, structured summary of the following movie/tv/music review: {curated_transcript}")



