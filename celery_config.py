from celery import Celery

# Create the Celery app
celery_app = Celery(
    "email_tasks",
    broker="amqp://guest:guest@localhost:5672//",
    # backend="redis://localhost:6379/0"  # Configure Redis as the result backend (optional)
)

# Celery configuration can be customized here
celery_app.conf.task_routes = {"send_email_smtp": {"queue": "email"}}
