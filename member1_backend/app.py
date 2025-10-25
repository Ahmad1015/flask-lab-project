"""
Flask Web Application for Lab 8 - Collaborative Development
Backend API Routes Implementation

This application provides the core backend functionality with:
- Homepage route (/)
- Health check route (/health)
- Data submission endpoint (/data)
"""

from flask import Flask, request, jsonify, render_template
from datetime import datetime
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# In-memory storage for demonstration (in production, use a database)
data_store = []

@app.route('/', methods=['GET'])
def homepage():
    """
    Homepage route - Returns welcome message and basic app info
    """
    try:
        app_info = {
            'app_name': 'Flask Lab Project',
            'version': '1.0.0',
            'description': 'Collaborative Flask Application with CI/CD & Docker',
            'team_members': ['Backend Lead', 'Frontend/API Integration', 'DevOps Engineer'],
            'timestamp': datetime.now().isoformat(),
            'endpoints': {
                'GET /': 'Homepage with app information',
                'GET /health': 'Health check endpoint',
                'POST /data': 'Submit data to the application',
                'GET /data': 'Retrieve all submitted data'
            }
        }
        
        # Return JSON for API clients or render template for browsers
        if request.headers.get('Accept') == 'application/json':
            return jsonify(app_info)
        else:
            return jsonify(app_info)  # For now, always return JSON
            
    except Exception as e:
        logger.error(f"Error in homepage route: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint - Returns service status hello how are you
    """
    try:
        health_status = {
            'status': 'OK',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'service': 'Flask Backend'
        }
        return jsonify(health_status), 200
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        return jsonify({'status': 'ERROR', 'message': str(e)}), 500

@app.route('/data', methods=['POST'])
def submit_data():
    """
    Data submission endpoint - Accepts JSON data and stores it
    """
    try:
        # Check if request contains JSON data
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json()
        
        # Validate that data is not None/empty
        if data is None:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Add metadata to the data entry
        entry_id = len(data_store) + 1
        data_entry = {
            'id': entry_id,
            'data': data,
            'timestamp': datetime.now().isoformat(),
            'ip_address': request.remote_addr
        }
        
        # Store the data
        data_store.append(data_entry)
        
        logger.info(f"Data submitted successfully: Entry ID {entry_id}")
        
        response = {
            'message': 'Data submitted successfully',
            'entry_id': entry_id,
            'data_received': data,
            'timestamp': data_entry['timestamp']
        }
        
        return jsonify(response), 201
        
    except Exception as e:
        logger.error(f"Error submitting data: {str(e)}")
        return jsonify({'error': 'Failed to submit data'}), 400

@app.route('/data', methods=['GET'])
def get_all_data():
    """
    Data retrieval endpoint - Returns all stored data
    """
    try:
        response = {
            'total_entries': len(data_store),
            'data': data_store,
            'timestamp': datetime.now().isoformat()
        }
        return jsonify(response), 200
    except Exception as e:
        logger.error(f"Error retrieving data: {str(e)}")
        return jsonify({'error': 'Failed to retrieve data'}), 500

@app.route('/data/<int:entry_id>', methods=['GET'])
def get_data_by_id(entry_id):
    """
    Get specific data entry by ID
    """
    try:
        # Find the entry with the specified ID
        entry = next((item for item in data_store if item['id'] == entry_id), None)
        
        if entry is None:
            return jsonify({'error': 'Data entry not found'}), 404
            
        return jsonify(entry), 200
        
    except Exception as e:
        logger.error(f"Error retrieving data by ID {entry_id}: {str(e)}")
        return jsonify({'error': 'Failed to retrieve data'}), 500

@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors
    """
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors
    """
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Development server configuration
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Flask application on port {port}")
    logger.info(f"Debug mode: {debug_mode}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )