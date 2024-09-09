from etl.models import Post


def transform_data(posts: list) -> list[Post]:
    transformed_data = []

    for post in posts:
        transformed_data.append(Post(**post))

    return transformed_data
