<template>
    <div class="summary-container">
      <h2>Customer Dashboard Summary</h2>
  
      <div class="chart-section">
        <h3>Service Requests Overview</h3>
        <canvas id="requestsChart"></canvas>
      </div>
  
      <div class="chart-section">
        <h3>Ratings Distribution</h3>
        <canvas id="ratingsChart"></canvas>
      </div>
  
      <div class="stat-section">
        <h3>Average Rating You've Given</h3>
        <p>{{ summary.average_rating_given }}</p>
      </div>
    </div>
  </template>
  
  <script>
  import { Chart } from 'chart.js/auto';
  import axios from '@/plugins/axios';
  
  export default {
    name: 'CustomerSummary',
    data() {
      return {
        summary: {
          total_requests: 0,
          completed_requests: 0,
          canceled_requests: 0,
          average_rating_given: 0,
          rating_distribution: []
        },
        requestsChartInstance: null,
        ratingsChartInstance: null
      };
    },
    mounted() {
      this.fetchSummary();
    },
    methods: {
      async fetchSummary() {
        try {
          const token = localStorage.getItem('access_token');
          const response = await axios.get('/customer/summary', {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });
          this.summary = response.data.summary;
  
          this.initRequestsChart();
          this.initRatingsChart();
        } catch (error) {
          console.error('Error fetching customer summary:', error);
        }
      },
  
      initRequestsChart() {
        if (this.requestsChartInstance) {
          this.requestsChartInstance.destroy();
        }
  
        const ctx = document.getElementById('requestsChart').getContext('2d');
        this.requestsChartInstance = new Chart(ctx, {
          type: 'doughnut',
          data: {
            labels: ['Total', 'Completed', 'Canceled'],
            datasets: [
              {
                data: [
                  this.summary.total_requests,
                  this.summary.completed_requests,
                  this.summary.canceled_requests
                ],
                backgroundColor: ['#36A2EB', '#4BC0C0', '#FF6384']
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
  
      initRatingsChart() {
        if (this.ratingsChartInstance) {
          this.ratingsChartInstance.destroy();
        }
  
        const ctx = document.getElementById('ratingsChart').getContext('2d');
        const labels = this.summary.rating_distribution.map(item => `Rating ${item.rating}`);
        const data = this.summary.rating_distribution.map(item => item.count);
  
        this.ratingsChartInstance = new Chart(ctx, {
          type: 'bar',
          data: {
            labels,
            datasets: [
              {
                label: 'Count of Ratings',
                data,
                backgroundColor: 'rgba(255, 206, 86, 0.5)',
                borderColor: 'rgba(255, 206, 86, 1)',
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
  