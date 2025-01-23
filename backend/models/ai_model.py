from typing import List, Dict

def analyze_transcript(transcript: List[Dict], keywords: List[str]) -> List[Dict]:
    results = []
    for entry in transcript:
        text = entry['text']
        if any(keyword.lower() in text.lower() for keyword in keywords):
            results.append({
                'start': entry['start'],
                'end': entry['start'] + entry['duration'],
                'text': text
            })
    return results
