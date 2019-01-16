
export var doc_types = [
    ['T', 'Academic Transcript'],
    ['E', 'Cerfificate'],
    ['C', 'Curriculum Vitae'],
    ['R', 'Reference'],
    ['O', 'Other']
];

export var job_state_names = {
    'L': 'Looking for Candidates',
    'F': 'Position Filled',
    'JO': 'Job Offer Made',
    'W': 'Position Withdrawn'
};

export var match_state_names = {
    'N': 'No Action Taken',
    'CI': 'Candidate Interested',
    'EI': 'Employer Interested',
    'P': 'In Progress',
    'DC': 'Declined by Candidate',
    'DE': 'Declined by Employer',
    'JO': 'Job Offer Made',
    'H': 'Hired',
    'JD': 'Job Offer Declined',
    'F': 'Position Filled',
    'W': 'Position Withdrawn'
};

export var education_names = [
    "None Specified",
    "High School",
    "Certificate",
    "Associate Diploma",
    "Diploma",
    "Bachelor's Degree",
    "Graduate Certificate",
    "Graduate Diploma",
    "Master's Degree",
    "Ph.D"
];

export function validate_user(user) {
    user.first_name = user.first_name.trim();
    user.last_name = user.last_name.trim();
    user.email = user.email.trim();
    user.city = user.city.trim();
    if (user.first_name.length == 0) {
        alert("First name cannot be blank.");
        return false;
    }
    if (user.last_name.length == 0) {
        alert("Last name cannot be blank.");
        return false;
    }
    if (user.email.length == 0) {
        alert("Email name cannot be blank.");
        return false;
    }
    if (!user.email.includes("@")) {
        alert("Email is invalid.");
        return false;
    }
    if (user.city.length == 0) {
        alert("City cannot be blank.");
        return false;
    }
    return true;
}
