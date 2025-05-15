# verklegt2/core/storage.py
from django.core.files.base import ContentFile, File
from django.core.files.storage import Storage
from django.apps import apps
from django.urls import reverse


class DatabaseStorage(Storage):
    """
    Stores every uploaded file inside the FileBlob table.
    """

    # ───────────────────────── internal helper ──
    def _fileblob(self):
        """
        Lazily retrieves the FileBlob model to avoid circular imports
        at module-import time.
        """
        return apps.get_model("core", "FileBlob")

    # ───────────────────────── Django Storage API ──
    def _save(self, name: str, content: File) -> str:
        content.open()
        FileBlob = self._fileblob()
        blob, _ = FileBlob.objects.update_or_create(
            path=name,
            defaults={
                "data": content.read(),
                "content_type": getattr(content, "content_type", ""),
            },
        )
        return blob.path

    def _open(self, name: str, mode: str = "rb") -> ContentFile:
        FileBlob = self._fileblob()
        blob = FileBlob.objects.get(path=name)
        return ContentFile(blob.data, name=name)

    def exists(self, name: str) -> bool:
        FileBlob = self._fileblob()
        return FileBlob.objects.filter(path=name).exists()

    def size(self, name: str) -> int:
        FileBlob = self._fileblob()
        blob = FileBlob.objects.get(path=name)
        return len(blob.data)

    # ───────────────────────── optional helpers ──
    def delete(self, name: str):
        FileBlob = self._fileblob()
        FileBlob.objects.filter(path=name).delete()

    def url(self, name: str) -> str:
        """
        Public URL shown in templates. Resolves to core.views.serve_db_file.
        """
        return reverse("db_file", kwargs={"file_path": name})
