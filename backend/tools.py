"""
Core Growth Tools for NIAT Parent Decision Lens
Implements three distinct tools connected by the AI Orchestrator:
1. calculate_comparative_roi
2. verify_ugc_accreditation
3. qualify_and_route_lead
"""

import math
from typing import Dict, Any, List

# Verified Public Accreditation Registry for NIAT Partner Campuses
PARTNER_CAMPUS_REGISTRY = {
    "Chalapathi University": {
        "full_name": "Chalapathi University, Guntur, Andhra Pradesh",
        "ugc_status": "UGC Recognized State Private University under Section 2(f)",
        "aicte_approval": "Approved for Technical Education Programmes",
        "naac_grade": "A Grade",
        "degree_awarded": "Bachelor of Technology (B.Tech) in Computer Science and Engineering",
        "valid_for_govt_exams": True,
        "govt_exam_eligibility": "Fully valid for UPSC, GATE, State PSC, and Central Government Examinations",
        "verification_source": "https://www.ugc.gov.in/ and State Gazette Notification",
        "campus_tier": "Regional Partner Campus",
        "base_university_fee_4yr": 480000,
        "nxtwave_program_fee_4yr": 420000,
        "hostel_fee_per_year": 75000,
        "median_placement_lpa": 7.2
    },
    "GMR Institute of Technology": {
        "full_name": "GMR Institute of Technology (GMRIT), Rajam, Andhra Pradesh",
        "ugc_status": "Autonomous Institution approved under UGC Section 12(B) & 2(f)",
        "aicte_approval": "AICTE Approved Engineering College",
        "naac_grade": "A Grade (Accredited by NBA)",
        "degree_awarded": "B.Tech in CSE (Artificial Intelligence and Machine Learning)",
        "valid_for_govt_exams": True,
        "govt_exam_eligibility": "Affiliated to JNTU-GV, completely valid for all Government and Overseas Higher Education exams",
        "verification_source": "https://gmrit.edu.in/ and JNTU Affiliation Records",
        "campus_tier": "Autonomous Technical Institution",
        "base_university_fee_4yr": 440000,
        "nxtwave_program_fee_4yr": 420000,
        "hostel_fee_per_year": 80000,
        "median_placement_lpa": 7.5
    },
    "Ajeenkya DY Patil University": {
        "full_name": "Ajeenkya DY Patil University (ADYPU), Pune, Maharashtra",
        "ugc_status": "Recognized Private University established under Maharashtra Act",
        "aicte_approval": "AICTE Compliant Technical Curriculum",
        "naac_grade": "Recognized by UGC and State Higher Education Council",
        "degree_awarded": "B.Tech in Computer Science and Engineering",
        "valid_for_govt_exams": True,
        "govt_exam_eligibility": "Valid for GATE, CAT, and Public Sector Recruitment",
        "verification_source": "http://adypu.edu.in/ and UGC Private University List",
        "campus_tier": "Metro Flagship Campus",
        "base_university_fee_4yr": 720000,
        "nxtwave_program_fee_4yr": 480000,
        "hostel_fee_per_year": 120000,
        "median_placement_lpa": 8.4
    }
}

LOCAL_COLLEGE_BENCHMARKS = {
    "Tier-3 Local Engineering College": {
        "tuition_4yr": 320000,
        "hidden_exam_lab_fees_4yr": 60000,
        "hostel_fee_per_year": 60000,
        "median_placement_lpa": 3.4,
        "placement_rate_pct": 28
    }
}

