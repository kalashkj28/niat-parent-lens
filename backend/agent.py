"""
AI Tool-Calling Agent Orchestrator for NIAT Parent Decision Lens
Coordinates three tools to generate parent-facing analysis and vernacular memos:
- calculate_comparative_roi
- verify_ugc_accreditation
- qualify_and_route_lead
"""

import time
import json
from typing import Dict, Any, Optional
from backend.tools import calculate_comparative_roi, verify_ugc_accreditation, qualify_and_route_lead
from backend.db import log_interaction, save_lead

def generate_vernacular_memo(
    language: str,
    student_name: str,
    roi_data: Dict[str, Any],
    accreditation_data: Dict[str, Any],
    qualification_data: Dict[str, Any]
) -> str:
    """
    Synthesizes tool outputs into a clear, respectful parent advisory note
    in Telugu, Hindi, or English without marketing fluff.
    """
    partner_name = roi_data["partner_campus"]
    fee_bif = roi_data["fee_bifurcation"]
    roi_metrics = roi_data["roi_metrics"]
    payback_months = roi_metrics["payback_period_months"]
    ugc_status = accreditation_data["ugc_recognition"]
    degree_title = accreditation_data["degree_conferred"]
    
    net_cost_lakhs = round(fee_bif["net_total_4yr"] / 100000.0, 2)
    univ_fee_lakhs = round(fee_bif["university_tuition_4yr"] / 100000.0, 2)
    nxtwave_fee_lakhs = round(fee_bif["nxtwave_upskilling_4yr"] / 100000.0, 2)
    scholarship_lakhs = round(fee_bif["scholarship_applied"] / 100000.0, 2)
    salary_delta = roi_metrics["salary_delta_lpa"]
    
    if language == "te":
        # Pure, respectful Telugu for parents
        memo = f"""గౌరవనీయులైన తల్లిదండ్రులకు నమస్కారం,

మీ విద్యార్థి {student_name} విద్యా భవిష్యత్తు కోసం తయారుచేసిన పూర్తి ఆర్థిక మరియు గుర్తింపు నివేదిక:

1. కళాశాల డిగ్రీ గుర్తింపు:
{accreditation_data['institution_name']} విశ్వవిద్యాలయం {ugc_status} కింద గుర్తింపు పొందింది. ఈ కోర్సు పూర్తి చేసిన విద్యార్థులకు అధికారిక {degree_title} డిగ్రీ ఇవ్వబడుతుంది. ఈ డిగ్రీ యూపీఎస్సీ (UPSC), గేట్ (GATE) మరియు ప్రభుత్వ ఉద్యోగాలకు పూర్తిగా చెల్లుబాటు అవుతుంది.

2. స్పష్టమైన 4 సంవత్సరాల ఫీజు వివరాలు:
- విశ్వవిద్యాలయ ట్యూషన్ ఫీజు: ₹{univ_fee_lakhs} లక్షలు (4 సంవత్సరాలు)
- నెక్స్ట్‌వేవ్ ప్రాక్టికల్ కోడింగ్ శిక్షణ ఫీజు: ₹{nxtwave_fee_lakhs} లక్షలు
- విద్యార్థికి లభించిన మెరిట్ స్కాలర్‌షిప్ మినహాయింపు: -₹{scholarship_lakhs} లక్షలు
- మొత్తం నికర ఫీజు: ₹{net_cost_lakhs} లక్షలు (సంవత్సరానికి సుమారు ₹{fee_bif['per_year_effective']} మాత్రమే)

3. ఉద్యోగ వేతనం మరియు రికవరీ:
సాధారణ స్థానిక కాలేజీ సగటు వేతనం కంటే సుమారు ₹{salary_delta} LPA ఎక్కువ వేతనం లభించే అవకాశం ఉంది. అదనంగా పెట్టిన పెట్టుబడి విద్యార్థి ఉద్యోగంలో చేరిన సుమారు {payback_months} నెలల్లో పూర్తిగా తిరిగి లభిస్తుంది.

ముఖ్య గమనిక: ఎలాంటి దాచిన ఛార్జీలు లేవు. మీకు ఫీజు వాయిదాలు లేదా బ్యాంకు లోన్ సదుపాయం కావాలంటే మా సీనియర్ అడ్మిషన్ల విభాగం నేరుగా మీకు సహాయం చేస్తుంది."""

    elif language == "hi":
        # Plain, respectful Hindi for parents
        memo = f"""आदरणीय अभिभावक,

आपके बच्चे {student_name} के लिए तैयार की गई कॉलेज फीस और मान्यता की पारदर्शी रिपोर्ट:

1. सरकारी डिग्री मान्यता:
{accreditation_data['institution_name']} {ugc_status} से मान्यता प्राप्त संस्थान है। पाठ्यक्रम पूरा होने पर छात्र को अधिकृत {degree_title} डिग्री प्राप्त होगी। यह डिग्री यूपीएससी (UPSC), गेट (GATE) और सरकारी नौकरियों के लिए पूरी तरह मान्य है।

2. चार वर्षों की स्पष्ट फीस संरचना:
- कॉलेज ट्यूशन फीस: ₹{univ_fee_lakhs} लाख (4 वर्ष)
- नेक्स्टवेव हैंड्स-ऑन कोडिंग एवं प्लेसमेंट फीस: ₹{nxtwave_fee_lakhs} लाख
- आपकी मेरिट छात्रवृत्ति छूट: -₹{scholarship_lakhs} लाख
- कुल शुद्ध फीस: ₹{net_cost_lakhs} लाख (वार्षिक लगभग ₹{fee_bif['per_year_effective']})

3. प्लेसमेंट एवं रिटर्न अनुमान:
स्थानीय कॉलेज की तुलना में तकनीकी कौशल से छात्र को लगभग ₹{salary_delta} लाख प्रति वर्ष अधिक पैकेज मिलने का अनुमान है। चार वर्षों की अतिरिक्त लागत छात्र की नौकरी लगने के लगभग {payback_months} महीनों में पूरी तरह वसूल हो जाती है।

महत्वपूर्ण सूचना: इसमें कोई छिपा हुआ शुल्क शामिल नहीं है। यदि आप ईएमआई या शिक्षा ऋण सहायता चाहते हैं, तो हमारी वरिष्ठ टीम सीधे आपसे संपर्क करेगी।"""

    else:
        # Plain, structured English
        memo = f"""Dear Parent,

Here is the unvarnished four-year financial and accreditation report prepared for {student_name}:

1. Degree Validity and Accreditation:
{accreditation_data['institution_name']} holds {ugc_status}. Graduating students receive a formal {degree_title} conferred directly by the university. This credential is valid for UPSC, GATE, state public service examinations, and post-graduate studies.

2. Transparent Four-Year Fee Breakdown:
- University Tuition Fee: ₹{univ_fee_lakhs} Lakhs (4 years)
- NxtWave Practical Upskilling Fee: ₹{nxtwave_fee_lakhs} Lakhs
- Applied Merit Scholarship: -₹{scholarship_lakhs} Lakhs
- Total Net Outlay: ₹{net_cost_lakhs} Lakhs (Effective ~₹{fee_bif['per_year_effective']} per year)

3. Placement Payback and Financial Return:
The curriculum targets a median software package of ₹{roi_metrics['niat_median_salary_lpa']} LPA compared to ₹{roi_metrics['local_median_salary_lpa']} LPA for regional colleges (a +₹{salary_delta} LPA advantage). The extra educational investment is recovered within approximately {payback_months} months of employment.

Important Note: Every fee component is accounted for upfront. For education loan or semester installment assistance, our senior academic team can review your case directly."""

    return memo

