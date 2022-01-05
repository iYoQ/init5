def check_or_add_users_changed_rating(serializer, instance, user, new_user_rating, coefficient):
    if current_user_dict := instance.users_changed_rating.get(user.username):
        if current_user_dict['value'] == new_user_rating:
            return serializer.fail('alredy_exists')

        instance.rating -= current_user_dict['value']*coefficient
        current_user_dict['value'] = new_user_rating

    else:
        instance.users_changed_rating[user.username] = {
            'url': user.url,
            'value': new_user_rating
        }