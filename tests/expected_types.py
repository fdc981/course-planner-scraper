class_col_types = {
    "Class Nbr" : range(10000, 100000),
    "Section" : str,
    "Size" : int,
    "Available" : int,
    "Dates" : str, # could add some parsing? possible value "no schedule"
    "Days" : ["No schedule", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    "Time" : str, # could add some parsing? possible value "no schedule"
    "Location" : str,
    "Class Type" : str,
    "Group" : ["none", "Group One", "Group Two", "Group Three", "Group Four", "Group Five", "Group Six", "Group Seven", "Group Eight", "Group Nine", "Group Ten", "Group Eleven", "Group Twelve", "Group Thirteen", "Group Fourteen", "Group Fifteen"],
    "Annotation" : str,
    "Subject Area" : {'MUSJAZZ', 'ANTH', 'ASIA', 'MUSHONS', 'APP MTH', 'GEOG', 'MUSSUPST', 'FOOD SC', 'DATA', 'CRIM', 'PROF', 'HONECMS', 'ARTH', 'CEME', 'BIOLOGY', 'MUSPERF', 'MUSEP', 'EXCHANGE', 'VET SC', 'PEACE', 'OCCTH', 'PSYCHIAT', 'PHARM', 'PHYSIOTH', 'MATHS', 'GEOLOGY', 'NURSING', 'CULTST', 'MUSPOP', 'PETROGEO', 'TRADE', 'CYBER', 'FILM', 'COMMGMT', 'ELEC ENG', 'OPHTHAL', 'ARCH', 'HIST', 'ECOTOUR', 'LAW', 'MUSGEN', 'GENETICS', 'AGRIC', 'MGRE', 'SCIENCE', 'CHIN', 'ANIML SC', 'PAEDIAT', 'AGRONOMY', 'APP BIOL', 'PHYSIOL', 'HONSCI', 'PROJMGNT', 'BIOMED', 'MARKETNG', 'SPEECH', 'MDIA', 'PALAEO', 'PLANNING', 'ARTS', 'CRWR', 'TECH', 'ACUCARE', 'GERM', 'HLTH SC', 'MEDICINE', 'BIOTECH', 'BIOMET', 'PATHOL', 'PETROENG', 'AGRIBUS', 'PHYSICS', 'BIOINF', 'VITICULT', 'HEALTH', 'COMMLAW', 'CHEM', 'BIOSTATS', 'PURE MTH', 'CLAS', 'MECH ENG', 'ACCTING', 'POLICY', 'STATS', 'ODONT', 'PSYCHOL', 'ITAL', 'UACOL', 'EDUC', 'RUR HLTH', 'HORTICUL', 'LING', 'AUST', 'MEDIC ST', 'SURGERY', 'SPAN', 'VET TECH', 'COMP SCI', 'ORALHLTH', 'GEND', 'DESST', 'MUSICOL', 'MUSCLASS', 'ABORIG', 'PPE', 'CHEM ENG', 'PUB HLTH', 'ENGL', 'SOCI', 'GEN PRAC', 'OENOLOGY', 'LARCH', 'MINING', 'BIOCHEM', 'CRARTS', 'ECON', 'POLIS', 'ACCTFIN', 'PLANT SC', 'DEFSCI', 'PHIL', 'SPATIAL', 'APP DATA', 'DEVT', 'AN BEHAV', 'COMMERCE', 'PROP', 'GSSA', 'ANAT SC', 'MUSTHEAT', 'INTBUS', 'ENTREP', 'ENV BIOL', 'JAPN', 'WINE', 'MICRO', 'MANAGEMT', 'CORPFIN', 'FREN', 'MUSONIC', 'ENG', 'MUSCOMP', 'DENT', 'CONMGNT', 'UAC'},
    "Catalogue Number" : str,
    "Course Title" : str,
    "Course ID" : str
}

course_col_types = {
    "Career" : {'Non-Award', 'Undergraduate', 'Undergraduate Law', 'PGRS', 'Postgraduate Coursework'},
    "Units" : {0.0, 1.5, 2.0, 3.0, 4.0, 4.5, 6.0, 7.5, 3.75, 9.0, 1.0, 10.0, 12.0, 8.0},
    "Term" : {'Term 1', 'Trimester 1', 'Online Teaching Period 4', 'Trimester 3', 'Term 2', 'Online Teaching Period 6', 'Melb Teaching Period 1', 'Melb Teaching Period 3', 'Semester 1', 'Winter School', 'Term 3', 'Online Teaching Period 3', 'Summer School', 'Trimester 2', 'Online Teaching Period 2', 'Melb Teaching Period 2', 'Online Teaching Period 1', 'Semester 2', 'Online Teaching Period 5', 'Term 4'},
    "Campus" : {'UofA College Melbourne', 'Waite', 'External', 'National Wine Centre', 'Online', 'University of Adelaide College', 'Teaching Hospitals', 'North Terrace', 'Adelaide College of ArtsandDes', 'Ngee Ann Academy', 'Flinders University', 'Regency Park', 'Melbourne', 'Roseworthy'},
    "Contact" : str,
    "Restriction" : str,
    "Available for Study Abroad and Exchange" : {"Yes", "No"},
    "Available for Non-Award Study" : {"Yes", "Check with School", "No"},
    "Pre-Requisite" : str,
    "Assessment" : str,
    "Syllabus" : str,
    "Course ID" : str,
    "Co-Requisite" : str,
    "Discovery Experience â Global" : str,
    "Discovery Experience â Working" : str,
    "Assumed Knowledge" : str,
    "Incompatible" : str,
    "Session" : {None, 'Half Year Part 1', 'Winter Session 1', 'Half Year Part 2', 'Late Add Session', 'Summer Session 4', 'Summer Session 2', 'Summer Session 1', 'Summer Session 3', 'Remedial Course'},
    "Quota" : str,
    "Discovery Experience â Community" : str,
    "Biennial Course" : str
}
