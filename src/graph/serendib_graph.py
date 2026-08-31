from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

from src.graph.state import SerendibState

class LangGraphRAG:
    def __init__(self, retrieve_manager, llm_manager, rag_pipeline):
        self.retrieve_manager = retrieve_manager
        self.llm_manager = llm_manager
        self.rag_pipeline = rag_pipeline

        self.memory = InMemorySaver()

        self.query_rewriter = None
        self.initialize_query_rewriter()

        self.graph = None
        self.build_graph()

    def initialize_query_rewriter(self):
        rewriter_system_prompt = """
You rewrite conversational traveler questions into standalone
search queries for the Serendib Routes knowledge base.

IMPORTANT RULES:

1. If the current question is already standalone and clear,
return it unchanged.

2. Only use information explicitly stated in the conversation.

3. NEVER invent:
- trip duration
- budget
- destinations
- traveler type
- hotel category
- activities
- dates

4. Resolve references such as:
- "what about for 7 days?"
- "can we make it cheaper?"
- "what about Ella?"
- "how much would that cost?"

5. Preserve known constraints from earlier traveler messages.

6. Do not answer the traveler.

7. Return only one concise standalone search query.

8. The meaning of the CURRENT traveler message must always be preserved.

Never remove a new request such as:
- cheaper / more affordable
- more luxurious
- shorter / longer
- add/remove a destination
- change activity
- change budget

Examples:

History:
Traveler: I want a luxury honeymoon in Sri Lanka.
Traveler: What about 7 days?

Current:
Can you make it cheaper?

Output:
lower-cost options for a 7-day luxury honeymoon in Sri Lanka
"""
        rewrite_prompt = ChatPromptTemplate.from_messages(
            [
                "system", rewriter_system_prompt,
                ("human", """
                Conversation: {history}
                Current question: {question}
                Standalone search query: 
                """)
            ]
        )
        self.query_rewriter = (rewrite_prompt | self.llm_manager.get_llm() | StrOutputParser())

        print("✅ Query rewriter initialized!")

    def retrieve_node(self, state: SerendibState):
        retrieval_query = state['retrieval_query']
        print(
            f"\n[Retriever Node] "
            f"Searching for: {retrieval_query}"
        )
        documents = self.retrieve_manager.retrieve(retrieval_query)

        print("__________Retrieved Documents_________________")

        for i, doc in enumerate(documents, start=1):
            print(f"\nDOCUMENT {i}")
            print(
            "Chunk ID:",
            doc.metadata.get("chunk_id")
                )
            print(
            "Title:",
            doc.metadata.get("title")
                )
            print(
            "Content:",
            doc.page_content[:500]
                )

        context = self.rag_pipeline.format_context(documents)

        return {
            "documents": documents,
            "context": context
        }

    def generate_node(self, state: SerendibState):
        question = state['question']
        retrieval_query = state['retrieval_query']
        context = state['context']

        print(
            "\n[Generator Node] "
            "Generating answer..."
        )

        answer = self.rag_pipeline.chain.invoke({'context': context,
                                                'question': question,
                                                'retrieval_query': retrieval_query})
        return {'answer': answer,
                'messages': [AIMessage(content=answer)]}

    def router_node(self, state: SerendibState):
        question = state['question'].lower().strip()
        greetings = {
                    "hi",
                    "hii",
                    "hiii",
                    "hello",
                    "hey",
                    "hiya",
                    "yoo",
                    "bro",
                    "greetings"
                    "good morning",
                    "good afternoon",
                    "good evening"
        }
            
        thanks = {
            "thanks",
            "thank you",
            "thankyou"
        }

        goodbyes = {
            "bye",
            "goodbye",
            "see you"
        }

        if question in greetings or question in thanks or question in goodbyes:
            route = 'smalltalk'
        else: 
            route = 'rag'

        return {
            'route': route
        }

    def smalltalk_node(self, state: SerendibState):
        question = state['question'].lower().strip()
        if question in {
            "hi",
            "hii",
            "hiii",
            "hello",
            "hey",
            "hiya",
            "yoo",
            "bro",
            "greetings",
            "good morning",
            "good afternoon",
            "good evening"
        }:
            answer = (
            "Hello! 👋 Welcome to Serendib Routes. "
            "How can I help you plan your Sri Lankan journey?"
        )

        elif question in {
                "thanks",
                "thank you",
                "thankyou"
        }:

            answer = (
            "You're very welcome! 😊 "
            "Let me know if you'd like help with anything else."
                )

        elif question in {
        "bye",
        "goodbye",
        "see you"
        }:

            answer = (
            "Goodbye! 👋 "
            "Have a wonderful day!"
            )    

        else:
            answer = (
            "Hello! How can I help you with "
            "your Sri Lanka travel plans?"
            )       
        return {'answer' :answer,
                'messages': [AIMessage(content=answer)]}

    def rewrite_query_node(self, state: SerendibState):
        question = state["question"]
        messages = state["messages"]
        previous_user_messages = [
        message.content
        for message in messages[:-1]
        if isinstance(message, HumanMessage)
    ]


        if not previous_user_messages:
            print("\n [Query Rewriter]" \
            "No previous context")
            return {
                "retrieval_query": question
            }

        recent_user_messages = previous_user_messages[-3:]
        history = "\n".join(
        f"Traveler: {message}"
        for message in recent_user_messages
                            )

        rewritten_query = self.query_rewriter.invoke(
            {
                "history": history,
                "question": question
            }
        )
        rewritten_query = str(
        rewritten_query
                    ).strip()

        print(
        f"\n[Query Rewriter]\n"
        f"History:\n{history}\n\n"
        f"Original: {question}\n"
        f"Rewritten: {rewritten_query}"
        )
        return {
        "retrieval_query": rewritten_query
                }

    def route_question(self, state: SerendibState):
        return state['route']

    def build_graph(self):
        builder = StateGraph(SerendibState)

        builder.add_node("router", self.router_node)
        builder.add_node("smalltalk", self.smalltalk_node)
        builder.add_node("retrieve", self.retrieve_node)
        builder.add_node("generate", self.generate_node)
        builder.add_node("rewrite_query", self.rewrite_query_node)
        builder.add_edge(START, 'router')
        builder.add_conditional_edges('router', 
                                      self.route_question,
                                      {
                                          'smalltalk': 'smalltalk',
                                          'rag': 'rewrite_query'
                                      })
        builder.add_edge("rewrite_query", "retrieve")
        builder.add_edge('retrieve', 'generate')
        builder.add_edge('generate', END)
        builder.add_edge('smalltalk', END)
        self.graph = builder.compile(checkpointer=self.memory)


        print(
            "✅ LangGraph RAG "
            "compiled successfully!"
        )

    def ask(self, question, thread_id = "traveler_001"):
        if not question.strip():
            raise ValueError("Question cannot be empty.")

        config = {
            'configurable': { 'thread_id': thread_id}
        }

        initial_state = {
            "messages": [
                HumanMessage(content=question)
            ],
            "question": question,
            "route": "",
            "retrieval_query": question,
            "documents": [],
            "context": "",
            "answer": ""
        }

        result = self.graph.invoke(initial_state, config=config)

        return (
            result["answer"]
        )
