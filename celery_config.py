from celery import Celery, Task

def make_celery(app):
    """Initialize Celery using the Flask app configuration"""
    class FlaskTask(Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery = Celery(
        app.import_name,
        backend="redis://redis:6379/0",
        broker="redis://redis:6379/0",
        include=("tasks"),
        task_cls=FlaskTask
    )

    celery.conf.update(app.config)

    return celery
