from datetime import date, timedelta
from random import Random

from app.database import Base, SessionLocal, engine
from app.models import Attendance, AttendanceStatus, Employee, LeaveRequest, LeaveStatus


RANDOM = Random(42)

DEPARTMENTS = {
    "HR": ["HR Manager", "Recruiter", "HR Executive", "Payroll Specialist"],
    "Finance": ["Finance Manager", "Accountant", "Financial Analyst", "Accounts Executive"],
    "IT": ["Software Engineer", "System Administrator", "QA Engineer", "IT Support Engineer"],
    "Sales": ["Sales Manager", "Business Development Executive", "Account Executive", "Sales Associate"],
    "Operations": ["Operations Manager", "Process Coordinator", "Logistics Executive", "Operations Analyst"],
}

FIRST_NAMES = [
    "Aarav",
    "Vivaan",
    "Aditya",
    "Vihaan",
    "Arjun",
    "Sai",
    "Reyansh",
    "Ayaan",
    "Krishna",
    "Ishaan",
    "Ananya",
    "Diya",
    "Aadhya",
    "Avni",
    "Kavya",
    "Ira",
    "Myra",
    "Riya",
    "Saanvi",
    "Anika",
    "Rohan",
    "Kabir",
    "Nikhil",
    "Kunal",
    "Rahul",
    "Meera",
    "Priya",
    "Sneha",
    "Pooja",
    "Neha",
    "Amit",
    "Suresh",
    "Vikram",
    "Manish",
    "Rakesh",
    "Nisha",
    "Shreya",
    "Tanvi",
    "Kritika",
    "Divya",
    "Harsh",
    "Yash",
    "Ankit",
    "Siddharth",
    "Mohit",
    "Swati",
    "Aparna",
    "Radhika",
    "Isha",
    "Pranav",
]

LAST_NAMES = [
    "Sharma",
    "Verma",
    "Patel",
    "Gupta",
    "Singh",
    "Kumar",
    "Reddy",
    "Nair",
    "Iyer",
    "Joshi",
    "Mehta",
    "Chopra",
    "Kapoor",
    "Malhotra",
    "Agarwal",
    "Bansal",
    "Mishra",
    "Pandey",
    "Tiwari",
    "Yadav",
    "Chatterjee",
    "Banerjee",
    "Mukherjee",
    "Das",
    "Ghosh",
]

LEAVE_TYPES = ["Sick Leave", "Casual Leave", "Annual Leave"]


def phone_number(index: int) -> str:
    return f"+91 9{RANDOM.randint(100, 999)}{RANDOM.randint(100000, 999999)}"


def email_for(first_name: str, last_name: str, index: int) -> str:
    return f"{first_name.lower()}.{last_name.lower()}{index:02d}@company.in"


def create_employees() -> list[Employee]:
    employees = []
    used_names = set()
    department_names = list(DEPARTMENTS.keys())

    for index in range(1, 51):
        first_name = FIRST_NAMES[index - 1]
        last_name = RANDOM.choice(LAST_NAMES)
        while (first_name, last_name) in used_names:
            last_name = RANDOM.choice(LAST_NAMES)
        used_names.add((first_name, last_name))

        department = department_names[(index - 1) % len(department_names)]
        designation = RANDOM.choice(DEPARTMENTS[department])
        joining_date = date.today() - timedelta(days=RANDOM.randint(120, 1800))

        employees.append(
            Employee(
                employee_code=f"EMP{index:03d}",
                first_name=first_name,
                last_name=last_name,
                email=email_for(first_name, last_name, index),
                phone=phone_number(index),
                department=department,
                designation=designation,
                hire_date=joining_date,
                salary=RANDOM.randint(35000, 180000),
            )
        )

    return employees


def create_leave_requests(employees: list[Employee], today: date) -> list[LeaveRequest]:
    leaves = []
    leave_today_employee_ids = {employee.id for employee in employees[:6]}

    for employee in employees:
        if employee.id in leave_today_employee_ids:
            leave_type = RANDOM.choice(LEAVE_TYPES)
            start_date = today - timedelta(days=RANDOM.randint(0, 1))
            end_date = today + timedelta(days=RANDOM.randint(0, 3))
            status = LeaveStatus.approved
        elif RANDOM.random() < 0.36:
            leave_type = RANDOM.choice(LEAVE_TYPES)
            start_date = today - timedelta(days=RANDOM.randint(3, 28))
            end_date = start_date + timedelta(days=RANDOM.randint(0, 3))
            status = RANDOM.choices(
                [LeaveStatus.approved, LeaveStatus.pending, LeaveStatus.rejected],
                weights=[0.62, 0.24, 0.14],
            )[0]
        else:
            continue

        leaves.append(
            LeaveRequest(
                employee_id=employee.id,
                start_date=start_date,
                end_date=end_date,
                reason=f"{leave_type} request",
                status=status,
            )
        )

    return leaves


def approved_leave_dates(leaves: list[LeaveRequest]) -> dict[int, set[date]]:
    leave_dates: dict[int, set[date]] = {}
    for leave in leaves:
        if leave.status != LeaveStatus.approved:
            continue
        current = leave.start_date
        while current <= leave.end_date:
            leave_dates.setdefault(leave.employee_id, set()).add(current)
            current += timedelta(days=1)
    return leave_dates


def create_attendance(employees: list[Employee], leaves: list[LeaveRequest], today: date) -> list[Attendance]:
    attendance = []
    leave_dates = approved_leave_dates(leaves)
    date_range = [today - timedelta(days=offset) for offset in range(29, -1, -1)]

    for index, employee in enumerate(employees):
        if index < 12:
            absence_rate = 0.02
        elif index < 36:
            absence_rate = 0.08
        else:
            absence_rate = 0.16

        for attendance_date in date_range:
            if attendance_date in leave_dates.get(employee.id, set()):
                status = AttendanceStatus.absent
                notes = "Approved leave"
            elif RANDOM.random() < absence_rate:
                status = AttendanceStatus.absent
                notes = "Unplanned absence"
            else:
                status = AttendanceStatus.present
                notes = ""

            attendance.append(
                Attendance(
                    employee_id=employee.id,
                    attendance_date=attendance_date,
                    status=status,
                    notes=notes,
                )
            )

    return attendance


def seed() -> tuple[int, int, int]:
    Base.metadata.create_all(bind=engine)
    today = date.today()

    db = SessionLocal()
    try:
        db.query(Attendance).delete()
        db.query(LeaveRequest).delete()
        db.query(Employee).delete()
        db.commit()

        employees = create_employees()
        db.add_all(employees)
        db.commit()
        for employee in employees:
            db.refresh(employee)

        leaves = create_leave_requests(employees, today)
        db.add_all(leaves)
        db.commit()

        attendance = create_attendance(employees, leaves, today)
        db.add_all(attendance)
        db.commit()

        total_employees = db.query(Employee).count()
        total_attendance = db.query(Attendance).count()
        total_leaves = db.query(LeaveRequest).count()
        return total_employees, total_attendance, total_leaves
    finally:
        db.close()


if __name__ == "__main__":
    employee_count, attendance_count, leave_count = seed()
    print("Seed complete")
    print(f"Total employees: {employee_count}")
    print(f"Total attendance records: {attendance_count}")
    print(f"Total leave records: {leave_count}")
