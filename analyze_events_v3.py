import os
import requests
from datetime import datetime, timedelta
import json
from collections import defaultdict
from base64 import b64encode
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_auth_header(api_secret):
    """Create authorization header for Mixpanel API"""
    credentials = b64encode(f"{api_secret}:".encode("utf-8")).decode("utf-8")
    return {"Authorization": f"Basic {credentials}"}

def analyze_event_patterns():
    """Analyze Mixpanel events to identify high-impact AI agent opportunities"""
    try:
        # Get credentials
        project_id = "3632652"  # Your project ID
        api_secret = os.getenv("MIXPANEL_API_SECRET")
        
        if not api_secret:
            print("❌ Error: Missing Mixpanel credentials")
            return False
            
        # Set up date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        # Query Mixpanel Export API
        url = "https://data.mixpanel.com/api/2.0/export"
        params = {
            "project_id": project_id,
            "from_date": start_date.strftime("%Y-%m-%d"),
            "to_date": end_date.strftime("%Y-%m-%d")
        }
        headers = get_auth_header(api_secret)
        
        print("Fetching events from Mixpanel...")
        response = requests.get(url, params=params, headers=headers, stream=True)
        
        if response.status_code != 200:
            print(f"❌ Error: Failed to fetch data. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
        # Process events
        event_counts = defaultdict(int)
        event_properties = defaultdict(set)
        user_sequences = defaultdict(list)
        
        print("Processing events...")
        for line in response.iter_lines():
            if line:
                try:
                    event = json.loads(line)
                    event_name = event.get('event')
                    properties = event.get('properties', {})
                    
                    if event_name:
                        event_counts[event_name] += 1
                        # Store unique property names for each event
                        event_properties[event_name].update(properties.keys())
                        
                except json.JSONDecodeError:
                    continue
        
        # Print summary
        print("\n=== Event Analysis Summary ===")
        print(f"Total unique events: {len(event_counts)}")
        print("\nTop 10 most frequent events:")
        for event, count in sorted(event_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"\n- {event}: {count} occurrences")
            print("  Properties:", ", ".join(sorted(event_properties[event])))
            
        # Look for potential user journey patterns
        print("\n=== Potential User Journey Analysis ===")
        journey_events = [
            event for event, props in event_properties.items()
            if any(word in event.lower() for word in [
                'view', 'click', 'start', 'complete', 'submit', 'create', 
                'edit', 'update', 'delete', 'search', 'filter'
            ])
        ]
        
        print("\nIdentified journey events:")
        for event in sorted(journey_events):
            print(f"- {event}")
            
        # Look for potential struggle points
        print("\n=== Potential Struggle Points ===")
        struggle_events = [
            (event, count) for event, count in event_counts.items()
            if any(word in event.lower() for word in [
                'error', 'fail', 'abandon', 'cancel', 'timeout', 'invalid',
                'retry', 'exception'
            ])
        ]
        
        for event, count in sorted(struggle_events, key=lambda x: x[1], reverse=True):
            print(f"- {event}: {count} occurrences")
            print("  Properties:", ", ".join(sorted(event_properties[event])))
            
        # Save detailed analysis
        analysis = {
            "total_events": len(event_counts),
            "event_counts": dict(event_counts),
            "event_properties": {k: list(v) for k, v in event_properties.items()},
            "journey_events": journey_events,
            "struggle_events": [e[0] for e in struggle_events]
        }
        
        with open('event_analysis.json', 'w') as f:
            json.dump(analysis, f, indent=2)
            
        print("\nDetailed analysis saved to event_analysis.json")
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing events: {str(e)}")
        return False

if __name__ == "__main__":
    analyze_event_patterns() 