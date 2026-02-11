# FCTC Field Extraction Update

## Summary
Updated the FCTC file processing logic to extract only required fields and ignore all other columns.

## Changes Made

### 1. Updated `ExamProcessor` Class Documentation
- Modified the class docstring to reflect the new field extraction approach
- Listed all required fields that will be extracted from FCTC files
- Added rule: "FCTC file: Extract ONLY required fields, ignore all other columns"

### 2. Modified `_extract_fctc_data()` Method

#### Required Fields Extracted (when present):
- **Timestamp** - Submission timestamp
- **Email Address** - Student email
- **Score** - Total score (CRITICAL - must be present)
- **Full name** - Student full name
- **College Name** - College name
- **Year** - Academic year
- **Roll Number** - Roll number
- **Branch** (Non-VIT) - Branch for non-VIT students
- **Division** (Non-VIT) - Division for non-VIT students
- **PRN** (VIT) - PRN for VIT students (CRITICAL - must be present)
- **Branch-Division** (VIT) - Branch-Division for VIT students

#### Key Features:
1. **Selective Extraction**: Only extracts the required fields listed above
2. **Ignore Other Columns**: All other columns in the FCTC file are completely ignored
3. **Critical vs Optional**: 
   - Critical fields (PRN, Score) must be present or processing aborts
   - Optional fields are extracted if present, skipped if missing
4. **Flexible Processing**: Continues processing even if some optional fields are missing
5. **Better Logging**: Shows which fields were found and which were ignored

#### Error Handling:
- Clear error messages if critical columns (PRN, Score) are missing
- Lists available columns to help users identify issues
- Continues processing if only optional fields are missing

## Benefits

1. **Cleaner Data Processing**: Only relevant fields are extracted
2. **Better Performance**: Ignoring unnecessary columns reduces memory usage
3. **More Flexible**: Can handle FCTC files with extra columns without errors
4. **Better User Experience**: Clear feedback about which fields were found/missing
5. **Maintains Compatibility**: Still works with existing Roll Call file processing

## Testing Recommendations

Test with FCTC files that have:
1. All required fields present
2. Extra columns that should be ignored
3. Missing optional fields (should still work)
4. Missing critical fields (should show clear error)

## No Breaking Changes

- Roll Call file processing remains unchanged
- Output format remains the same
- Existing functionality is preserved
- Only the FCTC field extraction logic was enhanced
