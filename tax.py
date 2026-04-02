import json
import hashlib
import getpass
import random
import time
import threading
from datetime import datetime, timedelta

class TaxCalculator:
    def __init__(self, salary, hra, deductions_80c, deductions_80d, capital_gains, tax_regime):
        self.salary = salary
        self.hra = hra
        self.deductions_80c = deductions_80c
        self.deductions_80d = deductions_80d
        self.capital_gains = capital_gains
        self.tax_regime = tax_regime

    def calculate_taxable_income(self):
        total_deductions = self.deductions_80c + self.deductions_80d
        taxable_income = self.salary - total_deductions + self.capital_gains
        return taxable_income

    def calculate_tax_payable(self):
        taxable_income = self.calculate_taxable_income()
        tax = 0
        
        if self.tax_regime == "old":
            if taxable_income <= 250000:
                tax = 0
            elif taxable_income <= 500000:
                tax = (taxable_income - 250000) * 0.05
            elif taxable_income <= 1000000:
                tax = 12500 + (taxable_income - 500000) * 0.1
            else:
                tax = 62500 + (taxable_income - 1000000) * 0.3
        elif self.tax_regime == "new":
            if taxable_income <= 250000:
                tax = 0
            elif taxable_income <= 500000:
                tax = (taxable_income - 250000) * 0.05
            elif taxable_income <= 750000:
                tax = 12500 + (taxable_income - 500000) * 0.1
            elif taxable_income <= 1000000:
                tax = 37500 + (taxable_income - 750000) * 0.15
            elif taxable_income <= 1250000:
                tax = 75000 + (taxable_income - 1000000) * 0.2
            elif taxable_income <= 1500000:
                tax = 125000 + (taxable_income - 1250000) * 0.25
            else:
                tax = 187500 + (taxable_income - 1500000) * 0.3

        return tax

    def tax_breakdown(self):
        return {
            "Taxable Income": self.calculate_taxable_income(),
            "Tax Payable": self.calculate_tax_payable()
        }

class LoanCalculator:
    def __init__(self, loan_amount, interest_rate, tenure):
        self.loan_amount = loan_amount
        self.interest_rate = interest_rate / 100 / 12
        self.tenure = tenure * 12

    def calculate_emi(self):
        emi = (self.loan_amount * self.interest_rate * (1 + self.interest_rate) ** self.tenure) / \
              ((1 + self.interest_rate) ** self.tenure - 1)
        return emi

    def total_payment(self):
        return self.calculate_emi() * self.tenure

    def total_interest(self):
        return self.total_payment() - self.loan_amount

class AdvanceTaxCalculator:
    def __init__(self, estimated_income):
        self.estimated_income = estimated_income

    def calculate_advance_tax(self):
        return self.estimated_income * 0.3

class TDSReconciliation:
    def __init__(self, tds_amount, form_26as_amount):
        self.tds_amount = tds_amount
        self.form_26as_amount = form_26as_amount

    def reconcile(self):
        if abs(self.tds_amount - self.form_26as_amount) < 1e-2:
            return "TDS Reconciliation Successful"
        else:
            return "TDS Mismatch: Please verify your Form 26AS"

class GSTCalculator:
    def __init__(self, turnover, gst_rate):
        self.turnover = turnover
        self.gst_rate = gst_rate / 100

    def calculate_gst_liability(self):
        return self.turnover * self.gst_rate

class DepreciationCalculator:
    def __init__(self, asset_cost, useful_life):
        self.asset_cost = asset_cost
        self.useful_life = useful_life

    def calculate_depreciation(self):
        return self.asset_cost / self.useful_life

class AuditRequirements:
    def __init__(self, turnover):
        self.turnover = turnover

    def check_audit_requirement(self):
        if self.turnover > 1000000:
            return "Audit Required under Sec 44AB"
        else:
            return "No Audit Required"

class ITRFiling:
    def __init__(self, user_profile):
        self.user_profile = user_profile

    def auto_file_itr(self):
        itr_type = "ITR-1"
        if self.user_profile['income_type'] == 'business':
            itr_type = "ITR-3"
        elif self.user_profile['income_type'] == 'foreign':
            itr_type = "ITR-2"
        return f"Auto-filing {itr_type} for user."

