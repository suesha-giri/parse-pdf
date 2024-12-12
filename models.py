import enum
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TaskStatusEnum(enum.Enum):
    """Enum for task statuses."""
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class FileUpload(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    filepath = db.Column(db.String(100), nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Enum(TaskStatusEnum), default=TaskStatusEnum.PROCESSING)

    def __repr__(self):
        return f"<FileUpload {self.filename} - {self.status.value}>"