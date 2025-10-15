from flask import Flask, request, jsonify, render_template
from classifiers.question_classifier import classify_question
from solvers.trigonometry import solve_trigonometry
from solvers.interest import solve_interest

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
        
        print(f"PROCESSING QUESTION: {question}")
        
        # Classify the question
        question_type = classify_question(question)
        print(f"CLASSIFIED AS: {question_type}")
        
        # Solve based on type
        if question_type == 'trigonometry':
            solution_data = solve_trigonometry(question)
            template_name = 'trigonometry.html'
        elif question_type == 'compound_interest':
            solution_data = solve_interest(question)
            template_name = 'compound_interest.html'
        else:
            return jsonify({'error': 'Unsupported question type'}), 400
        
        print(f"SOLUTION DATA: {solution_data}")
        
        # Render template with solution data
        rendered_html = render_template(template_name, **solution_data)
        
        return jsonify({
            'question_type': question_type,
            'solution_html': rendered_html
        })
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# Vercel requires this
if __name__ == '__main__':
    app.run(debug=True)