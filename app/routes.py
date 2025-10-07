"""Flask routes for the text viewer application."""

from __future__ import annotations

from typing import BinaryIO, Iterable

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from .models import TextFile, db

bp = Blueprint("main", __name__)


def _allowed_extension(filename: str) -> bool:
    """Return True when the uploaded filename has an allowed extension."""
    allowed: Iterable[str] = current_app.config.get("UPLOAD_ALLOWED_EXTENSIONS", [])
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in allowed


def _decode_bytes(data: BinaryIO) -> str:
    """Decode raw bytes into UTF-8 text, replacing undecodable characters."""
    if hasattr(data, "seek"):
        try:
            data.seek(0)
        except (OSError, ValueError):
            pass
    raw = data.read()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("utf-8", errors="replace")


@bp.route("/", methods=["GET", "POST"])
def index():
    """List all uploaded files and optionally accept new uploads."""
    if request.method == "POST":
        file = request.files.get("file")
        display_name = (request.form.get("display_name") or "").strip()

        if not file or file.filename == "":
            flash("Please select a TXT file to upload.", "warning")
            return redirect(url_for("main.index"))

        if not _allowed_extension(file.filename):
            flash("Only .txt files are supported.", "warning")
            return redirect(url_for("main.index"))

        content = _decode_bytes(file.stream)
        if not display_name:
            display_name = file.filename.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]

        text_file = TextFile(
            display_name=display_name,
            original_filename=file.filename,
            content=content,
        )

        db.session.add(text_file)
        db.session.commit()

        flash("File uploaded successfully!", "success")
        return redirect(url_for("main.index"))

    files = TextFile.query.order_by(TextFile.created_at.desc()).all()
    return render_template("index.html", files=files)


@bp.route("/files/<int:file_id>", methods=["GET"])
def detail(file_id: int):
    """Display a single text file."""
    text_file = TextFile.query.get_or_404(file_id)
    return render_template("detail.html", text_file=text_file)


@bp.route("/files/<int:file_id>/edit", methods=["GET", "POST"])
def edit(file_id: int):
    """Edit a text file's metadata or content."""
    text_file = TextFile.query.get_or_404(file_id)

    if request.method == "POST":
        display_name = (request.form.get("display_name") or "").strip() or text_file.display_name
        content_text = request.form.get("content")
        upload = request.files.get("file")

        if upload and upload.filename:
            if not _allowed_extension(upload.filename):
                flash("Only .txt files are supported.", "warning")
                return redirect(url_for("main.edit", file_id=file_id))
            content_text = _decode_bytes(upload.stream)
            text_file.original_filename = upload.filename

        if content_text is None:
            flash("Content cannot be empty.", "warning")
            return redirect(url_for("main.edit", file_id=file_id))

        text_file.update_content(display_name=display_name, content=content_text)
        db.session.commit()

        flash("File updated successfully.", "success")
        return redirect(url_for("main.detail", file_id=file_id))

    return render_template("edit.html", text_file=text_file)


@bp.route("/files/<int:file_id>/delete", methods=["POST"])
def delete(file_id: int):
    """Delete a stored text file."""
    text_file = TextFile.query.get(file_id)
    if text_file is None:
        abort(404)

    db.session.delete(text_file)
    db.session.commit()

    flash("File deleted.", "info")
    return redirect(url_for("main.index"))
