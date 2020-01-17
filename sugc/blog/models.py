from django.db import models
from wagtail.admin.edit_handlers import MultiFieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index


class BlogPage(Page):
    template = 'blog/blog.html'

    # DB fields
    post_date = models.DateField("Post Date", auto_now_add=True, editable=False)
    author = models.CharField("Author", max_length=255, blank=False)
    # title = models.CharField("Title", max_length=255, blank=False)
    body = StreamField([
        ('heading', blocks.CharBlock(classname='title')),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('quote', blocks.BlockQuoteBlock())
    ])

    # Search
    search_fields = Page.search_fields + [
        # index.SearchField('title'),
        index.FilterField('author'),
        index.FilterField('post_date'),
    ]

    # Editors
    content_panels = Page.content_panels + [
        # FieldPanel('title'),
        StreamFieldPanel('body'),
    ]

    promote_panels = Page.promote_panels + [
        MultiFieldPanel(Page.promote_panels, "Common Page Configuration"),
    ]