class FinancialAnalysis:
    def __init__(self, financials):
        # financials: dict of period -> {item_name: value}
        # e.g. {'2022': {'revenue': 1000, 'expenses': 700}, '2023': {...}}
        self.financials = financials  

    def horizontal_analysis(self):
        periods = list(self.financials.keys())
        items = self.financials[periods[0]].keys()
        results = {}
        for item in items:
            results[item] = {}
            base = self.financials[periods[0]][item]
            for period in periods[1:]:
                change = self.financials[period][item] - base
                percent_change = ((self.financials[period][item] - base) / base * 100) if base!=0 else None
                results[item][period] = {"Change": change, "Percent Change": percent_change}
        return results

    def vertical_analysis(self):
        # Express each item as a % of total revenue per period
        results = {}
        for period, data in self.financials.items():
            total_revenue = data.get('revenue', 1)
            results[period] = {}
            for item, value in data.items():
                results[period][item] = (value / total_revenue * 100) if total_revenue != 0 else None
        return results

    def ratio_analysis(self):
        ratios = {}
        latest_period = sorted(self.financials.keys())[-1]
        data = self.financials[latest_period]
        try:
            roe = data.get('net_profit', 0) / data.get('shareholders_equity', 1)
        except ZeroDivisionError:
            roe = None
        try:
            roi = data.get('net_profit', 0) / (data.get('total_assets', 1))
        except ZeroDivisionError:
            roi = None
        try:
            debt_equity = data.get('total_liabilities', 0) / data.get('shareholders_equity', 1)
        except ZeroDivisionError:
            debt_equity = None
        ratios['ROE'] = roe
        ratios['ROI'] = roi
        ratios['Debt-Equity'] = debt_equity
        return ratios

    def trend_analysis(self):
        # Compute percent changes over periods for revenue, expenses, profit
        periods = sorted(self.financials.keys())
        trends = {'revenue': {}, 'expenses': {}, 'net_profit': {}}
        for i in range(1, len(periods)):
            for item in trends.keys():
                prev = self.financials[periods[i-1]].get(item, 0)
                curr = self.financials[periods[i]].get(item, 0)
                percent_change = ((curr - prev) / prev * 100) if prev != 0 else None
                trends[item][periods[i]] = percent_change
        return trends

    def cost_volume_profit_analysis(self, price_per_unit, variable_cost_per_unit, fixed_costs, units_sold):
        contribution_margin_per_unit = price_per_unit - variable_cost_per_unit
        break_even_units = fixed_costs / contribution_margin_per_unit if contribution_margin_per_unit != 0 else None
        profit = contribution_margin_per_unit * units_sold - fixed_costs
        return {
            "Contribution Margin per Unit": contribution_margin_per_unit,
            "Break-even Units": break_even_units,
            "Profit": profit
        }
    
class InsuranceComparison:
    def __init__(self, policies):
        self.policies = policies
    def compare_policies(self):
        # Simplified comparison logic
        return sorted(self.policies, key=lambda x: x['premium'])
    

