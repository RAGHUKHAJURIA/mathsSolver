import re
import math

def solve_interest(question):
    """
    Solve compound interest problems dynamically
    """
    question_lower = question.lower()
    print(f"DEBUG: Processing question: {question}")
    
    # Extract values
    principal = extract_principal(question)
    amount = extract_amount(question)
    time_years = extract_time(question)
    rate = extract_rate(question)
    
    print(f"DEBUG: Extracted - P: {principal}, A: {amount}, T: {time_years}, R: {rate}")
    
    # Determine what to calculate
    if principal and amount and time_years and not rate:
        # Find rate
        print("DEBUG: Finding rate...")
        rate = calculate_rate(principal, amount, time_years)
        amount_2_years = calculate_amount(principal, rate, 2)
        solution = prepare_rate_solution(principal, amount, time_years, rate, amount_2_years)
        print(f"DEBUG: Rate solution keys: {list(solution.keys())}")
        return solution
    
    elif principal and rate and time_years and not amount:
        # Find amount
        print("DEBUG: Finding amount...")
        amount = calculate_amount(principal, rate, time_years)
        ci = amount - principal
        amount_2_years = calculate_amount(principal, rate, 2)
        solution = prepare_ci_solution(principal, rate, time_years, amount, ci, amount_2_years)
        print(f"DEBUG: CI solution keys: {list(solution.keys())}")
        return solution
    
    elif amount and rate and time_years and not principal:
        # Find principal
        print("DEBUG: Finding principal...")
        principal = calculate_principal(amount, rate, time_years)
        amount_2_years = calculate_amount(principal, rate, 2)
        solution = prepare_principal_solution(principal, amount, rate, time_years, amount_2_years)
        print(f"DEBUG: Principal solution keys: {list(solution.keys())}")
        return solution
    
    else:
        print(f"DEBUG: Insufficient data - P:{principal}, A:{amount}, T:{time_years}, R:{rate}")
        return create_default_solution(error='Unable to extract sufficient information from question')


def create_default_solution(**kwargs):
    """Create a solution dictionary with all required keys"""
    solution = {
        'principal': '0',
        'time_years': '0',
        'amount': '0',
        'ci': '0',
        'rate': '0',
        'rate_percent': '0',
        'final_rate': '0%',
        'fraction_step1': '1/1',
        'fraction_step2': '1/1',
        'cube_root_num': '1',
        'cube_root_den': '1',
        'cube_root_num_cubed': '1',
        'cube_root_den_cubed': '1',
        'rate_calc': '0/1',
        'amount_2_years': '0'
    }
    solution.update(kwargs)  # Add any additional keys like 'error'
    return solution


