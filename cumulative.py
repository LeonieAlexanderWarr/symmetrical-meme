import math

import matplotlib.pyplot as plt
import numpy as np


#this incomesupport worker is incomepissing me off
def calculate_cumulative_effort(role_name, total_applicants, hires, app_time_mins, interview_stages, target_probability=0.80):
    p_hire = hires / total_applicants
    n_apps = math.ceil(math.log(1 - target_probability) / math.log(1 - p_hire))
    
    expected_interview_time_mins = 0
    expected_interviews_breakdown = {}
    
    for stage in interview_stages:
        p_reach_stage = stage['candidates'] / total_applicants
        expected_interview_time_mins += (p_reach_stage * stage['time_mins'])
        
        expected_attended = n_apps * p_reach_stage
        expected_interviews_breakdown[stage['name']] = round(expected_attended)
        
    total_expected_time_per_app = app_time_mins + expected_interview_time_mins
    total_time_hours = (n_apps * total_expected_time_per_app) / 60
    
    return {
        "Role Type": role_name,
        "Applicants/Vacancy": total_applicants,
        "App Time (Mins)": app_time_mins,
        "Total Applications": n_apps,
        "Total Effort (Hours)": round(total_time_hours, 2),
        "Expected Interviews": expected_interviews_breakdown
    }

def plot_cumulative_distribution(target_applicants, survival_applicants):
    x_apps = np.linspace(1, 2500, 500)
    
    p_target = 1 / target_applicants
    p_survival = 1 / survival_applicants
    
    y_target = (1 - (1 - p_target)**x_apps) * 100
    y_survival = (1 - (1 - p_survival)**x_apps) * 100
    
    plt.figure(figsize=(10, 6))
    
    # Custom color palette preserved
    plt.plot(x_apps, y_target, color='#32a8a2', label='Target Roles (High Quality)', lw=2.5)
    plt.plot(x_apps, y_survival, color='#806649', label='Survival Roles (Low Quality)', lw=2.5)
    
    plt.title('Probability of Success vs. Total Applications Required', fontsize=14)
    plt.xlabel('Total Applications Needed', fontsize=12)
    plt.ylabel('Probability of Securing >= 1 Offer (%)\n (limit as x approaches infinity)', fontsize=12)
    
    plt.xlim(0, 1500)
    plt.ylim(0, 105)
    plt.legend(loc='lower right', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# --- Execution ---
print("="*80)
print("Real jobs Versus me applying to 1000 jobs for 15 dollars per hour and getting spat on all day type shit")
print("="*80)

survival_stages = [
    {"name": "In-Person/Phone Interview", "candidates": 5, "time_mins": 30}
]

survival_metrics = calculate_cumulative_effort(
    "Survival (Minimum Wage)", 500, 1, 5, survival_stages
)

target_stages = [
    {"name": "HR Prescreen Call", "candidates": 30, "time_mins": 20},
    {"name": "Interview 1 (Manager)", "candidates": 10, "time_mins": 60},
    {"name": "Interview 2 (Director)", "candidates": 2, "time_mins": 60}
]

target_metrics = calculate_cumulative_effort(
    "Target (AR Clerk/Office)", 100, 1, 15, target_stages
)

print("\n[ TARGET ROLES  ]")
print(f"Total Applications Needed: {target_metrics['Total Applications']}")
print("Expected Interview Pipeline Yield:")
for stage, count in target_metrics["Expected Interviews"].items():
    print(f"  -> {stage}: {count} expected")
print(f"Total Time Investment: {target_metrics['Total Effort (Hours)']} Hours")

print("\n[ SURVIVAL ROLES (MINIMUM WAGE) ]")
print(f"Total Applications Needed: {survival_metrics['Total Applications']}")
print("Expected Interview Pipeline Yield:")
for stage, count in survival_metrics["Expected Interviews"].items():
    print(f"  -> {stage}: {count} expected")
print(f"Total Time Investment: {survival_metrics['Total Effort (Hours)']} Hours")

print("\n[ EFFORT THRESHOLD SUMMARY ]")
thresholds = [0.25, 0.50, 0.75, 0.995]

print("Role Type | Target % | Apps Needed | Total Time (Hrs)")
print("-" * 65)

for t in thresholds:
    m = calculate_cumulative_effort("Target ", 100, 1, 15, target_stages, t)
    print(f"Target   | {round(t*100, 1)}% | {m['Total Applications']} | {m['Total Effort (Hours)']} hrs")

print("-" * 65)

for t in thresholds:
    m = calculate_cumulative_effort("Survival (Minimum Wage)", 500, 1, 5, survival_stages, t)
    print(f"Survival | {round(t*100, 1)}% | {m['Total Applications']} | {m['Total Effort (Hours)']} hrs")

print("\n" + "="*80)

plot_cumulative_distribution(
    target_metrics["Applicants/Vacancy"],
    survival_metrics["Applicants/Vacancy"]
)



print("The thing is, I don't think this is even a theoretically Oh just apply to both and split time type shit because it's the same expected amount of time and effort just to remain in poverty")
print("Like I would be stupid wouldn't I? I've gotten 5 interviews in like 30 highquality and 120 medium quality which are target jobs but with no cover letter or an extra generic quick apply ready cover letter")