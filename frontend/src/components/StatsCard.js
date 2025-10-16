import React from 'react';

const StatsCard = ({ title, value, icon, color = 'blue' }) => {
  const getColorClasses = (color) => {
    switch (color) {
      case 'green':
        return 'bg-green-500 text-white';
      case 'yellow':
        return 'bg-yellow-500 text-white';
      case 'red':
        return 'bg-red-500 text-white';
      case 'purple':
        return 'bg-purple-500 text-white';
      default:
        return 'bg-primary-500 text-white';
    }
  };

  return (
    <div className="card p-6">
      <div className="flex items-center">
        <div className={`p-3 rounded-lg ${getColorClasses(color)}`}>
          {icon}
        </div>
        <div className="ml-4">
          <p className="text-sm font-medium text-gray-600 dark:text-gray-300">
            {title}
          </p>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {value}
          </p>
        </div>
      </div>
    </div>
  );
};

export default StatsCard;
