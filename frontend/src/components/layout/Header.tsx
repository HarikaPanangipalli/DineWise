// src/components/layout/Header.tsx
import { UserMenu } from './UserMenu';
import { useAuth } from '../../hooks/useAuth';

export const Header = () => {
  const { user } = useAuth();

  return (
    <header className="bg-white h-16 min-h-[64px] p-2 border-b border-gray-200">
      <div className="flex justify-between items-center h-full px-4">
        {/* Left corner: Welcome message */}
        <div className="flex-shrink-0">
          <h1 className="text-2xl font-bold text-gray-900">Welcome, {user?.full_name}!</h1>
        </div>
        
        {/* Right corner: User menu */}
        <div className='mr-11'>
          <UserMenu />
        </div>
      </div>
    </header>
  );
};
