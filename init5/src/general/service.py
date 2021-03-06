from ..users.models import User
from django.db.models import F

def change_or_add_users_changed_rating(serializer, instance, validated_data):
    current_user = serializer.context['request'].user
    get_request_rating = validated_data.get('rating', instance.rating)
    author = User.objects.filter(pk=instance.author.pk)

    if current_user_exist := instance.users_changed_rating.get(current_user.username):
        if current_user_exist['value'] == get_request_rating:
            return serializer.fail('alredy_exists')

        instance.rating -= current_user_exist['value']
        author.update(rating=F('rating') - current_user_exist['value'])

        current_user_exist['value'] = get_request_rating

    else:
        instance.users_changed_rating[current_user.username] = {
            'url': current_user.get_absolute_url(),
            'value': get_request_rating
        }

    instance.rating += get_request_rating
    author.update(rating=F('rating') + get_request_rating)
