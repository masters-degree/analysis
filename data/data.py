import csv
from os import path

departmentInformation = []
studentCouncelingInformation = []
employeeInformation = []
studentPerformance = []
studentPerformanceV2 = []


with open(path.join(path.dirname(__file__), 'Department_Information.csv'), 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        departmentInformation.append(row)


with open(path.join(path.dirname(__file__), 'Student_Counceling_Information.csv'), 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        studentCouncelingInformation.append(row)


with open(path.join(path.dirname(__file__), 'Employee_Information.csv'), 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        employeeInformation.append(row)


with open(path.join(path.dirname(__file__), 'Student_Performance_Data.csv'), 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        studentPerformance.append(row)

with open(path.join(path.dirname(__file__), 'new_data.csv'), 'r') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        studentPerformanceV2.append(row)

if __name__ == '__main__':
    with open(path.join(path.dirname(__file__), 'new_data.csv'), 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        newData = []
        for row in reader:
            newData.append({
                "id": row['id'],
                "sub1": row['math score'],
                "sub2": row['reading score'],
                "sub3": row['writing score'],
            })

        newDatav2 = []
        for index, student in enumerate(newData):
            if index % 8 == 0 or index == 0:
                newDatav2.append([student])
            else:
                newDatav2[-1].append(student)


        for index, students in enumerate(newDatav2):
            marks = []
            for student in students:
                marks = [*marks, *list(student.values())[1:]]

            newStudent = {
                'id': index,
            }

            for markIndex, mark in enumerate(marks):
                newStudent.setdefault(f'sub{markIndex + 1}', mark)

            newDatav2[index] = newStudent

        currentGroupPopulation = 0
        for index, student in enumerate(newDatav2):
            currentGroup = newDatav2[index - 1]['group'] if not index == 0 else 1

            currentGroupPopulation += 1

            newDatav2[index] = {
                **newDatav2[index],
                'group': currentGroup if not currentGroupPopulation > 50 else currentGroup + 1
            }

            currentGroupPopulation = 0 if currentGroupPopulation > 50 else currentGroupPopulation

        with open(path.join(path.dirname(__file__), 'new-performance.csv'), 'w', newline='') as newCsvfile:
            writer = csv.DictWriter(newCsvfile, fieldnames=newDatav2[0].keys())
            writer.writeheader()

            for student in newDatav2:
                writer.writerow(student)

