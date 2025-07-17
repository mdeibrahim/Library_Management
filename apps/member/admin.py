from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Member, Book, Profile, Author, BorrowRecord

@admin.register(Member)
class MemberAdmin(ModelAdmin):
    list_display = ('id', 'email', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')

@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ('id', 'member', 'name', 'age', 'gender', 'address', 'phone')

@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = ('id', 'title', 'author', 'quantity', 'published_date', 'category', 'available')
    list_filter = ('available', 'category')

@admin.register(Author)
class AuthorAdmin(ModelAdmin):
    list_display = ('id', 'name', 'bio')

@admin.register(BorrowRecord)
class BorrowRecordAdmin(ModelAdmin):
    list_display = ('id', 'member', 'book', 'borrow_date', 'return_date')
    list_filter = ('borrow_date', 'return_date')
