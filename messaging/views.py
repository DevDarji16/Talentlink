# messaging/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from users.models import UserProfile
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


@api_view(['GET'])
def list_conversations(request):
    current_user = request.user.profile
    convs = Conversation.objects.filter(participants=current_user).order_by('-updated_at')
    serializer = ConversationSerializer(convs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_or_create_conversation(request, user_id):
    current_user = request.user.profile
    try:
        other_user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if conversation exists
    conv = Conversation.objects.filter(participants=current_user).filter(participants=other_user).first()
    if not conv:
        conv = Conversation.objects.create()
        conv.participants.add(current_user, other_user)

    serializer = ConversationSerializer(conv)
    return Response(serializer.data)


# messaging/views.py
@api_view(['POST'])
def send_message(request):
    current_user = request.user.profile
    conversation_id = request.data.get('conversation')
    text = request.data.get('text', '').strip()

    if not text:
        return Response({"error": "Message cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        conv = Conversation.objects.get(id=conversation_id)
    except Conversation.DoesNotExist:
        return Response({"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)

    # Ensure sender is part of conversation
    if current_user not in conv.participants.all():
        return Response({"error": "You are not part of this conversation"}, status=status.HTTP_403_FORBIDDEN)

    msg = Message.objects.create(conversation=conv, sender=current_user, text=text)

    # 🔥 Update conversation preview
    conv.last_message = text
    conv.save(update_fields=['last_message', 'updated_at'])

    serializer = MessageSerializer(msg)
    return Response(serializer.data)


@api_view(['GET'])
def get_messages(request, conversation_id):
    current_user = request.user.profile
    try:
        conv = Conversation.objects.get(id=conversation_id)
    except Conversation.DoesNotExist:
        return Response({"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)

    if current_user not in conv.participants.all():
        return Response({"error": "You are not part of this conversation"}, status=status.HTTP_403_FORBIDDEN)

    messages = conv.messages.order_by('created_at')

    # 🔹 mark unread messages as read
    unread = messages.exclude(read_by=current_user)
    for msg in unread:
        msg.read_by.add(current_user)
        if conv.participants.count() == 2:  # 1-1 chat
            msg.is_read = True
            msg.save(update_fields=['is_read'])

    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)
