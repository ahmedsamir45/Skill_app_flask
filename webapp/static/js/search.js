document.addEventListener('DOMContentLoaded', function() {
        const searchForm = document.querySelector('.form-search');
        const searchInput = document.getElementById('search');
        
        // Submit form when user stops typing (with small delay)
        let typingTimer;
        searchInput.addEventListener('input', function() {
            clearTimeout(typingTimer);
            typingTimer = setTimeout(() => {
                searchForm.submit();
            }, 500); // 500ms delay
        });
        
        // Also allow pressing Enter to submit
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchForm.submit();
            }
        });
    });
  

    console.log("people")