class InvestmentBanking:
    def __init__(self):
        self.deal_room_checklist = []

    def equity_debt_planning(self, equity_amount, debt_amount):
        total_capital = equity_amount + debt_amount
        equity_ratio = (equity_amount / total_capital) * 100 if total_capital else 0
        debt_ratio = (debt_amount / total_capital) * 100 if total_capital else 0
        return {
            "Total Capital": total_capital,
            "Equity Ratio (%)": equity_ratio,
            "Debt Ratio (%)": debt_ratio
        }

    def mn_a_assistance(self):
        checklist = [
            "Identify target",
            "Perform due diligence",
            "Negotiate terms",
            "Draft agreement",
            "Regulatory approvals",
            "Integration planning"
        ]
        return checklist
    def private_equity_venture_advisory(self):
        advice = "Focus on scalable ventures with strong management and disruptive business models."
        return advice

    def ipo_process_tracker(self, status):
        stages = ["Draft Red Herring Prospectus", "SEBI Review", "Approval", "Pricing", "Allocation", "Listing"]
        if status not in stages:
            return "Invalid stage"
        idx = stages.index(status)
        return {
            "Current Stage": status,
            "Completed Stages": stages[:idx],
            "Upcoming Stages": stages[idx+1:]
        }

    def financial_modeling_tools(self, revenue_growth_rate, expense_growth_rate, years, base_revenue, base_expense):
        projections = {}
        revenue = base_revenue
        expense = base_expense
        for year in range(1, years+1):
            revenue = revenue * (1 + revenue_growth_rate/100)
            expense = expense * (1 + expense_growth_rate/100)
            profit = revenue - expense
            projections[f"Year_{year}"] = {
                "Revenue": round(revenue, 2),
                "Expense": round(expense, 2),
                "Profit": round(profit, 2)
            }
        return projections

    def add_to_deal_room_checklist(self, item):
        self.deal_room_checklist.append(item)
        return f"Added '{item}' to Deal Room checklist."

    def get_deal_room_checklist(self):
        return self.deal_room_checklist

    def risk_return_profile(self, expected_return, volatility):
        if volatility == 0:
            sharpe_ratio = None
        else:
            sharpe_ratio = expected_return / volatility
        profile = "High Risk" if volatility > 20 else "Moderate Risk" if volatility > 10 else "Low Risk"
        return {
            "Expected Return (%)": expected_return,
            "Volatility (%)": volatility,
            "Sharpe Ratio": sharpe_ratio,
            "Risk Profile": profile
        }
    
# Simple user database simulation
class UserAuth:
    def __init__(self):
        self.users = {}  # username: hashed_password
        self.logged_in_user = None

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password):
        if username in self.users:
            return False, "User already exists."
        self.users[username] = self.hash_password(password)
        return True, "User registered successfully."

    def login(self, username, password):
        hashed = self.hash_password(password)
        if username in self.users and self.users[username] == hashed:
            self.logged_in_user = username
            return True, "Login successful."
        else:
            return False, "Invalid username or password."

    def logout(self):
        self.logged_in_user = None
        return "Logged out."

    def is_authenticated(self):
        return self.logged_in_user is not None

# API Connection stubs (simulate API interaction)

class CIBILAPI:
    def __init__(self, user_auth):
        self.authenticated = False
        self.user_auth = user_auth

    def authenticate(self):
        if not self.user_auth.is_authenticated():
            return False, "User not authenticated. Access denied."
        # Simulate authentication process
        time.sleep(1)
        self.authenticated = True
        return True, "CIBIL API authentication successful."

    def fetch_credit_score(self):
        if not self.authenticated:
            return None, "Not authenticated with CIBIL API."
        # Simulated credit score
        score = random.randint(300, 900)
        return score, "Credit score fetched."

class IRDAIAPI:
    def __init__(self, user_auth):
        self.authenticated = False
        self.user_auth = user_auth

    def authenticate(self):
        if not self.user_auth.is_authenticated():
            return False, "User not authenticated. Access denied."
        time.sleep(1)
        self.authenticated = True
        return True, "IRDAI API authentication successful."

    def fetch_policy_details(self):
        if not self.authenticated:
            return None, "Not authenticated with IRDAI API."
        # Simulated policy data
        policies = [
            {'policy_id': 'P123', 'type': 'Health', 'status': 'Active', 'premium': 15000},
            {'policy_id': 'P456', 'type': 'Life', 'status': 'Active', 'premium': 20000},
        ]
        return policies, "Policy details fetched."

class IncomeTaxAPI:
    def __init__(self, user_auth):
        self.authenticated = False
        self.user_auth = user_auth

    def authenticate(self):
        if not self.user_auth.is_authenticated():
            return False, "User not authenticated. Access denied."
        time.sleep(1)
        self.authenticated = True
        return True, "Income Tax API authentication successful."

    def fetch_tax_statements(self):
        if not self.authenticated:
            return None, "Not authenticated with Income Tax API."
        # Simulated tax statement data
        statements = {
            'Form16': 'Received',
            'Form26AS': 'Available',
            'RefundStatus': 'Processed',
        }
        return statements, "Tax statements fetched."

def authenticate_user_flow(user_auth):
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            username = input("Enter new username: ")
            password = getpass.getpass("Enter new password: ")
            success, msg = user_auth.register(username, password)
            print(msg)
        elif choice == '2':
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            success, msg = user_auth.login(username, password)
            print(msg)
            if success:
                break
        elif choice == '3':
            print("Exiting authentication.")
            break
        else:
            print("Invalid choice.")

