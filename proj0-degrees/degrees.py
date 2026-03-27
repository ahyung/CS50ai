import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")

def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.

    - no dupes in people.movies and movies.stars because python set() dedupes
    - people and movies are python Dictionaries
    - how does people[ source ] where source is the number work?  is the first element the key in the dict?
    - there are cycles in the graph created by neighbors
    """

    # handle edge case
    if (source == target):
        return []

    Q = QueueFrontier()
    n = Node(source, None, None)
    Q.add(n) # use State as the node's people_id

    # list of people_ids that have been visited/checked
    visited = dict()
    visited[source] = n

    # keepTrackOfExploredSet, then iterate parents of explored set to find the path from target back to source

    found = None

    while Q:
        if (Q.empty()): # "while Q" is a null/None check, need an empty queue check - should put this in while condition instead
            break

        curr = Q.remove()

        currPerson = curr.state
        if (currPerson == target):
            found = currPerson
            break

        neighbors = neighbors_for_person(currPerson)
        for p in neighbors:
            if (p[1] == source): # handle the cycles in graph
                continue
            if (p[1] in visited):
                continue

            n = Node(p[1],currPerson,p)
            visited[p[1]] = n
            Q.add(n)

    """
    print ("\n")
    for key in visited:
        print (key)
        print (visited[key].state)
        print (visited[key].parent)
        print (visited[key].action)
        print ("\n")
    """

    out = [];

    if (found): # is not None
        out.insert( 0, visited[found].action)
        pnode = visited[found].parent
        while (pnode):
            e = visited[pnode].action
            if (e):
                out.insert( 0, visited[pnode].action)
            pnode = visited[pnode].parent

    #print ( "out: ")
    #print ( out )

    if (out != []):
        return out
    else:
        return None

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
