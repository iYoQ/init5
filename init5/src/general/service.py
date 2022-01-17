def change_or_add_users_changed_rating(serializer, instance, validated_data):
    user = serializer.context['request'].user
    get_request_rating = validated_data.get('rating', instance.rating)

    if current_user_exist := instance.users_changed_rating.get(user.username):
        if current_user_exist['value'] == get_request_rating:
            return serializer.fail('alredy_exists')

        instance.rating -= current_user_exist['value']
        current_user_exist['value'] = get_request_rating

    else:
        instance.users_changed_rating[user.username] = {
            'url': user.url,
            'value': get_request_rating
        }

    instance.rating += get_request_rating
