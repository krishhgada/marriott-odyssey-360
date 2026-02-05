"""
AgentOps for Associates - Policy RAG stub
Simple keyword-based Q&A over policy documents
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from pathlib import Path
import re
from shared.security import jwt_verify
from shared.telemetry import telemetry
from shared.config import flags

router = APIRouter()


class PolicyQuestionRequest(BaseModel):
    """Request for policy question"""
    question: str


class PolicyAnswerResponse(BaseModel):
    """Response with answer and citations"""
    answer: str
    citations: List[str]


class DraftReplyRequest(BaseModel):
    """Request to draft a guest reply"""
    ticket_text: str


class DraftReplyResponse(BaseModel):
    """Response with drafted reply"""
    draft: str
    citations: List[str]


# Load policy documents
POLICY_DIR = Path(__file__).parent.parent / "data" / "policies"
POLICIES = {}

def load_policies():
    """Load all policy markdown files"""
    if not POLICY_DIR.exists():
        return
    
    for policy_file in POLICY_DIR.glob("*.md"):
        policy_id = policy_file.stem.upper()
        with open(policy_file, 'r') as f:
            POLICIES[policy_id] = f.read()

# Load policies on module import
load_policies()


def search_policies(query: str) -> tuple[str, List[str]]:
    """
    Simple keyword-based search over policy documents
    Returns answer and citations
    """
    query_lower = query.lower()
    keywords = set(query_lower.split())
    
    relevant_sections = []
    citations = []
    
    for policy_id, content in POLICIES.items():
        lines = content.split('\n')
        current_section = []
        
        for line in lines:
            if line.startswith('#'):
                # New section
                if current_section:
                    section_text = '\n'.join(current_section)
                    # Count matching keywords
                    matches = sum(1 for kw in keywords if kw in section_text.lower())
                    if matches >= 2:  # At least 2 keyword matches
                        relevant_sections.append((matches, section_text, policy_id))
                current_section = [line]
            else:
                current_section.append(line)
        
        # Don't forget last section
        if current_section:
            section_text = '\n'.join(current_section)
            matches = sum(1 for kw in keywords if kw in section_text.lower())
            if matches >= 2:
                relevant_sections.append((matches, section_text, policy_id))
    
    # Sort by relevance
    relevant_sections.sort(key=lambda x: x[0], reverse=True)
    
    if not relevant_sections:
        return "I couldn't find specific policy information about that. Please contact your supervisor.", []
    
    # Take top 2 most relevant sections
    top_sections = relevant_sections[:2]
    
    # Extract citations
    citations = [f"POL-{sec[2]}" for sec in top_sections]
    
    # Build answer from sections
    answer_parts = []
    for _, section_text, _ in top_sections:
        # Extract first few sentences
        sentences = re.split(r'[.!?]+', section_text)
        answer_parts.extend([s.strip() for s in sentences if len(s.strip()) > 20][:2])
    
    answer = '. '.join(answer_parts[:3]) + '.'
    
    return answer, list(set(citations))


@router.post("/answer", response_model=PolicyAnswerResponse)
async def answer_policy_question(
    request: PolicyQuestionRequest,
    token_payload: dict = Depends(jwt_verify)
):
    """
    Answer a policy question using RAG over policy corpus
    """
    
    if not flags.FEATURE_AGENTOPS:
        raise HTTPException(status_code=501, detail="AgentOps feature is not enabled")
    
    try:
        answer, citations = search_policies(request.question)
        
        telemetry({
            "event_type": "agentops_answer",
            "user_id": token_payload.get("sub", "unknown"),
            "question_length": len(request.question),
            "citations_count": len(citations),
            "metadata": {"feature": "agentops"}
        })
        
        return PolicyAnswerResponse(answer=answer, citations=citations)
        
    except Exception as e:
        telemetry({
            "event_type": "agentops_error",
            "user_id": token_payload.get("sub", "unknown"),
            "error": str(e),
            "metadata": {"feature": "agentops"}
        })
        raise HTTPException(status_code=500, detail=f"Policy search failed: {str(e)}")


@router.post("/draft_reply", response_model=DraftReplyResponse)
async def draft_guest_reply(
    request: DraftReplyRequest,
    token_payload: dict = Depends(jwt_verify)
):
    """
    Draft a reply to guest inquiry with policy citations
    """
    
    if not flags.FEATURE_AGENTOPS:
        raise HTTPException(status_code=501, detail="AgentOps feature is not enabled")
    
    try:
        # Extract key topics from ticket
        ticket_lower = request.ticket_text.lower()
        
        # Determine issue category
        if 'cancel' in ticket_lower or 'refund' in ticket_lower:
            draft = ("Thank you for contacting us. According to our cancellation policy [POL-BILLING], "
                    "cancellations made before 6:00 PM on the day of arrival receive a full refund. "
                    "I'd be happy to process this for you. May I have your confirmation number?")
            citations = ["POL-BILLING"]
            
        elif 'late' in ticket_lower and 'checkout' in ticket_lower:
            draft = ("Thank you for your request. Per our guest services policy [POL-GUEST-SERVICES], "
                    "complimentary late checkout until 2:00 PM is available for Bonvoy Titanium Elite and "
                    "Ambassador Elite members. Other guests may request late checkout for $25 per hour. "
                    "Would you like me to arrange this?")
            citations = ["POL-GUEST-SERVICES"]
            
        elif 'room' in ticket_lower and ('change' in ticket_lower or 'issue' in ticket_lower):
            draft = ("I sincerely apologize for the inconvenience. According to policy [POL-GUEST-SERVICES], "
                    "guests may request a room change within the first 24 hours at no charge. I'm arranging "
                    "an immediate room upgrade for you. Additionally, I'd like to offer you a $50 dining credit "
                    "for the inconvenience.")
            citations = ["POL-GUEST-SERVICES"]
            
        elif 'pet' in ticket_lower or 'dog' in ticket_lower or 'cat' in ticket_lower:
            draft = ("Thank you for asking! We welcome pets at our property [POL-AMENITIES]. We accept dogs "
                    "and cats up to 50 lbs, maximum 2 pets per room, with a $150 non-refundable fee per stay. "
                    "We provide pet beds, bowls, and treats upon request. Would you like me to add a pet to your reservation?")
            citations = ["POL-AMENITIES"]
            
        else:
            # Generic helpful response
            draft = ("Thank you for contacting us. I'd be happy to help you with your inquiry. Our team "
                    "can assist with room changes, amenity questions, and billing concerns [POL-GUEST-SERVICES]. "
                    "Could you provide more details so I can best assist you?")
            citations = ["POL-GUEST-SERVICES"]
        
        telemetry({
            "event_type": "agentops_draft",
            "user_id": token_payload.get("sub", "unknown"),
            "ticket_length": len(request.ticket_text),
            "citations_count": len(citations),
            "metadata": {"feature": "agentops"}
        })
        
        return DraftReplyResponse(draft=draft, citations=citations)
        
    except Exception as e:
        telemetry({
            "event_type": "agentops_error",
            "user_id": token_payload.get("sub", "unknown"),
            "error": str(e),
            "metadata": {"feature": "agentops"}
        })
        raise HTTPException(status_code=500, detail=f"Draft generation failed: {str(e)}")


