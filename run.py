#!/usr/bin/env python3
"""
Kambel Consult Website Runner
This script starts the Flask application with proper configuration.
"""

import os
import sys
from app import app

def main():
    """Main function to run the application"""
    # Set environment variables
    os.environ.setdefault('FLASK_ENV', 'development')
    os.environ.setdefault('FLASK_DEBUG', '1')
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    print("=" * 50)
    print("Kambel Consult Website")
    print("=" * 50)
    print("Starting Flask application...")
    print("Website will be available at: http://localhost:5001")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Run the Flask application
        app.run(
            host='0.0.0.0',
            port=5001,
            debug=True,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n" + "=" * 50)
        print("Server stopped by user")
        print("=" * 50)
        sys.exit(0)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
