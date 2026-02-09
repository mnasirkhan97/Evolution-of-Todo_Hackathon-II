from fastapi import FastAPI, Body
from dapr.ext.fastapi import DaprApp
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
dapr_app = DaprApp(app)

# Subscribe to 'task-events'
@dapr_app.subscribe(pubsub='kafka-pubsub', topic='task-events')
def task_subscriber(event_data = Body()):
    logger.info(f"Received task event: {event_data}")
    # Logic: If event has due date, maybe schedule something?
    # For now, just log it.
    return {"status": "SUCCESS"}

# Subscribe to 'reminders'
@dapr_app.subscribe(pubsub='kafka-pubsub', topic='reminders')
def reminder_subscriber(event_data = Body()):
    logger.info(f"Received REMINDER: {event_data}")
    # Mock sending email
    print(f"📧 SENDING EMAIL NOTIFICATION: {event_data}")
    return {"status": "SUCCESS"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6000)