def extract_principal(question):
    """Extract principal with better patterns"""
    patterns = [
        r'₹\s*(\d+(?:,\d+)*)\s+becomes',
        r'principal\s*(?:of|is|:|=)?\s*(?:₹|rs\.?|rupees?)?\s*(\d+(?:,\d+)*)',
        r'sum\s*(?:of|is|:|=)?\s*(?:₹|rs\.?|rupees?)?\s*(\d+(?:,\d+)*)',
        r'invest(?:ed|s)?\s*(?:₹|rs\.?)?\s*(\d+(?:,\d+)*)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, question.lower())
        if match:
            num = match.group(1).replace(',', '')
            return float(num)
    
    return None


def extract_amount(question):
    """Extract final amount"""
    patterns = [
        r'becomes\s*(?:₹|rs\.?)?\s*(\d+(?:,\d+)*)',
        r'(?:grows to|amounts to)\s*(?:₹|rs\.?)?\s*(\d+(?:,\d+)*)',
        r'final\s*amount\s*(?:is|:|=)?\s*(?:₹|rs\.?)?\s*(\d+(?:,\d+)*)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, question.lower())
        if match:
            num = match.group(1).replace(',', '')
            return float(num)
    
    return None


def extract_time(question):
    """Extract time period"""
    patterns = [
        r'(?:in|after|for)\s*(\d+)\s*years?',
        r'(\d+)\s*years?'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, question.lower())
        if match:
            return int(match.group(1))
    
    return None


def extract_rate(question):
    """Extract interest rate"""
    patterns = [
        r'(\d+(?:\.\d+)?)\s*%',
        r'rate\s*(?:of|is|:|=)?\s*(\d+(?:\.\d+)?)',
        r'(\d+(?:\.\d+)?)\s*percent'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, question.lower())
        if match:
            return float(match.group(1))
    
    return None


def calculate_amount(principal, rate, time):
    """Calculate compound amount: A = P(1 + r/100)^t"""
    return principal * ((1 + rate/100) ** time)


def calculate_rate(principal, amount, time):
    """Calculate rate: r = ((A/P)^(1/t) - 1) * 100"""
    return ((amount / principal) ** (1/time) - 1) * 100


def calculate_principal(amount, rate, time):
    """Calculate principal: P = A / (1 + r/100)^t"""
    return amount / ((1 + rate/100) ** time)


def safe_fraction_string(numerator, denominator):
    """Safely create fraction string"""
    try:
        num_int = int(round(float(numerator)))
        den_int = int(round(float(denominator)))
        
        if den_int == 0:
            return "1/1", "1/1"
        
        gcd_val = math.gcd(abs(num_int), abs(den_int))
        simplified_num = num_int // gcd_val
        simplified_den = den_int // gcd_val
        
        return f"{num_int}/{den_int}", f"{simplified_num}/{simplified_den}"
    except:
        return "1/1", "1/1"


def prepare_rate_solution(principal, amount, time_years, rate, amount_2_years):
    """Prepare solution for rate finding"""
    # Start with default solution
    solution = create_default_solution()
    
    # Update with actual values
    solution['principal'] = str(int(principal))
    solution['time_years'] = str(time_years)
    solution['amount'] = str(int(amount))
    solution['ci'] = str(int(amount - principal))
    solution['rate'] = str(int(rate)) if rate == int(rate) else f"{rate:.2f}"
    solution['rate_percent'] = f"{rate:.2f}"
    solution['final_rate'] = f"{rate:.2f}%"
    solution['amount_2_years'] = str(int(round(amount_2_years)))
    
    try:
        fraction_step1, fraction_step2 = safe_fraction_string(amount, principal)
        solution['fraction_step1'] = fraction_step1
        solution['fraction_step2'] = fraction_step2
        
        growth_factor = amount / principal
        root_value = growth_factor ** (1/time_years)
        
        best_num, best_den = 1, 1
        min_error = float('inf')
        for den in range(1, 100):
            num = round(root_value * den)
            if num > 0 and den > 0:
                error = abs(root_value - num/den)
                if error < min_error:
                    min_error = error
                    best_num, best_den = num, den
        
        solution['cube_root_num'] = str(best_num)
        solution['cube_root_den'] = str(best_den)
        solution['cube_root_num_cubed'] = str(best_num ** time_years)
        solution['cube_root_den_cubed'] = str(best_den ** time_years)
        solution['rate_calc'] = f"{best_num - best_den}/{best_den}"
    except Exception as e:
        print(f"DEBUG: Error in calculations: {e}")
    
    return solution


def prepare_ci_solution(principal, rate, time_years, amount, ci, amount_2_years):
    """Prepare CI calculation solution"""
    solution = create_default_solution()
    
    solution['principal'] = str(int(principal))
    solution['time_years'] = str(time_years)
    solution['rate_percent'] = f"{rate:.2f}"
    solution['rate'] = str(int(rate)) if rate == int(rate) else f"{rate:.2f}"
    solution['amount'] = str(int(round(amount)))
    solution['ci'] = str(int(round(ci)))
    solution['amount_2_years'] = str(int(round(amount_2_years)))
    solution['final_rate'] = f"{rate:.2f}%"
    
    try:
        fraction_step1, fraction_step2 = safe_fraction_string(amount, principal)
        solution['fraction_step1'] = fraction_step1
        solution['fraction_step2'] = fraction_step2
        solution['cube_root_num'] = str(int(100 + rate))
        solution['cube_root_den'] = '100'
        solution['cube_root_num_cubed'] = str(int((100 + rate) ** time_years))
        solution['cube_root_den_cubed'] = str(100 ** time_years)
        solution['rate_calc'] = f"{int(rate)}/100"
    except Exception as e:
        print(f"DEBUG: Error in calculations: {e}")
    
    return solution


def prepare_principal_solution(principal, amount, rate, time_years, amount_2_years):
    """Prepare principal finding solution"""
    solution = create_default_solution()
    
    solution['principal'] = str(int(round(principal)))
    solution['time_years'] = str(time_years)
    solution['rate_percent'] = f"{rate:.2f}"
    solution['rate'] = str(int(rate)) if rate == int(rate) else f"{rate:.2f}"
    solution['amount'] = str(int(amount))
    solution['ci'] = str(int(amount - principal))
    solution['amount_2_years'] = str(int(round(amount_2_years)))
    solution['final_rate'] = f"{rate:.2f}%"
    
    try:
        fraction_step1, fraction_step2 = safe_fraction_string(amount, principal)
        solution['fraction_step1'] = fraction_step1
        solution['fraction_step2'] = fraction_step2
        
        growth_factor = 1 + rate/100
        
        best_num, best_den = 1, 1
        min_error = float('inf')
        for den in range(1, 100):
            num = round(growth_factor * den)
            if num > 0 and den > 0:
                error = abs(growth_factor - num/den)
                if error < min_error:
                    min_error = error
                    best_num, best_den = num, den
        
        solution['cube_root_num'] = str(best_num)
        solution['cube_root_den'] = str(best_den)
        solution['cube_root_num_cubed'] = str(best_num ** time_years)
        solution['cube_root_den_cubed'] = str(best_den ** time_years)
        solution['rate_calc'] = f"{best_num - best_den}/{best_den}"
    except Exception as e:
        print(f"DEBUG: Error in calculations: {e}")
    
    return solution
