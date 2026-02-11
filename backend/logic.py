# Business logic for FCTC exam automation - PRN-FIRST PIPELINE ONLY
import pandas as pd
import os

class ExamProcessor:
    """
    PRN-FIRST PIPELINE - EXTRACTS ONLY REQUIRED FIELDS FROM FCTC:
    
    SATAKAM (FCTC) FILE - REQUIRED FIELDS (extracts only these, ignores all others):
    - "Timestamp"
    - "Email Address"
    - "Score" (Total score)
    - "Full name- MANDATORY FOR ALL COLLEGE STUDENTS"
    - "College Name-MANDATORY FOR ALL COLLEGE STUDENTS ( Please select your specific college name carefully and accurately )"
    - "Year-MANDATORY FOR ALL COLLEGE STUDENTS"
    - "Roll Number-MANDATORY FOR ALL COLLEGE STUDENTS"
    - "Branch-MANDATORY ONLY FOR NON-VISHWAKARMA INSTITUTE OF TECHNOLOGY STUDENTS"
    - "Division-MANDATORY ONLY FOR NON-VISHWAKARMA INSTITUTE OF TECHNOLOGY STUDENTS"
    - "PRN - MANDATORY ONLY FOR VISHWAKARMA INSTITUTE OF TECHNOLOGY STUDENTS" (CRITICAL)
    - "Branch-Division- MANDATORY ONLY FOR VISHWAKARMA INSTITUTE OF TECHNOLOGY STUDENTS"
    
    ROLL CALL FILE - REQUIRED EXACT COLUMNS:
    - "PRN"
    - "Roll No" 
    - "Name"
    - "Division"
    (All other columns safely ignored)
    
    RULES:
    1. PRN is the primary and authoritative identifier
    2. Roll No is NOT used for matching (included for reference only)
    3. Division comes ONLY from Roll Call file
    4. FCTC file: Extract ONLY required fields, ignore all other columns
    5. Attendance logic: If PRN exists in FCTC → Present, Else → Absent
    6. Missing critical columns (PRN, Score) = ABORT with clear error
    7. Missing optional fields = Continue processing with available fields
    """
    
    def __init__(self):
        pass
    
    def read_fctc_excel(self, file_path):
        """Read FCTC Excel file and extract ONLY required fields"""
        try:
            from utils import validate_excel_file, log_error
            
            # Validate file
            is_valid, message = validate_excel_file(file_path)
            if not is_valid:
                raise Exception(f"FCTC file validation failed: {message}")
            
            # Read Excel file - try to detect header row
            df = self._read_excel_with_header_detection(file_path)
            
            if df.empty:
                raise Exception("FCTC file contains no data")
            
            # Extract ONLY required fields from FCTC
            cleaned_df = self._extract_fctc_data(df)
            
            print(f"Info: Extracted {len(cleaned_df)} PRN records from FCTC file")
            return cleaned_df
            
        except Exception as e:
            from utils import log_error
            log_error(f"Error reading FCTC Excel file: {file_path}", e)
            raise Exception(f"Error reading FCTC Excel file: {str(e)}")
    
    def read_roll_call_excel(self, file_path):
        """Read Roll Call Excel file and extract PRN, Division, Branch"""
        try:
            from utils import validate_excel_file, log_error
            
            # Validate file
            is_valid, message = validate_excel_file(file_path)
            if not is_valid:
                raise Exception(f"Roll Call file validation failed: {message}")
            
            # Read Excel file - try to detect header row
            df = self._read_excel_with_header_detection(file_path)
            
            if df.empty:
                raise Exception("Roll Call file contains no data")
            
            # Extract PRN, Division, Branch from Roll Call
            cleaned_df = self._extract_roll_call_data(df)
            
            print(f"Info: Extracted {len(cleaned_df)} student records from Roll Call file")
            return cleaned_df
            
        except Exception as e:
            from utils import log_error
            log_error(f"Error reading Roll Call Excel file: {file_path}", e)
            raise Exception(f"Error reading Roll Call Excel file: {str(e)}")
    
    def _read_excel_with_header_detection(self, file_path):
        """
        Read Excel file with automatic header row detection.
        Handles files where headers are not in the first row.
        """
        import pandas as pd
        
        # Try reading with default header (row 0)
        df = pd.read_excel(file_path)
        
        # Check if we got "Unnamed" columns - indicates header issue
        unnamed_count = sum(1 for col in df.columns if str(col).startswith('Unnamed:'))
        
        if unnamed_count > 0:
            print(f"⚠ Detected {unnamed_count} unnamed columns - searching for header row...")
            
            # Read without header to inspect rows
            df_no_header = pd.read_excel(file_path, header=None)
            
            # Search for header row (look for rows with text values, not numbers)
            header_row = None
            for idx in range(min(10, len(df_no_header))):  # Check first 10 rows
                row = df_no_header.iloc[idx]
                
                # Check if this row looks like a header
                # Headers typically have text values and no NaN
                non_null_count = row.notna().sum()
                text_count = sum(1 for val in row if isinstance(val, str) and len(str(val).strip()) > 0)
                
                # If most values are non-null text, this is likely the header
                if text_count >= 3 and non_null_count >= 3:
                    header_row = idx
                    print(f"✓ Found header row at index {idx}")
                    break
            
            if header_row is not None:
                # Re-read with correct header row
                df = pd.read_excel(file_path, header=header_row)
                print(f"✓ Re-read file with header at row {header_row}")
                print(f"✓ Columns found: {list(df.columns)}")
            else:
                # Could not find header - show available data for debugging
                print(f"❌ Could not detect header row automatically")
                print(f"First 5 rows of file:")
                print(df_no_header.head())
                raise Exception("Could not detect header row in Excel file. Please ensure the file has column headers (PRN, Roll No, Name, Division).")
        
        return df
    
    def _extract_fctc_data(self, df):
        """Extract ONLY required fields from FCTC file, ignoring all other columns (CASE-INSENSITIVE)"""
        
        # Create a mapping of lowercase column names to actual column names
        column_map = {col.lower().strip(): col for col in df.columns}
        
        # REQUIRED FIELDS with variations (case-insensitive matching)
        REQUIRED_COLUMNS = {
            'timestamp': ['timestamp'],
            'email': ['email address', 'username', 'email'],
            'score': ['score', 'total score', 'marks', 'total marks'],
            'full_name': ['full name- mandatory for all college students', 'full name', 'name', 'student name'],
            'college_name': ['college name-mandatory for all college students ( please select your specific college name carefully and accurately )', 'college name', 'college'],
            'year': ['year-mandatory for all college students', 'year', 'academic year'],
            'roll_number': ['roll number-mandatory for all college students', 'roll number', 'roll no', 'rollno'],
            'branch_non_vit': ['branch-mandatory only for non-vishwakarma institute of technology students', 'branch'],
            'division_non_vit': ['division-mandatory only for non-vishwakarma institute of technology students', 'division', 'div'],
            'prn_vit': ['prn - mandatory only for vishwakarma institute of technology students', 'prn'],
            'branch_division_vit': ['branch-division- mandatory only for vishwakarma institute of technology students', 'branch-division', 'branch division']
        }
        
        # Check which required columns are present in the file (case-insensitive)
        available_columns = list(df.columns)
        found_columns = {}
        missing_columns = []
        
        for key, col_variations in REQUIRED_COLUMNS.items():
            found = False
            for col_name in col_variations:
                if col_name.lower() in column_map:
                    found_columns[key] = column_map[col_name.lower()]
                    found = True
                    break
            
            if not found:
                missing_columns.append(col_variations[0])  # Add primary name to missing list
        
        # STRICT VALIDATION: Check if critical columns exist (PRN and Score are mandatory)
        critical_missing = []
        if 'prn_vit' not in found_columns:
            critical_missing.append('PRN')
        if 'score' not in found_columns:
            critical_missing.append('Score (or Total score)')
        
        if critical_missing:
            error_msg = f"❌ FCTC FILE ERROR: Missing critical required columns\n\n"
            error_msg += f"Missing critical columns (case-insensitive search):\n"
            for col in critical_missing:
                error_msg += f"  • '{col}'\n"
            error_msg += f"\nAvailable columns in your file:\n"
            for col in available_columns:
                error_msg += f"  • '{col}'\n"
            error_msg += f"\n💡 Column matching is case-insensitive. Please ensure your FCTC file has PRN and Score columns."
            raise Exception(error_msg)
        
        # Extract ONLY the required columns that are present (ignore all others)
        result_data = {}
        
        # Always extract PRN and Score (critical fields)
        result_data['PRN_ORIGINAL'] = df[found_columns['prn_vit']]
        result_data['Total_Score'] = df[found_columns['score']]
        
        # Extract optional fields if present
        if 'timestamp' in found_columns:
            result_data['Timestamp'] = df[found_columns['timestamp']]
        if 'email' in found_columns:
            result_data['Email'] = df[found_columns['email']]
        if 'full_name' in found_columns:
            result_data['Full_Name'] = df[found_columns['full_name']]
        if 'college_name' in found_columns:
            result_data['College_Name'] = df[found_columns['college_name']]
        if 'year' in found_columns:
            result_data['Year'] = df[found_columns['year']]
        if 'roll_number' in found_columns:
            result_data['Roll_Number'] = df[found_columns['roll_number']]
        if 'branch_non_vit' in found_columns:
            result_data['Branch_Non_VIT'] = df[found_columns['branch_non_vit']]
        if 'division_non_vit' in found_columns:
            result_data['Division_Non_VIT'] = df[found_columns['division_non_vit']]
        if 'branch_division_vit' in found_columns:
            result_data['Branch_Division_VIT'] = df[found_columns['branch_division_vit']]
        
        result_df = pd.DataFrame(result_data)
        
        # Create PRN_CLEAN using exact normalization logic
        result_df['PRN_CLEAN'] = self._normalize_prn(result_df['PRN_ORIGINAL'])
        
        # STRICT VALIDATION: Check if any valid PRNs found after normalization
        valid_mask = result_df['PRN_CLEAN'].notna() & (result_df['PRN_CLEAN'] != '')
        result_df = result_df[valid_mask]
        
        if len(result_df) == 0:
            error_msg = f"❌ FCTC FILE ERROR: No valid PRNs found\n\n"
            error_msg += f"The FCTC file contains no valid PRN values after cleaning.\n"
            error_msg += f"Common issues:\n"
            error_msg += f"  • All PRN values are empty or invalid\n"
            error_msg += f"  • PRN column contains only 'NaN', 'NONE', or blank values\n"
            error_msg += f"  • File may be corrupted or incorrectly formatted\n\n"
            error_msg += f"💡 Please check your FCTC file and ensure it contains valid PRN values."
            raise Exception(error_msg)
        
        # Clean Total Score values using exact Streamlit logic
        result_df['Total_Score'] = self._process_total_score(result_df['Total_Score'])
        
        # Handle multiple exam attempts per student
        result_df = self._handle_multiple_attempts(result_df)
        
        print(f"✓ FCTC Data Extracted: {len(result_df)} unique PRN records")
        print(f"✓ Extracted {len(found_columns)} required fields, ignored {len(available_columns) - len(found_columns)} other columns")
        print(f"✓ Required fields found: {list(found_columns.keys())}")
        if missing_columns:
            print(f"⚠ Optional fields not found: {len(missing_columns)} columns")
        print(f"✓ Created PRN_CLEAN column with normalized values")
        print(f"✓ Processed Total_Score using Streamlit-compatible logic")
        print(f"✓ Handled multiple exam attempts - kept MAX score per PRN")
        return result_df
    
    def _extract_roll_call_data(self, df):
        """Extract PRN, Division, Branch from Roll Call file using CASE-INSENSITIVE column matching"""
        
        # Create a mapping of lowercase column names to actual column names
        column_map = {col.lower().strip(): col for col in df.columns}
        
        # Define required fields with their possible variations (case-insensitive)
        REQUIRED_FIELDS = {
            'prn': ['prn'],
            'roll_no': ['roll no', 'rollno', 'roll_no', 'roll number', 'sr.no', 'srno', 'sr no'],
            'name': ['name', 'student name', 'full name'],
            'division': ['division', 'div', 'section', 'class']
        }
        
        # Find actual column names (case-insensitive)
        found_columns = {}
        
        for field, variations in REQUIRED_FIELDS.items():
            found = False
            for variation in variations:
                if variation.lower() in column_map:
                    found_columns[field] = column_map[variation.lower()]
                    found = True
                    break
            
            if not found:
                # Try partial matching for division (handles 'dIV', 'DIV', etc.)
                if field == 'division':
                    for col_lower, col_actual in column_map.items():
                        if 'div' in col_lower:
                            found_columns[field] = col_actual
                            found = True
                            break
        
        # STRICT VALIDATION: Check if required columns exist
        missing_fields = []
        
        if 'prn' not in found_columns:
            missing_fields.append('PRN')
        
        if 'roll_no' not in found_columns:
            missing_fields.append('Roll No (or Sr.no)')
        
        if 'name' not in found_columns:
            missing_fields.append('Name')
        
        if 'division' not in found_columns:
            missing_fields.append('Division (or DIV/div/dIV)')
        
        if missing_fields:
            available_columns = list(df.columns)
            error_msg = f"❌ ROLL CALL FILE ERROR: Missing required columns\n\n"
            error_msg += f"Missing columns (case-insensitive search):\n"
            for field in missing_fields:
                error_msg += f"  • '{field}'\n"
            error_msg += f"\nAvailable columns in your file:\n"
            for col in available_columns:
                error_msg += f"  • '{col}'\n"
            error_msg += f"\n💡 Column matching is case-insensitive. Please ensure your Roll Call file has these columns."
            raise Exception(error_msg)
        
        # Extract required columns using found names (PRESERVE ORIGINALS)
        result_df = pd.DataFrame({
            'PRN_ORIGINAL': df[found_columns['prn']],      # Preserve original
            'Roll_No': df[found_columns['roll_no']],       # Store but don't use for matching
            'Name': df[found_columns['name']],
            'Division': df[found_columns['division']]      # Use the found division column
        })
        
        # Create PRN_CLEAN using exact normalization logic
        result_df['PRN_CLEAN'] = self._normalize_prn(result_df['PRN_ORIGINAL'])
        
        # STRICT VALIDATION: Check if any valid PRNs found after normalization
        valid_mask = result_df['PRN_CLEAN'].notna() & (result_df['PRN_CLEAN'] != '')
        result_df = result_df[valid_mask]
        
        if len(result_df) == 0:
            error_msg = f"❌ ROLL CALL FILE ERROR: No valid PRNs found\n\n"
            error_msg += f"The Roll Call file contains no valid PRN values after cleaning.\n"
            error_msg += f"Common issues:\n"
            error_msg += f"  • All PRN values are empty or invalid\n"
            error_msg += f"  • PRN column contains only 'NaN', 'NONE', or blank values\n"
            error_msg += f"  • File may be corrupted or incorrectly formatted\n\n"
            error_msg += f"💡 Please check your Roll Call file and ensure it contains valid PRN values."
            raise Exception(error_msg)
        
        # Clean other values
        result_df['Roll_No'] = result_df['Roll_No'].astype(str).str.strip()
        result_df['Name'] = result_df['Name'].astype(str).str.strip()
        result_df['Division'] = result_df['Division'].astype(str).str.strip().str.upper()
        
        print(f"✓ Roll Call Data Extracted: {len(result_df)} valid student records")
        print(f"✓ Used columns (case-insensitive match):")
        print(f"  - PRN: '{found_columns['prn']}'")
        print(f"  - Roll No: '{found_columns['roll_no']}'")
        print(f"  - Name: '{found_columns['name']}'")
        print(f"  - Division: '{found_columns['division']}'")
        print(f"✓ Created PRN_CLEAN column with normalized values")
        print(f"✓ Safely ignored all other columns in Roll Call file")
        return result_df
    
    def _normalize_prn(self, prn_series):
        """
        Normalize PRN values using EXACT logic:
        - Convert to string
        - Strip whitespace  
        - Convert to uppercase
        - Remove decimal points (handle .0 suffix from Excel)
        - Remove invalid values: "", "NAN", "NONE", "NAT"
        """
        
        # Step 1: Convert to string
        normalized = prn_series.astype(str)
        
        # Step 2: Strip whitespace
        normalized = normalized.str.strip()
        
        # Step 3: Remove decimal points (handle Excel float formatting like "12345.0" → "12345")
        normalized = normalized.str.replace(r'\.0+$', '', regex=True)
        
        # Step 4: Convert to uppercase (for any alphabetic PRNs)
        normalized = normalized.str.upper()
        
        # Step 5: Remove invalid values
        invalid_values = ["", "NAN", "NONE", "NAT"]
        
        # Replace invalid values with empty string (will be filtered out later)
        for invalid_value in invalid_values:
            normalized = normalized.replace(invalid_value, "")
        
        print(f"✓ PRN Normalization completed:")
        print(f"  Original count: {len(prn_series)}")
        print(f"  Valid after normalization: {len(normalized[normalized != ''])}")
        print(f"  Removed invalid values: {invalid_values}")
        print(f"  ✓ Fixed decimal formatting (.0 suffix removed)")
        
        # DEBUG: Show sample original vs normalized PRNs
        if len(prn_series) > 0:
            print(f"🔍 DEBUG - PRN Normalization samples:")
            for i in range(min(3, len(prn_series))):
                original = prn_series.iloc[i] if hasattr(prn_series, 'iloc') else prn_series[i]
                norm = normalized.iloc[i] if hasattr(normalized, 'iloc') else normalized[i]
                print(f"  '{original}' → '{norm}'")
        
        return normalized
    
    def _process_total_score(self, score_series):
        """
        Process Satakam "Total score" column exactly as Streamlit implementation:
        - Convert value to string
        - Split on "/"
        - Keep only the numeric score part
        - Convert to float
        - Invalid values → NaN
        """
        
        def process_single_score(score_value):
            try:
                # Step 1: Convert value to string
                score_str = str(score_value)
                
                # Step 2: Split on "/"
                if "/" in score_str:
                    # Keep only the numeric score part (before the "/")
                    score_str = score_str.split("/")[0]
                
                # Step 3: Convert to float
                score_float = float(score_str)
                
                return score_float
                
            except (ValueError, TypeError, AttributeError):
                # Step 4: Invalid values → NaN
                return pd.NA
        
        # Apply processing to entire series
        processed_scores = score_series.apply(process_single_score)
        
        # Convert to float dtype with NaN support
        processed_scores = pd.to_numeric(processed_scores, errors='coerce')
        
        print(f"✓ Total Score Processing completed:")
        print(f"  Original count: {len(score_series)}")
        print(f"  Valid scores after processing: {len(processed_scores.dropna())}")
        print(f"  Invalid/NaN scores: {len(processed_scores) - len(processed_scores.dropna())}")
        
        return processed_scores
    
    def _handle_multiple_attempts(self, fctc_df):
        """
        Handle multiple exam attempts per student:
        - Group Satakam data by PRN_CLEAN
        - Keep the MAX score per PRN
        - Count duplicate attempts for reporting
        - Output must contain exactly ONE row per PRN
        """
        
        if fctc_df.empty:
            return fctc_df
        
        # Count total records before deduplication
        total_records = len(fctc_df)
        
        # Count attempts per PRN
        attempt_counts = fctc_df['PRN_CLEAN'].value_counts()
        duplicate_prns = attempt_counts[attempt_counts > 1]
        
        print(f"✓ Multiple Attempts Analysis:")
        print(f"  Total FCTC records: {total_records}")
        print(f"  Unique PRNs: {len(attempt_counts)}")
        print(f"  PRNs with multiple attempts: {len(duplicate_prns)}")
        
        if len(duplicate_prns) > 0:
            print(f"  Duplicate attempt details:")
            for prn, count in duplicate_prns.head(10).items():  # Show first 10
                print(f"    {prn}: {count} attempts")
            if len(duplicate_prns) > 10:
                print(f"    ... and {len(duplicate_prns) - 10} more PRNs with duplicates")
        
        # Group by PRN_CLEAN and aggregate
        # For each PRN, keep the row with the maximum Total_Score
        # Handle NaN scores properly (NaN should not be considered as max)
        
        def get_best_attempt(group):
            """Get the row with maximum score, handling NaN values"""
            # Filter out NaN scores first
            valid_scores = group.dropna(subset=['Total_Score'])
            
            if len(valid_scores) > 0:
                # Return row with maximum valid score
                max_idx = valid_scores['Total_Score'].idxmax()
                best_row = group.loc[max_idx].copy()
            else:
                # All scores are NaN, just take the first row
                best_row = group.iloc[0].copy()
            
            # Add attempt count information
            best_row['Attempt_Count'] = len(group)
            
            return best_row
        
        # Group by PRN_CLEAN and get best attempt for each
        deduplicated_df = fctc_df.groupby('PRN_CLEAN', group_keys=False).apply(get_best_attempt).reset_index(drop=True)
        
        # Verify exactly one row per PRN
        final_unique_prns = len(deduplicated_df['PRN_CLEAN'].unique())
        final_total_rows = len(deduplicated_df)
        
        if final_unique_prns != final_total_rows:
            raise Exception(f"ERROR: Deduplication failed - {final_total_rows} rows but {final_unique_prns} unique PRNs")
        
        print(f"✓ Deduplication Results:")
        print(f"  Final records: {final_total_rows} (exactly one per PRN)")
        print(f"  Records removed: {total_records - final_total_rows}")
        print(f"  MAX score kept for each PRN")
        
        return deduplicated_df
    
    def process_and_generate_reports(self, fctc_file_path, roll_call_file_path, year=None):
        """PRN-FIRST PIPELINE: Process data according to established rules"""
        try:
            # Step 1: Extract data according to rules
            fctc_df = self.read_fctc_excel(fctc_file_path)  # PRN + Total Score ONLY
            roll_call_df = self.read_roll_call_excel(roll_call_file_path)  # PRN + Division + Branch + Name
            
            # Step 2: PRN-based matching and attendance logic
            master_df = self._create_prn_based_report(fctc_df, roll_call_df)
            
            # Step 3: Generate reports using master DataFrame
            report_files = self._generate_reports(master_df)
            
            return {
                'success': True,
                'message': 'PRN-first pipeline completed successfully',
                'matched_students': len(master_df[master_df['Attendance'] == 'Present']),
                'reports': {
                    'files_created': report_files
                }
            }
            
        except Exception as e:
            raise Exception(f"Error in PRN-first processing: {str(e)}")
    
    def _create_prn_based_report(self, fctc_df, roll_call_df):
        """Create final report using PRN-first attendance logic and score mapping"""
        
        # STRICT VALIDATION: Check if master DataFrame will be empty
        if len(roll_call_df) == 0:
            error_msg = f"❌ PROCESSING ERROR: No students found in Roll Call file\n\n"
            error_msg += f"Cannot create master DataFrame with zero students.\n"
            error_msg += f"Please check your Roll Call file and ensure it contains valid student data."
            raise Exception(error_msg)
        
        # Start with Roll Call as the master list (contains all students)
        final_df = roll_call_df.copy()
        
        # ATTENDANCE LOGIC: Create set of PRN_CLEAN from Satakam data
        satakam_prns = set(fctc_df['PRN_CLEAN'].tolist())
        
        # SCORE MAPPING: Create dictionary PRN_CLEAN → Score
        score_mapping = {}
        for _, row in fctc_df.iterrows():
            prn_clean = row['PRN_CLEAN']
            score = row['Total_Score']
            
            # Round score to 2 decimal places if it's a valid number
            if pd.notna(score):
                score_mapping[prn_clean] = round(float(score), 2)
            else:
                score_mapping[prn_clean] = pd.NA  # Keep NaN for invalid scores
        
        print(f"✓ Attendance Logic:")
        print(f"  PRNs found in Satakam: {len(satakam_prns)}")
        print(f"  Total students in Roll Call: {len(final_df)}")
        print(f"✓ Score Mapping:")
        print(f"  Created PRN_CLEAN → Score dictionary with {len(score_mapping)} entries")
        
        # DEBUG: Show sample PRNs for comparison
        print(f"🔍 DEBUG - PRN Matching Analysis:")
        print(f"  Sample Satakam PRNs: {list(satakam_prns)[:5]}")
        print(f"  Sample Roll Call PRNs: {final_df['PRN_CLEAN'].head().tolist()}")
        
        # Check for exact matches
        roll_call_prns = set(final_df['PRN_CLEAN'].tolist())
        matching_prns = satakam_prns.intersection(roll_call_prns)
        print(f"  Exact PRN matches found: {len(matching_prns)}")
        if len(matching_prns) > 0:
            print(f"  Sample matches: {list(matching_prns)[:5]}")
        else:
            print(f"  ❌ NO MATCHES FOUND - investigating...")
            print(f"  Satakam PRN sample: '{list(satakam_prns)[0] if satakam_prns else 'NONE'}'")
            print(f"  Roll Call PRN sample: '{list(roll_call_prns)[0] if roll_call_prns else 'NONE'}'")
            if satakam_prns and roll_call_prns:
                sat_sample = list(satakam_prns)[0]
                roll_sample = list(roll_call_prns)[0]
                print(f"  Length comparison: Satakam='{len(sat_sample)}', Roll Call='{len(roll_sample)}'")
                print(f"  Character comparison: Satakam='{[ord(c) for c in sat_sample]}', Roll Call='{[ord(c) for c in roll_sample]}'")
        
        # Apply attendance logic: If PRN_CLEAN exists in Satakam → Present, Else → Absent
        # DO NOT use roll numbers or division for attendance logic
        final_df['Attendance'] = final_df['PRN_CLEAN'].apply(
            lambda prn_clean: 'Present' if prn_clean in satakam_prns else 'Absent'
        )
        
        # Map scores from Satakam to Roll Call using PRN_CLEAN dictionary
        # Add column "Score" to Roll Call
        final_df['Score'] = final_df['PRN_CLEAN'].map(score_mapping)
        
        # Absent students must have NaN score (override any mapped scores)
        absent_mask = final_df['Attendance'] == 'Absent'
        final_df.loc[absent_mask, 'Score'] = pd.NA
        
        # Add attempt count information from FCTC data
        attempt_mapping = {}
        for _, row in fctc_df.iterrows():
            attempt_mapping[row['PRN_CLEAN']] = row['Attempt_Count']
        
        final_df['Attempt_Count'] = final_df['PRN_CLEAN'].map(attempt_mapping)
        final_df.loc[absent_mask, 'Attempt_Count'] = 0  # Absent students have 0 attempts
        
        # Calculate statistics for summary report
        total_students = len(final_df)
        present_students = len(final_df[final_df['Attendance'] == 'Present'])
        absent_students = len(final_df[final_df['Attendance'] == 'Absent'])
        multiple_attempts = len(fctc_df[fctc_df['Attempt_Count'] > 1])
        
        # Create the ONE master DataFrame with exact column order
        # Roll No | PRN | Name | Division | Attendance | Score
        master_df = pd.DataFrame({
            'Roll No': final_df['Roll_No'],           # Keep Roll No as-is from Roll Call
            'PRN': final_df['PRN_ORIGINAL'],          # Use original PRN (remove PRN_CLEAN)
            'Name': final_df['Name'],
            'Division': final_df['Division'],
            'Attendance': final_df['Attendance'],
            'Score': final_df['Score']
        })
        
        # STRICT VALIDATION: Check if master DataFrame is empty
        if len(master_df) == 0:
            error_msg = f"❌ PROCESSING ERROR: Master DataFrame is empty\n\n"
            error_msg += f"Failed to create master DataFrame with student data.\n"
            error_msg += f"This should not happen if Roll Call file contains valid data.\n"
            error_msg += f"Please contact support if this error persists."
            raise Exception(error_msg)
        
        # Store statistics for summary report
        self._processing_stats = {
            'total_students': total_students,
            'present_students': present_students,
            'absent_students': absent_students,
            'multiple_attempts': multiple_attempts,
            'attendance_percentage': (present_students / total_students * 100) if total_students > 0 else 0
        }
        
        # Score statistics for present students only
        present_scores = master_df[master_df['Attendance'] == 'Present']['Score']
        valid_scores = present_scores.dropna()
        invalid_scores = len(present_scores) - len(valid_scores)
        
        print(f"✓ Master DataFrame Created:")
        print(f"  Columns: Roll No | PRN | Name | Division | Attendance | Score")
        print(f"  Total Students: {total_students}")
        print(f"  Present: {present_students}")
        print(f"  Absent: {absent_students}")
        print(f"  Students with multiple attempts: {multiple_attempts}")
        print(f"  Present students with valid scores: {len(valid_scores)}")
        print(f"  Present students with invalid scores (NaN): {invalid_scores}")
        print(f"  ✓ Roll No kept as-is from Roll Call")
        print(f"  ✓ PRN_CLEAN removed before saving")
        print(f"  ✓ This master DataFrame is the base for ALL exports")
        
        # Verify no duplicate PRNs in master DataFrame
        duplicate_prns = master_df['PRN'].duplicated().sum()
        if duplicate_prns > 0:
            raise Exception(f"ERROR: {duplicate_prns} duplicate PRNs found in master DataFrame")
        
        return master_df
    
    def _generate_reports(self, master_df):
        """Generate Excel reports based on master DataFrame"""
        
        # Ensure output directories exist
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        master_output_dir = os.path.join(project_root, 'outputs', 'master')
        division_output_dir = os.path.join(project_root, 'outputs', 'division')
        os.makedirs(master_output_dir, exist_ok=True)
        os.makedirs(division_output_dir, exist_ok=True)
        
        generated_files = []
        
        # Generate master report using the ONE master DataFrame
        master_file = os.path.join(master_output_dir, 'Final_Master_Report.xlsx')
        
        # This file must always be generated if processing succeeds
        self._generate_master_report_with_summary(master_df, master_file)
        
        generated_files.append('master/Final_Master_Report.xlsx')
        print(f"✓ Generated: Final_Master_Report.xlsx")
        print(f"  Sheets: Attendance | Summary")
        print(f"  Records: {len(master_df)}")
        print(f"  This file must always be generated if processing succeeds")
        
        # Generate division-wise reports derived ONLY from master DataFrame
        division_files = self._generate_division_reports_from_master(master_df, division_output_dir)
        generated_files.extend(division_files)
        
        print(f"✓ This master DataFrame is the base for ALL exports")
        
        return generated_files
    
    def _generate_division_reports_from_master(self, master_df, division_output_dir):
        """
        Generate division-wise reports derived ONLY from the master DataFrame
        For each unique Division:
        1. Filter rows where Division == current division
        2. Sort by Roll No
        3. Reassign Roll No sequentially starting from 1
        4. Save file as: outputs/division/Division_<Division>.xlsx
        Never generate a division file if student count == 0
        """
        
        generated_files = []
        
        # Get unique divisions from master DataFrame
        unique_divisions = master_df['Division'].dropna().unique()
        unique_divisions = [div for div in unique_divisions if str(div).strip() != '']
        
        print(f"✓ Division-wise Report Generation:")
        print(f"  Found {len(unique_divisions)} unique divisions: {list(unique_divisions)}")
        
        for division in unique_divisions:
            try:
                # Step 1: Filter rows where Division == current division
                division_df = master_df[master_df['Division'] == division].copy()
                
                # Never generate a division file if student count == 0
                if len(division_df) == 0:
                    print(f"  ✗ Division {division}: 0 students - SKIPPING file generation")
                    continue
                
                print(f"  ✓ Division {division}: {len(division_df)} students")
                
                # Step 2: Sort by Roll No
                division_df = division_df.sort_values('Roll No').reset_index(drop=True)
                
                # Step 3: Reassign Roll No sequentially starting from 1
                division_df['Roll No'] = range(1, len(division_df) + 1)
                
                # Step 4: Save file as Division_<Division>.xlsx
                safe_division_name = str(division).replace('/', '_').replace('\\', '_').replace(':', '_')
                filename = f"Division_{safe_division_name}.xlsx"
                file_path = os.path.join(division_output_dir, filename)
                
                # Create safe sheet name (Excel has restrictions on sheet names)
                safe_sheet_name = f"Division {safe_division_name}"
                
                # STRICT VALIDATION: Create Excel file with error handling
                try:
                    # Create Excel file with formatting
                    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                        # Write division DataFrame (derived from master)
                        division_df.to_excel(writer, sheet_name=safe_sheet_name, index=False)
                        
                        # Get workbook and worksheet for formatting
                        workbook = writer.book
                        worksheet = writer.sheets[safe_sheet_name]
                        
                        # Auto-adjust column widths
                        for column in worksheet.columns:
                            max_length = 0
                            column_letter = column[0].column_letter
                            for cell in column:
                                try:
                                    if len(str(cell.value)) > max_length:
                                        max_length = len(str(cell.value))
                                except:
                                    pass
                            adjusted_width = min(max_length + 2, 50)
                            worksheet.column_dimensions[column_letter].width = adjusted_width
                
                except Exception as e:
                    print(f"    ✗ ERROR: Failed to create Excel file for Division {division}: {str(e)}")
                    continue
                
                # STRICT VALIDATION: Verify file was created successfully
                if not os.path.exists(file_path):
                    print(f"    ✗ ERROR: Division file not created: {filename}")
                    continue
                
                # STRICT VALIDATION: Verify file is not empty or corrupted
                try:
                    file_size = os.path.getsize(file_path)
                    if file_size < 1000:  # Excel files should be at least 1KB
                        print(f"    ✗ ERROR: Division file is too small ({file_size} bytes): {filename}")
                        # Remove corrupted file
                        try:
                            os.remove(file_path)
                        except:
                            pass
                        continue
                except OSError as e:
                    print(f"    ✗ ERROR: Cannot verify division file: {filename} - {str(e)}")
                    continue
                
                # File validation passed - add to generated files list
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    relative_path = f'division/{filename}'
                    generated_files.append(relative_path)
                    
                    print(f"    ✓ Created: {filename} ({file_size} bytes)")
                    print(f"    ✓ Students: {len(division_df)} with sequential Roll No 1-{len(division_df)}")
                    print(f"    ✓ Derived ONLY from master DataFrame")
                    print(f"    ✓ File validated successfully")
                else:
                    print(f"    ✗ ERROR: Failed to create {filename}")
                
            except Exception as e:
                print(f"  ✗ Error creating division report for {division}: {e}")
                continue
        
        print(f"✓ Division Reports Summary:")
        print(f"  Total divisions processed: {len(unique_divisions)}")
        print(f"  Files generated: {len(generated_files)}")
        
        return generated_files
    
    def _generate_master_report_with_summary(self, master_df, file_path):
        """
        Generate master report with Attendance and Summary sheets
        Export to: outputs/master/Final_Master_Report.xlsx
        Include:
        - Attendance sheet (master DataFrame)
        - Summary sheet (statistics)
        This file must always be generated if processing succeeds
        """
        
        # Calculate statistics for summary sheet
        total_students = len(master_df)
        present_count = len(master_df[master_df['Attendance'] == 'Present'])
        absent_count = len(master_df[master_df['Attendance'] == 'Absent'])
        attendance_percentage = (present_count / total_students * 100) if total_students > 0 else 0
        
        # Get duplicate attempts from processing stats if available
        duplicate_attempts = getattr(self, '_processing_stats', {}).get('multiple_attempts', 0)
        
        # Create summary data
        summary_data = pd.DataFrame({
            'Metric': [
                'Total Students',
                'Present Count', 
                'Absent Count',
                'Attendance %',
                'Duplicate Attempts'
            ],
            'Value': [
                total_students,
                present_count,
                absent_count,
                f"{attendance_percentage:.1f}%",
                duplicate_attempts
            ]
        })
        
        # STRICT VALIDATION: Create Excel file with error handling
        try:
            # Create Excel file with multiple sheets
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # Sheet 1: Attendance (master DataFrame)
                master_df.to_excel(writer, sheet_name='Attendance', index=False)
                
                # Sheet 2: Summary (statistics) - start from row 2 to leave space for title
                summary_data.to_excel(writer, sheet_name='Summary', index=False, startrow=1)
                
                # Format Attendance sheet
                attendance_sheet = writer.sheets['Attendance']
                self._format_excel_sheet(attendance_sheet)
                
                # Format Summary sheet
                summary_sheet = writer.sheets['Summary']
                self._format_excel_sheet(summary_sheet)
                
                # Add title to Summary sheet
                from openpyxl.styles import Font
                
                summary_sheet['A1'] = 'FCTC Exam Report Summary'
                summary_sheet['A1'].font = Font(bold=True, size=14)
                
                # Make headers bold
                summary_sheet['A2'].font = Font(bold=True)
                summary_sheet['B2'].font = Font(bold=True)
        
        except Exception as e:
            error_msg = f"❌ EXCEL CREATION ERROR: Failed to create master report\n\n"
            error_msg += f"Could not create file: {file_path}\n"
            error_msg += f"Error details: {str(e)}\n\n"
            error_msg += f"Common causes:\n"
            error_msg += f"  • File is open in Excel (close it and try again)\n"
            error_msg += f"  • Insufficient disk space\n"
            error_msg += f"  • Permission issues with output directory\n\n"
            error_msg += f"💡 Please ensure the output directory is writable and try again."
            raise Exception(error_msg)
        
        # STRICT VALIDATION: Verify file was created successfully
        if not os.path.exists(file_path):
            error_msg = f"❌ FILE CREATION ERROR: Master report file not found\n\n"
            error_msg += f"Expected file: {file_path}\n"
            error_msg += f"The file was not created successfully.\n\n"
            error_msg += f"💡 Please check output directory permissions and try again."
            raise Exception(error_msg)
        
        # STRICT VALIDATION: Verify file is not empty or corrupted
        try:
            file_size = os.path.getsize(file_path)
            if file_size < 1000:  # Excel files should be at least 1KB
                error_msg = f"❌ FILE CORRUPTION ERROR: Master report file is too small\n\n"
                error_msg += f"File: {file_path}\n"
                error_msg += f"Size: {file_size} bytes (expected > 1000 bytes)\n"
                error_msg += f"The file may be corrupted or empty.\n\n"
                error_msg += f"💡 Please try again or contact support if the issue persists."
                raise Exception(error_msg)
        except OSError as e:
            error_msg = f"❌ FILE ACCESS ERROR: Cannot verify master report file\n\n"
            error_msg += f"File: {file_path}\n"
            error_msg += f"Error: {str(e)}\n\n"
            error_msg += f"💡 Please check file permissions and try again."
            raise Exception(error_msg)
        
        print(f"✓ Master Report Details:")
        print(f"  File: Final_Master_Report.xlsx")
        print(f"  Attendance Sheet: {total_students} students")
        print(f"  Summary Sheet: 5 key metrics")
        print(f"  File size: {file_size} bytes")
        print(f"  ✓ File created successfully and validated")
    
    def _format_excel_sheet(self, worksheet):
        """Apply consistent formatting to Excel worksheet"""
        
        # Auto-adjust column widths
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    def process_and_generate_reports_with_warnings(self, fctc_file_path, roll_call_file_path, year=None):
        """Fallback method - same as main method for PRN-first approach"""
        return self.process_and_generate_reports(fctc_file_path, roll_call_file_path, year)