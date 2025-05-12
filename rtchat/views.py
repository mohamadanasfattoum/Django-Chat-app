from django.shortcuts import render, get_object_or_404, redirect
from .models import ChatGroup
from django.contrib.auth.decorators import login_required
from .forms import ChatmessageCreateForm
from django.contrib.auth.models import User
from django.http import Http404



@login_required
def chat_view(request, chatroom_name='public-chat'):
    chat_group = get_object_or_404(ChatGroup, group_name = chatroom_name)  # Get the chat group
    chat_messages = chat_group.chat_messages.all()[:30]  # Get all messages for the group, chat_messages is a related name for the GroupMessages model and ChatGroup model to get all messages related to the group
    form = ChatmessageCreateForm()  # Create a form instance for sending messages
    
    other_user=None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break


    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False) # Create a new message instance but don't save it to the database yet
            # Set the group and author fields before saving
            message.author = request.user
            message.group = chat_group
            message.save()
            context = {
                'message' : message,
                'user' : request.user,  
            }
            return render(request, 'rtchat/partials/chat_message_p.html', context)  # Redirect to the same page after sending a message
    context = {
        'chat_messages': chat_messages,
        'form': form,
        'other_user': other_user,
        'chatroom_name': chatroom_name,
        
    }
    return render(request, 'rtchat/chat.html', context)  # Render the chat page with the context data
# The chat_view function is a Django view that handles the chat functionality. It retrieves the chat group and its messages, and renders them in the 'chat.html' template.
# The @login_required decorator ensures that only authenticated users can access the chat view. If a user is not logged in, they will be redirected to the login page.
# The get_object_or_404 function is used to retrieve the chat group object from the database. If the object does not exist, a 404 error will be raised.
# The chat_messages variable retrieves the last 30 messages from the chat group using the related name 'chat_messages' defined in the GroupMessages model.
# The render function is used to render the 'chat.html' template with the chat group and messages as context.
# The chat.html template will display the chat group name and the messages in the chat.

@login_required
def get_or_create_chatroom(request, username):
    # Check if the user is authenticated
    if request.user.username == username:
        return redirect('home') # Redirect to the home page if the user is trying to access their own chatroom
    
    other_user = User.objects.get(username=username)  # Get the other user by username
    my_chatrooms = request.user.chat_groups.filter(is_private=True)  # Get the chatrooms where the user is a member

    if my_chatrooms.exists():
        for chatroom in my_chatrooms:
            if other_user in chatroom.members.all():
                chatroom = chatroom
                break
            else:
                chatroom = ChatGroup.objects.create(is_private=True)
                chatroom.members.add(request.user, other_user)
    else:
        chatroom = ChatGroup.objects.create(is_private=True)
        chatroom.members.add(other_user,request.user)


    return redirect('chatroom', chatroom.group_name)  # Redirect to the chatroom page