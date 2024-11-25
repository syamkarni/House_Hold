<template>
    <div>
      <h2>Reports</h2>
      <button @click="exportCSV">Export Closed Service Requests as CSV</button>
      <div v-if="csvData">
        <h3>CSV Data:</h3>
        <pre>{{ csvData }}</pre>
      </div>
      <div v-if="error" style="color: red;">{{ error }}</div>
    </div>
  </template>
  
  <script>
  import axios from '@/plugins/axios';
  
  export default {
    name: 'AdminReports',
    data() {
      return {
        csvData: null,
        error: null,
      };
    },
    methods: {
      async exportCSV() {
        this.error = null;
        try {
          const response = await axios.post(
            '/reports/export_csv',
            {},
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('access_token')}`,
              },
              responseType: 'blob',
            }
          );
  
          // for now just reading the CSV content
          const reader = new FileReader();
          reader.onload = () => {
            this.csvData = reader.result;
          };
          reader.readAsText(response.data);
  
          // maybe we can use trigger too for downloading!
        } catch (error) {
          this.error = 'Error exporting CSV.';
          console.error('Error exporting CSV:', error);
        }
      },
    },
  };
  </script>
  