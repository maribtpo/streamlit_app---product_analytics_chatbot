import os
from mixpanel import Mixpanel
from datetime import datetime, timedelta
import json
from collections import defaultdict

def analyze_event_patterns():
    """Analyze Mixpanel events to identify high-impact AI agent opportunities"""
    try:
        # Initialize Mixpanel client
        project_token = os.getenv("MIXPANEL_TOKEN")
        if not project_token:
            print("❌ Error: MIXPANEL_TOKEN environment variable not set")
            return False
            
        client = Mixpanel(project_token)
        
        # Get events from the last 7 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        # Query to analyze event patterns
        query = """
        function main() {
            return Events({
                from_date: '{start_date}',
                to_date: '{end_date}'
            })
            .groupBy(
                ["name", "properties"],
                mixpanel.reducer.count()
            );
        }
        """.format(
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d")
        )
        
        result = client.query("jql", {"script": query})
        
        # Analyze patterns
        event_counts = defaultdict(int)
        user_sequences = defaultdict(list)
        
        for event in result:
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
            "event_counts": dict(event_counts),
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