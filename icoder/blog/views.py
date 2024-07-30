from django.shortcuts import render,HttpResponse,redirect
from .models import Post,BlogComment
from django.contrib import messages

# Create your views here.
def bloghome(request):
    allpost=Post.objects.all()
    print(allpost)
    context = {
        "allpost" :allpost
        }
    return render(request,'blog/bloghome.html', context)

def blogpost(request,slug):
    post=Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post)
    print(request.user)
    context={"post":post, 'comments':comments,'user':request.user}
    return render(request,'blog/blogpost.html',context)




def postcomment(request):
    if request.method=="POST":
        comment = request.POST.get('comment')
        user = request.user
        postsno = request.POST.get('postsno')
        post = Post.objects.get(sno=postsno)

        comment= BlogComment(comment=comment, user=user, post=post)
        comment.save()
        messages.success(request,"your comment has been posted successfully")


    return redirect(f'/blog/{post.slug}')