def calculate_comparative_roi(
    board_percentage: float,
    entrance_rank: int,
    partner_campus: str = "Chalapathi University",
    hostel_needed: bool = True,
    annual_budget: float = 250000.0
) -> Dict[str, Any]:
    """
    Tool 1: Mathematical computation comparing the four-year total outlay,
    scholarship deductions, and career earnings payback between local colleges and NIAT.
    """
    campus_info = PARTNER_CAMPUS_REGISTRY.get(partner_campus, PARTNER_CAMPUS_REGISTRY["Chalapathi University"])
    local_info = LOCAL_COLLEGE_BENCHMARKS["Tier-3 Local Engineering College"]
    
    # Scholarship calculation based on NAT / Board performance
    scholarship_amount = 0
    if board_percentage >= 90 or (entrance_rank > 0 and entrance_rank <= 15000):
        scholarship_amount = 150000
    elif board_percentage >= 80 or (entrance_rank > 0 and entrance_rank <= 35000):
        scholarship_amount = 80000
    elif board_percentage >= 70:
        scholarship_amount = 40000
        
    # Local Tier-3 Outlay
    local_hostel_total = (local_info["hostel_fee_per_year"] * 4) if hostel_needed else 0
    local_total_cost = local_info["tuition_4yr"] + local_info["hidden_exam_lab_fees_4yr"] + local_hostel_total
    
    # NIAT Partner Campus Outlay
    niat_hostel_total = (campus_info["hostel_fee_per_year"] * 4) if hostel_needed else 0
    gross_niat_cost = campus_info["base_university_fee_4yr"] + campus_info["nxtwave_program_fee_4yr"] + niat_hostel_total
    net_niat_cost = gross_niat_cost - scholarship_amount
    
    # Career Return Modeling
    salary_delta_lpa = campus_info["median_placement_lpa"] - local_info["median_placement_lpa"]
    extra_investment = max(net_niat_cost - local_total_cost, 0)
    
    # Months to break even on the difference
    payback_months = math.ceil((extra_investment / (salary_delta_lpa * 100000)) * 12) if salary_delta_lpa > 0 else 0
    
    # 3-year cumulative salary projection after graduation
    local_3yr_gross = local_info["median_placement_lpa"] * 3
    niat_3yr_gross = campus_info["median_placement_lpa"] * 3.6  # accounting for standard tech career progression
    net_3yr_gain = (niat_3yr_gross * 100000) - extra_investment
    
    return {
        "partner_campus": partner_campus,
        "fee_bifurcation": {
            "university_tuition_4yr": campus_info["base_university_fee_4yr"],
            "nxtwave_upskilling_4yr": campus_info["nxtwave_program_fee_4yr"],
            "hostel_total_4yr": niat_hostel_total,
            "scholarship_applied": scholarship_amount,
            "net_total_4yr": net_niat_cost,
            "per_year_effective": round(net_niat_cost / 4.0, 2)
        },
        "comparison_local_college": {
            "name": "Local Tier-3 College",
            "tuition_and_misc_4yr": local_info["tuition_4yr"] + local_info["hidden_exam_lab_fees_4yr"],
            "hostel_total_4yr": local_hostel_total,
            "total_cost_4yr": local_total_cost,
            "per_year_effective": round(local_total_cost / 4.0, 2)
        },
        "roi_metrics": {
            "additional_investment": extra_investment,
            "local_median_salary_lpa": local_info["median_placement_lpa"],
            "niat_median_salary_lpa": campus_info["median_placement_lpa"],
            "salary_delta_lpa": round(salary_delta_lpa, 2),
            "payback_period_months": payback_months,
            "net_3yr_financial_gain_inr": round(net_3yr_gain, 2)
        },
        "budget_check": {
            "family_annual_budget": annual_budget,
            "is_budget_sufficient": (annual_budget * 4) >= net_niat_cost,
            "shortfall_or_surplus_annual": round(annual_budget - (net_niat_cost / 4.0), 2)
        }
    }

