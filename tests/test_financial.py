import unittest
from app.rag.financial import FinancialEngine

class TestFinancialEngine(unittest.TestCase):
    def test_emi_calculation(self):
        # Principal: 5,000,000 INR (50 Lakhs)
        # Rate: 8.5% annual
        # Tenure: 20 years (240 months)
        # Expected EMI: ~43,391 INR
        res = FinancialEngine.calculate_emi(5000000, 8.5, 20)
        self.assertAlmostEqual(res["monthly_emi"], 43391.14, places=1)
        self.assertEqual(res["tenure_months"], 240)
        self.assertGreater(res["total_payment"], 5000000)

    def test_rental_yield_calculation(self):
        # Annual Rent: 600,000 INR (50k/month)
        # Property Price: 8,500,000 INR (85 Lakhs)
        # Expected Gross Yield: (600000 / 8500000) * 100 = 7.06%
        res = FinancialEngine.calculate_rental_yield(600000, 8500000)
        self.assertAlmostEqual(res["gross_yield_pct"], 7.06, places=2)
        self.assertEqual(res["monthly_rent"], 50000.0)

    def test_price_per_sqft(self):
        rate = FinancialEngine.calculate_price_per_sqft(8450000, 1120)
        self.assertAlmostEqual(rate, 7544.64, places=2)

    def test_amortization_schedule(self):
        schedule = FinancialEngine.generate_amortization_schedule(5000000, 8.5, 20, max_years_displayed=3)
        self.assertEqual(len(schedule), 3)
        self.assertEqual(schedule[0]["year"], 1)
        self.assertGreater(schedule[0]["yearly_interest"], schedule[0]["yearly_principal"])

if __name__ == "__main__":
    unittest.main()

