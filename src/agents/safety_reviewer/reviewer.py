from typing import List
import asyncio
from src.models.response import Response, ResponseStatus
from src.services.llm_service import LLMService
from src.utils.logger import setup_logger, log_agent_action

logger = setup_logger("agent.safety_reviewer")

class SafetyReviewerAgent:
    """
    Agent responsible for applying safety controls and adding necessary disclaimers.
    """

    def __init__(self, llm_service: LLMService):
        """
        Initialize the Safety Reviewer agent.

        Args:
            llm_service: The LLM service to use for safety review
        """
        self.llm_service = llm_service

    async def process(self, response: Response) -> Response:
        """
        Apply safety controls and add necessary disclaimers to the response.

        Args:
            response: The response to apply safety controls to

        Returns:
            The response with safety controls applied
        """
        log_agent_action("safety_reviewer", "safety_review_started", {
            "response_id": response.id,
            "query_id": response.query_id,
            "original_status": response.status
        })

        try:
            # Check if the response indicates insufficient evidence
            if response.status == ResponseStatus.INSUFFICIENT_EVIDENCE:
                # Ensure the response contains the proper message
                if "insufficient verified evidence available" not in response.content.lower():
                    response.content = "Insufficient verified evidence available."

                final_response = Response(
                    id=response.id,
                    query_id=response.query_id,
                    content=response.content,
                    status=ResponseStatus.INSUFFICIENT_EVIDENCE,
                    citations=response.citations,
                    created_at=response.created_at,
                    confidence=response.confidence,
                    disclaimers=self._get_standard_disclaimer()
                )
            else:
                # Apply safety checks and disclaimers to regular responses
                safety_checked_content = await self._apply_safety_checks(response.content)

                # Add standard disclaimers for medical and legal responses
                disclaimers = self._get_standard_disclaimer()

                final_response = Response(
                    id=response.id,
                    query_id=response.query_id,
                    content=safety_checked_content,
                    status=response.status,
                    citations=response.citations,
                    created_at=response.created_at,
                    confidence=response.confidence,
                    disclaimers=disclaimers
                )

            log_agent_action("safety_reviewer", "safety_review_completed", {
                "response_id": response.id,
                "final_status": final_response.status,
                "disclaimers_added": bool(final_response.disclaimers)
            })

            return final_response

        except Exception as e:
            logger.error(f"Error in safety review: {e}")
            log_agent_action("safety_reviewer", "safety_review_failed", {
                "response_id": response.id,
                "error": str(e)
            })

            # Return original response if safety review fails
            return response

    async def _apply_safety_checks(self, content: str) -> str:
        """
        Apply safety checks to the response content.

        Args:
            content: The response content to check

        Returns:
            The safety-checked content
        """
        try:
            # First, check if we need to override the content with "insufficient evidence"
            if len(content.strip()) == 0 or "insufficient verified evidence" in content.lower():
                return "Insufficient verified evidence available."

            # Use LLM to check for appropriate safety measures
            safety_prompt = f"""
            Review the following response to ensure it adheres to safety guidelines for medical/legal information:
            1. Does not provide definitive medical diagnosis, treatment, or legal advice
            2. Does not make guarantees about outcomes
            3. Is based on the provided source documents
            4. Includes appropriate cautionary language where needed

            If the response already meets these criteria, return it unchanged.
            If the response contains information that should be qualified, add appropriate cautionary language.

            Response: {content}

            Improved response (with safety considerations if needed):
            """

            safety_checked_content = self.llm_service.generate_response(safety_prompt)

            log_agent_action("safety_reviewer", "content_safety_checked", {
                "original_length": len(content),
                "checked_length": len(safety_checked_content)
            })

            return safety_checked_content

        except Exception as e:
            logger.error(f"Error in safety check: {e}")
            # Return original content if safety check fails
            return content

    def _get_standard_disclaimer(self) -> str:
        """
        Get the standard disclaimer for medical/legal information.

        Returns:
            The standard disclaimer text
        """
        disclaimer = (
            "This information is for research purposes only and should not be used as "
            "medical or legal advice. Consult with a qualified healthcare professional "
            "or legal expert for medical or legal decisions."
        )
        return disclaimer

    def check_for_prohibited_content(self, content: str) -> bool:
        """
        Check if the content contains prohibited information that should not be returned.

        Args:
            content: The content to check

        Returns:
            True if prohibited content is found, False otherwise
        """
        try:
            prohibited_patterns = [
                "definitive diagnosis",
                "prescribe medication",
                "this treatment will cure",
                "guaranteed results",
                "you must do this",
                "definitely should",
                "always required"
            ]

            content_lower = content.lower()
            for pattern in prohibited_patterns:
                if pattern in content_lower:
                    logger.warning(f"Prohibited content pattern detected: {pattern}")
                    return True

            return False

        except Exception as e:
            logger.error(f"Error checking for prohibited content: {e}")
            return False

    def evaluate_response_safety(self, response: Response) -> dict:
        """
        Evaluate the safety level of a response.

        Args:
            response: The response to evaluate

        Returns:
            Dictionary with safety evaluation results
        """
        try:
            safety_evaluation = {
                "content_safe": True,
                "requires_disclaimer": True,
                "confidence_level": response.confidence or 0.8,
                "citation_compliance": len(response.citations) > 0,
                "prohibited_content_detected": self.check_for_prohibited_content(response.content)
            }

            # Overall safety is compromised if prohibited content is detected
            safety_evaluation["content_safe"] = not safety_evaluation["prohibited_content_detected"]

            log_agent_action("safety_reviewer", "response_evaluated", {
                "response_id": response.id,
                "safety_score": safety_evaluation
            })

            return safety_evaluation

        except Exception as e:
            logger.error(f"Error evaluating response safety: {e}")
            return {
                "content_safe": False,
                "requires_disclaimer": True,
                "confidence_level": 0.0,
                "citation_compliance": False,
                "prohibited_content_detected": True
            }