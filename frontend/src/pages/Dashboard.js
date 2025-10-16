import React, { useState, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';
import { format } from 'date-fns';
import { 
  Plus, 
  Search, 
  Filter, 
  Calendar, 
  CheckCircle, 
  Clock, 
  AlertCircle,
  BarChart3,
  Target
} from 'lucide-react';
import TaskCard from '../components/TaskCard';
import TaskModal from '../components/TaskModal';
import StatsCard from '../components/StatsCard';
import FilterModal from '../components/FilterModal';

const Dashboard = () => {
  const [tasks, setTasks] = useState([]);
  const [filteredTasks, setFilteredTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showTaskModal, setShowTaskModal] = useState(false);
  const [showFilterModal, setShowFilterModal] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [filters, setFilters] = useState({
    status: '',
    category: '',
    priority: ''
  });
  const [stats, setStats] = useState({
    total_tasks: 0,
    completed_tasks: 0,
    pending_tasks: 0,
    in_progress_tasks: 0,
    overdue_tasks: 0,
    completion_rate: 0
  });

  useEffect(() => {
    fetchTasks();
    fetchStats();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [tasks, searchTerm, filters]);

  const fetchTasks = async () => {
    try {
      const response = await axios.get('/api/tasks');
      setTasks(response.data.tasks);
    } catch (error) {
      toast.error('Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get('/api/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  const applyFilters = () => {
    let filtered = tasks;

    // Apply search filter
    if (searchTerm) {
      filtered = filtered.filter(task =>
        task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        task.description.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Apply status filter
    if (filters.status) {
      filtered = filtered.filter(task => task.status === filters.status);
    }

    // Apply category filter
    if (filters.category) {
      filtered = filtered.filter(task => task.category === filters.category);
    }

    // Apply priority filter
    if (filters.priority) {
      filtered = filtered.filter(task => task.priority === filters.priority);
    }

    setFilteredTasks(filtered);
  };

  const handleCreateTask = async (taskData) => {
    try {
      const response = await axios.post('/api/tasks', taskData);
      setTasks([response.data.task, ...tasks]);
      await fetchStats();
      toast.success('Task created successfully!');
    } catch (error) {
      toast.error('Failed to create task');
    }
  };

  const handleUpdateTask = async (taskId, taskData) => {
    try {
      const response = await axios.put(`/api/tasks/${taskId}`, taskData);
      setTasks(tasks.map(task => 
        task.id === taskId ? response.data.task : task
      ));
      await fetchStats();
      toast.success('Task updated successfully!');
    } catch (error) {
      toast.error('Failed to update task');
    }
  };

  const handleDeleteTask = async (taskId) => {
    try {
      await axios.delete(`/api/tasks/${taskId}`);
      setTasks(tasks.filter(task => task.id !== taskId));
      await fetchStats();
      toast.success('Task deleted successfully!');
    } catch (error) {
      toast.error('Failed to delete task');
    }
  };

  const handleEditTask = (task) => {
    setEditingTask(task);
    setShowTaskModal(true);
  };

  const handleCloseModal = () => {
    setShowTaskModal(false);
    setEditingTask(null);
  };

  const clearFilters = () => {
    setFilters({ status: '', category: '', priority: '' });
    setSearchTerm('');
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'Completed':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'In Progress':
        return <Clock className="w-5 h-5 text-blue-500" />;
      case 'Pending':
        return <AlertCircle className="w-5 h-5 text-yellow-500" />;
      default:
        return <AlertCircle className="w-5 h-5 text-gray-500" />;
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'High':
        return 'text-red-600 bg-red-100 dark:bg-red-900/30 dark:text-red-400';
      case 'Medium':
        return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/30 dark:text-yellow-400';
      case 'Low':
        return 'text-green-600 bg-green-100 dark:bg-green-900/30 dark:text-green-400';
      default:
        return 'text-gray-600 bg-gray-100 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            Dashboard
          </h1>
          <p className="text-gray-600 dark:text-gray-300 mt-1">
            Manage your tasks and stay organized
          </p>
        </div>
        <button
          onClick={() => setShowTaskModal(true)}
          className="btn-primary flex items-center space-x-2"
        >
          <Plus className="w-5 h-5" />
          <span>Add Task</span>
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Total Tasks"
          value={stats.total_tasks}
          icon={<Target className="w-6 h-6" />}
          color="blue"
        />
        <StatsCard
          title="Completed"
          value={stats.completed_tasks}
          icon={<CheckCircle className="w-6 h-6" />}
          color="green"
        />
        <StatsCard
          title="In Progress"
          value={stats.in_progress_tasks}
          icon={<Clock className="w-6 h-6" />}
          color="yellow"
        />
        <StatsCard
          title="Overdue"
          value={stats.overdue_tasks}
          icon={<AlertCircle className="w-6 h-6" />}
          color="red"
        />
      </div>

      {/* Progress Bar */}
      <div className="card p-6">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Completion Rate
          </h3>
          <span className="text-sm font-medium text-gray-600 dark:text-gray-300">
            {stats.completion_rate}%
          </span>
        </div>
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div
            className="bg-primary-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${stats.completion_rate}%` }}
          ></div>
        </div>
      </div>

      {/* Search and Filter */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1 relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            placeholder="Search tasks..."
            className="input-field pl-10"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <button
          onClick={() => setShowFilterModal(true)}
          className="btn-secondary flex items-center space-x-2"
        >
          <Filter className="w-5 h-5" />
          <span>Filter</span>
        </button>
        {(filters.status || filters.category || filters.priority || searchTerm) && (
          <button
            onClick={clearFilters}
            className="btn-secondary"
          >
            Clear
          </button>
        )}
      </div>

      {/* Tasks List */}
      <div className="space-y-4">
        {filteredTasks.length === 0 ? (
          <div className="text-center py-12">
            <div className="w-24 h-24 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mx-auto mb-4">
              <Calendar className="w-12 h-12 text-gray-400" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              No tasks found
            </h3>
            <p className="text-gray-600 dark:text-gray-300 mb-4">
              {tasks.length === 0 
                ? "Get started by creating your first task!"
                : "Try adjusting your search or filters."
              }
            </p>
            {tasks.length === 0 && (
              <button
                onClick={() => setShowTaskModal(true)}
                className="btn-primary"
              >
                Create Task
              </button>
            )}
          </div>
        ) : (
          <div className="grid gap-4">
            {filteredTasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onEdit={handleEditTask}
                onDelete={handleDeleteTask}
                onUpdate={handleUpdateTask}
              />
            ))}
          </div>
        )}
      </div>

      {/* Modals */}
      {showTaskModal && (
        <TaskModal
          task={editingTask}
          onClose={handleCloseModal}
          onSave={editingTask ? handleUpdateTask : handleCreateTask}
        />
      )}

      {showFilterModal && (
        <FilterModal
          filters={filters}
          onFiltersChange={setFilters}
          onClose={() => setShowFilterModal(false)}
        />
      )}
    </div>
  );
};

export default Dashboard;