# --- UserAuth and API classes from previous code should be here ---

class ClientPortal:
    def __init__(self):
        # Store docs as {client_username: {filename: status}}
        self.documents = {}

    def upload_document(self, client_username, filename):
        if client_username not in self.documents:
            self.documents[client_username] = {}
        self.documents[client_username][filename] = "Uploaded"
        return f"Document '{filename}' uploaded for {client_username}."

    def get_document_status(self, client_username):
        return self.documents.get(client_username, {})

class NotificationService:
    def __init__(self):
        # Store notifications per user {username: [notifications]}
        self.notifications = {}
        self.running = True

    def add_notification(self, username, message):
        if username not in self.notifications:
            self.notifications[username] = []
        self.notifications[username].append({"time": datetime.now(), "message": message})

    def get_notifications(self, username):
        return self.notifications.get(username, [])

    def start_periodic_notifications(self, username):
        def notify():
            while self.running:
                # Example: Deadlines and approval alerts
                now = datetime.now()
                if now.minute % 2 == 0:  # Every 2 minutes, send dummy notification
                    self.add_notification(username, f"Reminder: Upcoming deadline at {now.strftime('%H:%M:%S')}")
                time.sleep(60)
        t = threading.Thread(target=notify, daemon=True)
        t.start()
        return t

    def stop(self):
        self.running = False


class AnalyticsDashboard:
    def  init__(self, username, tax_calculator=None, loan_calculator=None,
                 client_portal=None, notification_service=None, financial_analysis=None):
        self.username = username
        self.tax_calculator = tax_calculator
        self.loan_calculator = loan_calculator
        self.client_portal = client_portal
        self.notification_service = notification_service
        self.financial_analysis = financial_analysis

    def get_tax_summary(self):
        if self.tax_calculator:
            breakdown = self.tax_calculator.tax_breakdown()
            return breakdown
        return {}

    def get_loan_summary(self):
        if self.loan_calculator:
            emi = self.loan_calculator.calculate_emi()
            total_interest = self.loan_calculator.total_interest()
            total_payment = self.loan_calculator.total_payment()
            return {
                "Monthly EMI": round(emi, 2),
                "Total Interest": round(total_interest, 2),
                "Total Payment": round(total_payment, 2)
            }
        return {}

    def get_documents_summary(self):
        if self.client_portal:
            docs = self.client_portal.get_document_status(self.username)
            total_docs = len(docs)
            uploaded = sum(1 for status in docs.values() if status == "Uploaded")
            processed = total_docs - uploaded
            return {
                "Total Documents": total_docs,
                "Uploaded": uploaded,
                "Processed": processed
            }
        return {}

    def get_notifications_summary(self):
        if self.notification_service:
            notes = self.notification_service.get_notifications(self.username)
            unread_count = len(notes)  # In a real app, have read/unread flag
            return {
                "Total Notifications": len(notes),
                "Unread Notifications": unread_count
            }
        return {}

    def get_financial_trends(self):
        if self.financial_analysis:
            trends = self.financial_analysis.trend_analysis()
            return trends
        return {}

    def display_dashboard(self):
        print(f"\nAnalytics Dashboard for {self.username}")
        print("------ Tax Summary ------")
        tax_summary = self.get_tax_summary()
        for k,v in tax_summary.items():
            print(f"{k}: {v}")

        print("\n------ Loan Summary ------")
        loan_summary = self.get_loan_summary()
        for k,v in loan_summary.items():
            print(f"{k}: {v}")

        print("\n------ Documents Summary ------")
        docs_summary = self.get_documents_summary()
        for k,v in docs_summary.items():
            print(f"{k}: {v}")

        print("\n------ Notifications Summary ------")
        notif_summary = self.get_notifications_summary()
        for k,v in notif_summary.items():
            print(f"{k}: {v}")

        print("\n------ Financial Trends ------")
        trends = self.get_financial_trends()
        print(json.dumps(trends, indent=4))

    
