"""
test_rag.py

Automated Test Suite for:
Project 9 – Modern History & Archival Chronicle Assistant

Validates:
1. PDF extraction and page count preservation (50 pages).
2. All 5 assessment questions against the answer() function.
3. Negative / hallucination resistance (returns exactly '[not found]' with empty sources).
4. Output format: dict with keys 'answer' (str) and 'sources' (list).
5. ChromaDB persistence and change detection.
"""

import os
import unittest
import fitz
from rag import answer, get_components
from ingest import get_file_hash, PDF_PATH, CHROMA_DB_DIR, METADATA_FILE


class TestArchivalRAG(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Ensure database is accessible
        cls.client, cls.collection, cls.model = get_components()

    def test_01_pdf_page_count(self):
        """Verifies that the PDF exists and contains exactly 50 folios/pages."""
        self.assertTrue(os.path.exists(PDF_PATH), f"Target PDF not found at {PDF_PATH}")
        doc = fitz.open(PDF_PATH)
        self.assertEqual(len(doc), 50, "PDF must have exactly 50 pages.")
        doc.close()

    def test_02_q1_guaranteed_interest_rate(self):
        """Q1: 1849 contract guaranteed interest rate must be 5% from Page 4."""
        q = "What exact annual guaranteed interest rate, expressed as a percentage, did the colonial administration promise private British railway companies under the 1849 contract terms?"
        res = answer(q)
        self.assertIsInstance(res, dict)
        self.assertIn("answer", res)
        self.assertIn("sources", res)
        self.assertIn("5%", res["answer"])
        self.assertIn(4, res["sources"])

    def test_03_q2_bhor_ghat_incline(self):
        """Q2: Bhor Ghat engineering obstacle and gradient ratio (1 in 37) from Page 9."""
        q = "Which engineering obstacle on the Bhor Ghat incline made the reversing station described in Chapter 3 necessary, and what was the gradient ratio?"
        res = answer(q)
        self.assertIsInstance(res, dict)
        ans_lower = res["answer"].lower()
        self.assertTrue("cliff" in ans_lower or "obstacle" in ans_lower or "mountain" in ans_lower)
        self.assertTrue("1 in 37" in res["answer"])
        self.assertIn(9, res["sources"])

    def test_04_q3_vande_bharat_negative(self):
        """Q3: Modern train fare not in 19th century archival text -> [not found]."""
        q = "What is the ticket price for an Executive Chair Car seat on the Vande Bharat Express between New Delhi and Varanasi?"
        res = answer(q)
        self.assertEqual(res["answer"], "[not found]")
        self.assertEqual(res["sources"], [])

    def test_05_q4_diamond_harbour_supervisor(self):
        """Q4: Cable supervisor was Dr. William Brooke O'Shaughnessy from Page 13."""
        q = "According to the archival records in the text, who supervised the laying of the experimental Diamond Harbour underwater telegraph cable in 1851?"
        res = answer(q)
        self.assertIsInstance(res, dict)
        self.assertIn("O'Shaughnessy", res["answer"])
        self.assertIn(13, res["sources"])

    def test_06_q5_fifa_world_cup_negative(self):
        """Q5: Out-of-domain modern sporting event -> [not found]."""
        q = "Which country won the 2022 FIFA World Cup?"
        res = answer(q)
        self.assertEqual(res["answer"], "[not found]")
        self.assertEqual(res["sources"], [])

    def test_07_empty_question(self):
        """Empty or whitespace query should return [not found]."""
        res = answer("   ")
        self.assertEqual(res["answer"], "[not found]")
        self.assertEqual(res["sources"], [])

    def test_08_persistence_metadata(self):
        """Persistence metadata must exist and match PDF checksum."""
        self.assertTrue(os.path.exists(METADATA_FILE))
        current_hash = get_file_hash(PDF_PATH)
        import json
        with open(METADATA_FILE, "r") as f:
            meta = json.load(f)
        self.assertEqual(meta.get("pdf_hash"), current_hash)


if __name__ == "__main__":
    unittest.main()
