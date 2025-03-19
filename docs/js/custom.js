// Custom JavaScript for Palo Alto Networks SCM Ansible Collection Documentation

document.addEventListener('DOMContentLoaded', function() {
  // Initialize all termynal elements on the page
  const terminals = document.querySelectorAll('[data-termynal]');
  for (let i = 0; i < terminals.length; i++) {
    new Termynal(terminals[i]);
  }

  // Add click handlers for code copy buttons
  const copyButtons = document.querySelectorAll('.md-clipboard');
  copyButtons.forEach(button => {
    button.addEventListener('click', () => {
      // Flash effect for better UX
      button.classList.add('copied');
      setTimeout(() => {
        button.classList.remove('copied');
      }, 1000);
    });
  });

  // Enhance tables by making them sortable
  enhanceTables();
});

// Function to enhance documentation tables
function enhanceTables() {
  const tables = document.querySelectorAll('.md-typeset table:not([class])');
  
  tables.forEach(table => {
    if (table.querySelector('thead')) {
      // Add hover effect to rows
      const rows = table.querySelectorAll('tbody tr');
      rows.forEach(row => {
        row.addEventListener('mouseenter', () => {
          row.classList.add('hovered');
        });
        row.addEventListener('mouseleave', () => {
          row.classList.remove('hovered');
        });
      });
    }
  });
}