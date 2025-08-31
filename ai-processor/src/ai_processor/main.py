from json import loads

from structlog import get_logger
from structlog.stdlib import BoundLogger

from ai_processor.databases.mongo import Mongo
from ai_processor.schemas.email import EmailCategory, EmailStatus
from ai_processor.services.nlp import NLP
from ai_processor.services.openai import OpenAI
from ai_processor.services.queue import AMQPQueue
from ai_processor.settings import Settings

logger: BoundLogger = get_logger()
settings = Settings()


async def main() -> None:
    logger.info("Starting processing queue...")

    db = Mongo(settings.database.dsn)
    queue = AMQPQueue(settings.ai_processor_amqp)
    openai = OpenAI(settings.openai)

    async for message in queue.receive():
        logger.info("Received message from queue.", message=message)

        message_content = NLP.process(message.raw_content)
        gpt_res = await openai.send(
            """
            You're a helpful assistant that provides concise answers.
            Your goal is to classify the emails (post NLP processing) as productive or unproductive (in a corporated environment) and create a quick answer to it.
            the quick answer needs to be in the same politeness level as the email.
            You must answer using the following json format:
            {
                "category": "productive" | "unproductive",
                "quick_answer": str
            }

            """  # noqa: E501
            f"Process this email: [{message.title}] {message_content}",
        )

        gpt_json = loads(gpt_res[0]["content"][0]["text"])
        logger.info("Received response from OpenAI.", response=gpt_json)

        message.status = EmailStatus.DONE

        message.category = EmailCategory(gpt_json["category"])
        message.quick_answer = gpt_json["quick_answer"]

        await db.update_item("email", message)
