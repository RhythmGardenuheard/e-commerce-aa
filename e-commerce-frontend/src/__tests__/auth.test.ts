import { loginUser, registerUser } from '../actions/auth';
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  rest.post('http://localhost:8000/auth/token', (req, res, ctx) => {
    return res(ctx.json({ access_token: 'fake_token', token_type: 'bearer' }));
  }),
  rest.post('http://localhost:8000/auth/register', (req, res, ctx) => {
    return res(ctx.json({ id: 1, username: 'testuser', email: 'test@example.com' }));
  }),
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('Auth Actions', () => {
  test('loginUser should return token', async () => {
    const result = await loginUser({ username: 'test', password: 'pass' });
    expect(result.access_token).toBe('fake_token');
  });

  test('registerUser should return user data', async () => {
    const result = await registerUser({ username: 'test', email: 'test@example.com', password: 'pass' });
    expect(result.username).toBe('testuser');
  });
});