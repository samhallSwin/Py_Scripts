import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

def simulate_investment(interest, loan_amount, capital_gains, term, deposit):
    monthly_interest_rate = interest / 100 / 12
    num_payments = term * 12
    principal = loan_amount - deposit

    if monthly_interest_rate == 0:
        monthly_payment = principal / num_payments
    else:
        monthly_payment = principal * (
            monthly_interest_rate * (1 + monthly_interest_rate) ** num_payments
        ) / ((1 + monthly_interest_rate) ** num_payments - 1)

    balance = principal
    total_interest_paid = 0.0
    loan_balance_over_time = []
    months = []

    for month in range(1, num_payments + 1):
        if balance <= 0:
            break
        monthly_interest = balance * monthly_interest_rate
        principal_payment = monthly_payment - monthly_interest
        balance -= principal_payment
        total_interest_paid += monthly_interest
        loan_balance_over_time.append(balance)
        months.append(month)

    property_value_over_time = [
        loan_amount * ((1 + capital_gains / 100) ** (m / 12)) for m in months
    ]
    equity_over_time = [property_value_over_time[i] - loan_balance_over_time[i] for i in range(len(months))]

    final_property_value = property_value_over_time[-1]
    total_capital_gains = final_property_value - loan_amount
    net_gain_loss = total_capital_gains - total_interest_paid

    return {
        "monthly_payment": monthly_payment,
        "interest_paid": total_interest_paid,
        "capital_gains": total_capital_gains,
        "net_gain_loss": net_gain_loss,
        "final_value": final_property_value,
        "loan_balance": loan_balance_over_time,
        "equity": equity_over_time,
        "property_value": property_value_over_time,
        "months": months
    }

def find_break_even_capital_gains(interest, loan_amount, term, deposit):
    lower = 0.0
    upper = 20.0
    tolerance = 0.0001
    max_iter = 100

    for _ in range(max_iter):
        mid = (lower + upper) / 2
        result = simulate_investment(interest, loan_amount, mid, term, deposit)
        diff = result["capital_gains"] - result["interest_paid"]

        if abs(diff) < tolerance:
            return round(mid, 4)

        if diff > 0:
            upper = mid
        else:
            lower = mid

    return round(mid, 4)

def calculate_and_plot_gui():
    try:
        interest = float(entry_interest.get())
        loan_amount = float(entry_loan.get())
        capital_gains = float(entry_gains.get())
        term = int(entry_term.get())
        deposit = float(entry_deposit.get())

        result = simulate_investment(interest, loan_amount, capital_gains, term, deposit)
        inflection_point = find_break_even_capital_gains(interest, loan_amount, term, deposit)

        summary = (
            f"Property Price: ${loan_amount:,.0f}\n"
            f"Deposit: ${deposit:,.0f}\n"
            f"Borrowed: ${loan_amount - deposit:,.0f}\n"
            f"Interest Rate: {interest:.2f}%\n"
            f"Term: {term} years\n"
            f"Monthly Payment: ${result['monthly_payment']:,.0f}\n"
            f"Total Interest Paid: ${result['interest_paid']:,.0f}\n"
            f"Final Property Value: ${result['final_value']:,.0f}\n"
            f"Capital Gains: ${result['capital_gains']:,.0f}\n"
            f"Net Gain/Loss: ${result['net_gain_loss']:,.0f}\n"
            f"Break-even Capital Gain Rate: ~{inflection_point:.2f}%"
        )

        messagebox.showinfo("Investment Summary", summary)

        # Plotting
        plt.figure(figsize=(12, 6))
        plt.plot(result["months"], result["loan_balance"], label="Loan Balance", color='red')
        plt.plot(result["months"], result["property_value"], label="Property Value", color='green')
        plt.plot(result["months"], result["equity"], label="Equity", color='blue')
        plt.title("Property Investment Projection")
        plt.xlabel("Months")
        plt.ylabel("Dollars ($)")
        plt.legend(loc="upper left")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("property_investment_summary.png")
        plt.show()

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric inputs.")

# GUI Setup
root = tk.Tk()
root.title("Property Investment Calculator")

labels = ["Interest Rate (%)", "Property Price ($)", "Capital Gains Rate (%)", "Loan Term (years)", "Deposit ($)"]
entries = []

for i, label_text in enumerate(labels):
    tk.Label(root, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky="e")
    entry = tk.Entry(root)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries.append(entry)

entry_interest, entry_loan, entry_gains, entry_term, entry_deposit = entries

tk.Button(root, text="Calculate and Plot", command=calculate_and_plot_gui).grid(row=6, column=0, columnspan=2, pady=20)

root.mainloop()
