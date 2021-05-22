import json

from services import users_register_login_create_posts, users_do_likes


def main():
    with open('bot_config.json') as f:
        config = json.load(f)

    NUMBER_OF_USERS = config.get("number_of_users")
    MAX_POSTS_PER_USER = config.get("max_posts_per_user")
    MAX_LIKES_PER_USER = config.get("max_likes_per_user")

    users_state = users_register_login_create_posts(
        count_users=NUMBER_OF_USERS,
        max_count_posts=MAX_POSTS_PER_USER
    )

    users_do_likes(users_state=users_state, max_count_likes=MAX_LIKES_PER_USER)


if __name__ == "__main__":
    main()
