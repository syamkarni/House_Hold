<template>
  <div>
      <h2>Reports</h2>
      <button @click="exportCSV">Download CSV</button>
      <div v-if="error" style="color: red;">{{ error }}</div>
  </div>
</template>

<script>
import axios from '@/plugins/axios'

export default {
  name: 'AdminReports',
  data() {
      return {
          csvData: null,
          error: null,
      }
  },
  methods: {
      async exportCSV() {
          this.error = null;
          try {
              const response = await axios.get('/report/export');
              const taskId = response.data.id;
              if (!taskId) {
                  this.error = 'Invalid task ID from server.';
                  return;
              }

              let isReady = false;
              let maxAttempts = 20; 
              let attempt = 0;
              while (!isReady && attempt < maxAttempts) {
                  const statusResponse = await axios.get(`/report/csv_result/${taskId}`, { responseType: 'blob' });
                  if (statusResponse.headers['content-type'] === 'application/json') {
                      await new Promise(resolve => setTimeout(resolve, 1000)); 
                      attempt++;
                  } else {
                      const blob = new Blob([statusResponse.data], { type: 'text/csv' });
                      const url = window.URL.createObjectURL(blob);
                      const a = document.createElement('a');
                      a.href = url;
                      a.download = `report_${taskId}.csv`;
                      a.click();
                      window.URL.revokeObjectURL(url);
                      isReady = true;

                      alert("CSV has been downloaded successfully!");
                  }
              }

              if (!isReady) {
                  this.error = "Report generation timed out.";
              }

          } catch (error) {
              this.error = 'Error exporting CSV.';
              console.error('Error exporting CSV:', error);
          }
      }
  }
}
</script>
