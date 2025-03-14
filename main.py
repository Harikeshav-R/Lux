from lux.llm.client import Client


def main():
    client = Client()
    client.start_new_conversation()

    while True:
        user_prompt = input("> ")

        if user_prompt == "exit":
            break

        result = client.generate_response("gpt-4o", user_prompt)
        print(result)


if __name__ == "__main__":
    main()
