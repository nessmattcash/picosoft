document.addEventListener('DOMContentLoaded', function() {
  const equipmentDataElement = document.getElementById('equipmentData');

  if (equipmentDataElement) {
      try {
          const rawData = JSON.parse(equipmentDataElement.textContent);
          console.log(rawData); // Vérifie le contenu ici

          const labels = rawData.map(item => {
              const dateParts = item.month.split('-');
              return new Date(dateParts[0], dateParts[1] - 1).toLocaleString('default', { month: 'long', year: 'numeric' });
          });

          const data = rawData.map(item => item.count);

          const ctx = document.getElementById("myAreaChart").getContext('2d');
          const myAreaChart = new Chart(ctx, {
              type: 'line',
              data: {
                  labels: labels,
                  datasets: [{
                      label: 'Nombre d\'équipements achetés',
                      data: data,
                      backgroundColor: 'rgba(75, 192, 192, 0.2)',
                      borderColor: 'rgba(75, 192, 192, 1)',
                      borderWidth: 1
                  }]
              },
              options: {
                  scales: {
                      x: {
                          type: 'category',
                          ticks: {
                              autoSkip: false
                          }
                      },
                      y: {
                          beginAtZero: true
                      }
                  }
              }
          });
      } catch (error) {
          console.error('Erreur lors de l\'analyse des données JSON :', error);
      }
  } else {
      console.error('Élément equipmentData introuvable');
  }
});
