def classify_question(question):
    """Classify question type"""
    question_lower = question.lower()
    
    # Trigonometry indicators
    trig_keywords = ['triangle', 'sec', 'cot', 'sin', 'cos', 'tan', 'cosec', 
                     'right angle', 'pythagoras', 'hypotenuse', 'perpendicular']
    
    # Interest indicators
    interest_keywords = ['interest', 'compound', 'principal', 'rate', 'amount',
                        'compounded', 'annually', 'invested']
    
    trig_score = sum(1 for kw in trig_keywords if kw in question_lower)
    interest_score = sum(1 for kw in interest_keywords if kw in question_lower)
    
    return 'trigonometry' if trig_score > interest_score else 'compound_interest'