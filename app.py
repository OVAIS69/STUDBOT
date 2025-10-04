"""
StudBot - AI Learning Companion Backend
Flask API for handling AI responses and quiz data
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import random
import re
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Load AI knowledge base
def load_knowledge_base():
    """Load the AI knowledge base from JSON file"""
    try:
        with open('ai_qa_dataset.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('qa_pairs', [])
    except FileNotFoundError:
        return []

def load_mcq_data():
    """Load MCQ data from JSON file"""
    try:
        with open('ai_mcq_500plus.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('mcqs', [])
    except FileNotFoundError:
        return []

# Load data
knowledge_base = load_knowledge_base()
mcq_data = load_mcq_data()

class AIResponseGenerator:
    """Generate AI responses based on user queries"""
    
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base
        self.response_templates = {
            'greeting': [
                "Hello! I'm StudBot, your AI learning companion. I'm here to help you understand Artificial Intelligence concepts!",
                "Hi there! Welcome to StudBot. I can help you learn about AI, answer your questions, and guide you through your studies.",
                "Greetings! I'm StudBot, your intelligent study partner. What AI topic would you like to explore today?"
            ],
            'help': [
                "I can help you with various AI topics including machine learning, search algorithms, neural networks, and more!",
                "Ask me about any AI concept and I'll provide detailed explanations. You can also take quizzes to test your knowledge!",
                "I'm here to assist with your AI studies. Try asking about specific topics or take a quiz to practice!"
            ],
            'fallback': [
                "That's an interesting question! While I have extensive knowledge about AI, could you be more specific about what aspect you'd like to learn about?",
                "I'd be happy to help you understand that AI concept! Could you provide more details so I can give you a more targeted explanation?",
                "That's a great question about AI! Let me help you understand this better. What specific aspect are you most curious about?"
            ]
        }
    
    def find_best_match(self, query):
        """Find the best matching Q&A pair for the query"""
        query_lower = query.lower()
        best_match = None
        best_score = 0
        
        for qa in self.knowledge_base:
            score = self.calculate_similarity(query_lower, qa['question'].lower())
            if score > best_score:
                best_score = score
                best_match = qa
        
        return best_match, best_score
    
    def calculate_similarity(self, query, question):
        """Calculate similarity between query and question"""
        # Simple keyword matching
        query_words = set(query.split())
        question_words = set(question.split())
        
        if not query_words:
            return 0
        
        intersection = query_words.intersection(question_words)
        return len(intersection) / len(query_words)
    
    def generate_response(self, query):
        """Generate AI response for the given query"""
        # Check for greetings
        if any(word in query.lower() for word in ['hello', 'hi', 'hey', 'greetings']):
            return random.choice(self.response_templates['greeting'])
        
        # Check for help requests
        if any(word in query.lower() for word in ['help', 'what can you do', 'how do you work']):
            return random.choice(self.response_templates['help'])
        
        # Find best matching Q&A
        best_match, score = self.find_best_match(query)
        
        if best_match and score > 0.3:  # Threshold for good match
            return self.format_response(best_match)
        else:
            return self.generate_contextual_response(query)
    
    def format_response(self, qa_pair):
        """Format Q&A pair into a response"""
        response = f"**{qa_pair['question']}**\n\n"
        response += qa_pair['answer']
        
        if qa_pair.get('keywords'):
            response += f"\n\n*Keywords: {', '.join(qa_pair['keywords'])}*"
        
        return response
    
    def generate_contextual_response(self, query):
        """Generate contextual response based on query keywords"""
        query_lower = query.lower()
        
        # AI Definition
        if any(word in query_lower for word in ['what is ai', 'artificial intelligence', 'define ai']):
            return """**What is Artificial Intelligence?**

Artificial Intelligence (AI) is the science and engineering of making intelligent machines, especially intelligent computer programs. It enables computers to perform tasks that typically require human intelligence, including learning, reasoning, problem-solving, perception, and understanding language.

**Key aspects of AI:**
• **Learning**: AI systems can learn from data and experience
• **Reasoning**: Ability to make logical decisions
• **Problem-solving**: Finding solutions to complex problems
• **Perception**: Understanding and interpreting sensory input
• **Language understanding**: Processing and generating human language

AI is transforming various industries and becoming an essential part of modern technology!"""
        
        # Machine Learning
        elif any(word in query_lower for word in ['machine learning', 'ml', 'deep learning']):
            return """**Machine Learning Explained**

Machine Learning is a subset of AI that focuses on algorithms and statistical models that enable computer systems to improve their performance on a specific task through experience, without being explicitly programmed.

**Types of Machine Learning:**
• **Supervised Learning**: Learning with labeled training data
• **Unsupervised Learning**: Finding patterns in data without labels
• **Reinforcement Learning**: Learning through interaction with environment
• **Deep Learning**: Using neural networks with multiple layers

