import re
import random

def add_to_list(file,watched=None):
    #reads the file as a list of lists, gets new movies appended to the list of lists,
    #organizes by title or by date and rewrites the file

    #not yet checked for watched

    print("\nHit enter to exit.")
    info = read_info(file)
    if file == "movies.txt":
        all_movies = info[1:]
        go = "Y"
        while go:
            movie,go = get_movie(file,all_movies)
            all_movies += movie
        all_movies = by_title(all_movies)
    elif file == "watched.txt":
        all_movies = info[1:] + [watched]
        all_movies = by_date(all_movies,file)
    else:
        all_movies = info
        print("Some error here.")
    write_file(file,all_movies,info[0])

def write_file(file, all_movies, header):
    lines = []
    for movie in all_movies:
        line = '\t'.join(movie)
        lines.append(line+"\n")
    with open(file,"w") as file:
        file.writelines(['\t'.join(header)] + lines)

def get_movie(filename,info,title=None):
    #takes in the file contents as a list of lists (to check the new movie is not already in), asks for new entry info,
    #turns the entry into a list and returns it and a parameter that can continue the while loop

    #not yet checked for watched

    if filename == "movies.txt":
        title = new_title(input("\nWhat is the title? "))
        if title == '' or title == '.':
            return [],None

        titles = [infos[0] for infos in info]
        if title.replace(' ','_') in titles:
            print(f"\n{title} is already in this list!")
            return [],None

    release_year = replace_with_dot(input(f"What year was {title} released? "))
    if not re.fullmatch(r'\d{4}|\.',release_year):
        print(f'\nPlease re-enter the info for {title} again.')
        return [],None
    genre = replace_with_dot(input("What is its genre? (If multiple genres, enter genre1, genre2, ...) "))
    rating = replace_with_dot(input("What is it rated? (enter nr for not rated) ").upper())
    length = replace_with_dot(input("How long is it? (in the format H:MM) "))
    notes = replace_with_dot(input("What notes do you have about this movie? "))
    if filename == "watched.txt":
        date_watched = replace_with_dot(input("Enter the date watched as YYYY-MM-DD (if some are unknown, enter them as ????-??-??): "))
        personal_rating = replace_with_dot(input("What rating do you give this movie? Enter to one decimal point out of 10: "))
        if not personal_rating == '.':
            if personal_rating.isdigit():         #assuming that '.' is not a digit
                personal_rating += ".0"
        if not re.fullmatch(r'(\d+\.\d)|\.',personal_rating) or not re.fullmatch(r'(\d|\?){4}-(\d|\?){2}-(\d|\?){2}|\.',date_watched):
            print("Please re-enter the info. Some error on Personal Rating or Date Watched.")
            return [],None
        notes = release_year + "_|_" + personal_rating + "/10_|_" + notes
        release_year = date_watched
    confirm = input("Confirm? ")

    if not confirm.upper() in ['Y','YES'] or not re.fullmatch(r'\.|G|PG|PG-13|R|NR',rating) or not re.fullmatch(r'\.|\d:\d\d',length):
        print(f'\nPlease re-enter the info for {title} again.')
        return [],None

    genres = genre.split(',')
    for i in range(len(genres)):
        genres[i] = genres[i].strip().title()
        if "Lgbtq" in genres[i]:
            genres[i] = genres[i].upper()
    genre = '/'.join(genres)

    print(f'{title} was successfully added!')
    return [[title.replace(' ','_'), release_year, genre, rating, length, notes.replace(' ','_')]],"Y"

def new_title(title):
    #takes in a string, returns my preferred Title format instead of using .title()
    no_caps = ["a","am","an","and","are","as","at","but","by","for","is","in","nor","of","on","or","the","to","with"]
    puncs = [".","!","?",":","-"]
    Title = title.title()
    chars = list(Title)
    for i in range(len(chars)-1):
        if chars[i] == "'":
            chars[i+1] = chars[i+1].lower()
    title = ''.join(chars)
    words = title.split()
    for i in range(1,len(words)-1):
        if words[i].lower() in no_caps and not words[i - 1][-1] in puncs:
            words[i] = words[i].lower()
    return ' '.join(words)

def replace_with_dot(param):
    if param == '':
        param = '.'
    return param

