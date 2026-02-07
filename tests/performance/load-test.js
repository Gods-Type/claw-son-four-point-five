import http from 'k6/http';
import { check, sleep } from 'k6';

// Configuration
export const options = {
  stages: [
    { duration: '30s', target: 20 },  // Ramp-up to 20 users
    { duration: '1m', target: 20 },    // Stay at 20 users
    { duration: '30s', target: 0 },    // Ramp-down to 0 users
  ],
  thresholds: {
    http_req_failed: ['rate<0.01'],   // Less than 1% failed requests
    http_req_duration: ['p(95)<500'], // 95% of requests should be below 500ms
  },
};

// API endpoints to test
const API_BASE_URL = __ENV.API_URL || 'http://localhost:8002';
const EDUCATION_API_BASE_URL = __ENV.EDUCATION_API_URL || 'http://localhost:8003';

// Test scenarios
export default function () {
  // Test API health endpoint
  let res = http.get(`${API_BASE_URL}/health`);
  check(res, {
    'API health status is 200': (r) => r.status === 200,
    'API health response is healthy': (r) => r.json().status === 'healthy',
  });

  // Test Education API health endpoint
  res = http.get(`${EDUCATION_API_BASE_URL}/health`);
  check(res, {
    'Education API health status is 200': (r) => r.status === 200,
    'Education API health response is healthy': (r) => r.json().status === 'healthy',
  });

  // Add more test scenarios as needed
  // Example:
  // res = http.get(`${API_BASE_URL}/api/v1/some-endpoint`);
  // check(res, { 'Some endpoint works': (r) => r.status === 200 });

  // Sleep between iterations
  sleep(1);
}
