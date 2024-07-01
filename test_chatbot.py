import unittest
from rag_model import RAGChatbot
from chain_of_thought import ChainOfThought

class TestChatbot(unittest.TestCase):
    def setUp(self):
        self.chatbot = RAGChatbot()
        self.chain_of_thought = ChainOfThought(self.chatbot)

    def test_generate_response(self):
        response = self.chatbot.generate_response("What is AI?")
        self.assertIn("artificial intelligence", response.lower())

    def test_chain_of_thought(self):
        response = self.chain_of_thought.process_query_with_chain_of_thought("What is AI?", "Previous context")
        self.assertIn("Previous context", response)
        self.assertIn("Generated response", response)

if __name__ == '__main__':
    unittest.main()
