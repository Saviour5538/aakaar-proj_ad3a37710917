import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from '../api/client';

interface ResourceCounts {
  tasks: number;
}

const Dashboard: React.FC = () => {
  const [resourceCounts, setResourceCounts] = useState<ResourceCounts | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchResourceCounts = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await axios.get('/api/health');
        setResourceCounts(response.data);
      } catch (err: any) {
        setError('Failed to fetch resource counts. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchResourceCounts();
  }, []);

  const handleCreateTask = () => {
    navigate('/tasks/create');
  };

  const handleViewTasks = () => {
    navigate('/tasks');
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">Dashboard</h1>
        {loading ? (
          <div className="text-center text-gray-500">Loading...</div>
        ) : error ? (
          <div className="text-center text-red-500">{error}</div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
              <div className="bg-white shadow rounded-lg p-6">
                <h2 className="text-lg font-semibold text-gray-700">Tasks</h2>
                <p className="text-3xl font-bold text-gray-900">{resourceCounts?.tasks || 0}</p>
              </div>
            </div>
            <div className="bg-white shadow rounded-lg p-6 mb-6">
              <h2 className="text-lg font-semibold text-gray-700 mb-4">Quick Actions</h2>
              <div className="flex space-x-4">
                <button
                  onClick={handleCreateTask}
                  className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                >
                  Create Task
                </button>
                <button
                  onClick={handleViewTasks}
                  className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
                >
                  View Tasks
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Dashboard;