import copy
import heapq

# INPUT_FILE = "a_example.txt"
# OUTPUT_FILE = "solution_a.txt"

# INPUT_FILE = "b_read_on.txt"
# OUTPUT_FILE = "solution_b.txt"

INPUT_FILE = "c_incunabula.txt"
OUTPUT_FILE = "solution_c.txt"

# INPUT_FILE = "d_tough_choices.txt"
# OUTPUT_FILE = "solution_d.txt"

# INPUT_FILE = "e_so_many_books.txt"
# OUTPUT_FILE = "solution_e.txt"

# INPUT_FILE = "f_libraries_of_the_world.txt"
# OUTPUT_FILE = "solution_f.txt"


def write_output_to_file(sol_libs, lib_details):
    out_file = open(OUTPUT_FILE, "w")
    out_file.write(str(len(sol_libs)))
    out_file.write("\n")

    lines_to_write = []
    # seen_books = []

    for sl in sol_libs:
        curr_books = []
        for e in lib_details[sl]['books_held']:
            # if e not in seen_books:
            curr_books.append(e)
                # seen_books.append(e)
        lines_to_write.append(f"{sl} {len(curr_books)}\n")

        lines_to_write.append(' '.join(str(e[0]) for e in curr_books))
        lines_to_write.append("\n")
    out_file.writelines(lines_to_write)
    out_file.close()


def find_lib_to_sign_up(libs, days, lib_details, libs_done):
    # lib_number = -1
    # max_score = 0

    heap_li = []
    heap_mapping = {}
    check_set = set()

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

        # Replace by creating a heap to store the score for each and return it 
        if (-1*score) not in check_set:
            heap_li.append(-1 * score)
            heap_mapping[-1 * score] = []
            heap_mapping[-1 * score].append(i)
            check_set.add(-1*score)
        else:
            heap_li.append(-1 * score)
            heap_mapping[-1 * score].append(i)
        # if score > max_score:
        #     max_score = score
        #     lib_number = i

    return heap_li, heap_mapping
    # return lib_number


if __name__ == "__main__":
    f = open(INPUT_FILE, "r")
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

    # print(lib_details)

    f.close()

    days_left = copy.deepcopy(days)
    libs_copy = copy.deepcopy(libs)
    lib_details_copy = copy.deepcopy(lib_details)

    libs_done = []
    
    # while days_left and len(libs_done) != libs:
    #     lib_number = find_lib_to_sign_up(
    #         libs_copy, days_left, lib_details_copy, libs_done)
    #     if lib_number == -1:
    #         break
    #     days_left -= lib_details[lib_number]['signup_days']
    #     del lib_details_copy[lib_number]
    #     libs_done.append(lib_number)
        # print(lib_number)

    # New Mugdha
    heap_li, heap_mapping = find_lib_to_sign_up(libs_copy, days_left, lib_details_copy, libs_done)

    while days_left and len(libs_done) != libs and heap_li:
        heapq.heapify(heap_li)
        lib_score = heapq.heappop(heap_li)
        lib_number_list = heap_mapping[lib_score] 
        lib_number = lib_number_list[0]
        libs_done.append(lib_number)
        lib_number_list.remove(lib_number)

        days_left -= lib_details[lib_number]['signup_days']
    
    write_output_to_file(libs_done, lib_details)