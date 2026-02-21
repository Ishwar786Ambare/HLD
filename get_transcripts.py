"""
YouTube Transcript Fetcher
==========================
Fetches transcripts from YouTube videos and saves them as .txt files.

Usage:
    1. Activate venv:  .venv\\Scripts\\activate
    2. Run:            python get_transcripts.py

Requires: youtube-transcript-api (v1.x+ API)
"""

import sys
import io
import os

# Force UTF-8 output on Windows terminals
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from youtube_transcript_api import YouTubeTranscriptApi

# ─── Config ───────────────────────────────────────────────────────────────────

VIDEOS = [
    {"id": "icAJxnynJZI", "title": "HLD_SQL_vs_NoSQL_5"},
    {"id": "QQOkT6wrpdE", "title": "HLD_SQL_vs_NoSQL_6"},
    {"id": "BaLdJ6GWWDg", "title": "HLD_NoSQL_continued_7"},
]

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "transcripts")

# ─── Functions ────────────────────────────────────────────────────────────────

def fetch_transcript(video_id: str, title: str):
    """Fetch transcript for a given YouTube video ID (new API v1.x)."""
    print(f"\n[FETCH] {title}  ->  https://youtu.be/{video_id}")

    try:
        # v1.x API: instantiate first, then call .list()
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)

        transcript = None

        # Priority 1: manually created English
        for t in transcript_list:
            if not t.is_generated and t.language_code == "en":
                transcript = t
                print("   [OK] Manually created English transcript found.")
                break

        # Priority 2: auto-generated English
        if transcript is None:
            for t in transcript_list:
                if t.is_generated and t.language_code == "en":
                    transcript = t
                    print("   [OK] Auto-generated English transcript found.")
                    break

        # Priority 3: any transcript (translate to English)
        if transcript is None:
            for t in transcript_list:
                transcript = t.translate("en")
                print(f"   [OK] Found '{t.language_code}' transcript, translated to English.")
                break

        if transcript is None:
            print("   [ERROR] No transcript found at all.")
            return None, None

        # Fetch the actual transcript data
        raw = transcript.fetch()

        # Plain text (no timestamps)
        plain_lines = [entry.text for entry in raw]
        plain_text = "\n".join(plain_lines)

        # Timestamped version
        ts_lines = []
        for entry in raw:
            mins = int(entry.start // 60)
            secs = int(entry.start % 60)
            ts_lines.append(f"[{mins:02d}:{secs:02d}] {entry.text}")
        timestamped_text = "\n".join(ts_lines)

        return plain_text, timestamped_text

    except Exception as e:
        print(f"   [ERROR] Could not fetch transcript: {e}")
        return None, None


def save_transcript(title: str, plain: str, timestamped: str):
    """Save plain + timestamped transcripts to the output directory."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    plain_path = os.path.join(OUTPUT_DIR, f"{title}_plain.txt")
    ts_path    = os.path.join(OUTPUT_DIR, f"{title}_timestamped.txt")

    with open(plain_path, "w", encoding="utf-8") as f:
        f.write(plain)

    with open(ts_path, "w", encoding="utf-8") as f:
        f.write(timestamped)

    print(f"   [SAVED] {plain_path}")
    print(f"   [SAVED] {ts_path}")


def main():
    print("=" * 60)
    print("  YouTube Transcript Fetcher - HLD SQL vs NoSQL Series")
    print("=" * 60)

    all_combined = []

    for video in VIDEOS:
        plain, timestamped = fetch_transcript(video["id"], video["title"])

        if plain:
            save_transcript(video["title"], plain, timestamped)
            header = (
                f"\n\n{'='*60}\n"
                f"# {video['title']}\n"
                f"# https://youtu.be/{video['id']}\n"
                f"{'='*60}\n\n"
            )
            all_combined.append(header + plain)
        else:
            print(f"   [SKIP] No transcript available for: {video['title']}")

    # Save one big combined file
    if all_combined:
        combined_path = os.path.join(OUTPUT_DIR, "ALL_TRANSCRIPTS_COMBINED.txt")
        with open(combined_path, "w", encoding="utf-8") as f:
            f.write("\n".join(all_combined))
        print(f"\n[DONE] Combined transcript saved -> {combined_path}")
        print(f"[INFO] {len(all_combined)} of {len(VIDEOS)} transcripts fetched.")
    else:
        print("\n[WARN] No transcripts were fetched.")
        print("[HINT] These videos may have transcripts disabled by the creator.")

    print("\n[COMPLETE] Finished!")


if __name__ == "__main__":
    main()
