import argparse
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

    for _ in range(num_payments):
        if balance <= 0:
            break
        monthly_interest = balance * monthly_interest_rate
        principal_payment = monthly_payment - monthly_interest
        balance -= principal_payment
        total_interest_paid += monthly_interest

    appreciated_value = loan_amount * ((1 + capital_gains / 100) ** term)
    capital_gain = appreciated_value - loan_amount

    return capital_gain, total_interest_paid

def find_inflection_point(interest, loan_amount, term, deposit):
    low = 0.0
    high = 20.0
    tolerance = 0.0001
    max_iter = 100

    for _ in range(max_iter):
        mid = (low + high) / 2
        gains, interest_paid = simulate_investment(interest, loan_amount, mid, term, deposit)
        diff = gains - interest_paid

        if abs(diff) < tolerance:
            return mid

        if diff > 0:
            high = mid
        else:
            low = mid

    return mid

def plot_inflection_vs_price(interest, term, deposit, price_min, price_max, step):
    prices = list(range(price_min, price_max + 1, step))
    inflections = []

    print("\nCalculating inflection points...")

    for price in prices:
        if deposit >= price:
            inflections.append(0)  # No loan needed
            continue
        inflection = find_inflection_point(interest, price, term, deposit)
        inflections.append(inflection)
        print(f"${price:,}: Break-even gains = {inflection:.2f}%")

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(prices, inflections, marker='o')
    plt.title("Break-Even Capital Gains Rate vs Property Price")
    plt.xlabel("Property Price ($)")
    plt.ylabel("Capital Gains Inflection Point (%)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("inflection_vs_price.png")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot inflection point vs property price (fixed deposit).")
    parser.add_argument("interest", type=float, help="Annual interest rate (%)")
    parser.add_argument("term", type=int, help="Loan term (years)")
    parser.add_argument("deposit", type=float, help="Deposit amount ($)")
    parser.add_argument("price_min", type=int, help="Minimum property price ($)")
    parser.add_argument("price_max", type=int, help="Maximum property price ($)")
    parser.add_argument("--step", type=int, default=50000, help="Step size for property prices ($)")

    args = parser.parse_args()

    plot_inflection_vs_price(
        args.interest,
        args.term,
        args.deposit,
        args.price_min,
        args.price_max,
        args.step
    )
