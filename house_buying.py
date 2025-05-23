import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

manual_actual_payment = False

def calculate_stamp_duty(vic_property_value):
    if vic_property_value <= 25000:
        return 0.014 * vic_property_value
    elif vic_property_value <= 130000:
        return 350 + 0.024 * (vic_property_value - 25000)
    elif vic_property_value <= 960000:
        return 2870 + 0.06 * (vic_property_value - 130000)
    else:
        return 0.055 * vic_property_value

def simulate_required_payment(interest, principal, term):
    monthly_interest_rate = interest / 100 / 12
    num_payments = term * 12
    if monthly_interest_rate == 0:
        return principal / num_payments
    return principal * (
        monthly_interest_rate * (1 + monthly_interest_rate) ** num_payments
    ) / ((1 + monthly_interest_rate) ** num_payments - 1)

def simulate_investment(interest, loan_amount, capital_gains, term, deposit, govt_scheme=False, actual_payment=None, include_stamp_duty=False):
    ownership_fraction = 0.75 if govt_scheme else 1.0
    property_price = loan_amount
    stamp_duty = calculate_stamp_duty(property_price) if include_stamp_duty else 0.0
    dutiable_principal = property_price * ownership_fraction + stamp_duty
    principal = dutiable_principal - deposit

    required_payment = simulate_required_payment(interest, principal, term)
    monthly_payment = max(required_payment, actual_payment or required_payment)

    balance = principal
    total_interest_paid = 0.0
    loan_balance_over_time = []
    months = []

    for month in range(1, term * 12 + 1):
        if balance <= 0:
            break
        monthly_interest = balance * interest / 100 / 12
        principal_payment = monthly_payment - monthly_interest
        if principal_payment <= 0:
            break
        balance -= principal_payment
        total_interest_paid += monthly_interest
        loan_balance_over_time.append(balance)
        months.append(month)

    property_value_over_time = [
        loan_amount * ((1 + capital_gains / 100) ** (m / 12)) for m in months
    ]
    equity_over_time = [
        ownership_fraction * property_value_over_time[i] - loan_balance_over_time[i]
        for i in range(len(months))
    ]

    final_property_value = property_value_over_time[-1]
    your_capital_gains = (final_property_value - loan_amount) * ownership_fraction
    govt_capital_gains = (final_property_value - loan_amount) * (1 - ownership_fraction) if govt_scheme else 0
    net_gain_loss = your_capital_gains - total_interest_paid

    return {
        "monthly_payment": monthly_payment,
        "required_payment": required_payment,
        "interest_paid": total_interest_paid,
        "capital_gains": your_capital_gains,
        "govt_capital_gains": govt_capital_gains,
        "net_gain_loss": net_gain_loss,
        "final_value": final_property_value,
        "loan_balance": loan_balance_over_time,
        "equity": equity_over_time,
        "property_value": property_value_over_time,
        "months": months,
        "stamp_duty": stamp_duty,
        "principal": principal
    }

def update_plot(event=None, force_reset_actual=False):
    global manual_actual_payment

    try:
        interest = float(entry_interest.get())
        loan_amount = float(entry_loan.get())
        capital_gains = float(entry_gains.get())
        term = int(entry_term.get())
        deposit = float(entry_deposit.get())
        govt_scheme = govt_var.get() == 1
        include_stamp_duty = stamp_duty_var.get() == 1
        ownership_fraction = 0.75 if govt_scheme else 1.0
        property_price = loan_amount
        stamp_duty = calculate_stamp_duty(property_price) if include_stamp_duty else 0.0
        dutiable_principal = property_price * ownership_fraction + stamp_duty
        principal = dutiable_principal - deposit
        required_payment = simulate_required_payment(interest, principal, term)

        if force_reset_actual or not manual_actual_payment:
            entry_actual.delete(0, tk.END)
            entry_actual.insert(0, f"{required_payment:.2f}")
            manual_actual_payment = False

        actual_payment = float(entry_actual.get())

        result = simulate_investment(interest, loan_amount, capital_gains, term, deposit, govt_scheme, actual_payment, include_stamp_duty)

        summary = (
            f"Property Price: ${loan_amount:,.0f}\n"
            f"Stamp Duty: ${result['stamp_duty']:,.0f} {'(Included)' if include_stamp_duty else '(Not Included)'}\n"
            f"Deposit: ${deposit:,.0f}\n"
            f"Borrowed: ${result['principal']:,.0f}\n"
            f"Interest Rate: {interest:.2f}%\n"
            f"Term: {term} years\n"
            f"Required Monthly Payment: ${result['required_payment']:,.0f}\n"
            f"Your Monthly Payment: ${result['monthly_payment']:,.0f}\n"
            f"Total Interest Paid: ${result['interest_paid']:,.0f}\n"
            f"Final Property Value: ${result['final_value']:,.0f}\n"
            f"Your Capital Gains: ${result['capital_gains']:,.0f}\n"
            f"{'Govt Capital Gains: $' + format(result['govt_capital_gains'], ',.0f') if govt_scheme else ''}\n"
            f"Net Gain/Loss: ${result['net_gain_loss']:,.0f}"
        )

        text_summary.config(state='normal')
        text_summary.delete("1.0", tk.END)
        text_summary.insert(tk.END, summary)
        text_summary.config(state='disabled')

        plt.clf()
        plt.plot(result["months"], result["loan_balance"], label="Loan Balance", color='red')
        plt.plot(result["months"], result["property_value"], label="Property Value", color='green')
        plt.plot(result["months"], result["equity"], label="Your Equity", color='blue')
        plt.title("Property Investment Projection")
        plt.xlabel("Months")
        plt.ylabel("Dollars ($)")
        plt.legend(loc="upper left")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("property_investment_summary.png")
        plt.pause(0.01)

    except ValueError:
        pass

def on_actual_change(event):
    global manual_actual_payment
    manual_actual_payment = True
    update_plot(force_reset_actual=False)

root = tk.Tk()
root.title("Property Investment Calculator")

labels = [
    "Interest Rate (%)", "Property Price ($)", "Capital Gains Rate (%)",
    "Loan Term (years)", "Deposit ($)", "Actual Monthly Payment ($)"
]
entries = []

for i, label_text in enumerate(labels):
    tk.Label(root, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky="e")
    entry = tk.Entry(root)
    entry.grid(row=i, column=1, padx=10, pady=5)
    if label_text == "Actual Monthly Payment ($)":
        entry.bind("<KeyRelease>", on_actual_change)
    else:
        entry.bind("<Return>", lambda e: update_plot(force_reset_actual=True))
        entry.bind("<FocusOut>", lambda e: update_plot(force_reset_actual=True))
    entries.append(entry)

entry_interest, entry_loan, entry_gains, entry_term, entry_deposit, entry_actual = entries

govt_var = tk.IntVar()
govt_check = tk.Checkbutton(root, text="Use Government Co-Ownership Scheme (25%)", variable=govt_var, command=lambda: update_plot(force_reset_actual=True))
govt_check.grid(row=6, column=0, columnspan=2, pady=5)

stamp_duty_var = tk.IntVar()
stamp_duty_check = tk.Checkbutton(root, text="Include Stamp Duty in Loan", variable=stamp_duty_var, command=lambda: update_plot(force_reset_actual=True))
stamp_duty_check.grid(row=7, column=0, columnspan=2, pady=5)

text_summary = tk.Text(root, width=65, height=18, wrap='word', bg='lightyellow', state='disabled')
text_summary.grid(row=0, column=2, rowspan=9, padx=10, pady=5)

plt.ion()
update_plot(force_reset_actual=True)
root.mainloop()