**Applications**: Recommendation systems, image recognition, natural language processing, autonomous vehicles, and much more!"""
        
        # Search Algorithms
        elif any(word in query_lower for word in ['search algorithm', 'search', 'bfs', 'dfs', 'a*']):
            return """**Search Algorithms in AI**

Search algorithms are fundamental techniques for finding solutions to problems by exploring possible states or paths. They're crucial for problem-solving agents.

**Main Types:**
• **Uninformed Search**: No additional information about the problem
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
  - Uniform Cost Search

• **Informed Search**: Uses heuristic information
  - A* Search
  - Greedy Best-First Search

**Applications**: Pathfinding, puzzle solving, game playing, and many other AI applications!"""
        
        # Neural Networks
        elif any(word in query_lower for word in ['neural network', 'neural', 'deep learning', 'neuron']):
            return """**Neural Networks Explained**

Neural Networks are computing systems inspired by biological neural networks. They consist of interconnected nodes (neurons) that process information by responding to external inputs.

**Key Components:**
• **Input Layer**: Receives initial data
• **Hidden Layers**: Process data through weighted connections
• **Output Layer**: Produces final result
• **Weights**: Parameters adjusted during training
• **Activation Functions**: Determine neuron activation

**Deep Learning** uses neural networks with many hidden layers to model complex patterns in data, leading to breakthroughs in computer vision, NLP, and more!"""
        
        else:
            return random.choice(self.response_templates['fallback'])

# Initialize AI response generator
ai_generator = AIResponseGenerator(knowledge_base)

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Generate AI response
        response = ai_generator.generate_response(message)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/quiz/<difficulty>')
def get_quiz(difficulty):
    """Get quiz questions by difficulty"""
    try:
        # Filter questions by difficulty
        filtered_questions = [q for q in mcq_data if q.get('difficulty', 'medium') == difficulty]
        
        # Shuffle and limit to 10 questions
        random.shuffle(filtered_questions)
        quiz_questions = filtered_questions[:10]
        
        if not quiz_questions:
            return jsonify({'error': 'No questions found for this difficulty'}), 404
        
        return jsonify({
            'questions': quiz_questions,
            'total': len(quiz_questions)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/quiz/submit', methods=['POST'])
def submit_quiz():
    """Submit quiz answers and get results"""
    try:
        data = request.get_json()
        answers = data.get('answers', [])
        questions = data.get('questions', [])
        
        if not answers or not questions:
            return jsonify({'error': 'Answers and questions are required'}), 400
        
        # Calculate score
        correct_answers = 0
        results = []
        
        for i, question in enumerate(questions):
            user_answer = answers[i] if i < len(answers) else None
            correct_answer = question.get('correct_answer', '')
            
            is_correct = user_answer == correct_answer
            if is_correct:
                correct_answers += 1
            
            results.append({
                'question_id': question.get('id'),
                'question': question.get('question'),
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'explanation': question.get('explanation', '')
            })
        
        score_percentage = (correct_answers / len(questions)) * 100
        
        return jsonify({
            'score': correct_answers,
            'total': len(questions),
            'percentage': round(score_percentage, 2),
            'results': results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/topics')
def get_topics():
    """Get available AI topics"""
    try:
        topics = list(set([qa.get('category', '') for qa in knowledge_base if qa.get('category')]))
        return jsonify({'topics': sorted(topics)})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Get knowledge base statistics"""
    try:
        stats = {
            'total_questions': len(knowledge_base),
            'total_mcqs': len(mcq_data),
            'categories': len(set([qa.get('category', '') for qa in knowledge_base if qa.get('category')])),
            'last_updated': datetime.now().isoformat()
        }
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search():
    """Search knowledge base"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Search through knowledge base
        results = []
        query_lower = query.lower()
        
        for qa in knowledge_base:
            if (query_lower in qa.get('question', '').lower() or 
                query_lower in qa.get('answer', '').lower() or
                any(query_lower in keyword.lower() for keyword in qa.get('keywords', []))):
                results.append({
                    'id': qa.get('id'),
                    'question': qa.get('question'),
                    'answer': qa.get('answer')[:200] + '...' if len(qa.get('answer', '')) > 200 else qa.get('answer'),
                    'category': qa.get('category'),
                    'keywords': qa.get('keywords', [])
                })
        
        return jsonify({
            'query': query,
            'results': results[:10],  # Limit to 10 results
            'total': len(results)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Copy index.html to templates directory
    if os.path.exists('index.html'):
        import shutil
        shutil.copy('index.html', 'templates/index.html')
    
    print("🤖 StudBot Backend Server Starting...")
    print("📚 Knowledge Base:", len(knowledge_base), "Q&A pairs loaded")
    print("📝 MCQ Database:", len(mcq_data), "questions loaded")
    print("🌐 Server running on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
