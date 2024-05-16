from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden

from users.models import CustomUser
from .forms import BookForm


from .forms import AddReviewForm
from .models import Books, Review
from django.urls import reverse_lazy
# Create your views here.


class BookListView(View):
    def get(self, request):
        book = Books.objects.all().order_by('-id')
        return render(request, 'book/book_list.html', {'book': book})

# class BookListView(ListView):
#     model = Books
#     template_name = 'book/book_list.html'
#     context_object_name = 'book'

class BookDetailView(View):
    def get(self, request, pk):
        book = Books.objects.get(pk=pk)
        reviews = Review.objects.filter(book=pk)
        print(reviews)
        context = {
            'book': book,
            'reviews': reviews
        }
        return render(request, 'book_detail.html', context=context)





class BookCreateView(View):
    template_name = 'book/book_create.html'

    def get(self, request):
        form = BookForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:book-list')
        return render(request, self.template_name, {'form': form})



class BookDeleteView(DeleteView):
    model = Books
    template_name = 'book/book_delete.html'
    success_url = reverse_lazy('products:book-list')


from django.contrib import messages

class AddReviewView(LoginRequiredMixin, View):
    def get(self, request, pk):
        books = Books.objects.get(pk=pk)
        add_review_form = AddReviewForm()
        context = {
            'books': books,
            'add_review_form': add_review_form
        }
        return render(request, 'book/add_review.html', context=context)

    def post(self, request, pk):
        books = Books.objects.get(pk=pk)
        add_review_form = AddReviewForm(request.POST)
        if add_review_form.is_valid():
            review = Review.objects.create(
                comment=add_review_form.cleaned_data['comment'],
                book=books,
                user=request.user,
                star_given=add_review_form.cleaned_data['star_given']
            )
            review.save()

            # Add success message
            messages.success(request, 'Review added successfully!')

            return redirect('products:book-detail', pk=pk)



class BookUpdateView(View):
    def get(self, request, pk):
        book = Books.objects.get(pk=pk)
        form = BookForm(instance=book)
        return render(request, 'update.html', {'form': form, 'book': book})

    def post(self, request, pk):
        book = Books.objects.get(pk=pk)
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('products:book-detail', pk=pk)
        return render(request, 'update.html', {'form': form, 'book': book})



class ReviewUpdate(View):
    def get(self, request, pk):
        review = Review.objects.get(pk=pk)
        form = AddReviewForm(instance=review)
        if review.user != request.user:
            return HttpResponseForbidden("Siz boshqa userning izohini o'zgartira olmaysiz!")
        return render(request, 'review_update.html', {'form': form, 'review': review})

    def post(self, request, pk):
        review = Review.objects.get(pk=pk)
        form = AddReviewForm(request.POST, instance=review)
        if review.user != request.user:
            return HttpResponseForbidden("Siz boshqa userning izohini o'zgartira olmaysiz!")
        if form.is_valid():
            form.save()
            return redirect('products:book-detail', pk=review.book.pk)
        return render(request, 'review_update.html', {'form': form, 'review': review})


# class ReviewDelete(View):
#     def get(self, request, pk):
#         review = Review.objects.get(pk=pk)
#         book = review.book
#         return render(request, 'review_confirm_delete.html', {'review': review, 'book': book})
#
#     def post(self, request, pk):
#         review = Review.objects.get(pk=pk)
#         review.delete()
#
#
#         return redirect('products:book-detail', pk=review.book.pk)




class ReviewDelete(View):
    def get(self, request, pk):
        review = Review.objects.get(pk=pk)
        if review.user != request.user:
            return HttpResponseForbidden("Siz boshqa userning izohini o'chira olmaysiz!")
        return render(request, 'review_confirm_delete.html', {'review': review})

    def post(self, request, pk):
        review = Review.objects.get(pk=pk)
        if review.user != request.user:
            return HttpResponseForbidden("Siz boshqa userning izohini o'chira olmaysiz!")
        review.delete()
        return redirect('products:book-detail', pk=review.book.pk)