def main():
    name = input("Enter your Name: ")
    print("Mr/Mrs",name,"Financial Lookout")
    print("==== Tax Calculator ====")
    salary = float(input("Enter your salary: "))
    hra = float(input("Enter your HRA: "))
    deductions_80c = float(input("Enter your 80C deductions: "))
    deductions_80d = float(input("Enter your 80D deductions: "))
    capital_gains = float(input("Enter your capital gains: "))
    tax_regime = input("Enter tax regime (old/new): ").lower()
    tax_calc = TaxCalculator(salary, hra, deductions_80c, deductions_80d, capital_gains, tax_regime)
    print(json.dumps(tax_calc.tax_breakdown(), indent=4))

    print("\n==== Loan Calculator ====")
    loan_amount = float(input("Enter loan amount: "))
    interest_rate = float(input("Enter interest rate (%): "))
    tenure = int(input("Enter tenure (in years): "))
    loan_calc = LoanCalculator(loan_amount, interest_rate, tenure)
    print(f"Monthly EMI: {loan_calc.calculate_emi():.2f}")
    print(f"Total Payment: {loan_calc.total_payment():.2f}")
    print(f"Total Interest: {loan_calc.total_interest():.2f}")

    print("\n==== Advance Tax Calculation ====")
    estimated_income = float(input("Enter estimated income: "))
    adv_tax_calc = AdvanceTaxCalculator(estimated_income)
    print(f"Advance Tax Payable: {adv_tax_calc.calculate_advance_tax():.2f}")

    print("\n==== TDS Reconciliation ====")
    tds_amount = float(input("Enter TDS amount: "))
    form_26as_amount = float(input("Enter Form 26AS amount: "))
    tds_recon = TDSReconciliation(tds_amount, form_26as_amount)
    print(tds_recon.reconcile())

    print("\n==== GST Liability Calculation ====")
    turnover = float(input("Enter turnover: "))
    gst_rate = float(input("Enter GST rate (%): "))
    gst_calc = GSTCalculator(turnover, gst_rate)
    print(f"GST Liability: {gst_calc.calculate_gst_liability():.2f}")

    print("\n==== Depreciation Calculator ====")
    asset_cost = float(input("Enter asset cost: "))
    useful_life = int(input("Enter useful life (in years): "))
    dep_calc = DepreciationCalculator(asset_cost, useful_life)
    print(f"Annual Depreciation: {dep_calc.calculate_depreciation():.2f}")

    print("\n==== Audit Requirements ====")
    turnover_for_audit = float(input("Enter turnover for audit check: "))
    audit_req = AuditRequirements(turnover_for_audit)
    print(audit_req.check_audit_requirement())

    print("\n==== ITR Filing ====")
    income_type = input("Enter income type (salary/business/foreign): ").lower()
    itr_filer = ITRFiling({'income_type': income_type})
    print(itr_filer.auto_file_itr())

    print("\n==== Financial Analysis ====")
    num_periods = int(input("Enter number of periods for financial data (min 2): "))
    financials = {}
    for _ in range(num_periods):
        period = input("Enter period (e.g. 2022): ")
        revenue = float(input(f"Enter revenue for {period}: "))
        expenses = float(input(f"Enter expenses for {period}: "))
        net_profit = float(input(f"Enter net profit for {period}: "))
        shareholders_equity = float(input(f"Enter shareholders' equity for {period}: "))
        total_assets = float(input(f"Enter total assets for {period}: "))
        total_liabilities = float(input(f"Enter total liabilities for {period}: "))
        financials[period] = {
            'revenue': revenue,
            'expenses': expenses,
            'net_profit': net_profit,
            'shareholders_equity': shareholders_equity,
            'total_assets': total_assets,
            'total_liabilities': total_liabilities
        }
    fin_analysis = FinancialAnalysis(financials)
    print("\nHorizontal Analysis:")
    print(json.dumps(fin_analysis.horizontal_analysis(), indent=4))
    print("\nVertical Analysis:")
    print(json.dumps(fin_analysis.vertical_analysis(), indent=4))
    print("\nRatio Analysis:")
    print(json.dumps(fin_analysis.ratio_analysis(), indent=4))
    print("\nTrend Analysis:")
    print(json.dumps(fin_analysis.trend_analysis(), indent=4))

    print("\n==== Cost-Volume-Profit Analysis ====")
    price_per_unit = float(input("Enter price per unit: "))
    variable_cost_per_unit = float(input("Enter variable cost per unit: "))
    fixed_costs = float(input("Enter total fixed costs: "))
    units_sold = float(input("Enter units sold: "))
    cvp = fin_analysis.cost_volume_profit_analysis(price_per_unit, variable_cost_per_unit, fixed_costs, units_sold)
    print(json.dumps(cvp, indent=4))

