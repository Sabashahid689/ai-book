from typing import List, Dict, Any
import logging


class RAGPromptEngineer:
    """
    Class to handle RAG prompt engineering to ensure responses are grounded in textbook content.
    """
    
    @staticmethod
    def construct_rag_prompt(question: str, context_list: List[str], 
                            max_context_length: int = 2000) -> str:
        """
        Construct a RAG prompt that ensures the response is grounded in the provided context.
        
        Args:
            question: The user's question
            context_list: List of relevant contexts from textbook
            max_context_length: Maximum length of context to include in prompt
            
        Returns:
            A formatted prompt for the language model
        """
        # Combine the context, truncating if necessary
        full_context = " ".join(context_list)
        if len(full_context) > max_context_length:
            full_context = full_context[:max_context_length]
            # Find the last complete sentence to avoid truncating mid-sentence
            last_period = full_context.rfind('.')
            if last_period != -1:
                full_context = full_context[:last_period + 1]
        
        prompt = f"""
        You are an AI assistant for a textbook on Physical AI and Humanoid Robotics. 
        Your goal is to answer questions based ONLY on the provided context from the textbook.
        
        Context from textbook:
        {full_context}
        
        Question: {question}
        
        Instructions:
        1. Answer the question based only on the provided context
        2. If the context does not contain information to answer the question, say "I cannot answer this question based on the textbook content provided."
        3. Do not make up or hallucinate information
        4. If relevant, mention which chapter or concept the information comes from
        5. Keep your answer concise and to the point
        
        Answer:
        """
        return prompt.strip()
    
    @staticmethod
    def validate_response_against_context(response: str, context: str) -> Dict[str, Any]:
        """
        Validate that the response is grounded in the provided context.
        
        Args:
            response: The response from the language model
            context: The context that was provided to the model
            
        Returns:
            A dictionary with validation results
        """
        # Simple validation - check if response contains information from context
        response_lower = response.lower()
        context_lower = context.lower()
        
        # Check if response contains any key terms from context
        context_words = set(context_lower.split())
        response_words = set(response_lower.split())
        
        # Calculate overlap
        intersection = context_words.intersection(response_words)
        overlap_ratio = len(intersection) / len(context_words) if context_words else 0
        
        # Check for hallucination indicators
        hallucination_indicators = [
            "not mentioned in the text",
            "not in the provided context",
            "i cannot find",
            "the text doesn't say",
            "not specified"
        ]
        
        contains_hallucination_indicator = any(indicator in response_lower 
                                             for indicator in hallucination_indicators)
        
        # Check for generic responses that might indicate lack of grounding
        generic_responses = [
            "i don't know",
            "no information provided",
            "not enough information"
        ]
        is_generic = any(phrase in response_lower for phrase in generic_responses)
        
        validation_result = {
            "is_valid": overlap_ratio > 0.1 or contains_hallucination_indicator or is_generic,
            "overlap_ratio": overlap_ratio,
            "contains_hallucination_indicator": contains_hallucination_indicator,
            "is_generic": is_generic,
            "confidence": min(overlap_ratio * 3, 1.0)  # Scale overlap to a confidence score
        }
        
        return validation_result
    
    @staticmethod
    def construct_conversation_prompt(messages: List[Dict[str, str]], 
                                   context: str, 
                                   question: str) -> str:
        """
        Construct a prompt that includes conversation history for contextual responses.
        
        Args:
            messages: List of previous messages in the conversation
            context: Retrieved context from textbook
            question: Current question from user
            
        Returns:
            A formatted prompt including conversation history
        """
        # Format conversation history
        conversation_history = ""
        for msg in messages:
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            conversation_history += f"{role.capitalize()}: {content}\n"
        
        prompt = f"""
        You are an AI assistant for a textbook on Physical AI and Humanoid Robotics.
        You are in a conversation with a user and need to answer their questions based ONLY on the textbook content provided.
        
        Previous conversation:
        {conversation_history if conversation_history else 'No previous conversation.'}
        
        Current question: {question}
        
        Context from textbook:
        {context}
        
        Instructions:
        1. Respond to the current question based only on the provided context
        2. Consider the conversation history to provide a contextual response
        3. If the context does not contain information to answer the question, say "I cannot answer this question based on the textbook content provided."
        4. Do not make up or hallucinate information
        5. If relevant, mention which chapter or concept the information comes from
        6. Keep your answer concise and to the point
        
        Response:
        """
        return prompt.strip()


# Create a singleton instance
rag_prompt_engineer = RAGPromptEngineer()