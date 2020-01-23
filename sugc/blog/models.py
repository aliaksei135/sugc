from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page
from wagtail.images.blocks import ImageChooserBlock


class BlogPost(Page):
    author = models.CharField(_("Author"), max_length=255)

    body = StreamField([
        ('heading', blocks.CharBlock(label='Heading', max_length=255)),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock())
    ])

    content_panels = Page.content_panels + [
        FieldPanel('author'),
        StreamFieldPanel('body'),
    ]

    template = 'blog-post.html'


class BlogIndex(Page):
    template = 'blog-index.html'