# Insurance Comparison
    print("\nInsurance Comparison")
    policies = []
    num_policies = int(input("Enter number of insurance policies to compare: "))
    for _ in range(num_policies):
        policy_name = input("Enter policy name: ")
        premium = float(input("Enter policy premium: "))
        policies.append({'name': policy_name, 'premium': premium})
    
    insurance_comparison = InsuranceComparison(policies)
    print("Sorted Policies by Premium:", insurance_comparison.compare_policies())

    print("\n==== Investment Banking Services ====")
    ib = InvestmentBanking()

    # Equity & Debt Financing Planning
    equity_amt = float(input("Enter equity amount: "))
    debt_amt = float(input("Enter debt amount: "))
    equity_debt_plan = ib.equity_debt_planning(equity_amt, debt_amt)
    print("Equity & Debt Financing Planning:", json.dumps(equity_debt_plan, indent=4))

    # M&A Assistance
    mn_a_checklist = ib.mn_a_assistance()
    print("M&A Assistance Checklist:")
    for step in mn_a_checklist:
        print(f"- {step}")

    # Private Equity & Venture Capital Advisory
    pe_advice = ib.private_equity_venture_advisory()
    print("\nPrivate Equity & Venture Capital Advisory:")
    print(pe_advice)

    # IPO/Private Placement Process Tracker
    ipo_stage = input("\nEnter current IPO stage (Draft Red Herring Prospectus, SEBI Review, Approval, Pricing, Allocation, Listing): ")
    ipo_status = ib.ipo_process_tracker(ipo_stage)
    print("IPO Process Tracker:")
    print(json.dumps(ipo_status, indent=4))

    # Financial Modeling Tools
    print("\nFinancial Modeling Tools")
    years = int(input("Enter number of years for projection: "))
    base_revenue = float(input("Enter base year revenue: "))
    base_expense = float(input("Enter base year expense: "))
    rev_growth = float(input("Enter annual revenue growth rate (%): "))
    exp_growth = float(input("Enter annual expense growth rate (%): "))
    projections = ib.financial_modeling_tools(rev_growth, exp_growth, years, base_revenue, base_expense)
    print("Financial Projections:")
    print(json.dumps(projections, indent=4))

    # Deal Room & Due Diligence Checklist
    print("\nManage Deal Room & Due Diligence Checklist")
    while True:
        action = input("Add item to checklist (a), View checklist (v), or Quit (q): ").lower()
        if action == "a":
            item = input("Enter checklist item: ")
            msg = ib.add_to_deal_room_checklist(item)
            print(msg)
        elif action == "v":
            checklist = ib.get_deal_room_checklist()
            print("Deal Room Checklist:")
            for idx, ci in enumerate(checklist, 1):
                print(f"{idx}. {ci}")
        elif action == "q":
            break
        else:
            print("Invalid choice.")

    # Risk-Return Profiling
    print("\nRisk-Return Profiling")
    expected_ret = float(input("Enter expected return (%): "))
    volatility = float(input("Enter volatility (%): "))
    risk_profile = ib.risk_return_profile(expected_ret, volatility)
    print("Risk-Return Profile:")
    print(json.dumps(risk_profile, indent=4))

    user_auth = UserAuth()
    print("=== User Authentication System ===")
    authenticate_user_flow(user_auth)

    if not user_auth.is_authenticated():
        print("You must be logged in to proceed with API access.")
        return

    # Init API connectors with auth
    cibil_api = CIBILAPI(user_auth)
    irdai_api = IRDAIAPI(user_auth)
    income_tax_api = IncomeTaxAPI(user_auth)

    # Authenticate with each API
    success, message = cibil_api.authenticate()
    print(message)
    if success:
        score, msg = cibil_api.fetch_credit_score()
        if score is not None:
            print(f"CIBIL Credit Score: {score}")
        else:
            print(msg)

    success, message = irdai_api.authenticate()
    print(message)
    if success:
        policies, msg = irdai_api.fetch_policy_details()
        if policies:
            print("Insurance Policies:")
            for pol in policies:
                print(f"  ID:{pol['policy_id']} Type:{pol['type']} Status:{pol['status']} Premium:{pol['premium']}")
        else:
            print(msg)

    success, message = income_tax_api.authenticate()
    print(message)
    if success:
        statements, msg = income_tax_api.fetch_tax_statements()
        if statements:
            print("Tax Statements:")
            for k, v in statements.items():
                print(f"  {k}: {v}")
        else:
            print(msg)

    # Assume user_auth from previous examples and user logged in as:
    user_auth = UserAuth()
    # Let's do a quick login for demo
    username = input("Enter username to simulate login: ")
    user_auth.logged_in_user = username  # Simulated login; in real app, use proper auth

    client_portal = ClientPortal()
    notification_service = NotificationService()

    # Start user notification thread
    notification_thread = notification_service.start_periodic_notifications(username)

    while True:
        print("\nClient Portal Menu:")
        print("1. Upload Document")
        print("2. View Uploaded Documents and Status")
        print("3. View Notifications")
        print("4. Exit")
        option = input("Select option: ").strip()
        if option == "1":
            filename = input("Enter document filename to upload: ")
            msg = client_portal.upload_document(username, filename)
            print(msg)
        elif option == "2":
            docs = client_portal.get_document_status(username)
            if not docs:
                print("No documents uploaded.")
            else:
                print("Documents and Statuses:")
                for doc, status in docs.items():
                    print(f" - {doc}: {status}")
        elif option == "3":
            notes = notification_service.get_notifications(username)
            if not notes:
                print("No new notifications.")
            else:
                print("Notifications:")
                for note in notes[-10:]:  # show last 10
                    time_str = note['time'].strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{time_str}] {note['message']}")
        elif option == "4":
            print("Exiting Client Portal.")
            notification_service.stop()
            break
        else:
            print("Invalid option.")
    
     # Simulated login for demo
    username = input("Enter username to simulate login: ")
    # Simulate some data for dashboards
    
    # Tax Calculator sample
    tax_calc = TaxCalculator(
        salary=1000000, hra=200000, deductions_80c=150000, deductions_80d=25000,
        capital_gains=50000, tax_regime='old'
    )
    # Loan Calculator sample
    loan_calc = LoanCalculator(loan_amount=500000, interest_rate=7.5, tenure=10)
    # Client Portal and Notification setup
    client_portal = ClientPortal()
    notification_service = NotificationService()

    # Simulate doc uploads and notifications
    client_portal.upload_document(username, "Form16.pdf")
    client_portal.upload_document(username, "InvestmentProof.pdf")
    notification_service.add_notification(username, "Tax Return due in 10 days")
    notification_service.add_notification(username, "Loan EMI due tomorrow")

    # Financial Analysis sample data
    financial_data = {
        '2022': {'revenue': 1000000, 'expenses': 700000, 'net_profit': 300000, 'shareholders_equity': 500000, 'total_assets': 800000, 'total_liabilities': 300000},
        '2023': {'revenue': 1100000, 'expenses': 720000, 'net_profit': 380000, 'shareholders_equity': 550000, 'total_assets': 870000, 'total_liabilities': 320000},
        
    }
    fin_analysis = FinancialAnalysis(financial_data)

    # Start periodic notifications thread
    notif_thread = notification_service.start_periodic_notifications(username)

    dashboard = AnalyticsDashboard (
        username,
        tax_calculator=tax_calc,
        loan_calculator=loan_calc,
        client_portal=client_portal,
        notification_service=notification_service,
        financial_analysis=fin_analysis
    )

    dashboard.display_dashboard()

    # Wait a moment for notification thread to run and show notifications summary update
    time.sleep(2)
    print("\nUpdated Notifications Summary after 2 seconds:")
    dashboard.display_dashboard()

    # Stop notification thread before exit
    notification_service.stop()


if __name__ == "__main__":
    main()

