# Email Filter 📩
Email filter is an AI email processing project, focused in automating email categorization and responses.

## How it works ⚙️
The project is divided into 3 primary parts: The frontend, the backend and the AI processor.
![arch image](./assets/arch.svg)

After the client sends the email using the `Frontend`, the frontend will send the email to the `Backend` for processing.
This email will be created in the database with status `Pending`, sending it to the queue.
The `AI Processor`, which is listening to the queue will be triggered, applying a NLP to the email content, categorizing it and generating a quick response. Then, it will update the task status in the database.
This update will be seen by the `Backend` (`Frontend` will be pulling the tasks), returning it to client render.

## Tech Stack 🔥
- Frontend: Rust - Yew
- Backend: Python - FastAPI
- Database: MongoDB
- Message Queue: RabbitMQ
- AI Processor: OpenAI
