# Multi-Level Matching - How It Works

## ✅ The System IS Working as OR Condition

Your multi-level matching system **already works** with OR logic. If ANY of the three methods match, the student is marked Present with their score.

---

## How the Matching Works (Step by Step)

### For Each Student in Roll Call:

```
1. Try PRN Match
   ↓ IF MATCH FOUND → Mark Present, Get Score, STOP
   ↓ IF NO MATCH → Continue to Level 2

2. Try Name Match (Fuzzy)
   ↓ IF MATCH FOUND → Mark Present, Get Score, STOP
   ↓ IF NO MATCH → Continue to Level 3

3. Try Roll No + Division Match
   ↓ IF MATCH FOUND → Mark Present, Get Score, STOP
   ↓ IF NO MATCH → Mark Absent
```

This is **OR logic** - only ONE needs to match!

---

## Code Flow Explanation

### Level 1: PRN Matching
```python
if prn and prn in fctc_lookup_by_prn:
    matched_record = fctc_lookup_by_prn[prn]
    match_method = "PRN"
    # Student is PRESENT with their score
```

### Level 2: Name Matching (only if Level 1 failed)
```python
elif roll_name:  # ← "elif" means "only if PRN didn't match"
    if roll_name in fctc_lookup_by_name:
        matched_record = candidates[0]
        match_method = "Name"
        # Student is PRESENT with their score
```

### Level 3: Roll+Div Matching (only if Levels 1 & 2 failed)
```python
if not matched_record and roll_no and division:  # ← Only if still no match
    key = f"{roll_no}_{division}"
    if key in fctc_lookup_by_roll_div:
        matched_record = fctc_lookup_by_roll_div[key]
        match_method = "Roll_Div"
        # Student is PRESENT with their score
```

### Final Status Assignment
```python
if matched_record:  # ← If ANY level matched
    status = "Present"
    score = matched_record.get('Score', 'N/A')  # ← Fetch actual score
else:
    status = "Absent"
    score = "N/A"
```

---

## What Gets Stored in Output

For each student, the CSV contains:
```
PRN, Roll_No, Name, Division, Attendance_Status, Score, Match_Method
```

Examples:
```csv
12345,1,John Doe,A,Present,85,PRN          ← Matched by PRN
67890,2,Jane Smith,A,Present,90,Name       ← Matched by Name
11111,3,Bob Johnson,A,Present,78,Roll_Div  ← Matched by Roll+Div
22222,4,Alice Brown,A,Absent,N/A,Not_Found ← No match found
```

---

## Why Students Might Still Show as Absent

If students are showing as Absent even though they're in the FCTC file, it's because:

### 1. PRN Doesn't Match
- FCTC: "ABC123" vs Roll Call: "ABC124" (typo)
- FCTC: "ABC123" vs Roll Call: "" (empty)

### 2. Name Doesn't Match (< 80% similarity)
- FCTC: "John Doe" vs Roll Call: "Jonathan Doe" (too different)
- FCTC: "John Smith" vs Roll Call: "John Smyth" (might match with fuzzy)

### 3. Roll No + Division Doesn't Match
- FCTC: Roll="1", Div="A" vs Roll Call: Roll="01", Div="A" (different format)
- FCTC: Roll="1", Div="A" vs Roll Call: Roll="1", Div="B" (different division)
- FCTC: Missing Roll No or Division fields

---

## How to Debug

### Check the Console Logs (Vercel Deployment Logs)

After processing, you'll see:
```
🔍 Creating lookup dictionaries for multi-level matching...
  ✓ PRN lookup: 50 entries
  ✓ Name lookup: 50 entries
  ✓ Roll+Div lookup: 45 entries  ← If this is 0, FCTC file missing Roll/Div
  📝 Sample PRN: ABC123
  📝 Sample Name: JOHN DOE
  📝 Sample Roll+Div: 1_A

🎯 Matching Statistics:
  ✓ PRN matches: 40
  ✓ Name matches: 5
  ✓ Roll+Div matches: 3
  ✗ No match (Absent): 2
  📈 Match Rate: 96.0% (48/50)
```

### What to Look For:

1. **Roll+Div lookup: 0 entries**
   - FCTC file doesn't have Roll Number or Division columns
   - Solution: Ensure FCTC file has these fields

2. **Name lookup: 0 entries**
   - FCTC file doesn't have Name/Full Name column
   - Solution: Ensure FCTC file has name field

3. **Low match rate (< 80%)**
   - Data quality issues
   - Check Match_Method column to see which students aren't matching

---

## Common Issues and Solutions

### Issue 1: FCTC File Missing Fields

**Problem**: FCTC file only has PRN and Score, missing Name/Roll/Division

**Solution**: 
- Check if FCTC file has these columns:
  - "Full name- MANDATORY FOR ALL COLLEGE STUDENTS"
  - "Roll Number-MANDATORY FOR ALL COLLEGE STUDENTS"
  - "Division-MANDATORY ONLY FOR NON-VISHWAKARMA INSTITUTE OF TECHNOLOGY STUDENTS"

### Issue 2: Different Data Formats

**Problem**: Roll numbers formatted differently
- FCTC: "1", "2", "3"
- Roll Call: "01", "02", "03"

**Solution**: The `_clean_roll_no()` function removes leading zeros, but if formats are very different, they won't match

### Issue 3: Names Too Different

**Problem**: Names don't meet 80% similarity threshold
- FCTC: "John"
- Roll Call: "Jonathan"

**Solution**: Lower the fuzzy match threshold (currently 0.8 = 80%)

---

## Testing the System

### Test Case 1: PRN Match
```
FCTC: PRN="ABC123", Name="John Doe", Roll="1", Div="A", Score=85
Roll Call: PRN="ABC123", Name="John Doe", Roll="1", Div="A"
Expected: Present, Score=85, Match_Method=PRN ✅
```

### Test Case 2: Name Match (PRN wrong)
```
FCTC: PRN="ABC123", Name="John Doe", Roll="1", Div="A", Score=85
Roll Call: PRN="WRONG", Name="John Doe", Roll="1", Div="A"
Expected: Present, Score=85, Match_Method=Name ✅
```

### Test Case 3: Roll+Div Match (PRN and Name wrong)
```
FCTC: PRN="ABC123", Name="John Doe", Roll="1", Div="A", Score=85
Roll Call: PRN="WRONG", Name="Wrong Name", Roll="1", Div="A"
Expected: Present, Score=85, Match_Method=Roll_Div ✅
```

### Test Case 4: No Match
```
FCTC: PRN="ABC123", Name="John Doe", Roll="1", Div="A", Score=85
Roll Call: PRN="WRONG", Name="Wrong Name", Roll="99", Div="B"
Expected: Absent, Score=N/A, Match_Method=Not_Found ✅
```

---

## Next Deployment

**Latest Commit**: `4314bd7`

This includes enhanced debug logging to help you see:
- Sample entries from each lookup dictionary
- Match rate percentage
- Detailed matching statistics

Deploy with: `4314bd7` in Vercel dashboard

---

## Summary

✅ **The system DOES use OR logic**
✅ **If ANY method matches → Present with Score**
✅ **Match_Method column shows which method worked**
✅ **Score is fetched from the matched FCTC record**

If students are still showing as Absent, it's a **data quality issue**, not a logic issue. Check the console logs to see which lookup dictionaries are empty or have low counts.
