import llm
import sferum


def send_story():
    story = llm.generate_story()
    sferum.send_message(story)


if __name__ == "__main__":
    send_story()
