import React, { useState } from 'react';
import { format, isAfter, isBefore, addDays } from 'date-fns';
import { 
  Edit, 
  Trash2, 
  Calendar, 
  Tag, 
  Flag,
  CheckCircle,
  Clock,
  AlertCircle
} from 'lucide-react';

const TaskCard = ({ task, onEdit, onDelete, onUpdate }) => {
  const [isUpdating, setIsUpdating] = useState(false);

  const handleStatusChange = async (newStatus) => {
    setIsUpdating(true);
    try {
      await onUpdate(task.id, { ...task, status: newStatus });
    } catch (error) {
      console.error('Failed to update task status:', error);
    } finally {
      setIsUpdating(false);
    }
  };

  const isOverdue = task.due_date && 
    isBefore(new Date(task.due_date), new Date()) && 
    task.status !== 'Completed';

  const isDueSoon = task.due_date && 
    isAfter(new Date(task.due_date), new Date()) &&
    isBefore(new Date(task.due_date), addDays(new Date(), 1)) &&
    task.status !== 'Completed';

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

  const getStatusColor = (status) => {
    switch (status) {
      case 'Completed':
        return 'status-completed';
      case 'In Progress':
        return 'status-in-progress';
      case 'Pending':
        return 'status-pending';
      default:
        return 'status-pending';
    }
  };

  return (
    <div className={`task-card ${getStatusColor(task.status)} ${
      task.priority === 'High' ? 'priority-high' : 
      task.priority === 'Medium' ? 'priority-medium' : 
      'priority-low'
    } ${isOverdue ? 'ring-2 ring-red-200 dark:ring-red-800' : ''} ${
      isDueSoon ? 'ring-2 ring-yellow-200 dark:ring-yellow-800' : ''
    }`}>
      <div className="flex items-start justify-between">
        <div className="flex-1 min-w-0">
          <div className="flex items-center space-x-2 mb-2">
            {getStatusIcon(task.status)}
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white truncate">
              {task.title}
            </h3>
            {isOverdue && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400">
                Overdue
              </span>
            )}
            {isDueSoon && !isOverdue && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400">
                Due Soon
              </span>
            )}
          </div>

          {task.description && (
            <p className="text-gray-600 dark:text-gray-300 mb-3 line-clamp-2">
              {task.description}
            </p>
          )}

          <div className="flex flex-wrap items-center gap-3 text-sm">
            {task.due_date && (
              <div className="flex items-center space-x-1 text-gray-600 dark:text-gray-300">
                <Calendar className="w-4 h-4" />
                <span>{format(new Date(task.due_date), 'MMM dd, yyyy')}</span>
              </div>
            )}

            <div className="flex items-center space-x-1">
              <Flag className="w-4 h-4 text-gray-400" />
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(task.priority)}`}>
                {task.priority}
              </span>
            </div>

            {task.category && (
              <div className="flex items-center space-x-1 text-gray-600 dark:text-gray-300">
                <Tag className="w-4 h-4" />
                <span>{task.category}</span>
              </div>
            )}

            {task.tags && task.tags.length > 0 && (
              <div className="flex items-center space-x-1">
                <Tag className="w-4 h-4 text-gray-400" />
                <div className="flex flex-wrap gap-1">
                  {task.tags.slice(0, 3).map((tag, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded-full text-xs"
                    >
                      {tag}
                    </span>
                  ))}
                  {task.tags.length > 3 && (
                    <span className="text-xs text-gray-500">
                      +{task.tags.length - 3} more
                    </span>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="flex items-center space-x-2 ml-4">
          {/* Status Dropdown */}
          <select
            value={task.status}
            onChange={(e) => handleStatusChange(e.target.value)}
            disabled={isUpdating}
            className="text-sm border border-gray-300 dark:border-gray-600 rounded-md px-2 py-1 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="Pending">Pending</option>
            <option value="In Progress">In Progress</option>
            <option value="Completed">Completed</option>
          </select>

          {/* Action Buttons */}
          <button
            onClick={() => onEdit(task)}
            className="p-2 text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors duration-200"
            title="Edit task"
          >
            <Edit className="w-4 h-4" />
          </button>

          <button
            onClick={() => onDelete(task.id)}
            className="p-2 text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors duration-200"
            title="Delete task"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
          <span>Created: {format(new Date(task.created_at), 'MMM dd, yyyy')}</span>
          {task.updated_at !== task.created_at && (
            <span>Updated: {format(new Date(task.updated_at), 'MMM dd, yyyy')}</span>
          )}
        </div>
      </div>
    </div>
  );
};

export default TaskCard;
