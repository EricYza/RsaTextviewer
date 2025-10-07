"""Database models for the text viewer application."""

from __future__ import annotations

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class TextFile(db.Model):
    """Represents a stored text file."""

    __tablename__ = "text_files"

    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def update_content(self, *, display_name: str | None = None, content: str | None = None) -> None:
        """Update this instance with new metadata or content."""
        if display_name is not None:
            self.display_name = display_name
        if content is not None:
            self.content = content

    def __repr__(self) -> str:  # pragma: no cover - repr is trivial
        return f"<TextFile id={self.id} display_name={self.display_name!r}>"
