import os
import numpy as np
from tkinter import *
from tkinter import ttk
from tkinter.font import Font

gradebook = {}
assignments = {}
assignments_no_cnr = {}
assignments_of_students = {}
students = {}


def get_list_grades(list_file, type, CRN):
    for each_file in list_file:
        with open(os.path.join(each_file), 'rt') as file:
            lines = file.readlines()
            lines = [line.strip().split('\t') for line in lines]
            for line in lines:
                if os.path.split(each_file)[-1][:-4] in gradebook[CRN][line[0]][type]:
                    gradebook[CRN][line[0]][type][os.path.split(each_file)[-1][:-4]].append(float(line[1]))
                else:
                    gradebook[CRN][line[0]][type][os.path.split(each_file)[-1][:-4]] = float(line[1])

                if os.path.split(each_file)[-1][:-4] in assignments[CRN]:
                    assignments[CRN][os.path.split(each_file)[-1][:-4]].append(float(line[1]))
                else:
                    assignments[CRN][os.path.split(each_file)[-1][:-4]] = [float(line[1])]

                if os.path.split(each_file)[-1][:-4] in assignments_no_cnr:
                    assignments_no_cnr[os.path.split(each_file)[-1][:-4]].append(float(line[1]))
                else:
                    assignments_no_cnr[os.path.split(each_file)[-1][:-4]] = [float(line[1])]

                if os.path.split(each_file)[-1][:-4] in assignments_of_students[line[0]]:
                    assignments_of_students[line[0]][os.path.split(each_file)[-1][:-4]].append(float(line[1]))
                else:
                    assignments_of_students[line[0]][os.path.split(each_file)[-1][:-4]] = float(line[1])


def generate_grade_book(CRN, roster_file_path, test_files, project_files, quiz_files):
    with open(roster_file_path, 'rt') as file:
        lines = file.readlines()
        lines = [line.strip().split('\t')[-1] for line in lines]

    for line in lines:
        gradebook[CRN][line] = {'Tests': {}, 'Quizzes': {}, 'Projects': {}, 'Weighted Grade': 0}
        assignments_of_students[line] = {}

    get_list_grades(test_files, 'Tests', CRN)
    get_list_grades(quiz_files, 'Quizzes', CRN)
    get_list_grades(project_files, 'Projects', CRN)

    for student in gradebook[CRN]:
        tests = list(gradebook[CRN][student]['Tests'].values())
        quizzes = list(gradebook[CRN][student]['Quizzes'].values())
        projects = list(gradebook[CRN][student]['Projects'].values())
        weighted_avg = np.mean(tests) * 0.3 + np.mean(quizzes) * 0.3 + np.mean(projects) * 0.4
        gradebook[CRN][student]['Weighted Grade'] = weighted_avg
        gradebook[CRN][student]['Test Median'] = np.median(tests)
        gradebook[CRN][student]['Quiz Median'] = np.median(quizzes)
        gradebook[CRN][student]['Project Median'] = np.median(projects)
        gradebook[CRN][student]['Test Mean'] = np.mean(tests)
        gradebook[CRN][student]['Quiz Mean'] = np.mean(quizzes)
        gradebook[CRN][student]['Project Mean'] = np.mean(projects)
        gradebook[CRN][student]['Test STD'] = np.std(tests)
        gradebook[CRN][student]['Quiz STD'] = np.std(quizzes)
        gradebook[CRN][student]['Project STD'] = np.std(projects)

        students[student] = gradebook[CRN][student]


def evaluate_folder(folder_path):
    sub_folders = [x[0] for x in os.walk(folder_path)]
    sub_folders = sub_folders[1:]
    for each_CRN in sub_folders:
        CRN = os.path.split(each_CRN)[-1]
        CRN = CRN.replace('crn', '')
        gradebook[CRN] = {}
        assignments[CRN] = {}
        project_list = []
        quiz_list = []
        test_list = []
        roster_path = ''
        each_file_in_each_CRN = [x for x in os.walk(each_CRN)][0][2]
        for sub_CRN_folder in each_file_in_each_CRN:
            if sub_CRN_folder[0] == 'r':
                roster_path = os.path.join(each_CRN, sub_CRN_folder)
            elif sub_CRN_folder[0] == 'P':
                project_list.append(os.path.join(each_CRN, sub_CRN_folder))
            elif sub_CRN_folder[0] == 'Q':
                quiz_list.append(os.path.join(each_CRN, sub_CRN_folder))
            elif sub_CRN_folder[0] == 'T':
                test_list.append(os.path.join(each_CRN, sub_CRN_folder))

        generate_grade_book(CRN, roster_path, test_list, project_list, quiz_list)
    return gradebook, assignments