def run_growth_agent(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main Agent Orchestration Execution Loop:
    1. Runs Tool 1 (calculate_comparative_roi)
    2. Runs Tool 2 (verify_ugc_accreditation)
    3. Runs Tool 3 (qualify_and_route_lead)
    4. Generates Vernacular Decision Memo
    5. Checks Human Escalation Triggers
    6. Logs audit interactions and persists lead to SQLite
    """
    student_name = payload.get("student_name", "Prospective Student")
    parent_phone = payload.get("parent_phone", "")
    board_percentage = float(payload.get("board_percentage", 75.0))
    entrance_rank = int(payload.get("entrance_rank", 25000))
    annual_budget = float(payload.get("annual_budget", 250000.0))
    partner_campus = payload.get("partner_campus", "Chalapathi University")
    hostel_needed = bool(payload.get("hostel_needed", True))
    language = payload.get("language", "en")
    user_notes = payload.get("notes", "")

    # Execute Tool 1
    t1_start = time.time()
    roi_result = calculate_comparative_roi(
        board_percentage=board_percentage,
        entrance_rank=entrance_rank,
        partner_campus=partner_campus,
        hostel_needed=hostel_needed,
        annual_budget=annual_budget
    )
    t1_latency = (time.time() - t1_start) * 1000.0
    log_interaction("AGENT", "calculate_comparative_roi", payload, roi_result, t1_latency)

    # Execute Tool 2
    t2_start = time.time()
    accreditation_result = verify_ugc_accreditation(partner_campus=partner_campus)
    t2_latency = (time.time() - t2_start) * 1000.0
    log_interaction("AGENT", "verify_ugc_accreditation", {"partner_campus": partner_campus}, accreditation_result, t2_latency)

    # Execute Tool 3
    t3_start = time.time()
    qualification_result = qualify_and_route_lead(
        student_name=student_name,
        parent_phone=parent_phone,
        board_percentage=board_percentage,
        entrance_rank=entrance_rank,
        annual_budget=annual_budget,
        roi_data=roi_result,
        accreditation_data=accreditation_result,
        user_notes=user_notes
    )
    t3_latency = (time.time() - t3_start) * 1000.0
    log_interaction("AGENT", "qualify_and_route_lead", {"notes": user_notes}, qualification_result, t3_latency)

    # Generate Decision Memo
    memo = generate_vernacular_memo(
        language=language,
        student_name=student_name,
        roi_data=roi_result,
        accreditation_data=accreditation_result,
        qualification_data=qualification_result
    )

    # Save to database
    lead_record = {
        "student_name": student_name,
        "parent_phone": parent_phone,
        "board_percentage": board_percentage,
        "entrance_rank": entrance_rank,
        "annual_budget": annual_budget,
        "state": payload.get("state", "Andhra Pradesh"),
        "comparison_college": payload.get("comparison_college", "Tier-3 Local College"),
        "partner_campus": partner_campus,
        "language": language,
        "intent_score": qualification_result["intent_score"],
        "priority_tier": qualification_result["priority_tier"],
        "routing_destination": qualification_result["routing_destination"],
        "primary_objection": qualification_result["primary_objection"],
        "human_escalation": qualification_result["human_escalation"],
        "decision_memo": memo
    }
    
    lead_id = save_lead(lead_record)

    return {
        "lead_id": lead_id,
        "student_name": student_name,
        "language": language,
        "roi_analysis": roi_result,
        "accreditation": accreditation_result,
        "qualification": qualification_result,
        "decision_memo": memo,
        "tools_executed": ["calculate_comparative_roi", "verify_ugc_accreditation", "qualify_and_route_lead"],
        "human_escalation": qualification_result["human_escalation"],
        "status": "COMPLETED"
    }
