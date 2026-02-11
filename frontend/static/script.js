// FCTC Exam Automation System - Pure JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const form = document.getElementById('uploadForm');
    const generateBtn = document.getElementById('generateBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    const messageSection = document.getElementById('messageSection');
    const messageContent = document.getElementById('messageContent');
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');

    // Form submit handler
    form.addEventListener('submit', handleFormSubmit);

    async function handleFormSubmit(event) {
        event.preventDefault();
        
        // Clear previous messages and results
        hideMessage();
        hideResults();
        
        // Get form inputs
        const fctcFile = document.getElementById('fctc_file').files[0];
        const rollCallFile = document.getElementById('roll_call_file').files[0];
        const year = document.getElementById('year').value;
        
        // Comprehensive validation
        const validationResult = validateAllInputs(fctcFile, rollCallFile, year);
        if (!validationResult.isValid) {
            showMessage('error', validationResult.message);
            console.error('Validation failed:', validationResult.message);
            return;
        }
        
        // Show loading state
        setLoadingState(true);
        
        try {
            // Create FormData
            const formData = new FormData();
            formData.append('fctc_file', fctcFile);
            formData.append('roll_call_file', rollCallFile);
            formData.append('year', year);
            
            console.log('Submitting files:', {
                fctc: fctcFile.name,
                rollCall: rollCallFile.name,
                year: year
            });
            
            // Send request
            const response = await fetch('/process', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            console.log('Server response:', result);
            
            if (response.ok && result.success) {
                showMessage('success', result.message);
                if (result.data) {
                    showResults(result.data);
                }
            } else {
                const errorMsg = result.message || 'An error occurred while processing files';
                showMessage('error', errorMsg);
                console.error('Server error:', errorMsg, 'Status:', response.status);
            }
            
        } catch (error) {
            console.error('Network error:', error);
            showMessage('error', 'Network error. Please check your connection and try again.');
        } finally {
            setLoadingState(false);
        }
    }

    function validateAllInputs(fctcFile, rollCallFile, year) {
        // Check if files are selected
        if (!fctcFile) {
            return { isValid: false, message: 'Please select the FCTC Excel file' };
        }
        
        if (!rollCallFile) {
            return { isValid: false, message: 'Please select the Roll Call Excel file' };
        }
        
        // Check year selection
        if (!year || year.trim() === '') {
            return { isValid: false, message: 'Please select an academic year' };
        }
        
        // Validate file types
        const allowedTypes = ['xlsx', 'xls'];
        
        const fctcValidation = validateSingleFile(fctcFile, 'FCTC Excel file', allowedTypes);
        if (!fctcValidation.isValid) {
            return fctcValidation;
        }
        
        const rollCallValidation = validateSingleFile(rollCallFile, 'Roll Call Excel file', allowedTypes);
        if (!rollCallValidation.isValid) {
            return rollCallValidation;
        }
        
        return { isValid: true, message: 'All inputs are valid' };
    }

    function validateSingleFile(file, fileLabel, allowedTypes) {
        if (!file) {
            return { isValid: false, message: `${fileLabel} is required` };
        }
        
        // Check file name
        if (!file.name || file.name.trim() === '') {
            return { isValid: false, message: `${fileLabel} has an invalid name` };
        }
        
        // Check file type
        const extension = file.name.split('.').pop().toLowerCase();
        if (!allowedTypes.includes(extension)) {
            return { 
                isValid: false, 
                message: `${fileLabel} must be an Excel file (.${allowedTypes.join(' or .')})` 
            };
        }
        
        // Check file size (16MB limit)
        const maxSize = 16 * 1024 * 1024;
        if (file.size > maxSize) {
            const sizeMB = (file.size / (1024 * 1024)).toFixed(1);
            return { 
                isValid: false, 
                message: `${fileLabel} is too large (${sizeMB}MB). Maximum size is 16MB.` 
            };
        }
        
        // Check if file is empty
        if (file.size === 0) {
            return { isValid: false, message: `${fileLabel} is empty` };
        }
        
        return { isValid: true, message: 'File is valid' };
    }

    function validateInputs(fctcFile, rollCallFile, year) {
        // Legacy function - keeping for compatibility
        return validateAllInputs(fctcFile, rollCallFile, year).isValid;
    }

    function isValidFileType(filename, allowedTypes) {
        const extension = '.' + filename.split('.').pop().toLowerCase();
        return allowedTypes.includes(extension);
    }

    function setLoadingState(loading) {
        if (loading) {
            generateBtn.disabled = true;
            btnText.style.display = 'none';
            btnLoader.style.display = 'inline-block';
        } else {
            generateBtn.disabled = false;
            btnText.style.display = 'inline';
            btnLoader.style.display = 'none';
        }
    }

    function showMessage(type, message) {
        messageContent.textContent = message;
        messageContent.className = 'message ' + type;
        messageSection.style.display = 'block';
        
        // Scroll to message
        messageSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function hideMessage() {
        messageSection.style.display = 'none';
    }

    function showResults(data) {
        if (!data) return;
        
        let html = '';
        
        // Show statistics
        if (data.matched_students !== undefined || data.year || data.generated_files) {
            html += '<div class="stats">';
            html += '<h4>Processing Summary</h4>';
            
            if (data.matched_students !== undefined) {
                html += '<div class="stat-item">';
                html += '<span class="stat-label">Matched Students:</span>';
                html += '<span class="stat-value">' + data.matched_students + '</span>';
                html += '</div>';
            }
            
            if (data.year) {
                html += '<div class="stat-item">';
                html += '<span class="stat-label">Academic Year:</span>';
                html += '<span class="stat-value">' + data.year + '</span>';
                html += '</div>';
            }
            
            if (data.generated_files && data.generated_files.length > 0) {
                html += '<div class="stat-item">';
                html += '<span class="stat-label">Reports Generated:</span>';
                html += '<span class="stat-value">' + data.generated_files.length + '</span>';
                html += '</div>';
            }
            
            html += '</div>';
        }
        
        // Show download links
        if (data.generated_files && data.generated_files.length > 0) {
            html += '<h4>Download Reports:</h4>';
            html += '<ul class="file-list">';
            
            data.generated_files.forEach(function(file) {
                const fileName = file.split('/').pop();
                const fileType = getFileTypeLabel(file);
                
                html += '<li>';
                html += '<a href="/download/' + encodeURIComponent(file) + '" class="download-link" target="_blank">';
                html += '📄 ' + fileName + ' (' + fileType + ')';
                html += '</a>';
                html += '</li>';
            });
            
            html += '</ul>';
        }
        
        resultsContent.innerHTML = html;
        resultsSection.style.display = 'block';
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function hideResults() {
        resultsSection.style.display = 'none';
    }

    function getFileTypeLabel(filePath) {
        if (filePath.includes('master')) {
            return 'Master Report';
        } else if (filePath.includes('department')) {
            return 'Department Report';
        } else if (filePath.includes('division')) {
            return 'Division Report';
        }
        return 'Report';
    }

    // File input validation on change
    document.getElementById('fctc_file').addEventListener('change', function(event) {
        validateFileOnChange(event.target, 'FCTC Excel file');
    });

    document.getElementById('roll_call_file').addEventListener('change', function(event) {
        validateFileOnChange(event.target, 'Roll Call Excel file');
    });

    function validateFileOnChange(input, fileLabel) {
        const file = input.files[0];
        if (!file) return;
        
        console.log(`Validating ${fileLabel}:`, {
            name: file.name,
            size: file.size,
            type: file.type
        });
        
        const allowedTypes = ['xlsx', 'xls'];
        const validation = validateSingleFile(file, fileLabel, allowedTypes);
        
        if (!validation.isValid) {
            showMessage('error', validation.message);
            input.value = '';
            console.error(`${fileLabel} validation failed:`, validation.message);
            return;
        }
        
        // Clear any previous error messages when valid file is selected
        hideMessage();
        console.log(`${fileLabel} validation passed`);
    }

    // Enhanced file type validation
    function isValidFileType(filename, allowedTypes) {
        if (!filename || typeof filename !== 'string') {
            return false;
        }
        
        const extension = filename.split('.').pop().toLowerCase();
        
        // Remove dots from allowedTypes for comparison
        const cleanAllowedTypes = allowedTypes.map(type => type.replace('.', ''));
        
        return cleanAllowedTypes.includes(extension);
    }

    // Add form validation on input changes
    function setupFormValidation() {
        const fctcInput = document.getElementById('fctc_file');
        const rollCallInput = document.getElementById('roll_call_file');
        const yearSelect = document.getElementById('year');
        
        // Real-time validation
        fctcInput.addEventListener('change', function() {
            validateFileOnChange(this, 'FCTC Excel file');
            checkFormReadiness();
        });
        
        rollCallInput.addEventListener('change', function() {
            validateFileOnChange(this, 'Roll Call Excel file');
            checkFormReadiness();
        });
        
        yearSelect.addEventListener('change', function() {
            checkFormReadiness();
        });
    }

    function checkFormReadiness() {
        const fctcFile = document.getElementById('fctc_file').files[0];
        const rollCallFile = document.getElementById('roll_call_file').files[0];
        const year = document.getElementById('year').value;
        
        const validation = validateAllInputs(fctcFile, rollCallFile, year);
        
        // Enable/disable submit button based on validation
        const submitBtn = document.getElementById('generateBtn');
        if (validation.isValid) {
            submitBtn.style.opacity = '1';
            submitBtn.title = 'Click to generate reports';
        } else {
            submitBtn.style.opacity = '0.7';
            submitBtn.title = validation.message;
        }
    }

    // Initialize form validation when DOM is loaded
    setupFormValidation();
});