# Get dicts with data from grade_book, already have access because of * import
# file_name = input('Enter file name with data: ')
# evaluate_folder(os.path.join('data', file_name))
evaluate_folder(os.path.join('data', 'course_grades'))

root = Tk()

# Creates title
root.title("Grade Book Data")
root.geometry("1000x700")

# tkinter vars created
tk1 = StringVar(root)
tk2 = StringVar(root)
tk3 = StringVar(root)

# Choices of a dropdown created, default set
choices_CRN = sorted([i for i in assignments.keys()])
choices_Students = list(dict.fromkeys(sum([[student for student in gradebook[crn]] for crn in gradebook], [])))
choices_Assignments = list(
    dict.fromkeys(sum([[assignment for assignment in assignments[crn]] for crn in assignments], [])))

tk1.set('None')
tk2.set('None')
tk3.set('None')

menuCRN = OptionMenu(root, tk1, *choices_CRN)  # Fix run config on INIT ERROR
menuStudents = ttk.Combobox(root, width=25, textvariable=tk2, values=choices_Students)
menuAssignments = ttk.Combobox(root, width=5, textvariable=tk3, values=choices_Assignments)

Label(root, text="Choose CRN").grid(row=0, column=1, padx=20)
Label(root, text="Choose Student").grid(row=0, column=2, padx=20)
Label(root, text="Choose Assignment").grid(row=0, column=3, padx=20)

titleFont = Font(family="Google", size=20)
title = Label(root, text='Grade Book Data', font=titleFont, cursor='dot', bg='blue', bd='8') \
    .grid(row=0, column=9, rowspan=7, padx=100)

menuCRN.grid(row=5, column=1, pady=10)
menuStudents.grid(row=5, column=2)
menuAssignments.grid(row=5, column=3)


def refreshCRN():
    tk1.set('None')
    text_box.grid_remove()
    y_scrollbar.grid_remove()
    change_dropdown1()
    change_dropdown2()


def refreshStudents():
    tk2.set('None')
    text_box.grid_remove()
    y_scrollbar.grid_remove()
    change_dropdown2()


def refreshAssignments():
    tk3.set('None')
    text_box.grid_remove()
    y_scrollbar.grid_remove()


btn1 = Button(root, text='reset', bd='5', command=refreshCRN)
btn1.grid(row=6, column=1)
btn2 = Button(root, text='reset', bd='5', command=refreshStudents)
btn2.grid(row=6, column=2)
btn3 = Button(root, text='reset', bd='5', command=refreshAssignments)
btn3.grid(row=6, column=3)

text_box = Text(root, width=100, wrap=WORD)
y_scrollbar = Scrollbar(root, orient=VERTICAL)
text_box.config(yscrollcommand=y_scrollbar.set)


def change_dropdown1(*args):
    if tk1.get() != "None":  # CRN has input
        menuStudents.config(values=list(gradebook[tk1.get()].keys()))
        menuAssignments.config(values=list(assignments[tk1.get()].keys()))
    else:  # CRN does not have input
        menuStudents.config(values=choices_Students)


def change_dropdown2(*args):
    if tk2.get() != "None":  # Student has input
        if tk1.get() == "None":  # and CRN does not have input
            menuAssignments.config(values=list(assignments_of_students[tk2.get()]))
        # menuStudents.config(values=list(gradebook[tk1.get()].keys()))

    elif tk2.get() == "None":  # Student does not have input
        menuAssignments.config(values=choices_Assignments)


types = {'T': 'Tests', 'Q': 'Quizzes', 'P': 'Projects'}


