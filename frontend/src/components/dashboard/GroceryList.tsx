// src/components/dashboard/GroceryList.tsx
import { useState } from 'react';
import api from '../../services/api';

interface GroceryItem {
  item_name: string;
  quantity: number;
}

interface GroceryListProps {
  groceryId: string | null;
  groceries: GroceryItem[];
  onUpdate: (groceries: GroceryItem[]) => void | null;
}

export const GroceryList: React.FC<GroceryListProps> = ({ groceryId, groceries, onUpdate }) => {
  const [newItem, setNewItem] = useState({ item_name: '', quantity: 1});
  const [isLoading, setIsLoading] = useState(false);
  const [deleteLoading, setDeleteLoading] = useState<number | null>(null);

  const handleDelete = async (index: number) => {
    setDeleteLoading(index);
    try {
      await api.delete(`grocery/${groceryId}/items/${index}`);
      const updatedGroceries = groceries.filter((_, i) => i !== index);
      onUpdate(updatedGroceries);
    } catch (error) {
      console.error('Failed to delete item:', error);
    } finally {
      setDeleteLoading(null);
    }
  };

  const handleAdd = async () => {
    if (newItem.item_name && newItem.quantity > 0) {
      setIsLoading(true);
      try {
        const response = await api.post(`grocery/${groceryId}/items`, {
          ...newItem,
        });
        
        onUpdate([...groceries, { ...newItem }]);
        setNewItem({ item_name: '', quantity: 1});
      } catch (error) {
        console.error('Failed to add item:', error);
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-3 gap-4 mb-6">
        <input
          type="text"
          placeholder="Item name"
          value={newItem.item_name}
          onChange={(e) => setNewItem({ ...newItem, item_name: e.target.value })}
          className="border rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          disabled={isLoading}
        />
        <input
          type="number"
          placeholder="Quantity"
          value={newItem.quantity}
          onChange={(e) => setNewItem({ ...newItem, quantity: parseInt(e.target.value) })}
          className="border rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          disabled={isLoading}
        />
        <button
          onClick={handleAdd}
          disabled={isLoading}
          className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition-colors"
        >
          {isLoading ? 'Adding...' : 'Add Item'}
        </button>
      </div>

      <div className="space-y-3">
        {groceries.map((item, index) => (
          <div 
            key={index} 
            className="flex justify-between items-center bg-white rounded-lg p-4 shadow-sm"
          >
            <div className="flex-1">
              <span className="font-medium text-gray-900">{item.item_name}</span>
              <span className="text-sm text-gray-500 ml-2">
                x {item.quantity}
              </span>
            </div>
            <button
              onClick={() => handleDelete(index)}
              disabled={deleteLoading === index}
              className="text-red-600 hover:text-red-700 disabled:opacity-50 px-3 py-1"
            >
              {deleteLoading === index ? (
                <span className="flex items-center">
                  <div className="animate-spin h-4 w-4 border-b-2 border-red-600 rounded-full mr-2"></div>
                  Deleting...
                </span>
              ) : (
                'Delete'
              )}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};