import os
import mixpanel
from datetime import datetime, timedelta
import json

def export_sample_events():
    """Export a sample of recent events from Mixpanel"""
    try:
        # Initialize Mixpanel client
        project_token = os.getenv("MIXPANEL_TOKEN")
        if not project_token:
            print("❌ Error: MIXPANEL_TOKEN environment variable not set")
            return False
            
        client = mixpanel.Mixpanel(project_token)
        
        # Get events from the last 7 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        # Query to get a sample of events
        query = """
        function main() {
            return Events({
                from_date: '{start_date}',
                to_date: '{end_date}',
                limit: 100
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
        
        # Save to file
        with open('sample_events.json', 'w') as f:
            json.dump(result, f, indent=2)
            
        print("✅ Successfully exported sample events to sample_events.json")
        print(f"Found {len(result)} unique event types")
        
        # Print event names for quick reference
        print("\nEvent names found:")
        for event in result:
            print(f"- {event['key'][0]}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error exporting events: {str(e)}")
        return False

if __name__ == "__main__":
    export_sample_events() 