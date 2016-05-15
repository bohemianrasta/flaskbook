from flask import Blueprint, abort, session

from user.models import User
from relationship.models import Relationship
from user.decorators import login_required

relationship_app = Blueprint('relationship_app', __name__)

@relationship_app.route('/add_friend/<to_username>', methods=('GET', 'POST'))
@login_required
def add_friend(to_username):
    logged_user = User.objects.filter(username=session.get('username')).first()
    to_user = User.objects.filter(username=to_username).first()
    if to_user:
        rel = Relationship.get_relationship(logged_user, to_user)
        if rel == "FRIENDS_PENDING":
            return rel
        elif rel == "BLOCKED":
            return rel
        elif rel == None:
            Relationship(
                from_user=logged_user, 
                to_user=to_user, 
                rel_type=Relationship.FRIENDS, 
                status=Relationship.PENDING
                ).save()
            return "FRIENDSHIP_REQUESTED"
        else:
            return to_user.username
    else:
        abort(404)