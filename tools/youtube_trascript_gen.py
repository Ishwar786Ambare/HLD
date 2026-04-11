from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def get_transcript(video_url_or_id: str, language: str = 'en') -> str:
    """
    Fetch transcript from a YouTube video.
    
    Args:
        video_url_or_id: Full YouTube URL or just the video ID
        language: Language code (default: 'en')
    
    Returns:
        Transcript as plain text
    """
    # Extract video ID if full URL is provided
    if "youtube.com/watch?v=" in video_url_or_id:
        video_id = video_url_or_id.split("v=")[1].split("&")[0]
    elif "youtu.be/" in video_url_or_id:
        video_id = video_url_or_id.split("youtu.be/")[1].split("?")[0]
    else:
        video_id = video_url_or_id  # Assume it's already a video ID

    try:
        # Fetch transcript
        transcript_list = YouTubeTranscriptApi().list(video_id)
        
        # Try to get transcript in preferred language, fallback to auto-generated
        try:
            transcript = transcript_list.find_transcript([language])
        except:
            print(f"No '{language}' transcript found. Trying auto-generated...")
            transcript = transcript_list.find_generated_transcript([language])
        
        # Format transcript as plain text
        formatter = TextFormatter()
        transcript_data = transcript.fetch()
        formatted_text = formatter.format_transcript(transcript_data)
        
        return formatted_text

    except Exception as e:
        return f"Error fetching transcript: {str(e)}"


def save_transcript(transcript: str, filename: str = "transcript.txt"):
    """Save transcript to a text file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(transcript)
    print(f"Transcript saved to '{filename}'")


if __name__ == "__main__":
    # --- Example Usage ---
    video_input = input("Enter YouTube URL or Video ID: ").strip()
    lang = input("Enter language code (default: 'en'): ").strip() or "en"

    print("\nFetching transcript...\n")
    transcript = get_transcript(video_input, lang)

    print(transcript[:2000])  # Preview first 2000 characters

    save_option = input("\nSave transcript to file? (y/n): ").strip().lower()
    if save_option == "y":
        save_transcript(transcript)
        