from django.db import models

class PDF(models.Model):
    file = models.FileField(upload_to="pdfs/")
    extracted_text = models.TextField(blank=True)

    def __str__(self):
        return self.file.name

