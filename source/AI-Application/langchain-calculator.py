from langchain.tools import tool
 
@tool
def salary_calculator(data: str) -> str:
    """
    Use this tool to calculate employee salary.
    
    Input format:
    monthly_salary,working_days,bonus,deductions
    
    Example:
    30000,26,5000,2000
    """
    try:
        monthly_salary, working_days, bonus, deductions = map(float, data.split(","))
 
        per_day_salary = monthly_salary / 30
        earned_salary = per_day_salary * working_days
        net_salary = earned_salary + bonus - deductions
 
        return (
            f"Monthly Salary: ₹{monthly_salary}\n"
            f"Working Days: {working_days}\n"
            f"Per Day Salary: ₹{per_day_salary:.2f}\n"
            f"Earned Salary: ₹{earned_salary:.2f}\n"
            f"Bonus: ₹{bonus}\n"
            f"Deductions: ₹{deductions}\n"
            f"Net Salary: ₹{net_salary:.2f}"
        )
 
    except Exception as e:
        return f"Error: {str(e)}"