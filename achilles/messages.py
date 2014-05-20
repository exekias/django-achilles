from django.contrib.messages import get_messages

from achilles import blocks

register = blocks.Library('messages')


def render(request):
    return [
        {
            'level': message.level,
            'message': message.message,
            'tags': message.tags,
            'extra_tags': message.extra_tags,
        }
        for message in get_messages(request)
    ]
