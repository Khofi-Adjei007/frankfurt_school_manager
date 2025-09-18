# students/utils.py
import os
import uuid
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

TEMP_DIR = "temp_uploads"

def save_temp_file(uploaded_file, prefix=None):
    """
    Save uploaded file to MEDIA_ROOT/temp_uploads/<prefix>_<uuid>_<origname>
    Returns storage path (relative path used by default_storage).
    """
    ext = os.path.splitext(uploaded_file.name)[1]
    uid = uuid.uuid4().hex
    base = f"{prefix or 'f'}_{uid}{ext}"
    path = os.path.join(TEMP_DIR, base)
    # read file content and save via default storage (supports remote storages)
    content = uploaded_file.read()
    saved_path = default_storage.save(path, ContentFile(content))
    return saved_path

def move_temp_to_model_field(instance, field_name, temp_path):
    """
    Move file previously saved in default_storage at temp_path into the model field.
    It opens the temp file, saves into model_field, deletes the temp file.
    """
    if not temp_path:
        return False
    if not default_storage.exists(temp_path):
        return False
    # read temp content
    with default_storage.open(temp_path, "rb") as fh:
        content = fh.read()
    filename = os.path.basename(temp_path)
    model_field = getattr(instance, field_name)
    model_field.save(filename, ContentFile(content), save=False)
    # remove temp file
    try:
        default_storage.delete(temp_path)
    except Exception:
        pass
    return True

def open_temp_file(temp_path):
    """Return file-like object for a stored path or None."""
    if default_storage.exists(temp_path):
        return default_storage.open(temp_path)
    return None