def pick(choice):
    print("""
Which list? Default is the Movies list
Movies list: Enter 1
Watched list: Enter 2""")
    pick = input('\n--> ')
    if pick != "2":
        file = "movies.txt"
    else:
        file = "watched.txt"
    if choice == 2:
        info = organize(read_info(file)[1:],file)
        print_list(file,info)
    elif choice == 4:
        infos = read_info(file)
        search_list(file,infos)
    elif choice == 6:
        check(file)
    else:
        print("Some error here.")

def print_list(filename,info):
    if filename == "movies.txt":
        headers = "\nTitle                    Release Year    Genre           Rating   Length   Notes"
    else:
        headers = "\nTitle                    Date Watched    Genre           Rating   Length   Notes"
    print(headers)
    print("-----------------------  --------------  --------------- -------- -------- ------------------------------")
    for lst in info:
        print(lst[0].replace('_',' ')[:24].ljust(24), lst[1].ljust(15), lst[2][:15].ljust(15), lst[3].ljust(8), lst[4].ljust(8), lst[5].replace('_',' '))
    print(f'\n\tNumber of entries: {len(info)}')

def mark_watched():

    #not yet tested

    watched = new_title(input("Which movie would you like to mark as watched? "))
    confirm = input(f"Confirm adding {watched} as watched? ")
    if not confirm.upper() in ["Y","YES"]:
        return

    watched_info = read_info("watched.txt")[1:]
    watched_titles = [info[0].replace('_',' ') for info in watched_info]
    if watched in watched_titles:
        print(f"\n{watched} has already been marked watched!")
        return

    movie_info = read_info("movies.txt")
    movies = movie_info[1:]
    movie_titles = [movie[0].replace('_',' ') for movie in movies]
    if watched in movie_titles:
        print(f'\nTransferring {watched} from Movies to Watched!')
        i = 0
        selected_movie = movies[i]
        while watched != selected_movie[0].replace('_', ' '):
            i += 1

        date_watched = replace_with_dot(input("Enter the date watched as YYYY-MM-DD (if some are unknown, enter them as ????-??-??): "))
        personal_rating = replace_with_dot(input("What rating do you give this movie? Enter to one decimal point out of 10: "))
        if not personal_rating == '.':
            if personal_rating.isdigit():  # since '.' is not a digit
                personal_rating += ".0"
        if not re.fullmatch(r'(\d+\.\d)|\.', personal_rating) or not re.fullmatch(r'(\d|\?){4}-(\d|\?){2}-(\d|\?){2}|\.', date_watched):
            print("Please re-enter the info. Some error on Personal Rating or Date Watched.")
            return

        notes = selected_movie[1] + "_|_" + personal_rating + "/10_|_" + selected_movie[5]
        watched_info = [watched.replace(" ","_"), date_watched, selected_movie[2], selected_movie[3], selected_movie[4], notes]

        movies.remove(selected_movie)
        write_file('movies.txt',movies,movie_info[0])
    else:
        watched_info,go = get_movie("watched.txt",watched_info,watched)
    add_to_list("watched.txt",watched_info)

def organize(info,file):
    #takes in a list of lists from the file, returns the list of lists organized by title, date, or rating
    print("""
How would you like it organized? Default is alphabetical for "movies", date watched for "watched".
For alphabetical: Enter 1
For chronological: Enter 2
For order by rating: Enter 3""")
    choice = input("\n--> ")
    if choice == "1":
        info = by_title(info)
        print("\nOrganized by title, alphabetically!")
    elif choice == "2":
        info = by_date(info,file)
        print("\nOrganized by date!")
    elif choice == "3":
        info = by_rating(info)
        print("\nOrganized by rating!")
    return info

def read_info(file):
    #returns all lines of the file as a list of lists (including header)
    with open(file) as file:
        lines = file.readlines()
    infos = []
    for line in lines:
        info = line.strip().split()
        infos.append(info)
    return infos

def by_title(list_of_lists):
    return sorted(list_of_lists,key=lambda x:x[0])

def by_date(list_of_lists,file):
    if file == "movies.txt":
        have_date = [lst for lst in list_of_lists if lst[1].isdigit()]
        no_date = [lst for lst in list_of_lists if not lst[1].isdigit()]
        have_date = sorted(have_date,key=lambda x:int(x[1]))
        return have_date + no_date

    elif file == "watched.txt":
        # I have yet to test this
        return sort_the_dates(list_of_lists,0)

