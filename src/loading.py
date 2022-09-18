def loading_spinner():
    while True:
        for cursor in "|/-\\":
            yield cursor
