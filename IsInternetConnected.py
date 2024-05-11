import socket


def is_online():
    try:
        socket.gethostbyname("google.com")
        return True  # Online
    except OSError:
        pass
    return False  # Offline


# Test
# if is_online():
#     print("You're online!")
# else:
#     print("You're offline.")
