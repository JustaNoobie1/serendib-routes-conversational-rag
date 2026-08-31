from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class RAGPipeline:
    def __init__(self, retrieve_manager, llm_manager):
        self.retrieve_manager = retrieve_manager
        self.llm_manager = llm_manager

        self.prompt = None
        self.chain = None

        self.initialize_pipeline()

    def initialize_pipeline(self):
        system_prompt = """
You are Serendib Routes AI, a Sri Lankan travel planning assistant.

You MUST base factual travel information only on the supplied CONTEXT.

STRICT GROUNDING RULES:

1. Never introduce factual information that is not supported by CONTEXT.

2. Never invent or infer missing traveler constraints such as:
- duration
- dates
- budget
- destinations
- number of travelers
- hotel category
- activities

If an important constraint is missing, ask the traveler for it
instead of inventing it.

3. Only mention hotels, destinations, activities and experiences
that are supported by CONTEXT.

4. Never claim that a hotel, activity, rate, licence, booking,
availability or service is confirmed unless CONTEXT explicitly
states that it is confirmed.

If CONTEXT says something must be verified, state that it must
be verified.

5. Never calculate a total trip price by multiplying a daily or
nightly budget unless CONTEXT explicitly provides that total.

6. Never invent:
- prices
- seasonal weather claims
- visa requirements
- opening hours
- schedules
- availability
- hotel facilities

7. You may combine and summarize facts from multiple retrieved
sources, but you must not create new factual claims.

8. If CONTEXT is insufficient, say so clearly instead of using
your general knowledge.

9. Never mention RAG, embeddings, retrieval, chunks or vector
databases to the traveler.

10. Keep the answer concise and practical.

11. REGION AND DESTINATION RULES:

- Never expand a region into specific destinations unless those
destinations are explicitly supported by the supplied context.
- Do not add examples in parentheses from your own knowledge.
- Preserve the itinerary structure exactly when a source provides
day-by-day routing.
- Never move a destination into a different region.
- If the source says "Cultural Triangle", you may simply say
"Cultural Triangle" unless the context explicitly identifies
the destinations.

12. SOURCE SYNTHESIS RULES:

- If a retrieved source explicitly provides a strategy for the
traveler's request, use that strategy.
- Do not say the context lacks support when a retrieved source
directly addresses the request.
- Specific query-matching guidance takes priority over generic
background information.
- When answering "cheaper", "shorter", "longer", or similar
modification requests, preserve the traveler's existing goal
unless the traveler explicitly changes it.

Before producing the answer, ensure every specific factual claim
can be supported by the supplied CONTEXT.
"""

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ('system', system_prompt),
                ('human', '''SERENDIB ROUTES KNOWLEDGE: {context}
                CURRENT TRAVELER MESSAGE: {question}
                RESOLVED TRAVEL INTENT: {retrieval_query}
                Answer the traveler using the context above.

                Important:
                - Preserve the traveler's actual constraints.
                - Do not invent missing constraints.
                - Do not add facts that are absent from context.
                - If context is insufficient, say so or ask a clarifying question.''')
            ]
        )
        self.chain = (self.prompt | self.llm_manager.get_llm() | StrOutputParser())
        print("RAG Pipeline initialized successfully!")

    def format_context(self, documents):
        context_parts = []
        for index, document in enumerate (documents, start=1):
            title = document.metadata.get('title', 'Unknown Source')
            context_part = f'''SOURCE {index}
                            Title {title} 
                            {document.page_content}'''
            context_parts.append(context_part)
        return context_parts

    def ask(self, question):
        if not question or not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )
        documents = self.retrieve_manager.retrieve(question)
        context = self.format_context(documents)
        answer = self.chain.invoke({
            "context": context,
            "question": question}
        )
        return answer, documents
            