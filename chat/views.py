from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Room, Message, ChatUser
from accounts.models import TTUser
from django.db.models import Q
from django.contrib.auth.decorators import login_required



def get_conversations(user):
    rooms = Room.objects.filter(Q(owner__TTUser=user) | Q(participant__TTUser=user)).order_by('-last_message_at')
    conversations = []
    for room in rooms:
        other = room.participant if room.owner.TTUser_id == user.id else room.owner
        last_message = Message.objects.filter(room=room).order_by('-created_at').first()
        if last_message:
            last_message_at = last_message.created_at
            last_message_content = last_message.content[:50]
        else:
            last_message_at = room.last_message_at
            last_message_content = ''
        conversations.append({
            'room': room,
            'other': other,
            'last_message_at': last_message_at,
            'last_message_content': last_message_content,
        })
    return conversations
    
@login_required
def index(request):
    # if logged in user is not a ChatUser, Create a new ChatUser
    if not ChatUser.objects.filter(TTUser=request.user).exists():
        ChatUser.objects.create(TTUser=request.user)
    # if logged in user is a ChatUser, get the conversations
    conversations = get_conversations(request.user)
    template_data = {}
    template_data['title'] = 'Chat'
    template_data['conversations'] = conversations
    return render(request, 'chat/index.html', {'template_data': template_data})




@login_required
def room(request, room_id):
    
    template_data = {}
    # if logged in user is not a ChatUser, Create a new ChatUser
    if not ChatUser.objects.filter(TTUser=request.user).exists():
        ChatUser.objects.create(TTUser=request.user)
    # if logged in user is a ChatUser, get the conversations
    conversations = get_conversations(request.user)
    template_data['title'] = 'Chat'
    template_data['conversations'] = conversations
    template_data['room_id'] = room_id
    # get the room. if the room does not exist, redirect to the index page.
    room = get_object_or_404(Room, id=room_id)
    if room.owner.TTUser_id != request.user.id and room.participant.TTUser_id != request.user.id:
        return redirect('chat.index')
    other = room.participant if room.owner.TTUser_id == request.user.id else room.owner
    template_data['other'] = other
    messages = Message.objects.filter(room=room).order_by('created_at')
    template_data['messages'] = messages   
    
    return render(request, 'chat/index.html', {'template_data': template_data})

@login_required
def send_message(request, room_id):
    if request.method == 'POST':
        content = request.POST.get('message', '')
        if not content:
            return redirect('chat.room', room_id=room_id)
        room = get_object_or_404(Room, id=room_id)
        try:
            chat_user = ChatUser.objects.get(TTUser=request.user)
        except ChatUser.DoesNotExist:
            return redirect('chat.index')
        if room.owner_id != chat_user.id and room.participant_id != chat_user.id:
            return redirect('chat.index')
        Message.objects.create(room=room, chat_user=chat_user, content=content)
        room.last_message_at = timezone.now()
        room.save(update_fields=['last_message_at'])
        return redirect('chat.room', room_id=room_id)
    return redirect('chat.index')

@login_required
def create_room(request, participant_id):
    """Create or get a room with the given participant. Creates ChatUser for both if needed."""
    participant = get_object_or_404(TTUser, id=participant_id)
    current_chat_user, _ = ChatUser.objects.get_or_create(TTUser=request.user)
    participant_chat_user, _ = ChatUser.objects.get_or_create(TTUser=participant)
    if current_chat_user.id == participant_chat_user.id:
        return redirect('chat.index')
    existing_room = Room.objects.filter(
        Q(owner=current_chat_user, participant=participant_chat_user) |
        Q(owner=participant_chat_user, participant=current_chat_user)
    ).first()
    if existing_room:
        return redirect('chat.room', room_id=existing_room.id)
    room = Room.objects.create(
        owner=current_chat_user,
        participant=participant_chat_user
    )
    return redirect('chat.room', room_id=room.id)