def search():
    text_box.delete('1.0', END)
    text = ''
    try:
        if tk1.get() != "None" and tk2.get() == "None" and tk3.get() == "None":  # Only CRN has input
            tests = []
            quizzes = []
            projects = []
            for assignment_type in assignments[tk1.get()]:
                text += 'Average grade for {} in CRN {}: '.format(assignment_type, tk1.get())
                text += str(np.mean(assignments[tk1.get()][assignment_type])) + '\n'
                type_assignment = assignment_type[0]
                print(type_assignment)
                if type_assignment == 'T':
                    tests.append(assignments[tk1.get()][assignment_type])
                elif type_assignment == 'Q':
                    quizzes.append(assignments[tk1.get()][assignment_type])
                elif type_assignment == 'P':
                    projects.append(assignments[tk1.get()][assignment_type])
            tests = sum(tests, [])
            quizzes = sum(quizzes, [])
            projects = sum(projects, [])
            text += "Average for tests for CRN {}: {}\n".format(tk1.get(), np.mean(tests))
            text += "Average for quizzes for CRN {}: {}\n".format(tk1.get(), np.mean(quizzes))
            text += "Average for projects for CRN {}: {}\n".format(tk1.get(), np.mean(projects))

            tot_weighted = 0

            for student in gradebook[tk1.get()]:
                tot_weighted += gradebook[tk1.get()][student]["Weighted Grade"]
            text += 'Overall Weighted Grade for CRN {}: {}'.format(tk1.get(), tot_weighted / len(gradebook[tk1.get()]))

        elif tk1.get() == "None" and tk2.get() != "None" and tk3.get() == "None":  # Only Student has input
            text += 'Data for {}\n'.format(tk2.get())
            for keys, items in students[tk2.get()].items():
                text += "{} - {}\n".format(keys, items)
        elif tk1.get() == "None" and tk2.get() == "None" and tk3.get() != "None":  # Only Assignment has input
            data = assignments_no_cnr[tk3.get()]
            text += 'Grades for {}:\n'.format(tk3.get())
            for grade in data:
                text += str(grade) + ' '
            text += '\nMean: {}\nMedian: {}\nSTD: {}\n'.format(
                np.mean(data), np.median(data), np.std(data)
            )
        elif tk1.get() == 'None' and tk2.get() != 'None' and tk3.get() != 'None':  # Student and Assignment have input
            text += 'Grade of {} for {}: {}'.format(tk3.get(), tk2.get(), assignments_of_students[tk2.get()][tk3.get()])
        elif tk1.get() != 'None' and tk2.get() == 'None' and tk3.get() != 'None':  # CRN and Assignment have input
            text += 'Average for {} in CRN {}: {}\n'.format(tk3.get(), tk1.get(),
                                                            np.mean(assignments[tk1.get()][tk3.get()]))
            text += 'Median for {} in CRN {}: {}\n'.format(tk3.get(), tk1.get(),
                                                           np.median(assignments[tk1.get()][tk3.get()]))
            text += 'STD for {} in CRN {}: {}\n'.format(tk3.get(), tk1.get(), np.std(assignments[tk1.get()][tk3.get()]))

            text += 'Grades for {} for CRN {}:\n'.format(tk3.get(), tk1.get())
            for each_grade in assignments[tk1.get()][tk3.get()]:
                text += '{}\n'.format(each_grade)
        elif tk1.get() != "None" and tk2.get() != "None" and tk3.get() == "None":  # CRN and Student have input
            text += 'Grades for {} who is in CRN {}:\n'.format(tk2.get(), tk1.get())
            for each_agn, grade in gradebook[tk1.get()][tk2.get()].items():
                text += '{}: {}\n'.format(each_agn, grade)
        elif tk1.get() != "None" and tk2.get() != "None" and tk3.get() != "None":  # All have input
            text += 'Grade for assignment {} for student {} who is in CRN {}:\n {}\n'.format(
                tk3.get(), tk2.get(), tk1.get(), gradebook[tk1.get()][tk2.get()][types[tk3.get()[0]]][tk3.get()]
            )
        else:
            text += 'Please enter a CRN, student, or assignment!'
    except KeyError:
        text += 'Invalid Combo - Try Selecting In this Order - CRN, Student, then Assignment!'
    text_box.insert(END, text)
    text_box.grid(row=7, column=1, columnspan=9, pady=100, sticky=NSEW)
    y_scrollbar.grid(row=7, column=1, columnspan=9, pady=100, sticky='NSE')


btn4 = Button(root, text='Search', bd='7', command=search)
btn4.grid(row=5, column=5, padx=15)

tk1.trace('w', change_dropdown1)
tk2.trace('w', change_dropdown2)

# Runs UI
root.mainloop()
