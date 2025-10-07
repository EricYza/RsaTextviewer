"""Integration tests for the text viewer routes."""

from __future__ import annotations

from io import BytesIO

from app.models import TextFile, db


def test_index_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Files" in response.get_data(as_text=True)


def test_upload_list_and_detail_flow(client):
    data = {
        "display_name": "Test file",
        "file": (BytesIO("Hello, world".encode("utf-8")), "hello.txt"),
    }
    response = client.post("/", data=data, content_type="multipart/form-data")
    assert response.status_code == 302

    # Follow redirect to ensure flash message appears
    response = client.get("/", follow_redirects=True)
    page_text = response.get_data(as_text=True)
    assert "File uploaded successfully!" in page_text
    assert "Test file" in page_text

    # Locate the created file
    text_file = TextFile.query.filter_by(display_name="Test file").first()
    assert text_file is not None

    # Detail view renders content
    detail = client.get(f"/files/{text_file.id}")
    assert detail.status_code == 200
    assert "Hello, world" in detail.get_data(as_text=True)


def test_edit_and_delete_file(client):
    # Seed with a file
    text = TextFile(display_name="Initial name", original_filename="init.txt", content="Old content")
    db.session.add(text)
    db.session.commit()

    # Edit using form textarea
    edit_data = {
        "display_name": "Updated name",
        "content": "Updated content",
    }
    response = client.post(
        f"/files/{text.id}/edit",
        data=edit_data,
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "File updated successfully." in response.get_data(as_text=True)

    db.session.refresh(text)
    assert text.display_name == "Updated name"
    assert text.content == "Updated content"

    # Delete the file
    response = client.post(f"/files/{text.id}/delete", follow_redirects=True)
    assert response.status_code == 200
    assert "File deleted." in response.get_data(as_text=True)
    assert db.session.get(TextFile, text.id) is None
