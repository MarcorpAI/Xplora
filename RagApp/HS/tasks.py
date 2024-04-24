from celery import shared_task
from.llm import load_and_embed_text

@shared_task
def process_file_and_embed(file_path, encoding, question):
    try:
        answer = load_and_embed_text(file_path=file_path, encoding=encoding, question=question)
        return f"Question:'{question}'| Answer: {answer}"
    except Exception as ex:
        return str(ex)