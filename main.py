import llm
import sferum
import wiki


def send_story():
    fact_and_subject = llm.generate_fact()
    fact, subject = fact_and_subject.split('%%%')
    fact = fact.strip()
    subject = subject.strip()
    image = wiki.get_image(subject)
    if image:
        sferum.send_message_with_image(fact, image)
    else:
        sferum.send_message(fact)


if __name__ == "__main__":
    send_story()
