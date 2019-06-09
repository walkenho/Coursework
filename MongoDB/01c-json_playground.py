# To experiment with this code freely you will have to run this code locally.
# Take a look at the main() function for an example of how to use the code.
# We have provided example json output in the other code editor tabs for you to
# look at, but you will not be able to run any queries through our UI.
import json
import requests


BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

# query parameters are given to the requests.get function as a dictionary; this
# variable contains some starter parameters.
query_type = {  "simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"}}


def query_site(url, params, uid="", fmt="json"):
    # This is the main function for making queries to the musicbrainz API.
    # A json document should be returned by the query.
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print "requesting", r.url

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    # This adds an artist name to the query parameters before making
    # an API call to the function above.
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    # After we get our output, we can format it to be more readable
    # by using this function.
    if type(data) == dict:
        print json.dumps(data, indent=indent, sort_keys=True)
    else:
        print data


def main():
    '''
    Modify the function calls and indexing below to answer the questions on
    the next quiz. HINT: Note how the output we get from the site is a
    multi-level JSON document, so try making print statements to step through
    the structure one level at a time or copy the output to a separate output
    file.
    '''

#### Example:
    #results = query_by_name(ARTIST_URL, query_type["simple"], "Nirvana")
    #pretty_print(results)

    #artist_id = results["artists"][1]["id"]
    #print "\nARTIST:"
    #pretty_print(results["artists"][1])

    #artist_data = query_site(ARTIST_URL, query_type["releases"], artist_id)
    #releases = artist_data["releases"]
    #print "\nONE RELEASE:"
    #pretty_print(releases[0], indent=2)
    #release_titles = [r["title"] for r in releases]

    #print "\nALL TITLES:"
    #for t in release_titles:
    #    print t

### How many bands named "First-Aid Kit"?
    results = query_by_name(ARTIST_URL, query_type["simple"], "First-Aid Kit")
    i = 0
    for entry in results["artists"]:
        if entry["name"].lower() == "First Aid Kit".lower():
            i += 1
    print "\nNumber of bands names First-Aid Kit: %d" %i

### Begin Area Name for Queen?
    results = query_by_name(ARTIST_URL, query_type["simple"], "Queen")
    #checking if the first one is the band that we are looking for:
    #pretty_print(results["artists"][0])
    #artist_id = results["artists"][0]["id"]
    #artist_data = query_site(ARTIST_URL, query_type["releases"], artist_id)
    #releases = artist_data["releases"]
    #release_titles = [r["title"] for r in releases]
    #print "\nALL TITLES:"
    #for t in release_titles:
    #    print t
    # Ok, it is the right group. 
    print "\nThe Begin Area Name for Queen is %s" %results["artists"][0]["begin-area"]["name"]

### Spanish Alias for Beatles?
    results = query_by_name(ARTIST_URL, query_type["simple"], "Beatles")
    #pretty_print(results)
    # Check, which beatles are the group, that we are looking for:
    for index in range(len(results)+1):
        artist_id = results["artists"][index]["id"]
        artist_data = query_site(ARTIST_URL, query_type["releases"], artist_id)
        releases = artist_data["releases"]
        release_titles = [r["title"] for r in releases]
        print "\nALL TITLES:"
        for t in release_titles:
            print t
    # -> The Beatles, that we are looking for is the first group.
    print "\nALIASES:"
    for alias in results["artists"][0]["aliases"]:
        print alias["locale"], alias["name"] 
    print "\nThe alias of the Beatles in Spain is %s" %results["artists"][0]["aliases"][8]["name"]

### Nirvana Disambiguation?
    results = query_by_name(ARTIST_URL, query_type["simple"], "Nirvana")
    disambiguation = results["artists"][0]["disambiguation"]
    print "\nDisambiguation for Nirvana: %s" %disambiguation

### When was One Direction formed?
    results = query_by_name(ARTIST_URL, query_type["simple"], "One Direction")
    #pretty_print(results)
    begin = results["artists"][0]["life-span"]["begin"]
    print "\nOne Direction was formed %s" %begin



if __name__ == '__main__':
    main()

