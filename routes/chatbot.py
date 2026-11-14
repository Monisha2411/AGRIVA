
from flask import Blueprint, request, jsonify, session, render_template, current_app
from flask_login import login_required, current_user
from models import db
from models.prediction import ChatHistory
from ai_modules.gemini_chat import GeminiChatbot

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')


@chatbot_bp.route('/')
@login_required
def chat():
    """Render chatbot UI."""
    return render_template('chatbot/chat.html')


@chatbot_bp.route('/ask', methods=['POST'])
@login_required
def ask():
    """Handle chatbot interaction and save chat history."""

    data = request.get_json(silent=True)

    if not data or not isinstance(data.get('message'), str) or not data['message'].strip():
        return jsonify({
            'status': 'error',
            'message': 'Please enter a message.'
        }), 400

    user_message = data['message'].strip()

    if 'chat_history' not in session:
        session['chat_history'] = []

    try:
        api_key = current_app.config.get('GROQ_API_KEY')
        model = current_app.config.get('GROQ_MODEL')

        chatbot = GeminiChatbot(api_key=api_key, model=model)

        bot_response = chatbot.get_response(
            user_message,
            history=session['chat_history']
        )

        if not bot_response:
            raise ValueError("The chatbot returned an empty response.")

        # Save conversation to the session
        history = session.get('chat_history', [])
        history.append({
            'role': 'user',
            'content': user_message
        })
        history.append({
            'role': 'model',
            'content': bot_response
        })

        session['chat_history'] = history[-20:]
        session.modified = True

        # Save conversation to the database
        chat_record = ChatHistory(
            user_id=current_user.id,
            user_message=user_message,
            bot_response=bot_response
        )

        db.session.add(chat_record)
        db.session.commit()

        # Confirm database save in terminal
        print(
            f"CHAT SAVED: ID={chat_record.id}, "
            f"USER={current_user.id}"
        )

        return jsonify({
            'status': 'success',
            'response': bot_response
        })

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("Chatbot request failed")

        return jsonify({
            'status': 'error',
            'message': 'Unable to process or save your message. Please try again.'
        }), 500


@chatbot_bp.route('/clear', methods=['POST'])
@login_required
def clear():
    """Clear session chat history."""
    session.pop('chat_history', None)

    return jsonify({
        'status': 'success'
    })
