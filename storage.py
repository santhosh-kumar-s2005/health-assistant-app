import json
import os
from datetime import datetime

# File to store conversations
STORAGE_FILE = "chat_conversations.json"

def load_conversations():
    """Load existing conversations from file"""
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_conversation(user_id, role, message, timestamp):
    """Save a single message to storage"""
    conversations = load_conversations()
    
    # Find or create user conversation
    user_convo = None
    for convo in conversations:
        if convo['user_id'] == user_id:
            user_convo = convo
            break
    
    if not user_convo:
        user_convo = {
            'user_id': user_id,
            'created_at': datetime.now().isoformat(),
            'messages': []
        }
        conversations.append(user_convo)
    
    # Add new message
    user_convo['messages'].append({
        'role': role,
        'content': message,
        'timestamp': timestamp
    })
    
    # Save back to file
    with open(STORAGE_FILE, 'w') as f:
        json.dump(conversations, f, indent=2)