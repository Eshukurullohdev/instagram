# create validator to accept only image and video
import os
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp4', '.jpg', '.png', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Qollab bolmaydigon fayl turlari\nSiz faqatgina mp4, jpeg, jpg, png file turlarini yuklay ololasiz')
    
def validate_file_video(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp4', '.mkv', '.avi', '.3gp', '.mov', '.flv']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Qollab bolmaydigon fayl turlari\nSiz faqatgina mp4 file turlarini yuklay ololasiz')
    
    
# salom.pdf
# salom.png