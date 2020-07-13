def validate_movie(movie):
    if (movie.title == '' or movie.release_date == ''):
        return False
    else:
        return True


def validate_actor(actor):
    if (actor.name == '' or actor.age == '' or actor.gender == ''):
        return False
    else:
        return True
    