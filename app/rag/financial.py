from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Any, List

class FinancialEngine:
    """
    Deterministic Financial Estimation Engine as defined in SRS Module 4.
    Implements precise decimal calculations for zero computational rounding drift.
    """

    @staticmethod
    def calculate_emi(principal: float, annual_rate_pct: float, tenure_years: int) -> Dict[str, Any]:
        """
        FR-4.1 EMI Calculation:
        E = P * r * (1 + r)^n / ((1 + r)^n - 1)
        """
        P = Decimal(str(principal))
        annual_rate = Decimal(str(annual_rate_pct))
        n = Decimal(str(tenure_years * 12))

        if P <= 0 or n <= 0:
            return {
                "monthly_emi": 0.0,
                "principal": float(P),
                "total_interest": 0.0,
                "total_payment": 0.0,
                "tenure_months": int(n)
            }

        if annual_rate == 0:
            emi = P / n
            return {
                "monthly_emi": float(emi.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
                "principal": float(P),
                "total_interest": 0.0,
                "total_payment": float(P),
                "tenure_months": int(n)
            }

        # Monthly interest rate
        r = annual_rate / Decimal("1200")
        
        # (1 + r)^n
        one_plus_r_pow_n = (Decimal("1") + r) ** int(n)
        
        # EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
        emi = P * r * one_plus_r_pow_n / (one_plus_r_pow_n - Decimal("1"))
        
        total_payment = emi * n
        total_interest = total_payment - P

        return {
            "monthly_emi": float(emi.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
            "principal": float(P),
            "total_interest": float(total_interest.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
            "total_payment": float(total_payment.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
            "tenure_months": int(n)
        }

    @staticmethod
    def calculate_rental_yield(annual_rent: float, purchase_price: float) -> Dict[str, Any]:
        """
        FR-4.2 Rental Yield Analysis:
        Gross Yield (%) = (Annual Expected Rent / Total Property Purchase Price) * 100
        """
        rent = Decimal(str(annual_rent))
        price = Decimal(str(purchase_price))

        if price <= 0:
            return {"gross_yield_pct": 0.0, "annual_rent": float(rent), "monthly_rent": 0.0}

        gross_yield = (rent / price) * Decimal("100")
        monthly_rent = rent / Decimal("12")

        return {
            "gross_yield_pct": float(gross_yield.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
            "annual_rent": float(rent),
            "monthly_rent": float(monthly_rent.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
        }

    @staticmethod
    def calculate_price_per_sqft(price_inr: float, carpet_area_sqft: int) -> float:
        if carpet_area_sqft <= 0:
            return 0.0
        price = Decimal(str(price_inr))
        area = Decimal(str(carpet_area_sqft))
        rate = price / area
        return float(rate.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

    @staticmethod
    def generate_amortization_schedule(principal: float, annual_rate_pct: float, tenure_years: int, max_years_displayed: int = 5) -> List[Dict[str, Any]]:
        """
        Generates detailed yearly amortization table for financial disclosures.
        """
        emi_data = FinancialEngine.calculate_emi(principal, annual_rate_pct, tenure_years)
        monthly_emi = Decimal(str(emi_data["monthly_emi"]))
        r = Decimal(str(annual_rate_pct)) / Decimal("1200")
        balance = Decimal(str(principal))

        schedule = []
        months_to_simulate = min(tenure_years, max_years_displayed) * 12

        for year in range(1, min(tenure_years, max_years_displayed) + 1):
            yearly_principal = Decimal("0")
            yearly_interest = Decimal("0")
            for _ in range(12):
                if balance <= 0:
                    break
                interest_payment = balance * r
                principal_payment = monthly_emi - interest_payment
                if principal_payment > balance:
                    principal_payment = balance
                balance -= principal_payment
                yearly_principal += principal_payment
                yearly_interest += interest_payment

            schedule.append({
                "year": year,
                "yearly_principal": float(yearly_principal.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
                "yearly_interest": float(yearly_interest.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)),
                "remaining_balance": float(balance.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
            })

        return schedule

