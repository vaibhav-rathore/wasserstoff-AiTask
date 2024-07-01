from transformers import RagTokenizer, RagRetriever, RagSequenceForGeneration

class RAGChatbot:
    def __init__(self):
        self.tokenizer = RagTokenizer.from_pretrained("facebook/rag-sequence-nq")
        self.retriever = RagRetriever.from_pretrained("facebook/rag-sequence-nq")
        self.model = RagSequenceForGeneration.from_pretrained("facebook/rag-sequence-nq")

    def generate_response(self, query, context=None):
        inputs = self.tokenizer(query, return_tensors="pt")
        generated = self.model.generate(input_ids=inputs["input_ids"])
        response = self.tokenizer.batch_decode(generated, skip_special_tokens=True)[0]
        return response

chatbot = RAGChatbot()
