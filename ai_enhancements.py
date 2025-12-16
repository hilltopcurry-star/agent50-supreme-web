# ai_enhancements.py
from flask import Flask, jsonify
from ml_integration import MLIntegration, setup_ml_routes
from nlp_processor import NLPProcessor, setup_nlp_routes
from computer_vision import ComputerVision, setup_cv_routes
from predictive_analytics import PredictiveAnalytics, setup_analytics_routes
from ai_code_generator import AICodeGenerator, setup_ai_code_routes

class AIEnhancements:
    def __init__(self, app):
        self.app = app
        self.ml_system = MLIntegration()
        self.nlp_processor = NLPProcessor()
        self.cv_system = ComputerVision()
        self.analytics_system = PredictiveAnalytics()
        self.ai_code_system = AICodeGenerator()
        
        self.setup_all_routes()
    
    def setup_all_routes(self):
        """Setup all AI enhancement routes"""
        setup_ml_routes(self.app, self.ml_system)
        setup_nlp_routes(self.app, self.nlp_processor)
        setup_cv_routes(self.app, self.cv_system)
        setup_analytics_routes(self.app, self.analytics_system)
        setup_ai_code_routes(self.app, self.ai_code_system)
        
        # AI Status endpoint
        @self.app.route('/api/ai/status')
        def ai_status():
            return jsonify({
                'ai_enhancements': {
                    'machine_learning': 'active',
                    'natural_language_processing': 'active',
                    'computer_vision': 'active',
                    'predictive_analytics': 'active',
                    'ai_code_generation': 'active'
                },
                'status': 'KING DEEPSEEK AI Enhancements Ready!'
            })

def setup_ai_enhancements(app):
    """Initialize AI enhancements for the app"""
    ai_system = AIEnhancements(app)
    return ai_system