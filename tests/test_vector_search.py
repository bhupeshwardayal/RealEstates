import unittest
import time
from app.database.seed_data import seed_properties
from app.vector_store.indexer import PropertyVectorIndex

class TestVectorSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        seed_properties()
        cls.vector_index = PropertyVectorIndex()

    def test_faiss_indexing_and_latency(self):
        # Measure vector search latency (must be <= 50ms per SRS NFR 5.1)
        start_time = time.time()
        results = self.vector_index.search("3 BHK near Hinjawadi IT Park", top_k=4)
        elapsed_ms = (time.time() - start_time) * 1000

        self.assertLess(elapsed_ms, 50.0, f"FAISS search took {elapsed_ms:.2f}ms, exceeding 50ms limit.")
        self.assertGreater(len(results), 0)
        top = results[0]
        self.assertIn("title", top)
        self.assertIn("match_confidence", top)
        self.assertGreaterEqual(top["match_confidence"], 50.0)

    def test_semantic_match_pune_it_park(self):
        results = self.vector_index.search("apartment near Infosys Hinjawadi", top_k=3)
        titles = [r["title"] for r in results]
        # Should rank Verdant Heights or Aura Tech Suites high
        self.assertTrue(any("Hinjawadi" in r["locality"] for r in results))

if __name__ == "__main__":
    unittest.main()

