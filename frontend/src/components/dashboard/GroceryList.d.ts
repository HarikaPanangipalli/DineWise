interface GroceryItem {
    item_name: string;
    quantity: number;
}
interface GroceryListProps {
    groceryId: string | null;
    groceries: GroceryItem[];
    onUpdate: (groceries: GroceryItem[]) => void | null;
}
export declare const GroceryList: React.FC<GroceryListProps>;
export {};
