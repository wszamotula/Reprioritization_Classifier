import urllib.request

def main():
    # TODO: Use search tags instead specific bug ID
    # TODO: Parsing of the JSON for ID of the bugs
    # TODO: Fetch the history and comment JSON for those bugs
    # TODO: Save all JSON to files, make sure file names match those in project already
    with urllib.request.urlopen('https://bugzilla.mozilla.org/rest/bug/35') as response:
        json = response.read()
        print(json)
    return

if __name__ == "__main__":
    main()