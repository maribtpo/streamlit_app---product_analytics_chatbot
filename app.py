from flask import Flask, render_template, jsonify, request, send_from_directory
import json
from datetime import datetime, timedelta
import speech_recognition as sr
from gtts import gTTS
import os
import re
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static')

# Ensure static/audio directory exists
os.makedirs('static/audio', exist_ok=True)

# Load events data
try:
    with open('events-export-3632652-1742487314667.json', 'r') as f:
        events = json.load(f)
except FileNotFoundError:
    logger.warning("Events file not found. Using empty events list.")
    events = []

# Conversation states
conversation_states = {}

def convert_webm_to_wav(webm_path, wav_path):
    """Convert WebM audio to WAV using ffmpeg"""
    try:
        subprocess.run([
            'ffmpeg', '-i', webm_path,
            '-acodec', 'pcm_s16le',
            '-ar', '44100',
            '-ac', '1',
            wav_path
        ], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error converting audio: {e.stderr.decode()}")
        return False

def analyze_user_context(user_events):
    """Analyze user's behavior to understand their context and struggles"""
    context = {
        'feature_attempts': {},
        'last_actions': [],
        'time_spent': {},
        'error_events': [],
        'navigation_pattern': []
    }
    
    # Sort events by time
    sorted_events = sorted(user_events, key=lambda x: x['properties']['time'])
    
    for event in sorted_events:
        event_name = event['event']
        properties = event['properties']
        
        # Track feature attempts
        if event_name.startswith('feature_'):
            feature = event_name.replace('feature_', '')
            if feature not in context['feature_attempts']:
                context['feature_attempts'][feature] = 0
            context['feature_attempts'][feature] += 1
        
        # Track last actions
        context['last_actions'].append({
            'event': event_name,
            'time': properties['time'],
            'properties': properties
        })
        
        # Track error events
        if 'error' in event_name.lower() or 'failed' in event_name.lower():
            context['error_events'].append(event)
        
        # Track navigation
        if event_name == 'page_view' or event_name == 'screen_view':
            context['navigation_pattern'].append({
                'screen': properties.get('screen_name', 'unknown'),
                'time': properties['time']
            })
    
    # Keep only last 10 actions
    context['last_actions'] = context['last_actions'][-10:]
    
    return context

def detect_stuck_users():
    # Group events by user
    user_events = {}
    for event in events:
        user_id = event['properties']['distinct_id']
        if user_id not in user_events:
            user_events[user_id] = []
        user_events[user_id].append(event)
    
    # Find stuck users with context
    stuck_users = []
    for user_id, user_events_list in user_events.items():
        app_opens = [e for e in user_events_list if e['event'] == 'app open']
        feature_uses = [e for e in user_events_list if e['event'] == 'favorite sandwich']
        
        if len(app_opens) >= 5 and len(feature_uses) == 0:
            # Analyze user context
            context = analyze_user_context(user_events_list)
            
            # Determine what they're trying to do
            struggling_with = determine_struggle(context)
            
            stuck_users.append({
                'user_id': user_id,
                'app_opens': len(app_opens),
                'last_event': max(user_events_list, key=lambda x: x['properties']['time']),
                'context': context,
                'struggling_with': struggling_with
            })
    
    return stuck_users

def determine_struggle(context):
    """Determine what the user is struggling with based on their behavior"""
    struggles = []
    
    # Check for repeated feature attempts
    for feature, attempts in context['feature_attempts'].items():
        if attempts >= 3:
            struggles.append(f"repeated_attempts_{feature}")
    
    # Check for error patterns
    if len(context['error_events']) >= 2:
        struggles.append("frequent_errors")
    
    # Check navigation patterns
    if len(context['navigation_pattern']) >= 3:
        # Look for back-and-forth navigation
        screens = [n['screen'] for n in context['navigation_pattern']]
        if len(set(screens)) >= 3 and len(screens) >= 5:
            struggles.append("confused_navigation")
    
    # Check time spent on specific screens
    for screen, time in context['time_spent'].items():
        if time > 300:  # More than 5 minutes
            struggles.append(f"long_time_{screen}")
    
    return struggles

def generate_response(user_text, user_id, context=None):
    """Generate a contextual response based on user's behavior"""
    # Initialize conversation state if not exists
    if user_id not in conversation_states:
        conversation_states[user_id] = {
            'stage': 'initial',
            'context': context
        }
    
    state = conversation_states[user_id]
    
    # Convert to lowercase for easier matching
    text = user_text.lower()
    
    # Use context to personalize the response
    if context and state['context']:
        struggles = state['context'].get('struggling_with', [])
        
        if 'repeated_attempts_favorite_sandwich' in struggles:
            return "I notice you've tried to use the favorite sandwich feature several times. Let me help you with that. What specific part are you finding difficult?"
        elif 'frequent_errors' in struggles:
            return "I see you've encountered some errors. Let me help you avoid those. Could you tell me what you're trying to do?"
        elif 'confused_navigation' in struggles:
            return "I notice you've been looking around different screens. Let me help you find what you're looking for. What are you trying to accomplish?"
        elif 'long_time_sandwich_builder' in struggles:
            return "I see you've spent some time in the sandwich builder. Would you like help saving your creation as a favorite?"
    
    # Fall back to the original conversation flow if no specific context
    if state['stage'] == 'initial':
        # Check for common issues
        if any(word in text for word in ['help', 'stuck', 'confused', 'how', 'what']):
            state['stage'] = 'help_needed'
            return "I understand you need help. Could you tell me what you're trying to do with the favorite sandwich feature?"
        elif any(word in text for word in ['don\'t know', 'not sure', 'explain']):
            state['stage'] = 'explanation_needed'
            return "Let me explain how the favorite sandwich feature works. You can save your favorite sandwich combinations to quickly reorder them later. Would you like me to show you how to use it?"
        else:
            state['stage'] = 'clarification_needed'
            return "I'm not sure I understand. Are you having trouble finding the favorite sandwich feature, or would you like to know more about how it works?"
    
    elif state['stage'] == 'help_needed':
        if any(word in text for word in ['save', 'remember', 'store']):
            state['stage'] = 'tutorial'
            return "Great! To save a sandwich as your favorite, first customize your sandwich, then look for the heart icon. Click it to save your creation. Would you like me to guide you through this process?"
        else:
            return "Could you be more specific about what you're trying to do? Are you trying to save a sandwich, find your saved sandwiches, or something else?"
    
    elif state['stage'] == 'explanation_needed':
        if any(word in text for word in ['yes', 'sure', 'okay', 'show']):
            state['stage'] = 'tutorial'
            return "Perfect! Let's start by creating your first favorite sandwich. First, go to the sandwich builder. Can you see that option on your screen?"
        else:
            state['stage'] = 'initial'
            return "No problem! Let me know if you change your mind and want to learn more about the favorite sandwich feature."
    
    elif state['stage'] == 'clarification_needed':
        if any(word in text for word in ['find', 'where', 'location']):
            state['stage'] = 'location_help'
            return "The favorite sandwich feature is located in the sandwich builder. Look for the heart icon at the top of the screen. Can you see it?"
        else:
            state['stage'] = 'initial'
            return "I understand. If you need help with the favorite sandwich feature in the future, just let me know!"
    
    elif state['stage'] == 'tutorial':
        if any(word in text for word in ['yes', 'see', 'found']):
            state['stage'] = 'next_step'
            return "Great! Now, customize your sandwich as you like. Once you're happy with your creation, look for the heart icon and click it to save. Let me know when you've done that!"
        else:
            return "Take your time to find the sandwich builder. It should be on the main menu. Can you see it?"
    
    elif state['stage'] == 'next_step':
        if any(word in text for word in ['done', 'finished', 'saved']):
            state['stage'] = 'complete'
            return "Excellent! You've successfully saved your favorite sandwich. You can find it anytime by clicking the 'Favorites' tab. Is there anything else you'd like to know?"
        else:
            return "No rush! Let me know when you've saved your sandwich, and I'll help you with the next step."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stuck-users')
def get_stuck_users():
    stuck_users = detect_stuck_users()
    return jsonify(stuck_users)

@app.route('/api/start-conversation', methods=['POST'])
def start_conversation():
    try:
        user_id = request.json.get('user_id')
        # Generate speech
        text = "I notice you haven't used the favorite sandwich feature yet. What are you trying to do?"
        tts = gTTS(text=text, lang='en')
        tts.save('static/audio/initial_message.mp3')
        return jsonify({'status': 'success'})
    except Exception as e:
        logger.error(f"Error in start_conversation: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/process-voice', methods=['POST'])
def process_voice():
    try:
        # Get audio file from request
        audio_file = request.files['audio']
        user_id = request.form.get('user_id', 'default_user')
        
        # Save WebM audio temporarily
        webm_path = 'temp_audio.webm'
        wav_path = 'temp_audio.wav'
        audio_file.save(webm_path)
        logger.debug(f"Saved WebM audio to {webm_path}")
        
        # Convert WebM to WAV
        if not convert_webm_to_wav(webm_path, wav_path):
            return jsonify({'error': 'Could not process audio format. Please try again.'})
        
        # Convert speech to text
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            # Adjust for ambient noise
            logger.debug("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            # Record audio
            logger.debug("Recording audio...")
            audio = recognizer.record(source)
            
            try:
                text = recognizer.recognize_google(audio)
                logger.debug(f"Recognized text: {text}")
                
                # Generate response
                response = generate_response(text, user_id)
                
                # Convert response to speech
                tts = gTTS(text=response, lang='en')
                tts.save('static/audio/response.mp3')
                
                # Clean up
                os.remove(webm_path)
                os.remove(wav_path)
                return jsonify({
                    'text': text,
                    'response': response
                })
            except sr.UnknownValueError:
                logger.error("Speech recognition failed - could not understand audio")
                return jsonify({'error': 'Could not understand audio. Please try speaking more clearly.'})
            except sr.RequestError as e:
                logger.error(f"Speech recognition service error: {str(e)}")
                return jsonify({'error': 'There was an error with the speech recognition service. Please try again.'})
            except Exception as e:
                logger.error(f"Unexpected error in speech recognition: {str(e)}")
                return jsonify({'error': 'An unexpected error occurred. Please try again.'})
    except Exception as e:
        logger.error(f"Error in process_voice: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/static/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory('static/audio', filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 