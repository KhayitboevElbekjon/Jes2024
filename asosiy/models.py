from django.db import models
class GeneratedGif(models.Model):
    text = models.TextField()
    gif_file = models.FileField(upload_to='generated_gifs/')
    vaqt=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" Gif #{self.id} -{self.text[:20]}"