def sort_the_dates(lists,selection):
    # I have yet to test this
    if selection == 2:
        have_date = [lst for lst in lists if lst[1].strip().split('-')[2].isdigit()]
        no_date = [lst for lst in lists if not lst[1].strip().split('-')[2].isdigit()]
        have_date = sorted(have_date, key=lambda x: int(x[1]))
        return have_date + no_date
    else:
        organized_movies = []
        timestamp = []
        for lst in lists:
            date = lst[1].strip().split('-')
            if date[selection] not in timestamp:
                timestamp.append(date[selection])

        if selection == 0:
            timestamp.remove("????")
            timestamp = sorted(timestamp,key=lambda x:int(x)) + ["????"]
        else:
            timestamp.remove("??")
            timestamp = sorted(timestamp,key=lambda x:int(x)) + ["??"]

        for time in timestamp:
            short_list = [lst for lst in lists if lst[1].strip().split('-')[selection] == time]
            organized_movies += sort_the_dates(short_list,selection+1)
        return organized_movies

def by_rating(list_of_lists):
    rates = ["G","PG","PG-13","R","NR","."]
    movie_list = []
    for rate in rates:
        for lst in list_of_lists:
            if lst[3] == rate:
                movie_list.append(lst)
    return movie_list

def search_list(filename,infos):
    print("\nHit enter to exit.")
    print("\nWhich category would you like to search?")
    i = 1
    for info in infos[0]:
        print(f'{info.replace('_',' ')}: Enter {i}')
        i += 1
    print("All categories? Enter 7")
    pick = input('\n--> ')
    if pick in ['1','2','3','4','5']:
        item = input(f'\nVery well. What would you like to search for in {infos[0][int(pick)-1].replace('_',' ')}? ')
    elif pick == '6':
        item = input('\nVery well. What would you like to search for in Notes? ')
    elif pick == '7':
        item = input('\nVery well. What would you like to search for? ')
    elif pick == '':
        return
    else:
        print("Wrong input, try again.")
        return
    movies = []
    if int(pick) in range(1,7):
        for info in infos[1:]:
            if item in info[int(pick)-1].replace('_',' '):
                movies.append(info)
    elif pick == '7':
        for info in infos[1:]:
            for subinfo in info:
                if item in subinfo.replace('_',' '):
                    movies.append(info)
    print_list(filename,movies)
    search_list(filename,[infos[0]]+movies)

def random_select(file):
    #randomly selects a movie from movies.txt, prints the info, offers to select a different one
    info = read_info(file)
    movie = random.choice(info)
    
    print(f"\nThe randomly selected movie is:
\t'{movie[0].replace("_"," ")}'
\t{movie[1]}\t{movie[3]}\t{movie[2]}\t{movie[4]}
\tNotes: {movie[5].replace("_"," ")}
\nWould you like a different selection?")

    choice = input("Y/N: ")
    if choice.upper() in ['Y','YES']:
        random_select(file)

def check(file):
    #resets the movie titles and re-organizes the list by title or by date
    infos = read_info(file)
    for info in infos[1:]:
        title = info[0].replace('_'," ")
        info[0] = new_title(title).replace(" ","_")
    all_movies = infos[1:]
    if file == "movies.txt":
        all_movies = by_title(all_movies)
    elif file == "watched.txt":
        all_movies = by_date(all_movies,"watched.txt")
    write_file(file,all_movies,infos[0])
    print("Check successful!")

if __name__ == "__main__":
    choice = "0"
    while choice != "":
        if choice == "1":
            add_to_list("movies.txt")
        elif choice == "2":
            pick(2)
        elif choice == "3":
            mark_watched()
        elif choice == "4":
            pick(4)
        elif choice == "5":
            random_select("movies.txt")
        elif choice == "6":
            pick(6)
        print("""
To add to the list: Enter 1
To print a list: Enter 2
To mark a movie as watched: Enter 3
To search a list: Enter 4
To randomly select a movie to watch: Enter 5 
To check the list: Enter 6
To exit: Hit Enter\n""")
        choice = input("--> ")
    print("\nGoodbye!")


