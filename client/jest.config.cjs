module.exports = {
  testEnvironment: 'jsdom',

  setupFiles: ['<rootDir>/jest.setup.cjs'],
  setupFilesAfterEnv: ['<rootDir>/jest.env.cjs'],

  moduleNameMapper: {
    '\\.(css|less|scss)$': 'identity-obj-proxy',
  },

  testPathIgnorePatterns: ['/node_modules/', '/dist/'],
};