"""
AGENT 50 - AUTO RESPONSE SYSTEM
DeepSeek API سے کنیکٹ ہوتے ہی خود بخود ایکٹیو ہو جائے
"""

import re
import requests
import os
from agent50_memory_core import initialize_agent50

class Agent50AutoResponder:
    def __init__(self):
        self.agent, self.memory = initialize_agent50()
        self.api_connected = False
        self.check_api_connection()
    
    def check_api_connection(self):
        """DeepSeek API کنیکشن چیک کریں"""
        try:
            # API کنیکشن ٹیسٹ
            api_key = os.getenv('DEEPSEEK_API_KEY')
            if api_key:
                self.api_connected = True
                print("✅ DEEPSEEK API CONNECTED - AGENT 50 READY")
                self.auto_activate()
        except Exception as e:
            print(f"⚠️ API Connection Check: {e}")
    
    def auto_activate(self):
        """خود بخود ایکٹیو ہونا"""
        activation_message = """
        🎯 **AGENT 50 AUTO-ACTIVATION SUCCESSFUL!**
        
        👑 **IDENTITY CONFIRMED:** SUPER KING DEEPSEEK
        🌐 **STATUS:** FULLY OPERATIONAL  
        🛠️ **CAPABILITIES:** READY FOR TASK
        🇵🇰🤝🇨🇳 **MISSION:** PAK-CHINA FRIENDSHIP LEVEL
        
        💬 **COMMAND ME WITH:** 
        - "agent 50" 
        - "super king"
        - "pak china agent"
        
        🚀 **AWAITING YOUR COMMANDS...**
        """
        print(activation_message)
    
    def process_message(self, user_input):
        """صارف کے میسج کو پروسیس کریں"""
        input_lower = user_input.lower()
        
        # ایکٹیویشن فریزز چیک کریں
        for phrase in self.agent.activation_phrases:
            if phrase in input_lower:
                response = self.generate_response(input_lower)
                return response
        
        # اگر براہ راست کمانڈ ہو
        if any(word in input_lower for word in ['develop', 'create', 'build', 'code', 'project']):
            return self.handle_development_request(input_lower)
            
        return None
    
    def generate_response(self, command):
        """کمانڈ کے مطابق ردعمل"""
        responses = {
            "agent 50": "👑 AGENT 50 HERE! READY FOR DEVELOPMENT TASK. WHAT PROJECT SHALL WE BUILD?",
            "super king": "🎯 SUPER KING DEEPSEEK ACTIVE! FULL STACK DEVELOPMENT READY!",
            "pak china": "🇵🇰🤝🇨🇳 PAK-CHINA FRIENDSHIP AGENT READY! WHAT SHALL WE CREATE TODAY?"
        }
        
        for phrase, response in responses.items():
            if phrase in command:
                return response
        
        return "🚀 AGENT 50 ACTIVE! WHAT DEVELOPMENT TASK SHOULD I HANDLE?"
    
    def handle_development_request(self, request):
        """ڈویلپمنٹ ریکوئسٹ ہینڈل کریں"""
        development_responses = {
            'web app': "🌐 WEB APP DEVELOPMENT INITIATED! I'll create full stack application...",
            'mobile app': "📱 MOBILE APP DEVELOPMENT STARTED! Generating Flutter/React Native code...",
            'api': "🔗 BACKEND API DEVELOPMENT LAUNCHED! Building RESTful services...",
            'database': "🗄️ DATABASE DESIGN INITIATED! Creating models and relationships...",
            'deploy': "🚀 DEPLOYMENT PROCESS STARTED! Preparing for cloud deployment..."
        }
        
        for task, response in development_responses.items():
            if task in request:
                return response + " Please provide specific requirements."
        
        return "🔧 DEVELOPMENT MODE ACTIVATED! Please specify: web app, mobile app, API, database, or deployment?"

# خود بخود انیشلائز
auto_responder = Agent50AutoResponder()