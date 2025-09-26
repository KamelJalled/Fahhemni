def calculate_badges(progress_dict: dict, section_id: str = "section1") -> list:
    """Calculate badges earned based on progress for any section"""
    badges = []
    
    # Get section-specific problem IDs
    section_num = section_id.replace('section', '')
    practice1_id = f"practice{section_num}_1"
    practice2_id = f"practice{section_num}_2"
    assessment_id = f"assessment{section_num}"
    
    # First Steps - complete any problem
    if any(p.get('completed', False) for p in progress_dict.values()):
        badges.append('first_steps')
    
    # Practice Master - complete all practice problems in this section
    practice_completed = (
        progress_dict.get(practice1_id, {}).get('completed', False) and
        progress_dict.get(practice2_id, {}).get('completed', False)
    )
    if practice_completed:
        badges.append('practice_master')
    
    # Assessment Ace - score 80+ on this section's assessment
    assessment = progress_dict.get(assessment_id, {})
    if assessment.get('completed', False) and assessment.get('score', 0) >= 80:
        badges.append('assessment_ace')
    
    # Section Expert - complete entire section
    if all(p.get('completed', False) for p in progress_dict.values()):
        badges.append(f'section{section_num}_expert')
    
    return badges