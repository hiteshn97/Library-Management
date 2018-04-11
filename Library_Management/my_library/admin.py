from django.contrib import admin

# Register your models here.
from .models import Publisher
from .models import Category
from .models import Book
from .models import Magazine
from .models import Newspaper
from .models import Receipent
from .models import Librarian
from .models import Issue

admin.site.register(Publisher)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Magazine)
admin.site.register(Newspaper)
admin.site.register(Receipent)
admin.site.register(Librarian)
admin.site.register(Issue)
