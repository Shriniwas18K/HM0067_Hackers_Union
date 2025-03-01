// Handle file input display
document.addEventListener('DOMContentLoaded', function() {
    const resumeInput = document.getElementById('resume');
    
    if (resumeInput) {
      resumeInput.addEventListener('change', function() {
        const fileName = this.files[0]?.name;
        const fileLabel = resumeInput.nextElementSibling;
        
        if (fileLabel && fileName) {
          fileLabel.textContent = fileName;
        }
      });
    }
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    
    if (alerts.length > 0) {
      setTimeout(() => {
        alerts.forEach(alert => {
          alert.style.opacity = '0';
          alert.style.transition = 'opacity 1s';
          
          setTimeout(() => {
            alert.style.display = 'none';
          }, 1000);
        });
      }, 5000);
    }
  });