from concurrent.futures import ProcessPoolExecutor
import copy


def return_score(i, lib_details, days):
    days_left = days - lib_details[i]['signup_days']
    total_books_can_be_shipped = days_left * lib_details[i]['ship_per_day']
    score = 0
    j = 0

    while total_books_can_be_shipped and j < len(lib_details[i]['books_held']):
        score += lib_details[i]['books_held'][j][1]
        j += 1
        total_books_can_be_shipped -= 1
    
    score_lib = []
    score_lib.append(i)
    score_lib.append(score)
    return score_lib


def find_lib_to_sign_up(libs, days, lib_details, libs_done):
    lib_number = -1
    max_score = 0

    i_list = list(i for i in range(libs) if i not in libs_done)
    # print(i_list)
    # Make 60 on Jarvis
    # with ProcessPoolExecutor(max_workers=60) as executor:
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = executor.map(return_score, i_list, lib_details, days)
        for result in results:
            print(result)

    for i in range(libs):
        if i in libs_done:
            continue
        days_left = days - lib_details[i]['signup_days']
        total_books_can_be_shipped = days_left * lib_details[i]['ship_per_day']
        score = 0
        j = 0

        while total_books_can_be_shipped and j < len(lib_details[i]['books_held']):
            score += lib_details[i]['books_held'][j][1]
            j += 1
            total_books_can_be_shipped -= 1

        if score > max_score:
            max_score = score
            lib_number = i

    return lib_number


def write_output_to_file(sol_libs, lib_details):
    books_done_set = []

    out_file = open("solution.txt", "w")
    out_file.write(str(len(sol_libs)))
    out_file.write("\n")
    for sl in sol_libs:
        out_file.write(f"{sl} {len(lib_details[sl]['books_held'])}")
        out_file.write("\n")

        flag_first = True
        for e in lib_details[sl]['books_held']:
            if e[0] not in books_done_set:
                books_done_set.append(e[0])
                if flag_first:
                    flag_first = False
                    write_string = str(e[0])
                else:
                    write_string = ' ' + str(e[0])
                out_file.write(write_string)

        out_file.write("\n")
    out_file.close()


if __name__ == "__main__":
    f = open("a_example.txt", "r")
    line = f.readline().split()
    books = int(line[0])
    libs = int(line[1])
    days = int(line[2])

    scores = f.readline().split()
    scores = [int(s) for s in scores]

    lib_details = {}

    for i in range(libs):
        curr_details = f.readline().split()
        books_held = f.readline().split()
        lib_details[i] = {
            "num_books": int(curr_details[0]),
            "signup_days": int(curr_details[1]),
            "ship_per_day": int(curr_details[2]),
            "books_held": [[int(b), scores[int(b)]] for b in books_held]
        }
        lib_details[i]['books_held'] = sorted(
            lib_details[i]['books_held'], key=lambda x: x[1], reverse=True)

    print(lib_details)

    f.close()

    days_left = copy.deepcopy(days)
    libs_copy = copy.deepcopy(libs)
    lib_details_copy = copy.deepcopy(lib_details)
    libs_done = []
    while days_left and len(libs_done) != libs:
        lib_number = find_lib_to_sign_up(
            libs_copy, days_left, lib_details_copy, libs_done)
        if lib_number == -1:
            break
        days_left -= lib_details[lib_number]['signup_days']
        del lib_details_copy[lib_number]
        libs_done.append(lib_number)
        print(lib_number)

    write_output_to_file(libs_done, lib_details)
