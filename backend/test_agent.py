"""
CLI Automated Test Suite for NIAT Parent Decision Lens AI Agent
Tests:
1. Standard user flow with Telugu regional generation
2. High merit scholarship calculation
3. Budget deficit and financial aid routing
4. Degree accreditation verification
5. Human escalation trigger (distress / dispute words)
6. Malformed and bad inputs handling
7. SQLite audit logging verification
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend import db
from backend.agent import run_growth_agent
from backend.tools import calculate_comparative_roi, verify_ugc_accreditation, qualify_and_route_lead

TEST_DB = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "test_growth_engine.db"))

class TestGrowthAgent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Override DB_FILE to test_growth_engine.db so production database remains untouched
        db.DB_FILE = TEST_DB
        db.init_db(TEST_DB)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(TEST_DB):
            try:
                os.remove(TEST_DB)
            except Exception:
                pass

    def test_standard_flow_telugu(self):
        payload = {
            "student_name": "Suresh Reddy",
            "parent_phone": "9876543210",
            "board_percentage": 82.5,
            "entrance_rank": 24000,
            "annual_budget": 250000,
            "partner_campus": "Chalapathi University",
            "hostel_needed": True,
            "language": "te",
            "notes": "Concerned about total four-year expenses"
        }
        result = run_growth_agent(payload)
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(len(result["tools_executed"]), 3)
        self.assertIn("గౌరవనీయులైన", result["decision_memo"])
        self.assertGreater(result["qualification"]["intent_score"], 60)
        self.assertFalse(result["human_escalation"])
        print("PASS: Standard Flow Telugu tested successfully.")

    def test_high_merit_scholarship(self):
        payload = {
            "student_name": "Ananya Sharma",
            "parent_phone": "9812345678",
            "board_percentage": 94.0,
            "entrance_rank": 8500,
            "annual_budget": 300000,
            "partner_campus": "GMR Institute of Technology",
            "hostel_needed": True,
            "language": "hi",
            "notes": "Looking for merit scholarship details"
        }
        result = run_growth_agent(payload)
        scholarship = result["roi_analysis"]["fee_bifurcation"]["scholarship_applied"]
        self.assertEqual(scholarship, 150000)
        self.assertIn("आदरणीय अभिभावक", result["decision_memo"])
        print("PASS: High Merit Scholarship tested successfully.")

    def test_budget_deficit_financial_aid_routing(self):
        payload = {
            "student_name": "Ramesh Kumar",
            "parent_phone": "9700012345",
            "board_percentage": 84.0,
            "entrance_rank": 31000,
            "annual_budget": 120000,  # Below annual fee
            "partner_campus": "Chalapathi University",
            "hostel_needed": False,
            "language": "en",
            "notes": "Need EMI or installment options"
        }
        result = run_growth_agent(payload)
        self.assertEqual(result["qualification"]["priority_tier"], "SCHOLARSHIP_PRIORITY")
        self.assertEqual(result["qualification"]["routing_destination"], "FINANCIAL_AID_DESK")
        print("PASS: Budget Deficit Financial Aid Routing tested successfully.")

    def test_accreditation_degree_validity(self):
        payload = {
            "student_name": "Venkatesh Rao",
            "parent_phone": "9988776655",
            "board_percentage": 78.0,
            "entrance_rank": 40000,
            "annual_budget": 280000,
            "partner_campus": "Chalapathi University",
            "hostel_needed": True,
            "language": "en",
            "notes": "Is the degree valid for UPSC and government exams?"
        }
        result = run_growth_agent(payload)
        self.assertTrue(result["accreditation"]["upsc_and_gate_eligible"])
        self.assertEqual(result["qualification"]["primary_objection"], "Degree Recognition & Accreditation")
        print("PASS: Accreditation Degree Validity tested successfully.")

    def test_human_escalation_trigger(self):
        payload = {
            "student_name": "Distressed Parent",
            "parent_phone": "9000000001",
            "board_percentage": 65.0,
            "entrance_rank": 80000,
            "annual_budget": 50000,
            "partner_campus": "Chalapathi University",
            "hostel_needed": True,
            "language": "en",
            "notes": "We are in severe debt and cannot afford non-refundable test fees. Please talk to human."
        }
        result = run_growth_agent(payload)
        self.assertTrue(result["human_escalation"])
        self.assertEqual(result["qualification"]["priority_tier"], "ESCALATED_HUMAN_REVIEW")
        self.assertEqual(result["qualification"]["routing_destination"], "DEAN_ACADEMIC_ADVISORY")
        print("PASS: Human Escalation Trigger tested successfully.")

    def test_bad_inputs_resilience(self):
        payload = {
            "student_name": "",  # Empty name
            "parent_phone": "123",  # Malformed phone
            "board_percentage": -15.0,  # Negative score
            "entrance_rank": 999999,  # Extreme rank
            "annual_budget": -50000,  # Negative budget
            "partner_campus": "Unknown College",  # Invalid college
            "language": "invalid_lang",  # Fallback language
            "notes": ""
        }
        result = run_growth_agent(payload)
        self.assertEqual(result["status"], "COMPLETED")
        self.assertIn("Dear Parent", result["decision_memo"])  # Defaults to English
        print("PASS: Bad Inputs Resilience tested successfully.")

    def test_audit_logging_persistence(self):
        conn = db.get_connection(TEST_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as c FROM interactions")
        interactions_count = cursor.fetchone()["c"]
        self.assertGreater(interactions_count, 0)
        cursor.execute("SELECT COUNT(*) as c FROM leads")
        leads_count = cursor.fetchone()["c"]
        self.assertGreater(leads_count, 0)
        conn.close()
        print(f"PASS: Audit Logging Persistence verified ({interactions_count} interactions, {leads_count} leads).")

if __name__ == "__main__":
    unittest.main()
