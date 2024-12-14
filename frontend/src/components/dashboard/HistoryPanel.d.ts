import { MealPlanTemp } from '../../types/mealplan.types';
interface HistoryPanelProps {
    onPlanSelect: (plan: MealPlanTemp) => void;
}
export declare const HistoryPanel: React.FC<HistoryPanelProps>;
export {};
