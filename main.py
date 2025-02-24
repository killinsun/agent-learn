import os

from agents.chat import ChatAgent
from chat_history.conversation import LocalConversationHistory
from search_engine.open_search import get_opensearch_client, FullTextSearchRetriever
from tools.ask_user import AskUserTool
from tools.search_docs import SearchDocsTool
from use_cases.index_docs import IndexDocsUseCase


def main():
    print("1. Chat")
    print("2. Index docs")
    print("3. Set index name")

    choice = input("Enter choice: ")

    if choice == "1":
        chat()

    if choice == "2":
        index_docs()

    if choice == "3":
        # 使うインデックス名をファイルに保存しておく
        index_name = input("Enter index name: ")
        with open("index_name.txt", "w") as f:
            f.write(index_name)


def index_docs():
    client = get_opensearch_client()

    use_case = IndexDocsUseCase(client)

    index_name = get_index_name_from_last_used()
    file_path = input("Enter file path from this project: ")
    use_case.index_from_json_file(index_name=index_name, file_path=file_path)


def chat():
    conversation_id = input("Enter conversation ID(001 ~ 999): ")

    index_name = get_index_name_from_last_used()

    fts_retriever = FullTextSearchRetriever(
        index_names=[index_name], client=get_opensearch_client()
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

        if question == "":
            continue

        agent.run(question)


def get_index_name_from_last_used():
    if not os.path.exists("index_name.txt"):
        raise ValueError("index_name.txt not found. Please set index name first")

    with open("index_name.txt", "r") as f:
        index_name = f.read()

    return index_name


if __name__ == "__main__":
    main()

    print("Done")
