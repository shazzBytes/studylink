# Sample Data User Summary

This document describes the seeded sample users in the backend sample data population script and the entities each user is connected to.

## Seeded Users

### 1. John Doe
- Email: `john.doe@example.com`
- Password: `password123`
- Role: standard user
- Primary institution: Massachusetts Institute of Technology
  - Institution role: `STUDENT`
  - Department: `Computer Science`
  - Title: `Undergraduate`
- Partner institution: Stanford University
  - Institution role: `RESEARCHER`
  - Department: `Applied AI`
  - Title: `Visiting Researcher`
- Researcher profile: yes
  - Linked researcher name: `John Doe`
  - Qualification: `M.S. in Data Science`
  - Institute: `Massachusetts Institute of Technology`
  - Department: `Computer Science`
  - Bio: `Sample researcher profile for seeded user John Doe.`
- Publications: none seeded for this researcher profile.

### 2. Jane Smith
- Email: `jane.smith@example.com`
- Password: `password123`
- Role: standard user
- Primary institution: Stanford University
  - Institution role: `RESEARCHER`
  - Department: `Data Science`
  - Title: `Postdoctoral Researcher`
- Partner institution: Carnegie Mellon University
  - Institution role: `RESEARCHER`
  - Department: `Human-Computer Interaction`
  - Title: `Visiting Scholar`
- Researcher profile: yes
  - Linked researcher name: `Jane Smith`
  - Qualification: `M.S. in Computational Biology`
  - Institute: `Stanford University`
  - Department: `Data Science`
  - Bio: `Sample researcher profile for seeded user Jane Smith.`
- Publications: none seeded for this researcher profile.

### 3. Bob Johnson
- Email: `bob.johnson@example.com`
- Password: `password123`
- Role: standard user
- Primary institution: Carnegie Mellon University
  - Institution role: `FACULTY`
  - Department: `Robotics`
  - Title: `Assistant Professor`
- Partner institution: Imperial College London
  - Institution role: `RESEARCHER`
  - Department: `Robotics`
  - Title: `Visiting Researcher`
- Researcher profile: no
- Publications: not linked to a seeded researcher profile.

### 4. Alice Williams
- Email: `alice.williams@example.com`
- Password: `password123`
- Role: standard user
- Primary institution: Oxford University
  - Institution role: `RESEARCHER`
  - Department: `Quantum Computing`
  - Title: `Research Scientist`
- Partner institution: Massachusetts Institute of Technology
  - Institution role: `RESEARCHER`
  - Department: `Computer Vision`
  - Title: `Visiting Researcher`
- Researcher profile: no
- Publications: not linked to a seeded researcher profile.

### 5. Charlie Brown
- Email: `charlie.brown@example.com`
- Password: `password123`
- Role: standard user
- Primary institution: Imperial College London
  - Institution role: `STUDENT`
  - Department: `Bioinformatics`
  - Title: `Graduate Student`
- Partner institutions: none seeded
- Researcher profile: no
- Publications: not linked to a seeded researcher profile.

## Partner Institutions Seeded

The seeded institutions used for membership assignments are:
- Massachusetts Institute of Technology
- Stanford University
- Carnegie Mellon University
- Oxford University
- Imperial College London

## Notes

- The seeded sample population script is located at `backend/app/populate_sample_data.py`.
- To populate this sample data, run:
  ```powershell
  cd backend
  .\.venv\Scripts\Activate.ps1
  python -m app.populate_sample_data
  ```
