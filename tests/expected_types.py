# Expected columns and expected data expressed in regex.

subject_area = r"(MUSJAZZ|ANTH|ASIA|MUSHONS|APP MTH|GEOG|MUSSUPST|FOOD SC|DATA|CRIM|PROF|HONECMS|ARTH|CEME|BIOLOGY|MUSPERF|MUSEP|EXCHANGE|VET SC|PEACE|OCCTH|PSYCHIAT|PHARM|PHYSIOTH|MATHS|GEOLOGY|NURSING|CULTST|MUSPOP|PETROGEO|TRADE|CYBER|FILM|COMMGMT|ELEC ENG|OPHTHAL|ARCH|HIST|ECOTOUR|LAW|MUSGEN|GENETICS|AGRIC|MGRE|SCIENCE|CHIN|ANIML SC|PAEDIAT|AGRONOMY|APP BIOL|PHYSIOL|HONSCI|PROJMGNT|BIOMED|MARKETNG|SPEECH|MDIA|PALAEO|PLANNING|ARTS|CRWR|TECH|ACUCARE|GERM|HLTH SC|MEDICINE|BIOTECH|BIOMET|PATHOL|PETROENG|AGRIBUS|PHYSICS|BIOINF|VITICULT|HEALTH|COMMLAW|CHEM|BIOSTATS|PURE MTH|CLAS|MECH ENG|ACCTING|POLICY|STATS|ODONT|PSYCHOL|ITAL|UACOL|EDUC|RUR HLTH|HORTICUL|LING|AUST|MEDIC ST|SURGERY|SPAN|VET TECH|COMP SCI|ORALHLTH|GEND|DESST|MUSICOL|MUSCLASS|ABORIG|PPE|CHEM ENG|PUB HLTH|ENGL|SOCI|GEN PRAC|OENOLOGY|LARCH|MINING|BIOCHEM|CRARTS|ECON|POLIS|ACCTFIN|PLANT SC|DEFSCI|PHIL|SPATIAL|APP DATA|DEVT|AN BEHAV|COMMERCE|PROP|GSSA|ANAT SC|MUSTHEAT|INTBUS|ENTREP|ENV BIOL|JAPN|WINE|MICRO|MANAGEMT|CORPFIN|FREN|MUSONIC|ENG|MUSCOMP|DENT|CONMGNT|UAC)"

short_month = r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"

hour12 = r"([1-9]|1[0-2])"

minute = r"([1-9]|[1-5][0-9]|60)"

time_12hr = f"({hour12}(am|pm)|{hour12}:{minute}(am|pm))"

date = r"([1-9]|[1-2][0-9]|3[0-1])"

class_type = r"(Studio|Seminar|Project|Technique/Repertoire|Clinical|Performance|Laboratory|Jazz Performance Forum|Thesis|Dissertation|Teaching Practice|Independent Study|Small Group Discovery|Lecture|Paper|Practical|Computer Exercise|Class Meeting|Unspecified|Workshop|Tutorial|Fieldwork|Rehearsal|Tuition|Placement|Resource Session|Performance Forum|Supervision|Repertoire|Class Exercise|PBL Session)"

english_numeral = r"(One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|Eleven|Twelve|Thirteen|Fourteen|Fifteen|Sixteen|Seventeen|Eighteen|Nineteen|Twenty)"

day_of_the_week = "(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)"

course_id_regex = r"^([01]{2}[0-9]{4}+1+[0-9]{4}+())$" # note: currently broken

class_col_types = {
    "Class Nbr" : r"^([1-9][0-9]{4})$",
    "Section" : r"^([0-9]{2}[A-Z]{2}|[A-Z]{2}[0-9]{2}|[A-Z]{3}[0-9]|TU0|WT|PF0)$",
    "Size" : r"^(0|[1-9][0-9]*)$",
    "Available" : r"^(0|[1-9][0-9]*)$",
    "Dates" : f"^(No schedule|({date} {short_month} - {date} {short_month}))$",
    "Days" : f"^(No schedule|({day_of_the_week}(, {day_of_the_week})*))$",
    "Time" : f"^(No schedule|{time_12hr} - {time_12hr})$",
    "Location" : r"^.*$", # not sure how to parse
    "Class Type" : f"^(((Automatic )?Enrolment|Related) Class: {class_type})$",
    "Group" : f"^(none|(Group {english_numeral}))$",
    "Annotation" : r"^.*$", # not sure how to parse
    "Subject Area" : f"^{subject_area}$",
    "Catalogue Number" : r"^([0-9]{4}[A-Z]*)$",
    "Course Title" : r"^.*$", # not sure how to parse
    "Course ID" : course_id_regex
}




course_col_types = {
    "Career" : "^(Non-Award|Undergraduate|Undergraduate Law|PGRS|Postgraduate Coursework)$",
    "Units" : {0.0, 1.5, 2.0, 3.0, 4.0, 4.5, 6.0, 7.5, 3.75, 9.0, 1.0, 10.0, 12.0, 8.0},
    "Term" : "^(Term 1|Trimester 1|Online Teaching Period 4|Trimester 3|Term 2|Online Teaching Period 6|Melb Teaching Period 1|Melb Teaching Period 3|Semester 1|Winter School|Term 3|Online Teaching Period 3|Summer School|Trimester 2|Online Teaching Period 2|Melb Teaching Period 2|Online Teaching Period 1|Semester 2|Online Teaching Period 5|Term 4)$",
    "Campus" : "^(UofA College Melbourne|Waite|External|National Wine Centre|Online|University of Adelaide College|Teaching Hospitals|North Terrace|Adelaide College of ArtsandDes|Ngee Ann Academy|Flinders University|Regency Park|Melbourne|Roseworthy)$",
    "Contact" : r"^.*$", # not sure how to parse
    "Restriction" : r"^.*$", # not sure how to parse
    "Available for Study Abroad and Exchange" : "^(Yes|No)$",
    "Available for Non-Award Study" : "^(Yes|Check with School|No)$",
    "Pre-Requisite" : r"^.*$", # not sure how to parse
    "Assessment" : r"^.*$", # not sure how to parse
    "Syllabus" : r"^.*$", # not sure how to parse
    "Course ID" : course_id_regex,
    "Co-Requisite" : r"^.*$", # not sure how to parse
    "Discovery Experience â Global" : "^(nan|Yes)$",
    "Discovery Experience â Working" : "^(nan|Yes)$",
    "Assumed Knowledge" : r"^.*$", # not sure how to parse
    "Incompatible" : r"^.*$", # not sure how to parse
    "Session" : "^(Half Year Part 1|Winter Session 1|Half Year Part 2|Late Add Session|Summer Session 4|Summer Session 2|Summer Session 1|Summer Session 3|Remedial Course)$",
    "Quota" : r"^.*$", # not sure how to parse
    "Discovery Experience â Community" : "^(nan|Yes)$",
    "Biennial Course" : "^(nan|Course offered in odd years)$"
}
