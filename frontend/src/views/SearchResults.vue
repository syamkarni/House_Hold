<!-- Ignore this file -->

<template>
    <div>
      <h2>Search Results for {{ role }}</h2>
      <ul v-if="results.length > 0">
        <li v-for="result in results" :key="result.id">
          <span v-if="role === 'admin'">
            <strong>{{ result.name || result.email }}</strong> - {{ result.description || result.service || 'N/A' }}
          </span>
          <span v-else-if="role === 'professional'">
            <strong>{{ result.name || 'Service' }}</strong> - {{ result.description || result.remarks }}
          </span>
          <span v-else-if="role === 'customer'">
            <strong>{{ result.name || 'Package' }}</strong> - {{ result.description }}
          </span>
        </li>
      </ul>
      <p v-else>No results found.</p>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      role: String,
      results: {
        type: Array,
        default: () => []
      }
    }
  };
  </script>
  