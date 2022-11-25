from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Post, Like
from profiles.models import Profile
from .forms import PostModelForm, CommentModelForm
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here. 
@login_required
def post_comment_create_and_list_view(request):
    posts = Post.objects.prefetch_related('liked')
    profile = Profile.objects.get(user=request.user)

    # Valores iniciais 
    p_form = PostModelForm()
    c_form = CommentModelForm()

    if 'submit_p_form' in request.POST:
        p_form = PostModelForm(request.POST, request.FILES)
        if p_form.is_valid():
            instance = p_form.save(commit=False)
            instance.author = profile
            instance.save()
            # reseta o form
            p_form = PostModelForm()

        return redirect('posts:main-post-view')

    if 'submit_c_form' in request.POST:
        c_form = CommentModelForm(request.POST)
        if c_form.is_valid():
            instance = c_form.save(commit=False)
            instance.user = profile
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            # reseta o form
            c_form = CommentModelForm()

        return redirect('posts:main-post-view')

    context = {
        'posts': posts,
        'profile': profile,
        'p_form': p_form,
        'c_form': c_form,
    }

    return render(request, 'posts/main.html', context)


@login_required
def like_unlike_post(request):
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        profile = Profile.objects.select_related('user').get(user=user)

        # Verifica se o perfil já deu Like na postagem(ManyToManyField)
        if profile in post_obj.liked.all():
            post_obj.liked.remove(profile)
        else:
            post_obj.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post_id=post_id)
    
        if not created:
            if like.value == "Like":
                like.value = "Unlike"
            else:
                like.value = "Like"
        else:
            like.value = "Like"

        post_obj.save()
        like.save()

        data = {
            'value': like.value,
            'likes': post_obj.liked.all().count(),

        }
        
        return JsonResponse(data, safe=False)

    return redirect('posts:main-post-view')



class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/confirm_del.html'
    success_url = reverse_lazy('posts:main-post-view')
    # success_url = '/posts/'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, "Você precisa ser o autor para apagar esse post.")

        return obj


class PostUpdateView(LoginRequiredMixin, UpdateView):
    form_class = PostModelForm
    model = Post
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:main-post-view')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        # Caso a pessoa que está editando não seja o autor, lança um erro
        else:
            form.add_error(None, "Você precisa ser o autor para atualizar esse post.")
            return super().form_invalid(form)