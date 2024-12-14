//Login.test.tsx

jest.mock('../../hooks/useAuth');
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { Login } from './Login';
import { AuthProvider } from '../../contexts/AuthContext';

const mockLogin = jest.fn();

// Mock the useAuth hook
const mockedUseAuth = require('../../hooks/useAuth');
mockedUseAuth.useAuth = () => ({
  login: mockLogin,
});

describe('Login Component', () => {
  test('renders the login form', () => {
    render(
      <AuthProvider>
        <MemoryRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
          <Login />
        </MemoryRouter>
      </AuthProvider>
    );

    // Check if all form elements are rendered
    expect(screen.getByLabelText(/Email address/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Password/i)).toBeInTheDocument();
    expect(screen.getByText(/Sign in/i)).toBeInTheDocument();
  });

  test('calls login with correct credentials', async () => {
    render(
      <AuthProvider>
        <MemoryRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
          <Login />
        </MemoryRouter>
      </AuthProvider>
    );

    // Simulate user input
    fireEvent.change(screen.getByLabelText(/Email address/i), {
      target: { value: 'testuser@example.com' },
    });
    fireEvent.change(screen.getByLabelText(/Password/i), {
      target: { value: 'securepassword' },
    });

    // Simulate form submission
    fireEvent.click(screen.getByText(/Sign in/i));

    // Wait for login to be called
    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith('testuser@example.com', 'securepassword');
    });
  });

  test('displays an error for invalid credentials', async () => {
    mockLogin.mockRejectedValue(new Error('Invalid credentials'));

    render(
      <AuthProvider>
        <MemoryRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
          <Login />
        </MemoryRouter>
      </AuthProvider>
    );

    // Simulate user input
    fireEvent.change(screen.getByLabelText(/Email address/i), {
      target: { value: 'invaliduser@example.com' },
    });
    fireEvent.change(screen.getByLabelText(/Password/i), {
      target: { value: 'wrongpassword' },
    });

    // Simulate form submission
    fireEvent.click(screen.getByText(/Sign in/i));

    // Wait for error message
    const errorMessage = await screen.findByText(/Invalid email or password/i);
    expect(errorMessage).toBeInTheDocument();
  });
});
