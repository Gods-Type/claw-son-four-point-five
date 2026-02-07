#!/usr/bin/env python3
"""
Integration tests for the Education API service.
"""
import os
import time
import requests
import unittest


class TestEducationAPIIntegration(unittest.TestCase):
    """Integration tests for the Education API service."""

    @classmethod
    def setUpClass(cls):
        """Set up test class."""
        cls.api_url = os.environ.get('EDUCATION_API_URL', 'http://localhost:8003')
        cls.max_retries = 5
        cls.retry_delay = 2

        # Wait for Education API to be ready
        for i in range(cls.max_retries):
            try:
                response = requests.get(f"{cls.api_url}/health", timeout=5)
                if response.status_code == 200:
                    print(f"Education API is ready after {i+1} attempts")
                    break
            except (requests.ConnectionError, requests.Timeout):
                if i == cls.max_retries - 1:
                    raise
                time.sleep(cls.retry_delay)

    def test_health_endpoint(self):
        """Test the health endpoint."""
        response = requests.get(f"{self.api_url}/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'healthy')

    def test_education_endpoint(self):
        """Test a basic Education API endpoint."""
        # This is a placeholder - replace with actual Education API endpoints
        response = requests.get(f"{self.api_url}/api/v1/education/info")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('version', data)


if __name__ == '__main__':
    unittest.main()
