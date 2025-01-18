def calculate_reimbursement(data):
    validated_meals = data['meals_validated']
    type_rates = data['type_rates']

    total_reimbursement = 0
    for meal, counts in validated_meals.items():
        free_rate = counts['free'] * type_rates[meal]['free']
        reduced_rate = counts['reduced'] * type_rates[meal]['reduced']
        paid_rate = counts['paid'] * type_rates[meal]['paid']
        total_reimbursement += free_rate + reduced_rate + paid_rate

    return {'total_reimbursement': round(total_reimbursement * 0.85, 2)}
