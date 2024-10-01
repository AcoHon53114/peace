from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
@stringfilter
def youtube_embed(value):
    try:
        if "youtube.com/watch?v=" in value:
            video_id = value.split("v=")[1].split("&")[0]
        elif "youtu.be/" in value:
            video_id = value.split("youtu.be/")[1]
        else:
            return f"Invalid YouTube URL: {value}"
        
        embed_url = f"https://www.youtube.com/embed/{video_id}"
        return mark_safe(f'<iframe width="560" height="315" src="{embed_url}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>')
    except Exception as e:
        return f"Error processing YouTube URL: {str(e)}"