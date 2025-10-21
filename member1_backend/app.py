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
            return jsonify(app_info), 200  # For now return JSON, frontend team will add templates
            
    except Exception as e:
        logger.error(f"Error in homepage route: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint - Returns application health status
    Used by load balancers and monitoring systems
    """
    try:
        health_status = {
            'status': 'OK',
            'timestamp': datetime.now().isoformat(),
            'uptime': 'Running',
            'version': '1.0.0',
            'database_status': 'Connected',  # Placeholder for database connection
            'memory_usage': 'Normal',
            'disk_space': 'Available'
        }
        
        logger.info("Health check performed successfully")
        return jsonify(health_status), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'ERROR',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/data', methods=['POST'])
def submit_data():
    """
    POST endpoint for data submission
    Accepts JSON data and stores it (in-memory for now)
    """
    try:
        # Validate request content type
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type must be application/json',
                'received': request.content_type
            }), 400
        
        # Get JSON data from request
        submitted_data = request.get_json()
        
        # Validate that data exists
        if not submitted_data:
            return jsonify({'error': 'No data provided in request body'}), 400
        
        # Create data entry with metadata
        data_entry = {
            'id': len(data_store) + 1,
            'data': submitted_data,
            'timestamp': datetime.now().isoformat(),
            'source_ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', 'Unknown')
        }
        
        # Store data (in production, this would go to a database)
        data_store.append(data_entry)
        
        # Log successful data submission
        logger.info(f"Data submitted successfully. Entry ID: {data_entry['id']}")
        
        # Return success response with created data
        return jsonify({
            'message': 'Data submitted successfully',
            'entry_id': data_entry['id'],
            'timestamp': data_entry['timestamp'],
            'data_received': submitted_data
        }), 201
        
    except Exception as e:
        logger.error(f"Error in data submission: {str(e)}")
        return jsonify({
            'error': 'Failed to process data submission',
            'details': str(e)
        }), 500

@app.route('/data', methods=['GET'])
def get_data():
    """
    GET endpoint to retrieve all submitted data
    Returns all stored data entries
    """
    try:
        # Return all stored data with metadata
        response_data = {
            'total_entries': len(data_store),
            'data': data_store,
            'retrieved_at': datetime.now().isoformat()
        }
        
        logger.info(f"Data retrieved successfully. Total entries: {len(data_store)}")
        return jsonify(response_data), 200
        
    except Exception as e:
        logger.error(f"Error retrieving data: {str(e)}")
        return jsonify({
            'error': 'Failed to retrieve data',
            'details': str(e)
        }), 500

@app.route('/data/<int:entry_id>', methods=['GET'])
def get_data_by_id(entry_id):
    """
    GET endpoint to retrieve specific data entry by ID
    """
    try:
        # Find entry by ID
        entry = next((item for item in data_store if item['id'] == entry_id), None)
        
        if not entry:
            return jsonify({
                'error': 'Data entry not found',
                'entry_id': entry_id
            }), 404
        
        logger.info(f"Data entry {entry_id} retrieved successfully")
        return jsonify(entry), 200
        
    except Exception as e:
        logger.error(f"Error retrieving data entry {entry_id}: {str(e)}")
        return jsonify({
            'error': 'Failed to retrieve data entry',
            'details': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested URL was not found on the server',
        'available_endpoints': [
            'GET /',
            'GET /health',
            'POST /data',
            'GET /data',
            'GET /data/<id>'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred on the server'
    }), 500

if __name__ == '__main__':
    # Development server configuration
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    logger.info(f"Starting Flask application on port {port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(
        host='0.0.0.0',  # Allow external connections
        port=port,
        debug=debug
    )