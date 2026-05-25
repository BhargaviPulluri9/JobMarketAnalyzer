def skill_extraction_prompt(job_description):
    return f"""
You are an expert technical recruiter.
Analyze this job description and extract information.

Job Description:
{job_description}

Respond in this EXACT format:

REQUIRED_SKILLS:
- [skill 1]
- [skill 2]
...

NICE_TO_HAVE:
- [skill 1]
...

EXPERIENCE_LEVEL: [Entry/Mid/Senior]

KEY_RESPONSIBILITIES:
- [responsibility 1]
...

INDUSTRY: [industry name]
"""

def gap_analysis_prompt(job_description, resume_text):
    return f"""
You are a career coach helping a fresher land their first job.
Compare this resume against the job description.

Job Description:
{job_description}

Resume:
{resume_text}

Respond in this EXACT format:

MATCHING_SKILLS:
- [skill from resume that matches job]
...

MISSING_SKILLS:
- [required skill not found in resume]
...

RESUME_SCORE: [X/10]

TOP_3_SUGGESTIONS:
1. [Most important thing to add/improve]
2. [Second most important]
3. [Third most important]

INTERVIEW_TIPS:
- [Tip 1 specific to this job]
- [Tip 2]
...

OVERALL_VERDICT: [2-3 sentences honest assessment]
"""