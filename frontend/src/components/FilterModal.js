import React from 'react';
import { X, Filter } from 'lucide-react';

const FilterModal = ({ filters, onFiltersChange, onClose }) => {
  const categories = [
    'General', 'Work', 'Personal', 'Shopping', 'Health', 
    'Education', 'Finance', 'Travel', 'Home', 'Other'
  ];

  const priorities = ['Low', 'Medium', 'High'];
  const statuses = ['Pending', 'In Progress', 'Completed'];

  const handleFilterChange = (key, value) => {
    onFiltersChange({
      ...filters,
      [key]: value
    });
  };

  const clearAllFilters = () => {
    onFiltersChange({
      status: '',
      category: '',
      priority: ''
    });
  };

  const hasActiveFilters = filters.status || filters.category || filters.priority;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-md">
        <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white flex items-center space-x-2">
            <Filter className="w-5 h-5" />
            <span>Filter Tasks</span>
          </h2>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors duration-200"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 space-y-6">
          {/* Status Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              Status
            </label>
            <div className="space-y-2">
              <label className="flex items-center">
                <input
                  type="radio"
                  name="status"
                  value=""
                  checked={filters.status === ''}
                  onChange={(e) => handleFilterChange('status', e.target.value)}
                  className="w-4 h-4 text-primary-600 bg-gray-100 border-gray-300 focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                />
                <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">All Statuses</span>
              </label>
              {statuses.map(status => (
                <label key={status} className="flex items-center">
                  <input
                    type="radio"
                    name="status"
                    value={status}
                    checked={filters.status === status}
                    onChange={(e) => handleFilterChange('status', e.target.value)}
                    className="w-4 h-4 text-primary-600 bg-gray-100 border-gray-300 focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                  />
                  <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">{status}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Category Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              Category
            </label>
            <select
              value={filters.category}
              onChange={(e) => handleFilterChange('category', e.target.value)}
              className="input-field"
            >
              <option value="">All Categories</option>
              {categories.map(category => (
                <option key={category} value={category}>{category}</option>
              ))}
            </select>
          </div>

          {/* Priority Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              Priority
            </label>
            <div className="space-y-2">
              <label className="flex items-center">
                <input
                  type="radio"
                  name="priority"
                  value=""
                  checked={filters.priority === ''}
                  onChange={(e) => handleFilterChange('priority', e.target.value)}
                  className="w-4 h-4 text-primary-600 bg-gray-100 border-gray-300 focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                />
                <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">All Priorities</span>
              </label>
              {priorities.map(priority => (
                <label key={priority} className="flex items-center">
                  <input
                    type="radio"
                    name="priority"
                    value={priority}
                    checked={filters.priority === priority}
                    onChange={(e) => handleFilterChange('priority', e.target.value)}
                    className="w-4 h-4 text-primary-600 bg-gray-100 border-gray-300 focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
                  />
                  <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">{priority}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Actions */}
          <div className="flex justify-between pt-6 border-t border-gray-200 dark:border-gray-700">
            <button
              onClick={clearAllFilters}
              className="btn-secondary"
              disabled={!hasActiveFilters}
            >
              Clear All
            </button>
            <button
              onClick={onClose}
              className="btn-primary"
            >
              Apply Filters
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FilterModal;
