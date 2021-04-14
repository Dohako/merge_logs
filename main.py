
file_name = 'result_1.jsonl'
log_1 = '.\\logs\\log_a.jsonl'
log_2 = '.\\logs\\log_b.jsonl'
# with open(log_1, 'r') as file:
#     p = file.readlines(1)
#     print(p)

file_log_a = open(log_1,'r')
file_log_b = open(log_2,'r')
result_file = open(file_name, 'w')
# while
first = file_log_a.readlines()
string_to_search = 'timestamp": "'
# if string_to_search in first[1]:
#     print(first[1].split(string_to_search)[1].split('"')[0])
# first_date = datetime.datetime.strptime(first[1].split(string_to_search)[1].split('"')[0], "%Y-%m-%d %H:%M:%S")
# second_date = datetime.datetime.strptime(first[2].split(string_to_search)[1].split('"')[0], "%Y-%m-%d %H:%M:%S")
# print(first_date > second_date)
second = file_log_b.readlines()

trigger = True
i, j = 0, 0
end_first_file = False
end_second_file = False
string_from_first = None
string_from_second = None
take_first = True
take_second = True
while trigger:
    if end_first_file is False and take_first:
        try:
            string_from_first = first[i]
            i += 1
        except IndexError:
            end_first_file = True
            string_from_first = None
        take_first = False
    if end_second_file is False and take_second:
        try:
            string_from_second = second[j]
            j += 1
        except IndexError:
            end_second_file = True
            string_from_second = None
        take_second = False
    if end_second_file and end_first_file:
        trigger = False # It can be done without trigger, but still
        break
    if string_from_first is None:
        result_file.write(string_from_second)
        take_second = True
        continue
    if string_from_second is None:
        result_file.write(string_from_first)
        take_first = True
        continue

    if string_to_search in string_from_first:
        first_timestamp = string_from_first.split(string_to_search)[1].split('"')[0]
    else:
        take_first = True
        continue
    if string_to_search in string_from_second:
        second_timestamp = string_from_second.split(string_to_search)[1].split('"')[0]
    else:
        take_second = True
        continue
    if first_timestamp > second_timestamp:
        result_file.write(string_from_second)
        take_second = True
    elif first_timestamp == second_timestamp:
        result_file.write(string_from_first)
        result_file.write(string_from_second)
        take_second, take_first = True, True
    elif first_timestamp < second_timestamp:
        result_file.write(string_from_first)
        take_first = True


result_file.close()
file_log_a.close()
file_log_b.close()