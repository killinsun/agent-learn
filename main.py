from agents.chat import ChatAgent
from chat_history.conversation import LocalConversationHistory
from search_engine.open_search import get_opensearch_client, FullTextSearchRetriever
from tools.ask_user import AskUserTool
from tools.search_docs import SearchDocsTool
from use_cases.index_docs import IndexDocsUseCase


def main():
    print("1. Chat")
    print("2. Index docs")

    choice = input("Enter choice: ")

    if choice == "1":
        chat()

    if choice == "2":
        index_docs()


def index_docs():
    client = get_opensearch_client()

    use_case = IndexDocsUseCase(client)

    use_case.index_from_json_file("huistenbosch", "documents/huistenbosch.json")

    print("Done")


def chat():
    conversation_id = input("Enter conversation ID(001 ~ 999): ")

    fts_retriever = FullTextSearchRetriever(
        index_names=["huistenbosch"], client=get_opensearch_client()
    )

    agent = ChatAgent(
        tools=[
            SearchDocsTool(
                retriever=fts_retriever,
            ),
            AskUserTool(),
        ],
        conversation_repo=LocalConversationHistory(conversation_id=conversation_id),
    )

    while True:
        question = input("> ")
        if question == "exit":
            break

        agent.run(question)


if __name__ == "__main__":
    main()

    print("Done")
