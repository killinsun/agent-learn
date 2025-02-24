from agents.chat import ChatAgent
from chat_history.conversation import LocalConversationHistory
from tools.ask_user import AskUserTool
from tools.search_docs import SearchDocsTool


def main():
    conversation_id = input("Enter conversation ID(001 ~ 999): ")

    agent = ChatAgent(
        tools=[SearchDocsTool(), AskUserTool()],
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
