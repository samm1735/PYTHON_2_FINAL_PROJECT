import socket


def is_online():
    try:
        # Try to establish a connection to Google's public DNS server
        socket.gethostbyname("google.com")
        return True  # If successful, you're online
    except OSError:
        pass
    return False  # Otherwise, you're offline


# Test the function
if is_online():
    print("You're online!")
else:
    print("You're offline.")
