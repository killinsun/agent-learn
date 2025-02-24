import pprint

from openai.types.chat import ChatCompletion

from agents.chat import ChatAgent
from chat_history.conversation import LocalConversationHistory
from tools.ask_user import AskUserTool
from tools.search_docs import SearchDocsTool


def tool_call(chat_completion: ChatCompletion):
    tool_name = chat_completion.choices[0].message.tool_calls[0].function.name
    arguments = chat_completion.choices[0].message.tool_calls[0].function.arguments

    pprint.pprint(tool_name)
    pprint.pprint(arguments)


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
