from models import User, Idea


def count_ideas_of_user():
    return db.session.query((User, db.func.count(Idea.id))).outerjoin(Idea).group_by(User.id).all()


def user_with_max_number_of_idea():
    return db.session.query(User, db.func.count(Idea.id), db.func.max(db.func.count(Idea.id))).outerjoin(Idea).group_by(User.id).all()


def get_idea_by_word():
    return Idea.query.filter(Idea.activity.contains('listen')).all()


def get_users_by_more_than_5_ideas():
    return User.query.join(Idea).group_by(User.id).having(db.func.count(Idea.id) > 5).all()


def update_name():
    user = User.query.get(1)
    if user:
        user.name = 'New Name'
    return db.session.commit()


def delete_idea_with_word():
    ideas = Idea.query.filter(Idea.activity.contains('play')).all()
    for idea in ideas:
        db.session.delete(idea)
    return db.session.commit()


if __name__ == "__main__":
    from app import db, app

    with app.app_context():
        result = delete_idea_with_word()
        print(result)
