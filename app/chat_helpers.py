# from flask_socketio import join_room, leave_room
# from app import online_users as users
# """
# Adds a new user to global dictionary
#     username: Handle for this user
#     roomnane: Room of the user
#     sid: Session ID for the user
# """
# def add_user(username, roomname, sid):
#     user = {'name': username.upper(), 'room': roomname.upper(), 'sid': sid}
#     join_room(roomname)
#     users[sid] = user


# """
# Gets a user based on the session ID
#     sid: SID for the user
# """
# def get_user_by_sid(sid):
#     if sid in users:
#         return users[sid]
#     return None


# """
# gets a user based on user handle
#     name: Handle for this user
# """
# def get_user_by_name(name):
#     for key, value in users.items():
#         if value['name'] == name.upper():
#             return value
#     return None


# """
# Deletes a user from global dictionary
#     roomnane: Room of the user
#     sid: SID for the user
# """
# def del_user(sid, roomname):
#     elm = None
#     if sid in users:
#         elm = users[sid]
#         leave_room(roomname)
#         del users[sid]
#     return elm


# """
# Gets all users in a Room
#     roomnane: Room of the user
# """
# def get_all_users(roomname):
#     all_users = []
#     for key, value in users.items():
#         if value['room'] == roomname.upper():
#             all_users.append(value['name'])
#     return all_users 