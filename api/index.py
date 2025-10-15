from flask import Flask, request, jsonify, render_template
import os
import sys

# Add the parent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

try:
    from classifiers.question_classifier import classify_question
    from solvers.trigonometry import solve_trigonometry
    from solvers.interest import solve_interest
except ImportError:
    # Try relative imports
    import importlib.util
    
    def load_module(module_path, module_name):
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    
    classifiers_dir = os.path.join(parent_dir, 'classifiers')
    solvers_dir = os.path.join(parent_dir, 'solvers')
    
    classifier_module = load_module(os.path.join(classifiers_dir, 'question_classifier.py'), 'question_classifier')
    trig_module = load_module(os.path.join(solvers_dir, 'trigonometry.py'), 'trigonometry')
    interest_module = load_module(os.path.join(solvers_dir, 'interest.py'), 'interest')
    
    classify_question = classifier_module.classify_question
    solve_trigonometry = trig_module.solve_trigonometry
    solve_interest = interest_module.solve_interest

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/solve', methods=['POST'])
def solve_question():
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        # Classify the question
        question_type = classify_question(question)
        
        # Solve based on type
        if question_type == 'trigonometry':
            solution_data = solve_trigonometry(question)
            template_name = 'trigonometry.html'
        elif question_type == 'compound_interest':
            solution_data = solve_interest(question)
            template_name = 'compound_interest.html'
        else:
            return jsonify({'error': 'Unsupported question type'}), 400
        
        # Render template with solution data
        rendered_html = render_template(template_name, **solution_data)
        
        return jsonify({
            'question_type': question_type,
            'solution_html': rendered_html
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel serverless function handler
def handler(request):
    with app.app_context():
        response = app.full_dispatch_request()
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.get_data(as_text=True)
        }