<template>
    <div class="summary-container">
      <h2>Professional Dashboard Summary</h2>
  
      <div class="chart-section">
        <h3>Request Overview</h3>
        <canvas id="requestsChart"></canvas>
      </div>
  
      <div class="stat-section">
        <h3>Average Rating</h3>
        <p>{{ summary.average_rating }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import { Chart } from 'chart.js/auto';
  import axios from '@/plugins/axios';
  
  export default {
    name: "ProfessionalSummary",
    data() {
      return {
        summary: {
          assigned_count: 0,
          completed_count: 0,
          average_rating: 0
        },
        requestsChartInstance: null
      };
    },
    mounted() {
      this.fetchSummary();
    },
    methods: {
      async fetchSummary() {
        try {
          const token = localStorage.getItem('access_token');
          const response = await axios.get('/professional/summary', {
            headers: { Authorization: `Bearer ${token}` }
          });
          this.summary = response.data.summary;
  
          this.initRequestsChart();
        } catch (error) {
          console.error('Error fetching professional summary:', error);
        }
      },
      initRequestsChart() {
        if (this.requestsChartInstance) {
          this.requestsChartInstance.destroy();
        }
  
        const ctx = document.getElementById('requestsChart').getContext('2d');
        this.requestsChartInstance = new Chart(ctx, {
          type: 'pie',
          data: {
            labels: ['Assigned Requests', 'Completed Requests'],
            datasets: [
              {
                data: [
                  this.summary.assigned_count,
                  this.summary.completed_count
                ],
                backgroundColor: ['#36A2EB', '#FF6384']
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
  
  .stat-section {
    text-align: center;
    margin-bottom: 40px;
  }
  
  canvas {
    max-width: 600px;
    margin: auto;
    display: block;
  }
  </style>
  