from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def save_file(title,content):
    filename = f"gst/{title}"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename,ContentFile(content))