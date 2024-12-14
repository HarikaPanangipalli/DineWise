export default {
  testEnvironment: 'jest-environment-jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setup-tests.ts'],
  moduleNameMapper: {
    '\\.(css|scss)$': 'identity-obj-proxy',
  },
  transform: {
    '^.+\\.(ts|tsx)$': [
      'ts-jest',
      {
        tsconfig: '<rootDir>/tsconfig.app.json',
      },
    ],
  },
};
