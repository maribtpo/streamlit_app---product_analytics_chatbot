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
        project_token = os.getenv("MIXPANEL_TOKEN")
        api_secret = os.getenv("MIXPANEL_API_SECRET")
        
        if not project_token or not api_secret:
            print("❌ Error: Missing Mixpanel credentials")
            return False
            
        # Set up date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        # Query Mixpanel JQL API
        url = "https://mixpanel.com/api/2.0/jql"
        headers = get_auth_header(api_secret)
        
        # JQL query to get event counts
        query = """
        function main() {
            return Events({
                from_date: '%s',
                to_date: '%s'
            })
            .groupBy(["name"], mixpanel.reducer.count());
        }
        """ % (start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
        
        print("Fetching events from Mixpanel...")
        response = requests.post(url, json={"script": query}, headers=headers)
        
        if response.status_code != 200:
            print(f"❌ Error: Failed to fetch data. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
        # Process events
        event_counts = {}
        data = response.json()
        
        for event in data:
            event_name = event['key'][0]
            event_count = event['value']
            event_counts[event_name] = event_count
            
            # Look for potential error or struggle patterns
            if any(word in event_name.lower() for word in ['error', 'fail', 'abandon', 'cancel']):
                print(f"Potential struggle event found: {event_name} (count: {event_count})")
        
        # Print summary
        print("\n=== Event Analysis Summary ===")
        print(f"Total unique events: {len(event_counts)}")
        print("\nTop 10 most frequent events:")
        for event, count in sorted(event_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"- {event}: {count} occurrences")
            
        # Save detailed analysis
        analysis = {
            "total_events": len(event_counts),
            "event_counts": event_counts,
            "potential_struggle_events": [
                event for event in event_counts.keys()
                if any(word in event.lower() for word in ['error', 'fail', 'abandon', 'cancel'])
            ]
        }
        
        with open('event_analysis.json', 'w') as f:
            json.dump(analysis, f, indent=2)
            
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing events: {str(e)}")
        return False

if __name__ == "__main__":
    analyze_event_patterns() 