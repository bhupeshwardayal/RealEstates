import unittest
from app.rag.intent import QueryIntentExtractor
from app.rag.engine import RealEstateRAGEngine
from app.database.seed_data import seed_properties

class TestRAGEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        seed_properties()
        cls.rag = RealEstateRAGEngine()

    def test_intent_extraction_budget_and_bhk(self):
        query = "Looking for a 2 or 3 BHK near an IT park in Pune under 85 Lakhs"
        intent = QueryIntentExtractor.extract_intent(query)
        self.assertEqual(intent["max_budget_inr"], 8500000.0)
        self.assertIn(intent["min_bhk"], [2, 3])
        self.assertEqual(intent["target_city"], "Pune")

    def test_intent_extraction_cr_budget(self):
        query = "Spacious 3 BHK in Hinjawadi budget ₹1.2 Cr with covered parking"
        intent = QueryIntentExtractor.extract_intent(query)
        self.assertEqual(intent["max_budget_inr"], 12000000.0)
        self.assertEqual(intent["min_bhk"], 3)
        self.assertIn("Covered Parking", intent["required_amenities"])

    def test_grounded_response_generation(self):
        query = "Spacious 3 BHK near Hinjawadi Phase 1 under 1.5 Cr with immediate possession"
        res = self.rag.process_query(query)
        self.assertGreater(res["total_matches"], 0)
        self.assertEqual(res["grounding"]["status"], "GROUNDED_VERIFIED")
        self.assertIn("Verdant Heights 3BHK", [p["title"] for p in res["properties"]])
        # Verify no hallucination: AI response references actual title and locality
        self.assertIn("Verdant Heights", res["ai_response"])
        self.assertIn("Hinjawadi", res["ai_response"])

    def test_fallback_when_relaxed(self):
        # Query with extreme budget constraints
        query = "Penthouse in Worli Mumbai under 50 Lakhs"
        res = self.rag.process_query(query)
        # Should either relax or report fallback
        self.assertTrue(res["is_relaxed_fallback"] or res["total_matches"] == 0)

if __name__ == "__main__":
    unittest.main()

