import os
import mixpanel
from datetime import datetime, timedelta

def test_mixpanel_connection():
    """Test Mixpanel connection and data access"""
    try:
        # Initialize Mixpanel client
        project_token = os.getenv("MIXPANEL_TOKEN")
        if not project_token:
            print("❌ Error: MIXPANEL_TOKEN environment variable not set")
            return False
            
        client = mixpanel.Mixpanel(project_token)
        
        # Test basic query
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)
        
        # Simple JQL query to test access
        query = """
        function main() {
            return Events({
                from_date: '2024-01-01',
                to_date: '2024-01-02',
                limit: 1
            });
        }
        """
        
        result = client.query("jql", {"script": query})
        print("✅ Successfully connected to Mixpanel")
        print(f"Sample data: {result[:1] if result else 'No data found'}")
        return True
        
    except Exception as e:
        print(f"❌ Error connecting to Mixpanel: {str(e)}")
        return False

if __name__ == "__main__":
    test_mixpanel_connection() 