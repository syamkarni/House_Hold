<template>
    <div class="summary-container">
      <h2>Admin Dashboard Summary</h2>
  
      <div class="chart-section">
        <h3>Users and Professionals Overview</h3>
        <canvas id="overviewChart"></canvas>
      </div>
  
      <div class="chart-section">
        <h3>Services Distribution (Packages per Service)</h3>
        <canvas id="servicesChart"></canvas>
      </div>
    </div>
  </template>
  
  <script>
  import { Chart } from 'chart.js/auto';
  import axios from 'axios';
  
  export default {
    name: "AdminSummary",
    data() {
      return {
        summary: {
          total_users: 0,
          active_professionals: 0,
          pending_professionals: 0,
          total_services: 0,
          services_distribution: []
        },
        overviewChartInstance: null,
        servicesChartInstance: null
      };
    },
    mounted() {
      this.fetchSummaryData();
    },
    methods: {
      async fetchSummaryData() {
        try {
          const response = await axios.get('/admin/summary', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`
            }
          });
  
          this.summary = response.data.summary;
  
          this.initializeOverviewChart();
          this.initializeServicesChart();
        } catch (error) {
          console.error('Error fetching summary data:', error);
        }
      },
  
      initializeOverviewChart() {
        if (this.overviewChartInstance) {
          this.overviewChartInstance.destroy();
        }
  
        const ctx = document.getElementById('overviewChart').getContext('2d');
        this.overviewChartInstance = new Chart(ctx, {
          type: 'doughnut',
          data: {
            labels: [
              'Total Users',
              'Active Professionals',
              'Pending Professionals',
              'Total Services'
            ],
            datasets: [
              {
                data: [
                  this.summary.total_users,
                  this.summary.active_professionals,
                  this.summary.pending_professionals,
                  this.summary.total_services
                ],
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
              }
            ]
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: 'top'
              }
            }
          }
        });
      },
  
      initializeServicesChart() {
        if (this.servicesChartInstance) {
          this.servicesChartInstance.destroy();
        }
  
        const ctx = document.getElementById('servicesChart').getContext('2d');
        const labels = this.summary.services_distribution.map(
          (item) => item.service_name
        );
        const data = this.summary.services_distribution.map(
          (item) => item.package_count
        );
  
        this.servicesChartInstance = new Chart(ctx, {
          type: 'bar',
          data: {
            labels,
            datasets: [
              {
                label: 'Number of Packages',
                data,
                backgroundColor: 'rgba(75, 192, 192, 0.5)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
              }
            ]
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      }
    }
  };
  </script>
  
  <style scoped>
  .summary-container {
    padding: 20px;
  }
  
  .chart-section {
    margin-bottom: 40px;
  }
  
  h3 {
    text-align: center;
    margin-bottom: 10px;
  }
  
  canvas {
    max-width: 600px;
    margin: auto;
    display: block;
  }
  </style>
  