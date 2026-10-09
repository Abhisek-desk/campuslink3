import datetime as dt
from accounts.models import User
from jobs.models import Company, JobDescription, Match
from drives.models import Drive
from offers.models import Offer
from engine.matcher import run_match

ALL = ["CSE", "IT", "ECE", "EEE", "ME", "CE"]

# username, company, industry, jobs[(title, type, ctc, min_cgpa, backlogs, branches, skills)]
RECRUITERS = [
 ("technova", "TechNova", "Software", [
   ("Software Engineer", "fulltime", 12.0, 7.0, 1, ["CSE", "IT", "ECE"],
    ["python", "django", "sql", "git", "rest api"]),
   ("Frontend Developer", "fulltime", 10.0, 7.0, 1, ["CSE", "IT"],
    ["javascript", "react", "node", "git"]),
 ]),
 ("datasphere", "DataSphere", "Analytics", [
   ("Data Analyst", "fulltime", 8.0, 6.5, 2, ALL,
    ["sql", "excel", "python", "communication"]),
 ]),
 ("cloudworks", "CloudWorks", "Cloud", [
   ("Cloud Engineer", "fulltime", 9.5, 7.0, 1, ["CSE", "IT", "ECE", "EEE"],
    ["aws", "cloud", "docker", "linux", "git"]),
 ]),
 ("buildcore", "BuildCore", "Core engineering", [
   ("Graduate Engineer Trainee", "fulltime", 5.5, 6.5, 2, ["ME", "CE", "EEE", "ECE"],
    ["excel", "communication", "python"]),
 ]),
]

# how many top matches per job get an offer, and their statuses/doc states
OFFER_PLAN = [
 ("accepted", "verified"), ("joined", "verified"), ("accepted", "submitted"),
 ("issued", "pending"), ("deferred", "pending"), ("accepted", "pending"),
]

jobs = []
for uname, cname, industry, jlist in RECRUITERS:
    u = User.objects.filter(username=uname).first()
    if not u:
        u = User(username=uname, email=f"hr@{uname}.com", role="recruiter",
                 first_name=cname, is_approved=True)
        u.set_password("Demo@12345")
        u.save()
        Company.objects.create(user=u, name=cname, industry=industry,
                               contact_email=f"hr@{uname}.com")
    company = Company.objects.get(user=u)
    for title, jt, ctc, cg, bk, br, sk in jlist:
        j, _ = JobDescription.objects.get_or_create(
            company=company, title=title,
            defaults=dict(description=f"{title} at {cname}. Skills: {', '.join(sk)}.",
                          job_type=jt, location="Bhubaneswar", openings=5,
                          min_cgpa=cg, max_backlogs=bk, allowed_branches=br,
                          required_skills=sk, mock_benchmark=55, ctc_lpa=ctc))
        jobs.append(j)

for j in jobs:
    try:
        run_match(j)
    except Exception as e:
        print("Matching failed for", j.title, e)

issued = 0
for j in jobs:
    ms = list(Match.objects.filter(job=j, eligible=True).order_by("-fit_score")[:6])
    if not ms:
        ms = list(Match.objects.filter(job=j).order_by("-fit_score")[:6])
    for m, (status, docs) in zip(ms, OFFER_PLAN):
        if Offer.objects.filter(student=m.student, job=j).exists():
            continue
        Offer.objects.create(
            student=m.student, job=j, ctc_lpa=j.ctc_lpa, status=status,
            docs_status=docs, bond_signed=(docs == "verified"),
            doc_deadline=dt.date(2026, 11, 15), joining_date=dt.date(2027, 7, 1))
        if status in ("accepted", "joined") and not m.student.placed:
            m.student.placed = True
            m.student.save(update_fields=["placed", "updated_at"])
        issued += 1

base = dt.date(2026, 10, 20)
for i, j in enumerate(jobs):
    if not Drive.objects.filter(job=j).exists():
        Drive.objects.create(job=j, venue=f"Seminar Hall {i + 1}", panel=f"Panel {chr(65 + i)}",
                             date=base + dt.timedelta(days=i), start_time=dt.time(10, 0),
                             end_time=dt.time(13, 0))

print(f"Jobs: {len(jobs)}, offers created: {issued}")