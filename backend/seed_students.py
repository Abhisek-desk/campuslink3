from students.serializers import RosterSerializer
from students.services import refresh_readiness

# roll_no, first, last, branch, cgpa, backlogs, aptitude, mock, soft, skills
DATA = [
 ("CS2026001","Aarav","Sharma","CSE",8.9,0,88,82,80,["python","django","sql","rest api","git","docker"]),
 ("CS2026002","Ananya","Iyer","CSE",9.2,0,92,85,84,["python","machine learning","sql","git","communication"]),
 ("CS2026003","Rohan","Mehta","CSE",8.1,0,78,70,72,["javascript","react","node","sql","git"]),
 ("CS2026004","Priya","Nair","CSE",7.6,1,70,65,68,["python","sql","excel"]),
 ("CS2026005","Karan","Singh","CSE",6.8,2,55,50,58,["python"]),
 ("CS2026006","Yash","Agarwal","CSE",8.7,0,85,79,81,["javascript","react","node","docker","aws","git"]),
 ("CS2026007","Tanmay","Behera","CSE",7.1,1,61,56,63,["python","django"]),
 ("IT2026001","Sneha","Patel","IT",8.5,0,84,78,79,["javascript","react","node","rest api","git"]),
 ("IT2026002","Vikram","Rao","IT",7.9,0,74,68,70,["python","django","sql","git"]),
 ("IT2026003","Meera","Das","IT",8.8,0,86,80,82,["aws","cloud","docker","linux","git"]),
 ("IT2026004","Arjun","Reddy","IT",7.2,1,62,58,60,["javascript","sql"]),
 ("IT2026005","Divya","Menon","IT",6.5,3,48,45,52,["excel"]),
 ("EC2026001","Rahul","Verma","ECE",8.0,0,76,70,74,["python","linux","git"]),
 ("EC2026002","Nisha","Kapoor","ECE",7.7,0,72,66,71,["python","excel","communication"]),
 ("EC2026003","Siddharth","Jain","ECE",8.4,0,80,74,76,["python","machine learning","sql"]),
 ("EC2026004","Pooja","Bose","ECE",6.9,1,58,52,60,["excel","communication"]),
 ("EC2026005","Manish","Yadav","ECE",6.2,2,45,42,50,[]),
 ("EE2026001","Tanvi","Deshmukh","EEE",8.3,0,79,72,75,["python","excel","sql"]),
 ("EE2026002","Harsh","Gupta","EEE",7.4,0,66,60,65,["python","git"]),
 ("EE2026003","Kavya","Pillai","EEE",7.0,1,60,55,62,["excel","communication"]),
 ("EE2026004","Aditya","Joshi","EEE",6.6,2,50,46,54,["linux"]),
 ("EE2026005","Ritu","Sahoo","EEE",8.0,0,75,69,73,["python","sql","excel"]),
 ("ME2026001","Deepak","Mishra","ME",7.5,0,64,58,66,["excel","communication"]),
 ("ME2026002","Sana","Khan","ME",8.2,0,77,71,74,["python","excel","git"]),
 ("ME2026003","Gaurav","Pandey","ME",6.4,2,47,44,52,["excel"]),
 ("ME2026004","Lipsa","Mohanty","ME",7.8,0,69,63,70,["python","communication"]),
 ("CE2026001","Nikhil","Kumar","CE",7.3,0,63,57,64,["excel","communication"]),
 ("CE2026002","Shreya","Banerjee","CE",8.6,0,82,76,78,["python","sql","git","excel"]),
 ("CE2026003","Amit","Panda","CE",6.7,1,52,48,56,["excel"]),
 ("CE2026004","Isha","Choudhury","CE",7.9,0,71,65,69,["python","sql"]),
]

added = 0
for roll, fn, ln, br, cg, bk, apt, mock, soft, skills in DATA:
    s = RosterSerializer(data={
        "roll_no": roll, "first_name": fn, "last_name": ln,
        "email": f"{roll.lower()}@campus.edu", "branch": br, "cgpa": cg,
        "backlogs": bk, "batch": 2026,
        "aptitude_score": apt, "mock_score": mock, "soft_score": soft,
    })
    if not s.is_valid():
        print("SKIPPED", roll, s.errors)
        continue
    p = s.save()
    p.skills = skills
    p.save()
    refresh_readiness(p)          # calculates the readiness score and level
    p.user.set_password("Demo@12345")   # lets you log in without the activation step
    p.user.save()
    added += 1
print(f"Added {added} students")