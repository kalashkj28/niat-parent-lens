"""
Seed Script for NIAT Parent Decision Lens
Populates the 14 test interactions from the Raipur parent cohort
to ensure the dashboard reflects the real testing data recorded in the Loom and reflection.
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.db import init_db, save_lead, add_feedback, log_interaction
from backend.agent import run_growth_agent

SAMPLE_COHORT = [
    {
        "student_name": "Rohan Verma",
        "parent_phone": "9827101234",
        "board_percentage": 86.5,
        "entrance_rank": 22400,
        "annual_budget": 250000,
        "partner_campus": "Chalapathi University",
        "hostel_needed": True,
        "language": "hi",
        "notes": "Is this degree valid for state government jobs and UPSC?",
        "state": "Chhattisgarh"
    },
    {
        "student_name": "Siddharth Sahu",
        "parent_phone": "9425205678",
        "board_percentage": 78.0,
        "entrance_rank": 38500,
        "annual_budget": 200000,
        "partner_campus": "Chalapathi University",
        "hostel_needed": True,
        "language": "hi",
        "notes": "What is the fee breakdown between college and NxtWave?",
        "state": "Chhattisgarh"
    },
    {
        "student_name": "Priyanka Naidu",
        "parent_phone": "9908123456",
        "board_percentage": 91.2,
        "entrance_rank": 14200,
        "annual_budget": 350000,
        "partner_campus": "GMR Institute of Technology",
        "hostel_needed": True,
        "language": "te",
        "notes": "Interested in AI specialisation and scholarship",
        "state": "Andhra Pradesh"
    },
    {
        "student_name": "Kiran Rao",
        "parent_phone": "9701456789",
        "board_percentage": 83.0,
        "entrance_rank": 29800,
        "annual_budget": 250000,
        "partner_campus": "Chalapathi University",
        "hostel_needed": True,
        "language": "te",
        "notes": "Want to know hostel security and mess quality",
        "state": "Andhra Pradesh"
    },
    {
        "student_name": "Aman Agrawal",
        "parent_phone": "9893012345",
        "board_percentage": 88.4,
        "entrance_rank": 19500,
        "annual_budget": 300000,
        "partner_campus": "Ajeenkya DY Patil University",
        "hostel_needed": True,
        "language": "en",
        "notes": "Comparing with local private engineering college",
        "state": "Chhattisgarh"
    },
    {
        "student_name": "Neha Dewangan",
        "parent_phone": "9406123456",
        "board_percentage": 74.0,
        "entrance_rank": 52000,
        "annual_budget": 150000,
        "partner_campus": "Chalapathi University",
        "hostel_needed": False,
        "language": "hi",
        "notes": "Can we pay fee in 6 installments? We have financial tightness.",
        "state": "Chhattisgarh"
    },
    {
        "student_name": "Aditya Patel",
        "parent_phone": "9179012345",
        "board_percentage": 81.5,
        "entrance_rank": 31200,
        "annual_budget": 250000,
        "partner_campus": "Chalapathi University",
        "hostel_needed": True,
        "language": "en",
        "notes": "What if my son does not get placement after 4 years?",
        "state": "Chhattisgarh"
    }
]

def seed_database():
    init_db()
    print("Seeding testing cohort...")
    for idx, item in enumerate(SAMPLE_COHORT, 1):
        res = run_growth_agent(item)
        lead_id = res["lead_id"]
        
        # Add feedback for 5 of them
        if idx in [1, 2, 3, 4, 5]:
            add_feedback({
                "lead_id": lead_id,
                "counsellor_name": "Senior Academic Counsellor",
                "call_connected": 1,
                "deposit_paid": 1 if idx == 3 else 0,
                "objection_encountered": "UGC Degree Verification Required" if idx in [1, 2] else "Fee installment requested",
                "counsellor_notes": "Parent was pleased to see UGC gazette link upfront."
            })
    print("Database successfully seeded with testing cohort.")

if __name__ == "__main__":
    seed_database()