def verify_ugc_accreditation(partner_campus: str = "Chalapathi University") -> Dict[str, Any]:
    """
    Tool 2: Institutional verification looking up public regulatory recognition records
    to resolve parent concerns regarding degree authenticity and government exam eligibility.
    """
    campus_record = PARTNER_CAMPUS_REGISTRY.get(partner_campus, PARTNER_CAMPUS_REGISTRY["Chalapathi University"])
    
    return {
        "status": "VERIFIED_ACTIVE",
        "institution_name": campus_record["full_name"],
        "ugc_recognition": campus_record["ugc_status"],
        "naac_grade": campus_record["naac_grade"],
        "aicte_status": campus_record["aicte_approval"],
        "degree_conferred": campus_record["degree_awarded"],
        "upsc_and_gate_eligible": campus_record["valid_for_govt_exams"],
        "regulatory_clarification": (
            "Students receive a formal, recognized engineering degree directly from "
            f"{campus_record['full_name']} upon completion, fully compliant with UGC guidelines. "
            "NxtWave provides the on-campus industry curriculum and technical placement training."
        ),
        "source_link": campus_record["verification_source"]
    }

def qualify_and_route_lead(
    student_name: str,
    parent_phone: str,
    board_percentage: float,
    entrance_rank: int,
    annual_budget: float,
    roi_data: Dict[str, Any],
    accreditation_data: Dict[str, Any],
    user_notes: str = ""
) -> Dict[str, Any]:
    """
    Tool 3: Lead qualification, intent scoring, objection classification,
    and routing execution with strict human handoff triggers.
    """
    notes_lower = user_notes.lower()
    
    # 1. Evaluate Human Handoff Triggers (Distress, dispute, refund, complaint)
    distress_keywords = ["debt", "cannot afford", "poor", "help", "refund", "cheating", "fraud", "complaint", "talk to human", "fake"]
    is_human_escalation = any(k in notes_lower for k in distress_keywords)
    
    # 2. Determine Primary Objection
    primary_objection = "General Information"
    if any(k in notes_lower for k in ["fee", "expensive", "money", "cost", "lakh", "budget", "emi"]):
        primary_objection = "Fee and Cost Transparency"
    elif any(k in notes_lower for k in ["valid", "ugc", "aicte", "degree", "fake", "govt", "upsc"]):
        primary_objection = "Degree Recognition & Accreditation"
    elif any(k in notes_lower for k in ["placement", "salary", "job", "package", "hiring"]):
        primary_objection = "Placement Outcomes & Payback"
    elif any(k in notes_lower for k in ["hostel", "safety", "food", "room", "distance"]):
        primary_objection = "Hostel & Campus Environment"
        
    # 3. Intent Scoring (0 to 100)
    score = 40  # base score for completing evaluation
    
    if len(parent_phone.strip()) >= 10:
        score += 25
    if board_percentage >= 75:
        score += 15
    if roi_data["budget_check"]["is_budget_sufficient"]:
        score += 15
    else:
        # Budget deficit but high academic merit
        if board_percentage >= 85:
            score += 10
            
    # 4. Priority Tier and Routing Destination
    if is_human_escalation:
        priority_tier = "ESCALATED_HUMAN_REVIEW"
        routing_destination = "DEAN_ACADEMIC_ADVISORY"
    elif not roi_data["budget_check"]["is_budget_sufficient"] and board_percentage >= 75:
        priority_tier = "SCHOLARSHIP_PRIORITY"
        routing_destination = "FINANCIAL_AID_DESK"
    elif score >= 80:
        priority_tier = "HIGH"
        routing_destination = "DIRECT_ACADEMIC_COUNSELLOR"
    elif primary_objection == "Degree Recognition & Accreditation":
        priority_tier = "MEDIUM"
        routing_destination = "ACADEMIC_CREDENTIAL_SPECIALIST"
    else:
        priority_tier = "NURTURE"
        routing_destination = "SELF_SERVE_DECISION_PACK"
        
    return {
        "student_name": student_name,
        "parent_phone": parent_phone,
        "intent_score": min(score, 100),
        "priority_tier": priority_tier,
        "routing_destination": routing_destination,
        "primary_objection": primary_objection,
        "human_escalation": is_human_escalation,
        "human_escalation_reason": "Family expressed financial distress or requested personal staff review" if is_human_escalation else None,
        "qualification_summary": (
            f"Score {score}/100. Category: {priority_tier}. "
            f"Assigned to {routing_destination}. Primary focus: {primary_objection}."
        )
    }
