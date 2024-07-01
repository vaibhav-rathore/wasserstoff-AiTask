class ChainOfThought:
    def __init__(self, chatbot):
        self.chatbot = chatbot

    def develop_reasoning_steps(self, response, previous_context):
        steps = []
        if previous_context:
            steps.append(f"Previous context: {previous_context}")
        steps.append(f"Generated response: {response}")
        steps.append(f"Based on the response, the next logical step is to ask about X.")
        return steps

    def refine_response_based_on_thought_steps(self, steps):
        refined_response = "\n".join(steps)
        return refined_response

    def process_query_with_chain_of_thought(self, user_query, previous_context):
        initial_response = self.chatbot.generate_response(user_query)
        thought_steps = self.develop_reasoning_steps(initial_response, previous_context)
        final_response = self.refine_response_based_on_thought_steps(thought_steps)
        return final_response

chatbot = RAGChatbot()
chain_of_thought = ChainOfThought(chatbot)
